from unittest.mock import Mock

from pants.base.build_root import BuildRoot
from pants.core.util_rules.system_binaries import (
    BinaryPath,
    BinaryPathRequest,
    BinaryPaths,
)
from pants.engine.process import Process, ProcessResult
from pants.testutil.rule_runner import MockGet, run_rule_with_mocks

from internal_plugins.project_version.rules import GitTagVersion, get_git_repo_version


def test_get_git_version() -> None:
    """Test running a specific rule returning a GitVersion."""

    def mock_binary_paths(request: BinaryPathRequest) -> BinaryPaths:
        return BinaryPaths(binary_name="git", paths=[BinaryPath("/usr/bin/git")])

    def mock_process_git_describe(process: Process) -> ProcessResult:
        return Mock(stdout=b"10.6.1\n")

    result: GitTagVersion = run_rule_with_mocks(
        get_git_repo_version,
        rule_args=[BuildRoot, ""],
        mock_gets=[
            MockGet(
                output_type=BinaryPaths,
                input_type=BinaryPathRequest,
                mock=mock_binary_paths,
            ),
            MockGet(
                output_type=ProcessResult,
                input_type=Process,
                mock=mock_process_git_describe,
            ),
        ],
    )
    assert result == GitTagVersion("10.6.1")
