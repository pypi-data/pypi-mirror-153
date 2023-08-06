import os

import click

from harpo.cli.user.commands import complete_user_name
from harpo.cli.util import complete_from_list, print_formatted, with_harpo_context
from harpo.main import Harpo
from harpo.util import find_harpo_basedir


def complete_group_name(ctx, args, incomplete):
    """Complete group name

    NOTE: Context is not yet initialized
    and we have no access to default options values from here

    So just return empty list if we weren't successful
    in determining harpo base_dir
    """
    base_dir = ctx.parent.parent.params.get("base_dir") or find_harpo_basedir()
    if base_dir is not None and os.path.isdir(base_dir):
        harpo = Harpo(base_dir, gpg_home=None)
        return complete_from_list(incomplete, harpo.groups.list())
    else:
        return []


@click.group()
def group():
    """Manage groups"""
    pass


@group.command()
@click.argument("group_name")
@with_harpo_context
def create(harpo, common_parameters, group_name):
    harpo.group_create(group_name)


@group.command()
@click.argument("group_name", shell_complete=complete_group_name)
@with_harpo_context
def destroy(harpo, common_parameters, group_name):
    harpo.group_destroy(group_name)


@group.command()
@with_harpo_context
def list(harpo, common_parameters):
    print_formatted(harpo.group_list(), output_format=common_parameters["format"])


@group.command()
@click.argument("group_name", shell_complete=complete_group_name)
@click.argument("user_name", shell_complete=complete_user_name)
@with_harpo_context
def include_user(harpo, common_parameters, group_name, user_name):
    """Add user to group"""
    harpo.group_include_user(group_name, user_name)


@group.command()
@click.argument("group_name", shell_complete=complete_group_name)
@click.argument("user_name", shell_complete=complete_user_name)
@with_harpo_context
def exclude_user(harpo, common_parameters, group_name, user_name):
    """Remove user from group"""
    harpo.group_exclude_user(group_name, user_name)
