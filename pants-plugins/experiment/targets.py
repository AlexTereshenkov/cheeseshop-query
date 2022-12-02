from pants.engine.target import (
    COMMON_TARGET_FIELDS,
    Dependencies,
    SingleSourceField,
    StringField,
    Target,
)


class CustomField(StringField):
    alias = "custom_field"
    help = "A custom field."


class CustomTarget(Target):
    alias = "custom_target"
    core_fields = (*COMMON_TARGET_FIELDS, Dependencies, SingleSourceField, CustomField)
    help = (
        "A custom target to demo the Target API.\n\n"
        "This docstring will be used in the output of "
        "`./pants help $target_type`."
    )
