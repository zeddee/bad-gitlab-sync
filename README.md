# Bad GitLab Filesync

## Install

```bash
python -m pip install git+https://github.com/zeddee/bad-gitlab-filesync.git
```

## Usage: CLI

This package provides a rudimentary command-line script.
To sync files listed in `./manifest.json`, run in the same directory:

```bash
GITLAB_ACCESS_KEY=<gitlab_access_key> gitlab-filesync
```

See the ``example.manifest.json`` file for an example of how the manifest file should look like.

## Usage: Python library

You can also import the package and use it in
your Python scripts for more granular control:

```python
from bad_gitlab_filesync import FileSyncClient
from os import environ

GITLAB_ACCESS_TOKEN = environ.get("GITLAB_ACCESS_TOKEN")
GITLAB_HOST = "https://gitlab.com" # Default value; you can omit this.

client = FileSyncClient(gitlab_url=GITLAB_HOST, gitlab_access_token=GITLAB_ACCESS_TOKEN)

manifest = {
  "projects": {
    "name": "<project_name>",
    "files": [
      {
        "src": "file/path.rst",
      }
    ]
  }
}

client.pull_from_manifest(manifest)
```

## Manifest

| Field | Required | Description |
|-|-|-|
| `.ref` | No | Git reference to apply to all projects. Defaults to 'master'. |
| `.projects` | Yes | A list of projects to pull files from. |
| `.projects[].name` | Yes | The name of your GitLab project. This should be the `<project_name>` portion of your repository URL `gitlab.com/<username>/<project_name>` |
| `.projects[].ref` | No | Git ref to apply to this project. Inherits from `.ref` |
| `.projects[].files` | Yes | A list of dictionaries specifying where to pull files from, and where to write them to. |
| `.projects[].files[].src` | Yes | Path to a file on the GitLab project to pull. |
| `.projects[].files[].dest` | No | Path on the local filesystem to write the pulled file to. |

Example `manifest.json`:

```json
{
  "ref": "master",
  "projects": [
    {
      "name": "docs-management",
      "ref": "1-draft-km-policy",
      "files": [
        {
        "src": "README.rst",
        "dest": "docs-management/readme.rst"
      }
      ]
    },
    {
      "name": "new-ganges",
      "files": [
        {
          "src": "site/basic-rules/README.md"
        }
      ]
    }
  ]
}
```