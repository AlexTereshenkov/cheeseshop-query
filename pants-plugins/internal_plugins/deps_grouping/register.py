from typing import Iterable

from pants.engine.target import Target

import internal_plugins.deps_grouping.rules as deps_grouping_rules
from internal_plugins.deps_grouping.target_types import DepsGroupTarget


def target_types() -> Iterable[type[Target]]:
    return [DepsGroupTarget]


def rules():
    return [
        *deps_grouping_rules.rules(),
    ]
