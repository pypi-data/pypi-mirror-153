import os

import click

from harpo.main import Harpo
from harpo.util import find_harpo_basedir

from ..group.commands import complete_group_name
from ..user.commands import complete_user_name
from ..util import complete_from_list, print_formatted, with_harpo_context


def complete_domain_name(ctx, args, incomplete):
    """Complete domain name

    NOTE: Context is not yet initialized
    and we have no access to default options values from here

    So just return empty list if we weren't successful
    in determining harpo base_dir
    """
    base_dir = ctx.parent.parent.params.get("base_dir") or find_harpo_basedir()
    if base_dir is not None and os.path.isdir(base_dir):
        harpo = Harpo(base_dir, gpg_home=None)
        return complete_from_list(incomplete, [str(domain) for domain in harpo.domains.list()])
    else:
        return []


@click.group()
def domain():
    """Manage domains"""


@domain.command()
@click.option(
    "--no-inherit-recipients",
    is_flag=True,
    help="This domain should not inherit recipients from its parent",
)
@click.argument("domain_name", shell_complete=complete_domain_name)
@with_harpo_context
def create(harpo, common_parameters, domain_name, no_inherit_recipients):
    """Create a new domain"""
    inherit_recipients = not no_inherit_recipients
    harpo.domain_create(domain_name, inherit_recipients=inherit_recipients)


@domain.command()
@click.argument("domain_name", shell_complete=complete_domain_name)
@with_harpo_context
def destroy(harpo, common_parameters, domain_name):
    """Destroy an existing domain"""
    harpo.domain_destroy(domain_name)


@domain.command()
@with_harpo_context
def list(harpo, common_parameters):
    """List all existing domains"""
    result = [domain.dict() for domain in harpo.domain_list()]
    print_formatted(result, output_format=common_parameters["format"])


@domain.command()
@click.argument("domain_name", shell_complete=complete_domain_name)
@with_harpo_context
def info(harpo, common_parameters, domain_name):
    """Show detailed information about domain"""
    print_formatted(harpo.domain_info(domain_name), output_format=common_parameters["format"])


def complete_user_and_group(ctx, args, incomplete):
    if incomplete.startswith("%"):
        incomplete = incomplete[1:]
    user_results = complete_user_name(ctx, args, incomplete)
    group_results = complete_group_name(ctx, args, incomplete)
    group_results = ["%" + group for group in group_results]
    return user_results + group_results


@domain.command()
@click.argument("domain_name", shell_complete=complete_domain_name)
@click.argument("entity", shell_complete=complete_user_and_group)
@with_harpo_context
def allow(harpo, common_parameters, domain_name, entity):
    """Grant access to domain for user or %group"""
    harpo.domain_allow(domain_name, entity)


@domain.command()
@click.argument("domain_name", shell_complete=complete_domain_name)
@click.argument("entity", shell_complete=complete_user_and_group)
@with_harpo_context
def deny(harpo, common_parameters, domain_name, entity):
    """Revoke/deny access to domain for user or %group"""
    harpo.domain_deny(domain_name, entity)
