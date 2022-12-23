from pants.engine.target import COMMON_TARGET_FIELDS, SingleSourceField, Target


class ProjectVersionSourceField(SingleSourceField):
    alias = "source"
    help = "Path to the file with the project version."
    default = "VERSION"
    required = False


class ProjectVersionTarget(Target):
    alias = "version_file"
    core_fields = (*COMMON_TARGET_FIELDS, ProjectVersionSourceField)
    help = "A project version target representing the VERSION file."
