from __future__ import annotations

from dataclasses import dataclass

from pants.core.goals.tailor import (
    AllOwnedSources,
    PutativeTarget,
    PutativeTargets,
    PutativeTargetsRequest,
    group_by_dir,
)
from pants.engine.fs import PathGlobs, Paths
from pants.engine.internals.selectors import Get
from pants.engine.rules import collect_rules, rule
from pants.engine.unions import UnionRule
from project_version.target_types import ProjectVersionTarget


@dataclass(frozen=True)
class PutativeProjectVersionTargetsRequest(PutativeTargetsRequest):
    pass


@rule(desc="Determine candidate project_version targets to create")
async def find_putative_targets(
    req: PutativeProjectVersionTargetsRequest,
    all_owned_sources: AllOwnedSources,
) -> PutativeTargets:
    all_project_version_files = await Get(Paths, PathGlobs, req.path_globs("VERSION"))
    unowned_project_version_files = set(all_project_version_files.files) - set(
        all_owned_sources
    )
    classified_unowned_project_version_files = {
        ProjectVersionTarget: unowned_project_version_files
    }

    putative_targets = []
    for tgt_type, paths in classified_unowned_project_version_files.items():
        for dirname, filenames in group_by_dir(paths).items():
            putative_targets.append(
                PutativeTarget.for_target_type(
                    ProjectVersionTarget,
                    path=dirname,
                    name="project-version-file",
                    triggering_sources=sorted(filenames),
                )
            )

    return PutativeTargets(putative_targets)


def rules():
    return [
        *collect_rules(),
        UnionRule(PutativeTargetsRequest, PutativeProjectVersionTargetsRequest),
    ]
