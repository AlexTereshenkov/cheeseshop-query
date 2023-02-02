import pytest
from click.testing import CliRunner

from cheeseshop.cli import cli
from cheeseshop.version import VERSION


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["--version"])
    assert result.exit_code == 0
    assert VERSION in result.output


@pytest.mark.vcr()
def test_cli_info():
    runner = CliRunner()
    with open("tests/testdata/test_package_name.txt") as fh:
        package_name = fh.read().strip()
    result = runner.invoke(cli.cli, ["info", "--package", package_name])
    assert result.exit_code == 0
    assert "Core utilities for Python packages" in result.output


@pytest.mark.vcr()
def test_cli_list_versions():
    runner = CliRunner()
    result = runner.invoke(
        cli.cli,
        [
            "list-versions",
            "--package=numpy",
            "--python-version=cp38",
            "--package-type=bdist_wheel",
            "--platform=macos",
            "--arch=x86_64",
        ],
    )
    assert result.exit_code == 0
    assert "numpy==1.17.3" in result.output
