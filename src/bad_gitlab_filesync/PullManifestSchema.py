from marshmallow import Schema, fields, validates, ValidationError


class PullManifestFileRecord(Schema):
    """Manifest for a single file"""

    src = fields.String(
        required=True, error_messages={"required": "Must specify file to sync"}
    )
    # Pull this file from a GitLab project.
    # Must be a path within the specified GitLab project.
    dest = fields.String()
    # File path to write synced files to.
    # If left empty, will write to default sync directory.


class PullManifestProject(Schema):
    """Manifest for a single project"""

    ref = fields.String()  # Git branch, tag, or commit to retrieve files from.
    name = fields.String(
        required=True,
        error_messages={
            "required": "Specify a project name",
        },
    )  # Name of project
    files = fields.List(
        fields.Nested(PullManifestFileRecord()),
        required=True,
        error_messages={"required": "You must specify a list of files to pull"},
    )  # List of filepaths to pull from this GitLab project

    @validates("files")
    def validate_file_list(self, file_list):
        if len(file_list) == 0:
            raise ValidationError("`files` list must not be empty")


class PullManifest(Schema):
    """Manifest containing a dictionary of files
    to retrieve from projects on GitLab.
    """

    ref = fields.String()
    # Git reference to apply to all projects.
    projects = fields.List(
        fields.Nested(PullManifestProject()),
        required=True,
        error_messages={"required": "Must specify at least one project"},
    )
    # List of projects
