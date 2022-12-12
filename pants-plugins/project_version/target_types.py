from pants.engine.target import COMMON_TARGET_FIELDS, SingleSourceField, Target


class ProjectVersionTarget(Target):
    alias = "version_file"
    core_fields = (*COMMON_TARGET_FIELDS, SingleSourceField)
    help = "A project version target representing the VERSION file."
