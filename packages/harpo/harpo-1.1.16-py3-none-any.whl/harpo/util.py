# coding=utf-8
import errno
import json
import os
from functools import wraps
from hashlib import md5

import yaml
from filelock import FileLock, Timeout

import harpo

from .exceptions import HarpoLockFileExists
from .log import get_logger


class ParametricSingleton(type):
    """Metaclass for parametrized singleton
    Returns different instances if parameters differ

    Example:
        def MyAwesomeClass(metaclass=ParametricSingleton):
            pass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        logger = get_logger()

        if cls in [harpo.Domain, harpo.User, harpo.Group]:
            params_hash = kwargs["name"] + str(id(kwargs.get("harpo"))) + str(id(kwargs.get("secrets_manager")))
        elif cls == harpo.meta.MetaData:
            params_hash = str(id(kwargs.get("harpo")))
        elif cls == harpo.secret.SecretManager:
            params_hash = kwargs["domain_metadata"]["name"] + str(id(kwargs.get("harpo")))
        else:
            args_hash = md5(":".join(sorted([str(arg) for arg in args])).encode("utf8")).hexdigest()
            kwargs_hash = md5(str(sorted(list(kwargs.items()))).encode("utf8")).hexdigest()
            params_hash = md5("{}{}".format(args_hash, kwargs_hash).encode("utf8")).hexdigest()
        logger.debug3("args: %s, kwargs: %s, hash: %s", args, kwargs, params_hash)
        full_name = "{}:{}".format(cls, params_hash)
        if full_name not in cls._instances:
            logger.debug3(
                "New ParametricSingleton instance for %s: %s, %s => %s",
                cls,
                str(args),
                str(kwargs),
                params_hash,
            )
            cls._instances[full_name] = super(ParametricSingleton, cls).__call__(*args, **kwargs)
        logger.debug3("Reusing existing ParametricSingleton instance: %s", full_name)
        return cls._instances[full_name]


class Singleton(type):
    """Metaclass for singletons

    Example:
        def MyAwesomeClass(metaclass=Singleton):
            pass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        logger = get_logger()
        full_name = cls
        if full_name not in cls._instances:
            logger.debug3(
                "New Singleton instance for %s: %s, %s => %s",
                cls,
                str(args),
                str(kwargs),
            )
            cls._instances[full_name] = super(Singleton, cls).__call__(*args, **kwargs)
        logger.debug3("Reusing existing ParametricSingleton instance: %s", full_name)
        return cls._instances[full_name]


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def to_pretty_json(obj):
    return json.dumps(obj, indent=2, sort_keys=True)


def to_pretty_yaml(obj):
    return yaml.safe_dump(obj)


def find_harpo_basedir(cwd=os.getcwd(), name=".harpo"):
    basedir = os.path.join(cwd, name)
    if os.path.exists(basedir):
        return basedir
    else:
        if cwd == "/":
            return None
        new_cwd = os.path.normpath(os.path.join(cwd, ".."))
        return find_harpo_basedir(new_cwd, name)


def with_lock(func):
    """A wrapper to execute a function with a lock"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        lock_file = "/tmp/.harpo.lock"
        lock = FileLock(lock_file=lock_file, timeout=10)
        try:
            logger.debug2("Acquiring lock: %s", lock_file)
            with lock:
                logger.debug2("Lock acquired: %s", lock.is_locked)
                return func(*args, **kwargs)
        except Timeout as exc:
            raise HarpoLockFileExists("Lock file exists: " + lock_file) from exc
        finally:
            logger.debug2("Releasing lock")

    return wrapper
