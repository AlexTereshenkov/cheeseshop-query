import dataclasses
import json
import logging
import os
from dataclasses import dataclass

from packaging.version import InvalidVersion, Version
from pants.core.util_rules.system_binaries import BinaryPathRequest, BinaryPaths
from pants.engine.console import Console
from pants.engine.fs import DigestContents
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.internals.native_engine import Digest
from pants.engine.internals.selectors import Get, MultiGet
from pants.engine.process import Process, ProcessCacheScope, ProcessResult
from pants.engine.rules import collect_rules, goal_rule, rule
from pants.engine.target import (
    HydratedSources,
    HydrateSourcesRequest,
    SourcesField,
    Targets,
)
from pants.option.option_types import BoolOption
from project_version.target_types import ProjectVersionSourceField, ProjectVersionTarget

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProjectVersionFileView:
    path: str
    version: str


@rule
async def get_project_version_file_view(
    target: ProjectVersionTarget,
) -> ProjectVersionFileView:
    sources = await Get(HydratedSources, HydrateSourcesRequest(target[SourcesField]))
    digest_contents = await Get(DigestContents, Digest, sources.snapshot.digest)
    file_content = digest_contents[0]
    return ProjectVersionFileView(
        path=file_content.path, version=file_content.content.decode("utf-8").strip()
    )


class ProjectVersionSubsystem(GoalSubsystem):
    name = "project-version"
    help = "Show representation of the project version from the `VERSION` file."

    as_json = BoolOption(
        default=False,
        help="Show project version information as JSON.",
    )
    check_git = BoolOption(
        default=False,
        help="Check Git tag of the repository matches the project version.",
    )


class ProjectVersionGoal(Goal):
    subsystem_cls = ProjectVersionSubsystem


class InvalidProjectVersionString(ValueError):
    pass


class ProjectVersionGitTagMismatch(ValueError):
    pass


class GitTagVersion(str):
    pass


@goal_rule
async def goal_show_project_version(
    console: Console,
    targets: Targets,
    project_version_subsystem: ProjectVersionSubsystem,
) -> ProjectVersionGoal:
    targets = [tgt for tgt in targets if tgt.has_field(ProjectVersionSourceField)]
    results = await MultiGet(
        Get(ProjectVersionFileView, ProjectVersionTarget, target) for target in targets
    )
    if project_version_subsystem.check_git:
        git_repo_version = await Get(GitTagVersion, str, "")

    for result in results:
        try:
            _ = Version(result.version)
        except InvalidVersion:
            raise InvalidProjectVersionString(
                f"Invalid version string '{result.version}' from '{result.path}'"
            )
        if project_version_subsystem.check_git:
            if git_repo_version != result.version:
                raise ProjectVersionGitTagMismatch(
                    f"Project version string '{result.version}' from '{result.path}' "
                    f"doesn't match latest Git tag '{git_repo_version}'"
                )

        if project_version_subsystem.as_json:
            console.print_stdout(json.dumps(dataclasses.asdict(result)))
        else:
            console.print_stdout(str(result))

    return ProjectVersionGoal(exit_code=0)


@rule
async def get_git_repo_version(description: str = "") -> GitTagVersion:
    git_paths = await Get(
        BinaryPaths,
        BinaryPathRequest(
            binary_name="git",
            search_path=["/usr/bin", "/bin"],
        ),
    )
    git_bin = git_paths.first_path
    if git_bin is None:
        raise OSError("Could not find 'git'.")
    git_describe = await Get(
        ProcessResult,
        Process(
            argv=[git_bin.path, "-C", os.getcwd(), "describe", "--tags"],
            description=description,
            cache_scope=ProcessCacheScope.PER_SESSION,
        ),
    )
    return GitTagVersion(git_describe.stdout.decode().strip())


def rules():
    return collect_rules()
