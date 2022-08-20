import sys

import click
from loguru import logger

from cheeseshop.cli.utils import choices
from cheeseshop.repository.query import get_versions, filter_releases, is_stable_version
from cheeseshop.repository.package import PackageType
from cheeseshop.repository.properties import Platform, Architecture
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


@cli.command()
@click.option("--package", "package_name", help="Package name.")
@click.option("--python-version", "python_version", help="Python version.")
@click.option(
    "--package-type",
    "package_type",
    help="Python package type.",
    type=click.Choice(choices(PackageType)),
)
@click.option(
    "--platform",
    "platform",
    help="Platform name.",
    type=click.Choice(choices(Platform)),
)
@click.option(
    "--arch",
    "arch",
    help="Architecture name.",
    type=click.Choice(choices(Architecture)),
)
@click.option(
    "--stable-only",
    "stable_only",
    help="Set to ignore dev-, pre-, and post-releases.",
    is_flag=True,
    default=False,
)
def list_versions(
    package_name: str,
    python_version: str,
    package_type: str,
    platform: str,
    arch: str,
    stable_only: bool,
) -> None:
    """Get compatible versions given the query."""
    repository = Repository()
    try:
        package = repository.get(package_name)
        releases = filter_releases(
            package=package,
            python_version=python_version,
            package_type=package_type,
            platform=platform,
            arch=arch,
        )
        filters = [is_stable_version] if stable_only else []
        versions = get_versions(
            releases=releases,
            filters=filters,
        )
        versions.sort()

    except Exception as err:
        logger.error(str(err))
        sys.exit(1)

    for v in versions:
        click.echo(f"{package_name}=={v}")
    return


if __name__ == "__main__":
    cli()
    # for local debugging
    # list_versions(
    #     [
    #         "--package=numpy",
    #         "--python-version=cp310",
    #         "--package-type=bdist_wheel",
    #         "--platform=macos",
    #         "--arch=x86_64",
    #         "--stable-only",
    #     ]
    # )
