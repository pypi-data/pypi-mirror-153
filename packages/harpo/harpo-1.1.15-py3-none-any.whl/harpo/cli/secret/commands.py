import os
import subprocess
import sys
import tempfile
from distutils.spawn import find_executable

import click

from harpo.cli.domain.commands import complete_domain_name
from harpo.cli.util import complete_from_list, print_formatted, with_harpo_context
from harpo.exceptions import HarpoException, HarpoSecretNotFound
from harpo.main import Harpo
from harpo.util import find_harpo_basedir


def complete_secret_name(ctx, args, incomplete):
    base_dir = ctx.parent.parent.params.get("base_dir") or find_harpo_basedir()
    if base_dir is not None and os.path.isdir(base_dir):
        harpo = Harpo(base_dir, gpg_home=None)
        domain_name = ctx.params["domain_name"]
        return complete_from_list(incomplete, harpo.secret_list(domain_name))
    else:
        return []


@click.group()
def secret():
    """Manage secrets"""
    pass


@secret.command()
@click.option("--force/-f", is_flag=True, help="Overwrite secret if it already exists")
@click.argument("domain_name", shell_complete=complete_domain_name)
@click.argument("secret_name")
@click.argument("secret_value")
@with_harpo_context
def create(harpo, common_parameters, force, domain_name, secret_name, secret_value):
    """Create a new secret

    PROTIP: Use '-' as SECRET_VALUE to read it from STDIN
    """
    if secret_value == "-":
        secret_value = sys.stdin.read()
    harpo.secret_create(domain_name, secret_name, secret_value, force)


@secret.command()
@click.argument("domain_name", shell_complete=complete_domain_name)
@click.argument("secret_name", shell_complete=complete_secret_name)
@with_harpo_context
def read(harpo, common_parameters, domain_name, secret_name):
    """Read and decrypt a secret"""
    print(harpo.secret_read(domain_name, secret_name))


@secret.command()
@click.argument("domain_name", shell_complete=complete_domain_name)
@click.argument("secret_name", shell_complete=complete_secret_name)
@with_harpo_context
def destroy(harpo, common_parameters, domain_name, secret_name):
    harpo.secret_destroy(domain_name, secret_name)


@secret.command()
@click.argument("domain_name", shell_complete=complete_domain_name)
@with_harpo_context
def list(harpo, common_parameters, domain_name):
    result = [{"name": secret} for secret in harpo.secret_list(domain_name)]
    print_formatted(result, output_format=common_parameters["format"])


def edit_file(file):
    editor = os.environ.get("VISUAL", None) or os.environ.get("EDITOR", None)
    if editor is None:
        editor = find_executable("editor") or find_executable("vi")

    if editor is None:
        raise HarpoException("Can't find suitable editor.")
    args = [editor, file]
    subprocess.call(args)


@secret.command()
@click.argument("domain_name", shell_complete=complete_domain_name)
@click.argument("secret_name", shell_complete=complete_secret_name)
@with_harpo_context
def edit(harpo, common_parameters, domain_name, secret_name):
    tmp = tempfile.NamedTemporaryFile(mode="w+")
    try:
        data = harpo.secret_read(domain_name, secret_name)
    except HarpoSecretNotFound:
        data = ""
    tmp.write(str(data))
    tmp.seek(0)
    edit_file(tmp.name)
    tmp.seek(0)
    content = tmp.read().strip()
    harpo.secret_create(domain_name, secret_name, str(content), force=True)
