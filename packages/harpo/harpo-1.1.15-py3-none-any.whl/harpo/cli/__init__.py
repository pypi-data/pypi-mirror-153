# coding=utf-8

import logging
import sys

import click

from harpo.log import configure_logging, get_logger

# Click doesn't work properly on Py2.7
if sys.version_info < (3, 0):
    configure_logging()
    logger = get_logger()
    logger.error("Sorry, Harpo CLI requires Python 3.x")
    logger.info("However the library itself is fully functional under Python 2.7")
    sys.exit(1)

from harpo.cli.domain.commands import domain
from harpo.cli.group.commands import group
from harpo.cli.key.commands import key
from harpo.cli.secret.commands import secret
from harpo.cli.system.commands import system
from harpo.cli.user.commands import user


def get_version():
    """
    Returns the version string
    """
    try:
        import importlib.metadata as importlib_metadata
    except ImportError:
        # In python 3.6, we rely on the backport of the stdlib package
        import importlib_metadata  # type: ignore

    full_version = str(importlib_metadata.version("harpo"))
    return full_version


@click.group()
@click.option("--debug", is_flag=True)
@click.option("-v", "--verbose", count=True)
@click.option(
    "--format",
    type=click.Choice(choices=["json", "yaml", "normal"]),
    default="normal",
    show_default=True,
)
@click.option("--base-dir", type=click.Path())
@click.option("--gpg-home", type=click.Path(), default="$HOME/.gnupg", show_default=True)
@click.version_option(version=get_version())
def main(debug, verbose, format, base_dir, gpg_home):
    """Harpo CLI

    PROTIP: Enable autocompletion using the following command:

        eval "$(_HARPO_COMPLETE=bash_source harpo)"
    """
    level = logging.DEBUG - verbose + 1 if verbose > 0 else logging.INFO
    configure_logging(level)


main.add_command(domain)
main.add_command(group)
main.add_command(key)
main.add_command(secret)
main.add_command(user)
main.add_command(system)
