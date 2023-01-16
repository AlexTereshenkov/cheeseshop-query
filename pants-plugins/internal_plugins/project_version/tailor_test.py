from pathlib import Path

import pytest
from pants.core.goals.tailor import AllOwnedSources, PutativeTarget, PutativeTargets
from pants.engine.rules import QueryRule
from pants.testutil.rule_runner import RuleRunner

from internal_plugins.project_version.tailor import (
    PutativeProjectVersionTargetsRequest,
    rules,
)
from internal_plugins.project_version.target_types import ProjectVersionTarget


@pytest.fixture
def rule_runner() -> RuleRunner:
    return RuleRunner(
        rules=[
            *rules(),
            QueryRule(
                PutativeTargets, (PutativeProjectVersionTargetsRequest, AllOwnedSources)
            ),
        ],
        target_types=[ProjectVersionTarget],
    )


def test_find_putative_avnpkg_files_targets(rule_runner: RuleRunner) -> None:
    """Test generating `version_file` targets in a project directory."""
    files = {
        "project/dir1/VERSION": "10.6.1",
        "project/dir2/file.txt": "",
        "project/dir3/VERSION": "10.7.1",
        # Note that dir3/VERSION already has the target and should be ignored.
        "project/dir3/BUILD": "version_file(source='VERSION')",
    }
    rule_runner.write_files(files)
    for filepath, _ in files.items():
        assert Path(rule_runner.build_root, filepath).exists()

    putative_targets = rule_runner.request(
        PutativeTargets,
        [
            PutativeProjectVersionTargetsRequest(
                ("project/dir1", "project/dir2", "project/dir3"),
            ),
            # Declare that all these files in the project are already owned by targets.
            AllOwnedSources(["project/dir2/file.txt", "project/dir3/VERSION"]),
        ],
    )

    assert (
        PutativeTargets(
            [
                PutativeTarget(
                    path="project/dir1",
                    name="project-version-file",
                    type_alias="version_file",
                    triggering_sources=("VERSION",),
                    owned_sources=("VERSION",),
                )
            ]
        )
        == putative_targets
    )
