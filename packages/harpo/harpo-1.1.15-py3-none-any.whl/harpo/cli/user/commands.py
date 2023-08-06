import os

import click

from harpo.cli.util import complete_from_list, print_formatted, with_harpo_context
from harpo.main import Harpo
from harpo.util import find_harpo_basedir


def complete_user_name(ctx, args, incomplete):
    """Complete domain name

    NOTE: Context is not yet initialized
    and we have no access to default options values from here

    So just return empty list if we weren't successful
    in determining harpo base_dir
    """
    base_dir = ctx.parent.parent.params.get("base_dir") or find_harpo_basedir()
    if base_dir is not None and os.path.isdir(base_dir):
        harpo = Harpo(base_dir, gpg_home=None)
        return complete_from_list(incomplete, harpo.users.list())
    else:
        return []


@click.group()
def user():
    """Manage users"""
    pass


@user.command()
@click.argument("user_name")
@click.argument(
    "key_fingerprint",
)
@with_harpo_context
def create(harpo, common_parameters, user_name, key_fingerprint):
    harpo.user_create(user_name=user_name, key_fingerprint=key_fingerprint)


@user.command()
@click.argument("user_name", shell_complete=complete_user_name)
@with_harpo_context
def destroy(harpo, common_parameters, user_name):
    harpo.user_destroy(user_name)


@user.command()
@with_harpo_context
def list(harpo, common_parameters):
    print_formatted(harpo.user_list(), output_format=common_parameters["format"])
