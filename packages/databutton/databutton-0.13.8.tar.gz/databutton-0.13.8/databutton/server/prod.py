import logging
import os

import sentry_sdk
from databutton_web import get_static_file_path
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from databutton.decorators.jobs.schedule import Scheduler
from databutton.server.processes import StreamlitProcess
from databutton.utils import get_databutton_config, get_databutton_login_info
from databutton.utils.build import read_artifacts_json
from databutton.version import __version__

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

components = read_artifacts_json()
# Set up proxies for streamlit apps
# They are ran as containers somewhere
for st in components.streamlit_apps:
    p = StreamlitProcess(st.route, "", st.port)
    p.add_route_to_app(app)


@app.get("/")
async def index():
    return RedirectResponse(url="/index.html")


@app.on_event("startup")
async def startup():
    scheduler = Scheduler()
    await scheduler.load_schedules(components)


app_dir = get_static_file_path()
app.mount("/static", StaticFiles(directory=".databutton"), name=".databutton")
app.mount("/", StaticFiles(directory=app_dir), name="app")


@app.get("/healthz")
async def healthz():
    return Response(status_code=status.HTTP_200_OK)


if os.environ.get("SENTRY_DSN"):
    logging.info("Found SENTRY_DSN, logging errors")
    sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN"))
    config = get_databutton_config()
    login_info = get_databutton_login_info()
    sentry_tags = {
        "databutton_release": os.environ.get("DATABUTTON_RELEASE", "latest"),
        "databutton_project_id": config.uid,
        "databutton_project_name": config.name,
        "databutton_version": __version__,
        "databutton_user_id": login_info.uid if login_info else None,
    }
    sentry_sdk.set_user({"uid": login_info.uid if login_info else None})
    for k, v in sentry_tags.items():
        sentry_sdk.set_tag(k, v)

    app = SentryAsgiMiddleware(app)
