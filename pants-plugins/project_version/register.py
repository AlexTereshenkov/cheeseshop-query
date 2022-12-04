from project_version.targets import ProjectVersionTarget
import project_version.custom_rules as custom_rules


def target_types():
    return [ProjectVersionTarget]


def rules():
    return [*custom_rules.rules()]
