# coding=utf-8
import os
from functools import wraps

import click
from tabulate import tabulate

from harpo.exceptions import HarpoFileNotFound, handle_harpo_exceptions
from harpo.main import Harpo
from harpo.util import find_harpo_basedir, to_pretty_json, to_pretty_yaml


def complete_from_list(incomplete, choices_list):
    return [element for element in choices_list if element.startswith(incomplete)]


def print_json(obj):
    print(to_pretty_json(obj))


def print_normal(obj, tablefmt="psql"):
    if type(obj) is dict:
        printable_obj = {str(k).strip(): str(v).strip() for k, v in obj.items()}
        result = tabulate([printable_obj], headers="keys", tablefmt=tablefmt)
    elif type(obj) is list:
        result = tabulate(obj, headers="keys", tablefmt=tablefmt)
    else:
        result = str(obj)
    print(result)


def print_yaml(obj):
    print(to_pretty_yaml(obj))


def print_formatted(obj, output_format="normal"):
    outputters = {
        "normal": print_normal,
        "json": print_json,
        "yaml": print_yaml,
    }
    if output_format in outputters:
        outputters[output_format](obj)
    else:
        raise ValueError("Unsupported output format: {}".format(output_format))


def _find_ctx_root_parent(ctx):
    if ctx.parent is None:
        return ctx
    else:
        ctx = _find_ctx_root_parent(ctx.parent)
    return ctx


def read_from_stdin_or_file_or_string(string):
    if string.startswith("@"):
        # Read secret from file
        file_path = string[1:]
        if os.path.isfile(file_path):
            pass
    elif string.startswith("-"):
        # Read secret from STDIN
        pass
    else:
        return string


def with_harpo_context(func):
    """A decorator to pass harpo context

    * harpo - harpo instance
    * common_parameters - top level cli parameters (--debug, --format, etc..)
    """

    @wraps(func)
    @click.pass_context
    @handle_harpo_exceptions
    def wrapper(ctx, *args, **kwargs):
        common_parameters = _find_ctx_root_parent(ctx).params
        if common_parameters.get("base_dir") is not None:
            base_dir = common_parameters.get("base_dir")
            if not os.path.exists(base_dir):
                raise HarpoFileNotFound("Specified Harpo home directory doesn't exist: " + base_dir)
        else:
            base_dir = find_harpo_basedir()
            if base_dir is None:
                raise HarpoFileNotFound(
                    "Can't find .harpo in current or parent directories " "and --base-dir is not specified!"
                )
        harpo = Harpo(base_dir, gpg_home=os.path.expandvars(common_parameters["gpg_home"]))
        return func(*((harpo, common_parameters) + args), **kwargs)

    return wrapper
