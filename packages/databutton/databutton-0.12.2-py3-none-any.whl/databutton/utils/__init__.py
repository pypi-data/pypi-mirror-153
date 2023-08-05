import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from time import time
from typing import List, Optional, Union

import requests
import schedule

try:
    from urllib.parse import quote
except Exception:
    from urllib import quote


@dataclass
class LoginData:
    refreshToken: str
    uid: str


DEFAULT_GLOB_EXCLUDE = ["venv", ".venv", "__pycache__", ".databutton"]


@dataclass
class ProjectConfig:
    uid: str
    name: str
    # List of fnmatch patterns to exclude, similar to .gitignore
    exclude: Optional[List[str]] = field(default_factory=lambda: DEFAULT_GLOB_EXCLUDE)


CONFIG_PATH = "databutton.json"


def get_databutton_config(config_path=CONFIG_PATH, retries=2) -> ProjectConfig:
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return ProjectConfig(
                name=config["name"], uid=config["uid"], exclude=config["exclude"]
            )
    except FileNotFoundError as e:
        if retries == 0:
            raise e
        return get_databutton_config(f"../{config_path}", retries=retries - 1)


def get_databutton_login_info() -> Union[LoginData, None]:
    if "DATABUTTON_TOKEN" in os.environ:
        config = get_databutton_config()
        return LoginData(refreshToken=os.environ["DATABUTTON_TOKEN"], uid="token")

    auth_path = get_databutton_login_path()
    if not os.path.exists(auth_path):
        os.makedirs(auth_path)

    uids = [f for f in os.listdir(auth_path) if f.endswith(".json")]
    if len(uids) > 0:
        # Just take a random one for now
        with open(os.path.join(auth_path, uids[0])) as f:
            config = json.load(f)
            return LoginData(uid=config["uid"], refreshToken=config["refreshToken"])
    return None


def get_databutton_login_path():
    return os.path.join(Path.home(), ".config", "databutton")


def create_databutton_config(
    name: str, uid: str, project_directory=os.curdir
) -> ProjectConfig:
    config = ProjectConfig(name=name, uid=uid, exclude=DEFAULT_GLOB_EXCLUDE)
    with open(os.path.join(project_directory, CONFIG_PATH), "w") as f:
        f.write(json.dumps(config.__dict__, indent=2))
        return config


FIREBASE_CONFIG = {
    "apiKey": "AIzaSyAdgR9BGfQrV2fzndXZLZYgiRtpydlq8ug",
    "authDomain": "databutton.firebaseapp.com",
    "projectId": "databutton",
    "storageBucket": "databutton.appspot.com",
    "databaseURL": "",
}
storage_bucket = (
    f"https://firebasestorage.googleapis.com/v0/b/{FIREBASE_CONFIG['storageBucket']}"
)


def get_dataframe_path(project_id: str, key: str):
    return f"projects/{project_id}/dataframes/{key}"


def upload_to_bucket(
    file_buf, config: ProjectConfig, key: str, content_type: str = "text/csv"
):
    upload_path = get_dataframe_path(config.uid, key)
    url = f"{storage_bucket}/o"
    token = get_auth_token()
    headers = {
        "Authorization": f"Firebase {token}",
        "Content-type": content_type,
    }
    response = requests.post(
        url, headers=headers, data=file_buf, params={"name": upload_path}
    )
    if not response.ok:
        raise Exception(f"Could not upload to path {key}")
    return response


def download_from_bucket(key: str, config: ProjectConfig):
    download_path = get_dataframe_path(config.uid, key)
    url = f"{storage_bucket}/o/{quote(download_path, safe='')}"
    token = get_auth_token()
    headers = {"Authorization": f"Firebase {token}"}
    response = requests.get(url, params={"alt": "media"}, headers=headers)
    if not response.ok:
        if response.status_code == 404:
            raise FileNotFoundError(f"Could not find {key}")
        raise Exception(f"Could not download {key}")
    return response


def upload_archive(config: ProjectConfig, deployment_id: str, archive_path: str):
    get_signed_url = (
        "https://europe-west1-databutton.cloudfunctions.net/upload_project_signer"
    )
    refresh_token = get_databutton_login_info().refreshToken
    headers = {
        "Authorization": f"Bearer {get_auth_token()}",
    }
    request_body = {
        "project_id": config.uid,
        "deployment_id": deployment_id,
        "databutton_token": refresh_token,
    }

    signed_url_res = requests.post(get_signed_url, headers=headers, json=request_body)
    if not signed_url_res.ok:
        raise Exception("Could not upload")

    signed_url = signed_url_res.json()["signed_url"]
    signed_headers = {
        "Authorization": headers["Authorization"],
        "x-goog-meta-databutton-token": refresh_token,
        "content-type": "application/tar+gzip",
    }

    with open(archive_path, "rb") as f:
        response = requests.put(signed_url, headers=signed_headers, data=f)
        if not response.ok:
            logging.info(response.json())
            raise Exception("Could not upload archive")
        return True


_cached_auth_token = None


def get_auth_token() -> str:
    global _cached_auth_token
    # This has a 15 minute cache
    if _cached_auth_token is not None and time() - _cached_auth_token[0] > 60 * 15:
        _cached_auth_token = None
    if _cached_auth_token is None:
        login_info = get_databutton_login_info()
        if login_info is None:
            raise Exception(
                "Could not find any login information."
                "\nAre you sure you are logged in?"
            )
        res = requests.post(
            f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_CONFIG['apiKey']}",
            {"grant_type": "refresh_token", "refresh_token": login_info.refreshToken},
        )
        if not res.ok:
            raise Exception("Could not authenticate")
        json = res.json()
        _cached_auth_token = (time(), json["id_token"])
    return _cached_auth_token[1]


import functools


def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except Exception as e:
                import traceback

                logging.info(traceback.format_exc())
                if os.environ.get("SENTRY_DSN"):
                    import sentry_sdk

                    sentry_sdk.capture_exception(e)
                if cancel_on_failure:
                    return schedule.CancelJob

        return wrapper

    return catch_exceptions_decorator


def create_databutton_cloud_project(name: str):
    """Creates a Databutton Cloud Project"""
    token = get_auth_token()

    res = requests.post(
        "https://europe-west1-databutton.cloudfunctions.net/createOrUpdateProject",
        json={"name": name},
        headers={"Authorization": f"Bearer {token}"},
    )

    res_json = res.json()
    new_id = res_json["id"]
    return new_id


def get_build_logs(build_id: str) -> str:
    log_url_response = requests.get(
        "https://europe-west1-databutton.cloudfunctions.net/get_cloud_build_logs",
        params={"build_id": build_id},
        headers={"Authorization": f"Bearer {get_auth_token()}"},
    )
    log_url = log_url_response.json()["signed_url"]
    return log_url
