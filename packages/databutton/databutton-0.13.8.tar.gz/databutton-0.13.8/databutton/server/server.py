import shutil
import sys
import time
from pathlib import Path

import click
import psutil
from databutton_web import get_static_file_path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from databutton.decorators.jobs.schedule import Scheduler
from databutton.server.processes import _streamlit_processes, start_processes
from databutton.utils.build import generate_components, write_artifacts_json
from databutton.utils.log_status import log_devserver_screen

start_time = time.time()
app = FastAPI()
sys.path.insert(0, str(Path.cwd()))

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create .databutton if not exists
Path(".databutton").mkdir(exist_ok=True)

shutil.rmtree(".databutton/app", ignore_errors=True)
shutil.rmtree(".databutton/data", ignore_errors=True)

artifacts = generate_components()

write_artifacts_json(artifacts)

app.mount("/static", StaticFiles(directory=".databutton"), name=".databutton")

app_dir = get_static_file_path()


@app.on_event("startup")
async def start_servers():
    await start_processes(app, artifacts.streamlit_apps)
    scheduler = Scheduler()
    await scheduler.load_schedules(artifacts)

    @app.get("/")
    async def index():
        return FileResponse(f"{get_static_file_path()}/index.html")

    app.mount("/", StaticFiles(directory=app_dir), name="app")
    time_spent_starting = int((time.time() - start_time) * 1000)
    log_devserver_screen(components=artifacts, time_spent_starting=time_spent_starting)


@app.on_event("shutdown")
async def shutdown_event():
    # close connections here
    click.echo()
    click.echo(click.style("stopping...", fg="green"))
    for process in _streamlit_processes.values():
        process.stop()
    dangling_processes = []
    fpaths = [app.fpath for app in _streamlit_processes.values()]
    for process in psutil.process_iter():
        try:
            cmdline = process.cmdline()
            for fpath in fpaths:
                if fpath in cmdline:
                    dangling_processes.append(process)
        except Exception:
            pass
    for p in dangling_processes:
        p.kill()
