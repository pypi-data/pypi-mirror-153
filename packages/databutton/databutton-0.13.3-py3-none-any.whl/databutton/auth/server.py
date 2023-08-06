import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from databutton.utils import get_databutton_login_path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuthSuccess(BaseModel):
    refreshToken: str
    uid: str


@app.post("/")
async def auth_success(auth: AuthSuccess):
    filename = Path(get_databutton_login_path(), f"{auth.uid}.json")
    # Create files with necessary folder structure if it does not exist
    filename.parent.mkdir(exist_ok=True, parents=True)
    with open(filename, "w") as f:
        f.write(
            json.dumps({"uid": auth.uid, "refreshToken": auth.refreshToken}, indent=2)
        )

    return {"success": True}
