import json
import os

import six

from .exceptions import (
    HarpoMetadataNotFound,
    HarpoMetadataParsingError,
    HarpoMetadataReadError,
    HarpoMetadataVersionMismatch,
    HarpoOSError,
)
from .log import get_logger
from .util import ParametricSingleton, to_pretty_json


class MetaData(six.with_metaclass(ParametricSingleton, object)):
    __storage_version__ = 1

    def __init__(self, harpo):
        self.harpo = harpo
        self.logger = get_logger()
        self.meta_dir = os.path.join(self.harpo.base_dir, "meta")
        self.meta_supported_types = ["domain", "user", "group", "sys"]

    def initialize(self):
        """Initializes empty metadata files
        if the don't exist already"""
        for meta_type in self.meta_supported_types:
            path = os.path.join(self.meta_dir, meta_type + ".json")
            self.logger.debug2("Create %s", path)
            if not os.path.exists(path):
                if meta_type == "sys":
                    data = {"storage_version": MetaData.__storage_version__}
                else:
                    data = {}
                self._write_metadata_file(type=meta_type, data=data)

    def _verify_metadata_dir(self):
        self.logger.debug2("Verifying metadata directories")
        if not os.path.isdir(self.meta_dir) or not os.path.exists(self.meta_dir):
            raise HarpoMetadataNotFound("Can't find valid metadata in " + self.meta_dir)
        self.logger.debug2("Metadata directories - OK")
        return True

    def _verify_metadata_storage_version(self):
        self.logger.debug2("Verifying metadata storage version")
        try:
            data = self._read_metadata_file("sys")
            metadata_storage_version = data.get("storage_version")
            if metadata_storage_version != MetaData.__storage_version__:
                raise HarpoMetadataVersionMismatch("Incompatible metadata storage version or metadata not found")
            self.logger.debug2("Metadata storage version - OK")
        except HarpoOSError as exc:
            raise HarpoMetadataReadError("Failed to read Harpo metadata: " + exc)
        return True

    def _verify_metadata(self):
        self.logger.debug2("Verifying metadata")
        self._verify_metadata_dir()
        self._verify_metadata_storage_version()
        self.logger.debug2("Metadata - OK")

    def _get_metadata_file(self, type):
        if type not in self.meta_supported_types:
            raise ValueError("Unsupported metadata type: {}".format(type))
        metadata_filename = os.path.join(self.meta_dir, type + ".json")
        return metadata_filename

    def _read_metadata_file(self, type):
        metadata_filename = self._get_metadata_file(type)
        self.logger.debug2("Reading metadata in %s", metadata_filename)
        try:
            with open(metadata_filename, "r") as json_file:
                json_data = json_file.read()
                data = json.loads(json_data)
        except json.decoder.JSONDecodeError as exc:
            raise HarpoMetadataParsingError from exc
        except FileNotFoundError as exc:
            raise HarpoOSError from exc
        self.logger.debug2("Read metadata: %s", data)
        return data

    def _write_metadata_file(self, type, data):
        metadata_filename = self._get_metadata_file(type)
        self.logger.debug2("Writing metadata to %s", metadata_filename)
        with open(metadata_filename, "w") as metadata_file:
            metadata_file.write(to_pretty_json(data))
        self.logger.debug2("Wrote metadata: %s", data)

    # Sys
    def get_sys(self):
        return self._read_metadata_file("sys")

    def set_sys(self, data):
        self._write_metadata_file("sys", data)

    sys = property(get_sys, set_sys)

    # Domain
    def get_domain(self):
        self._verify_metadata()
        return self._read_metadata_file("domain")

    def set_domain(self, data):
        self._write_metadata_file("domain", data)

    domains = property(get_domain, set_domain)

    # User
    def get_user(self):
        return self._read_metadata_file("user")

    def set_user(self, data):
        self._write_metadata_file("user", data)

    users = property(get_user, set_user)

    # Group
    def get_group(self):
        return self._read_metadata_file("group")

    def set_group(self, data):
        self._write_metadata_file("group", data)

    groups = property(get_group, set_group)
