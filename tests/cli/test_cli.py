import pytest
from click.testing import CliRunner

import tabulate
from cheeseshop.cli import cli
from cheeseshop.version import VERSION


def test_cli():

    assert tabulate.tabulate("") == ""
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["--version"])
    assert result.exit_code == 0
    assert VERSION in result.output


@pytest.mark.vcr()
def test_cli_info():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["info", "--package", "packaging"])
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
