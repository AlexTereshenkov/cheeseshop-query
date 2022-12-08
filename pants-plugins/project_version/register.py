from typing import Iterable

import project_version.rules as project_version_rules
from pants.engine.target import Target
from project_version.target_types import ProjectVersionTarget


def target_types() -> Iterable[type[Target]]:
    return [ProjectVersionTarget]


def rules():
    return [*project_version_rules.rules()]
