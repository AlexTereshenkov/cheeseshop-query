import sys

import click
from loguru import logger

from cheeseshop.repository.repository import Repository
from cheeseshop.version import VERSION

HELP_OPTS = dict(help_option_names=["-h", "--help"])


@click.group()
@click.version_option(VERSION)
@click.pass_context
def cli(ctx: click.Context):
    """Main entrance point."""
    return


@cli.command()
@click.option(
    "--package", "package_name", help="Package name to get information about."
)
def info(package_name: str) -> None:
    """Show information about the package."""
    repository = Repository()
    try:
        package = repository.get(package_name)
    except Exception as err:
        logger.error(str(err))
        sys.exit(1)

    click.echo(package.info.summary)
    return


if __name__ == "__main__":
    # for local debugging
    info(["--package", "tabulate"])
