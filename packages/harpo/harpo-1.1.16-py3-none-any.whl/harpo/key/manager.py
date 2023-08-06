import os
from distutils.spawn import find_executable

import gnupg
import six

from harpo.exceptions import HarpoKeyNotFound
from harpo.log import get_logger
from harpo.util import ParametricSingleton


class KeyManager(six.with_metaclass(ParametricSingleton, object)):
    """Manages GPG keys"""

    def __init__(self, harpo):
        self.logger = get_logger()
        self.harpo = harpo
        self.gpg_home = os.path.join(self.harpo.base_dir, "keystore")
        # Select gpg executable, prefer gpg2
        gpgbinary = find_executable("gpg2") or find_executable("gpg")
        if gpgbinary is None:
            raise RuntimeError("GPG binary not found.")
        self.gpg = gnupg.GPG(gnupghome=self.gpg_home, keyring=os.path.join(self.gpg_home, "pubring.gpg"))

    def create(self, key_material):
        return self.gpg.import_keys(key_material)

    def destroy(self, key_id):
        return self.gpg.delete_keys(fingerprints=[key_id])

    def list(self, keys=None):
        return list(self.gpg.list_keys(keys=keys))

    def get(self, keys, default=None):
        try:
            return self[keys]
        except HarpoKeyNotFound:
            return default

    def __getitem__(self, keys):
        keys = self.list(keys=keys)
        if not keys:
            raise HarpoKeyNotFound("Can't find key using search term '{}'".format(keys))
        if len(keys) > 1:
            self.logger.warning(
                "Multiple keys were found using search term '%s'" "Try specifying an exact key fingerprint",
                keys,
            )
            return None
        return keys
