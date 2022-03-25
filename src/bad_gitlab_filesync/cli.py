import json
from os import environ
from pathlib import Path

from dotenv import load_dotenv

from .client import FileSyncClient

load_dotenv()


def main():
    GITLAB_ACCESS_TOKEN: str = environ.get("GITLAB_ACCESS_TOKEN", "")
    # Access token should at least
    # have ``read-api`` permissions.

    GITLAB_URL: str = environ.get("GITLAB_URL", "https://www.gitlab.com")
    MANIFEST_FILE: Path = environ.get("MANIFEST_FILE", Path("manifest.json"))

    client = FileSyncClient(
        gitlab_url=GITLAB_URL, gitlab_access_token=GITLAB_ACCESS_TOKEN
    )

    with MANIFEST_FILE.open("r") as fp:
        client.pull_from_manifest(json.loads(fp.read()))