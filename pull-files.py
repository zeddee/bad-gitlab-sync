import os
import base64
import json
import io
import logging
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
import gitlab
from gitlab.v4.objects import files, Project

load_dotenv()
logging.basicConfig(level=logging.INFO)

GITLAB_ACCESS_TOKEN: str = os.environ.get("ACCESS_TOKEN", "")
# Access token should at least
# have ``read-api`` permissions.

GITLAB_URL: str = "https://www.gitlab.com"
SYNC_BASEDIR: Path = Path("_synced")
MANIFEST_FILE: Path = Path("manifest.json")


def pull_files_from_project(client: gitlab.Gitlab, project: Dict[str, str], ref: str) -> None:
    # Allow specifying 'ref' in 'project' dict
    if not ref:
        ref = project.get("ref", "")
    repo = client.projects.get(project.get("id"))

    file_list: List[str] = project.get("files", [])

    if len(file_list) == 0:
        raise Exception(f"No files to sync in {project['name']}@{ref}")

    for file_path in file_list:
        obj = repo.files.get(file_path=file_path, ref=ref)

        content_b64: str = obj.content

        dest: Path = SYNC_BASEDIR.joinpath(project.get("name")).joinpath(file_path)

        logging.info(f"Pulling file {dest} from {project['name']}@{ref}")

        dest.parent.mkdir(parents=True, exist_ok=True)

        with open(dest, "wb") as fp:
            buffer = base64.b64decode(content_b64)
            fp.write(buffer)
            fp.close()


def pull_from_manifest(
        gitlab_url=GITLAB_URL,
        gitlab_token=GITLAB_ACCESS_TOKEN,
):
    with gitlab.Gitlab(url=gitlab_url, private_token=gitlab_token) as gl:
        gl.auth()

        # TODO:
        # - Should create a proper and validated data structure here
        manifest: Dict[str, Any] = json.loads(MANIFEST_FILE.read_bytes())
        ref: str = manifest.get("ref")
        projects: List = manifest.get("projects", [])

        if len(projects) == 0:
            raise Exception("No projects listed in manifest")

        for project in projects:
            pull_files_from_project(gl, project, ref)


if __name__ == "__main__":
    pull_from_manifest()
