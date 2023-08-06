import importlib
import os
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from dataclasses_json import dataclass_json

import databutton as db
from databutton.decorators.apps.streamlit import StreamlitApp
from databutton.decorators.jobs.schedule import DatabuttonSchedule
from databutton.helpers import parse
from databutton.kubernetes.generate import generate_manifest
from databutton.version import __version__


@dataclass_json
@dataclass
class ArtifactDict:
    streamlit_apps: List[StreamlitApp] = field(default_factory=List)
    schedules: List[DatabuttonSchedule] = field(default_factory=List)


def generate_artifacts_json():
    # Sort the apps so that the port proxy remains stable
    for i, st in enumerate(sorted(db.apps._streamlit_apps, key=lambda x: x.route)):
        st.port = 8501 + i
    artifacts = ArtifactDict(
        streamlit_apps=[st for st in db.apps._streamlit_apps],
        schedules=[sched for sched in db.jobs._schedules],
    )
    return artifacts


def write_artifacts_json(artifacts: ArtifactDict):
    with open(Path(".databutton", "artifacts.json"), "w") as f:
        f.write(artifacts.to_json())


def read_artifacts_json() -> ArtifactDict:
    with open(Path(".databutton", "artifacts.json"), "r") as f:
        return ArtifactDict.from_json(f.read())


def generate_components(rootdir: Path = Path.cwd()):
    normalized_rootdir = rootdir.resolve().relative_to(Path.cwd())
    sys.path.insert(0, str(rootdir.resolve()))
    # Find all directive modules and import them
    imports = parse.find_databutton_directive_modules(rootdir=normalized_rootdir)

    # Clean the existing artifacts, generate new one
    # TODO: Have a cache mechanism to improve performance
    shutil.rmtree(Path(".databutton"), ignore_errors=True)
    os.makedirs(Path(".databutton"))
    decorator_modules = {}
    for name in imports:
        decorator_modules[name] = importlib.import_module(name)

    # Write the artifacts
    # Sort the apps so that the port proxy remains stable
    artifacts = generate_artifacts_json()
    write_artifacts_json(artifacts)

    # Copy the Dockerfile
    parent_folder = Path(__file__).parent.parent
    current_dockerfile_path = Path(parent_folder, "docker", "Dockerfile")

    docker_folder_path = Path(".databutton", "docker")
    docker_folder_path.mkdir(exist_ok=True, parents=True)
    dest_dockerfile_path = Path(docker_folder_path, "Dockerfile")
    with open(current_dockerfile_path, "r") as original:
        contents = original.read()
        with open(dest_dockerfile_path, "w") as dest:
            dest.write(
                # Overwrite image
                contents.replace("REPLACE_ME_VERSION", __version__)
            )

    # Generate a kubernetes manifest
    generate_manifest(artifacts)
    return artifacts
