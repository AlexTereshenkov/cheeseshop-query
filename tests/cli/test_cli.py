from click.testing import CliRunner

from cheeseshop.cli import cli
from cheeseshop.version import VERSION


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["--version"])
    assert result.exit_code == 0
    assert VERSION in result.output


def test_cli_info():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["info", "--package", "packaging"])
    assert result.exit_code == 0
    assert "Core utilities for Python packages" in result.output
