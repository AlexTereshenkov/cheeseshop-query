from pants.engine.console import Console
from pants.engine.fs import DigestContents
from pants.engine.goal import GoalSubsystem, Goal
from pants.engine.internals.native_engine import Digest
from pants.engine.internals.selectors import Get, MultiGet
from pants.engine.rules import collect_rules, rule, goal_rule
from pants.engine.target import (
    Targets,
    HydratedSources,
    HydrateSourcesRequest,
    SourcesField,
)

from project_version.targets import ProjectVersionTarget
from dataclasses import dataclass


import logging

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProjectVersionFileView:
    path: str
    version: str


@rule
async def get_project_version_file_view(
    target: ProjectVersionTarget,
) -> ProjectVersionFileView:
    # TODO: is running `--no-pantsd` the only option to make sure logger messages are
    #  shown in the console?
    # TODO: how to set value for a field? custom_target[CustomField].value = "SomeValue"
    sources = await Get(HydratedSources, HydrateSourcesRequest(target[SourcesField]))
    digest_contents = await Get(DigestContents, Digest, sources.snapshot.digest)

    # TODO: better way to check that the repo contains only one target of a certain type
    if len(digest_contents) > 1:
        raise ValueError("There should be only one source file.")

    file_content = digest_contents[0]
    return ProjectVersionFileView(
        path=file_content.path, version=file_content.content.decode("utf-8").strip()
    )


class ProjectVersionSubsystem(GoalSubsystem):
    name = "project-version"
    help = "Show representation of the project version from the `VERSION` file."


class ProjectVersionGoal(Goal):
    subsystem_cls = ProjectVersionSubsystem


@goal_rule
async def main(console: Console, targets: Targets) -> ProjectVersionGoal:
    targets = [tgt for tgt in targets if tgt.alias == ProjectVersionTarget.alias]

    # instead of doing:
    # for target in targets:
    #     console.print_stdout(target.address.spec)
    #     # await Get(OutputType, InputType, input)
    #     result = await Get(MyResult, CustomTarget, target)
    #     console.print_stdout(result)
    # we can use MultiGet
    # https://www.pantsbuild.org/docs/rules-api-concepts#multiget-for-concurrency
    results = await MultiGet(
        Get(ProjectVersionFileView, ProjectVersionTarget, target) for target in targets
    )
    console.print_stdout(str(results[0]))
    return ProjectVersionGoal(exit_code=0)


def rules():
    return collect_rules()
