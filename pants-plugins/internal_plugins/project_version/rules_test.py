import pytest
from pants.build_graph.address import Address
from pants.testutil.rule_runner import QueryRule, RuleRunner

from internal_plugins.project_version.rules import (
    ProjectVersionFileView,
    get_project_version_file_view,
)
from internal_plugins.project_version.target_types import ProjectVersionTarget


@pytest.fixture
def rule_runner() -> RuleRunner:
    return RuleRunner(
        rules=[
            get_project_version_file_view,
            QueryRule(ProjectVersionFileView, [ProjectVersionTarget]),
        ],
        target_types=[ProjectVersionTarget],
    )


def test_get_project_version_file_view(rule_runner: RuleRunner) -> None:
    """Test plugin rules in isolation (not specifying what rules need to be
    run)."""
    rule_runner.write_files(
        {"project/VERSION": "10.6.1", "project/BUILD": "version_file(source='VERSION')"}
    )
    target = rule_runner.get_target(Address("project", target_name="project"))
    result = rule_runner.request(ProjectVersionFileView, [target])
    assert result == ProjectVersionFileView(path="project/VERSION", version="10.6.1")
