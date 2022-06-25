import click
from cheeseshop.version import VERSION


HELP_OPTS = dict(help_option_names=["-h", "--help"])


@click.group()
@click.version_option(VERSION)
def cli():
    """Main entrance point."""
    return
