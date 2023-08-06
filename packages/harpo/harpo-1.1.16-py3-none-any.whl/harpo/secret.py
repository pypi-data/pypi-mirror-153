import glob
import os
from abc import ABCMeta, abstractmethod
from distutils.spawn import find_executable

import gnupg
import six

from .exceptions import (
    HarpoSecretBackendException,
    HarpoSecretBackendNotFound,
    HarpoSecretDecryptionError,
    HarpoSecretNotFound,
)
from .log import get_logger
from .util import ParametricSingleton


class SecretBackend(six.with_metaclass(ABCMeta, object)):
    @abstractmethod
    def decrypt(self, secret_name):
        pass

    @abstractmethod
    def encrypt(self, secret_name, secret_value):
        pass

    @abstractmethod
    def destroy(self, secret_name):
        pass

    @abstractmethod
    def list(self):
        pass


class SecretPlaintextBackend(SecretBackend):
    """Test backend that stores everything in plaintext"""

    def __init__(self, harpo, domain_metadata):
        self.logger = get_logger()
        self.domain_name = domain_metadata["name"]
        self.data_dir = os.path.join(harpo.data_dir, self.domain_name)
        self.logger.debug2("%s initialized: %s", self, self.__dict__)

    def locate(self, secret_name):
        return os.path.join(self.data_dir, secret_name)

    def decrypt(self, secret_name):
        filename = self.locate(secret_name)
        with open(filename, "r") as file:
            data = file.read()
        return data

    def encrypt(self, secret_name, secret_value):
        filename = os.path.join(self.data_dir, secret_name)
        with open(filename, "w") as file:
            file.write(secret_value)

    def destroy(self, secret_name):
        filename = os.path.join(self.data_dir, secret_name)
        os.remove(filename)

    def list(self):
        return [
            os.path.basename(file)
            for file in glob.glob(os.path.join(self.data_dir, "*"))
            if os.path.isfile(os.path.join(self.data_dir, file))
        ]


class HarpoGPGNoRecipients(HarpoSecretBackendException):
    """No valid recipients found"""


class SecretGPGBackend(SecretBackend):
    """GPG backend"""

    def __init__(self, harpo, domain_metadata):
        self.logger = get_logger()
        self.harpo = harpo
        self.domain_name = domain_metadata["name"]
        self.data_dir = os.path.join(harpo.data_dir, self.domain_name)

        self.logger.debug2("%s initialized: %s", self, self.__dict__)

    def locate(self, secret_name):
        return os.path.join(self.data_dir, secret_name)

    def decrypt(self, secret_name):
        secret_file_path = self.locate(secret_name)
        try:
            with open(secret_file_path, "r") as file:
                ascii_encrypted_data = file.read()
        except FileNotFoundError as exc:
            raise HarpoSecretNotFound("Secret doesn't exists: " + secret_name) from exc
        gpg = gnupg.GPG()
        result = gpg.decrypt(ascii_encrypted_data)
        if result.ok:
            return result
        else:
            raise HarpoSecretDecryptionError("Decryption failed:\n" + result.stderr)

    def _build_recipients_list(self, shared=False):
        """
        Generates list of GPG recipients
        :param shared: generate recipients for a 'shared' secret
        :return:
        """
        domain = self.harpo.domains[self.domain_name]
        recipients = domain.recipients
        if shared:
            self.logger.debug3("This is a shared secret!")
            chld_queue = list()
            chld_queue.append(domain)
            while chld_queue:
                current_node = chld_queue.pop()
                recipients += current_node.recipients
                for chld in current_node.children:
                    chld_queue.append(chld)
        return list(set(recipients))

    def encrypt(self, secret_name, secret_value):
        is_shared = secret_name.endswith(".shared")
        recipients = self._build_recipients_list(shared=is_shared)
        if len(recipients) == 0:
            raise HarpoGPGNoRecipients("No valid recipients found for domain '{}'".format(self.domain_name))

        self.logger.debug1(
            "Encrypt %s::%s for recipients: %s",
            self.domain_name,
            secret_name,
            recipients,
        )
        key_fingerprints = [recipient.key_fingerprint for recipient in recipients]
        self.logger.debug1("Encrypting with keys: %s", key_fingerprints)

        gpg_home = os.path.join(self.harpo.base_dir, "keystore")
        # Select gpg executable, prefer gpg2
        gpgbinary = find_executable("gpg2") or find_executable("gpg")
        if gpgbinary is None:
            raise RuntimeError("GPG binary not found.")
        gpg = gnupg.GPG(gnupghome=gpg_home)
        encrypted_ascii_data = gpg.encrypt(secret_value, key_fingerprints, always_trust=True)

        if encrypted_ascii_data.ok:
            self.logger.debug1(
                "Successfully encrypted %s::%s. Writing...",
                self.domain_name,
                secret_name,
            )
        else:
            raise HarpoSecretBackendException("Error encrypting {}::{}".format(self.domain_name, secret_name))

        secret_file_path = os.path.join(self.data_dir, secret_name)
        with open(secret_file_path, "w") as file:
            self.logger.debug1("Secret file: %s", secret_file_path)
            file.write(str(encrypted_ascii_data))
        return encrypted_ascii_data

    def destroy(self, secret_name):
        filename = os.path.join(self.data_dir, secret_name)
        os.remove(filename)

    def list(self):
        return [
            os.path.basename(file)
            for file in glob.glob(os.path.join(self.data_dir, "*"))
            if os.path.isfile(os.path.join(self.data_dir, file))
        ]


class SecretManager(six.with_metaclass(ParametricSingleton, object)):
    def __init__(self, harpo, domain_metadata):
        self.logger = get_logger()
        self.domain_name = domain_metadata["name"]
        self.harpo = harpo
        self.domain_metadata = domain_metadata
        self.backend = self._initialize_backend()
        self.logger.debug2("%s initialized: %s", self, self.__dict__)

    def _initialize_backend(self):
        type = self.domain_metadata.get("backend", "gpg")
        backend_types = {
            "gpg": SecretGPGBackend,
            "plaintext": SecretPlaintextBackend,
        }
        self.logger.debug2("Domain %s has selected backend: %s", self.domain_name, type)
        backend = backend_types.get(type)
        if backend:
            return backend(self.harpo, self.domain_metadata)
        else:
            raise HarpoSecretBackendNotFound("Unsupported backend: " + type)

    def encrypt(self, secret_name, secret_value):
        return self.backend.encrypt(secret_name, secret_value)

    def decrypt(self, secret_name):
        return self.backend.decrypt(secret_name)

    def destroy(self, secret_name):
        return self.backend.destroy(secret_name)

    def locate(self, secret_name):
        return self.backend.locate(secret_name)

    def list(self):
        return self.backend.list()
