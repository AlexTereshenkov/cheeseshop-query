import pytest
from pants.engine.internals.scheduler import ExecutionError
from pants.testutil.rule_runner import RuleRunner

from internal_plugins.project_version.rules import ProjectVersionGoal
from internal_plugins.project_version.rules import rules as project_version_rules
from internal_plugins.project_version.target_types import ProjectVersionTarget


@pytest.fixture
def rule_runner() -> RuleRunner:
    return RuleRunner(
        rules=project_version_rules(), target_types=[ProjectVersionTarget]
    )


def test_project_version_goal(rule_runner: RuleRunner) -> None:
    """Test a `project-version` goal using VERSION files."""
    rule_runner.write_files(
        {
            "project/VERSION": "10.6.1",
            "project/BUILD": "version_file(source='VERSION')",
        }
    )
    result = rule_runner.run_goal_rule(
        ProjectVersionGoal, args=["--as-json", "project:"]
    )
    assert result.stdout.splitlines() == [
        '{"path": "project/VERSION", "version": "10.6.1"}'
    ]

    # invalid version string
    rule_runner.write_files(
        {
            "project/VERSION": "foo.bar",
            "project/BUILD": "version_file(source='VERSION')",
        }
    )
    with pytest.raises(ExecutionError):
        rule_runner.run_goal_rule(ProjectVersionGoal, args=["project:"])
