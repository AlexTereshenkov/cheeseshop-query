import project_version.rules as project_version_rules
from project_version.targets import ProjectVersionTarget


def target_types():
    return [ProjectVersionTarget]


def rules():
    return [*project_version_rules.rules()]
