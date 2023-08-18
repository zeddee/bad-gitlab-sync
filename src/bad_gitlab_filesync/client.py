import base64
import logging
from pathlib import Path
from typing import Dict, List

import gitlab

from .PullManifestSchema import PullManifest, PullManifestProject
from .RunSummary import RunSummary

logging.basicConfig(level=logging.INFO)


class FileSyncClient:
    def __init__(
        self,
        gitlab_url: str = "https://gitlab.com",
        gitlab_access_token: str = "",
    ):
        """Create a client object
        acting as middleware that interacts with GitLab APIv4.
        """
        self.SUMMARY = RunSummary()
        if gitlab_access_token == "" or None:
            # Require authentication because we rely on
            # GitLab.projects.list to retrieve a list
            # of owned project, to which we find and match
            # project names from manifest.json
            self.SUMMARY.error += 1
            raise ValueError("Cannot find GitLab access token")

        self.gl = gitlab.Gitlab(url=gitlab_url, private_token=gitlab_access_token)
        # Init RunSummary object. Used to count and present log level occurences at the end of a run.

    def _get_owned_projects(self) -> List[Dict[str, int]]:
        """
        Retrieves a list of projects owned by the authenticated user.
        Convenience function to help check if a project is known and accessible,
        and subsequently retrieve the ID of that project.

        :return: A list of a {<project_name>: <project_id>} key-value pair.
        """
        out = []
        project_list = self.gl.projects.list(owned=True, as_list=False)
        for project in project_list:
            out.append({project.attributes["path"]: project.get_id()})

        return out

    def _pull_files_from_project(
        self,
        project: PullManifestProject,
        ref: str = "master",
        default_sync_basedir: Path = Path("./_synced"),
    ):
        """Pull files from a project drawing parameters from a PullManifestProject object.

        :param project: A PullManifestProject object.
        :param ref: Git reference. This will be overwritten if the PullManifestProject already specifies a 'ref'.
        :default_sync_basedir: The default directory to write pulled files to.
        """
        proj = PullManifestProject().dump(project)

        if proj.get("ref"):
            # If 'ref' is specified in PullManifestProject object,
            # then prefer this over the global 'ref'.
            ref = proj.get("ref")

        proj_id = ""

        for _p in self._get_owned_projects():
            if proj["name"] in _p.keys():
                proj_id = _p.get(proj["name"])

        if proj_id is ("" or None):
            self.SUMMARY.warnings += 1
            logging.warning(f"Empty project name: {proj['name']}")

        try:
            gl_proj = self.gl.projects.get(id=proj_id)
        except gitlab.exceptions.GitlabParsingError as e:
            self.SUMMARY.errors += 1
            logging.error("Cannot find project: {proj_id}")
            raise e

        for file in proj["files"]:
            logging.info(f"Retrieving file {proj['name']}/{file['src']}@{ref}")
            try:
                obj = gl_proj.files.get(file_path=file["src"], ref=ref)
            except gitlab.exceptions.GitlabGetError as e:
                self.SUMMARY.warnings += 1
                logging.warning(f"Could not find {file['src']}: {e}")
                continue
            content_b64: str = obj.content

            if file.get("dest"):
                dest = Path(file["dest"])
            else:
                dest: Path = default_sync_basedir.joinpath(
                    project.get("name")
                ).joinpath(file["src"])
                # Construct a file write destination
                # that mirrors the file's location on the project.

            dest.parent.mkdir(parents=True, exist_ok=True)

            with dest.open("wb") as fp:
                buffer = base64.b64decode(content_b64)
                fp.write(buffer)
                fp.close()
                self.SUMMARY.success += 1
                logging.info(f"Success: Written to {dest}")

    def pull_from_manifest(self, manifest: PullManifest):
        _manifest = PullManifest().dump(manifest)

        for project in _manifest["projects"]:
            self._pull_files_from_project(project, _manifest.get("ref", "master"))
