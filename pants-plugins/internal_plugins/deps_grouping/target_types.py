from pants.engine.target import COMMON_TARGET_FIELDS, SingleSourceField, Target


class DepsGroupSourceField(SingleSourceField):
    alias = "source"
    help = "Path to the file with the dependency groups."
    required = True


class DepsGroupTarget(Target):
    alias = "deps_group"
    core_fields = (*COMMON_TARGET_FIELDS, DepsGroupSourceField)
    help = "A dependency group target with access to dependency groups stored in a given file."
