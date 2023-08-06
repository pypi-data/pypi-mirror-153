import sys

import click

from harpo.cli.util import print_formatted, with_harpo_context


@click.group()
def key():
    """Manage GPG keys in Harpo keychain"""
    pass


@key.command()
@click.argument("key_material")
@with_harpo_context
def create(harpo, common_parameters, key_material):
    """Add a new key to Harpo keychain, use '-' to read from STDIN"""
    if key_material == "-":
        key_material = sys.stdin.read()
    print_formatted(
        harpo.key_create(key_material).results,
        output_format=common_parameters["format"],
    )


@key.command()
@click.argument("fingerprint")
@with_harpo_context
def destroy(harpo, common_parameters, fingerprint):
    """Destroy existing GPG key by its fingerprint"""
    result = harpo.key_destroy(fingerprint)
    msg = {
        "status": result.status,
        "stderr": result.stderr,
    }
    print_formatted(msg, output_format=common_parameters["format"])


@key.command()
@with_harpo_context
def list(harpo, common_parameters):
    """List all existing GPG keys"""
    print_formatted(harpo.key_list(), output_format=common_parameters["format"])
