import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from databutton.utils import get_databutton_login_path

dir_path = Path(__file__).parent

templates = Jinja2Templates(directory=dir_path)

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def serve_auth(request: Request):
    return templates.TemplateResponse(
        "auth.html", {"sign_in_url": request.url, "request": request}
    )


class AuthSuccess(BaseModel):
    refreshToken: str
    uid: str


@app.post("/success")
async def auth_success(auth: AuthSuccess):
    filename = Path(get_databutton_login_path(), f"{auth.uid}.json")
    # Create files with necessary folder structure if it does not exist
    filename.parent.mkdir(exist_ok=True, parents=True)
    with open(filename, "w") as f:
        f.write(
            json.dumps({"uid": auth.uid, "refreshToken": auth.refreshToken}, indent=2)
        )

    return {"success": True}
