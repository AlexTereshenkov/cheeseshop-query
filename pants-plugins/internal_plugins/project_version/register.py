from typing import Iterable

import internal_plugins.project_version.rules as project_version_rules
import internal_plugins.project_version.tailor as tailor_rules
from internal_plugins.project_version.target_types import ProjectVersionTarget
from pants.engine.target import Target


def target_types() -> Iterable[type[Target]]:
    return [ProjectVersionTarget]


def rules():
    return [*project_version_rules.rules(), *tailor_rules.rules()]
