import logging
from dataclasses import dataclass

from pants.engine.console import Console
from pants.engine.fs import DigestContents
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.internals.native_engine import Digest
from pants.engine.internals.selectors import Get, MultiGet
from pants.engine.rules import collect_rules, goal_rule, rule
from pants.engine.target import (
    HydratedSources,
    HydrateSourcesRequest,
    SourcesField,
    Targets,
)
from project_version.targets import ProjectVersionTarget

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
async def goal_show_project_version(
    console: Console, targets: Targets
) -> ProjectVersionGoal:
    targets = [tgt for tgt in targets if tgt.alias == ProjectVersionTarget.alias]
    results = await MultiGet(
        Get(ProjectVersionFileView, ProjectVersionTarget, target) for target in targets
    )
    for result in results:
        console.print_stdout(str(result))
    return ProjectVersionGoal(exit_code=0)


def rules():
    return collect_rules()
