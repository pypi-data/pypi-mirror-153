import os

from .domain import DomainManager
from .exceptions import HarpoAlreadyInitialized, HarpoDomainNotFound, HarpoGroupNotFound, HarpoUserNotFound
from .group.manager import GroupManager
from .key import KeyManager
from .log import get_logger
from .meta import MetaData
from .user import UserManager
from .util import mkdir_p, with_lock


class Harpo(object):
    def __init__(self, base_dir, gpg_home):
        self.logger = get_logger()
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "data")
        self.meta_dir = os.path.join(base_dir, "meta")
        self.gpg_home = gpg_home
        self.logger.debug3("%s initialized: %s", self.__class__, self.__dict__)

    # System
    @with_lock
    def initialize(self):
        """Create required directory structure in 'path'
        if it doesn't exists already"""
        if os.path.exists(self.base_dir):
            raise HarpoAlreadyInitialized("Looks like Harpo is already initialized at " + self.base_dir)
        logger = get_logger()
        logger.info("Initializing Harpo in %s", self.base_dir)
        keystore_dir = os.path.join(self.base_dir, "keystore")
        directories = [self.data_dir, self.meta_dir, keystore_dir]
        for directory in directories:
            logger.debug("Create %s", directory)
            mkdir_p(directory)

        metadata = MetaData(harpo=self)
        metadata.initialize()

    # Domain ------------------------------------------------------------------
    @property
    def domains(self):
        return DomainManager(harpo=self)

    def domain_create(self, domain_name, inherit_recipients=True):
        return self.domains.create(domain_name, inherit_recipients)

    def domain_destroy(self, domain_name):
        return self.domains.destroy(domain_name)

    def domain_list(self):
        return self.domains.list()

    def domain_info(self, domain_name):
        domain = self.domains[domain_name]
        info = domain.dict()
        info["recipients"] = [recipient.name for recipient in domain.recipients]
        return info

    def domain_allow(self, domain_name, entity, reencrypt=True):
        result = self.domains.allow(domain_name, entity)
        if reencrypt:
            self.domains[domain_name].reencrypt()
        return result

    def domain_deny(self, domain_name, entity, reencrypt=True):
        result = self.domains.deny(domain_name, entity)
        if reencrypt:
            self.domains[domain_name].reencrypt()
        return result

    # Group -------------------------------------------------------------------
    @property
    def groups(self):
        return GroupManager(harpo=self)

    def group_create(self, group_name):
        return self.groups.create(group_name)

    def group_destroy(self, group_name):
        return self.groups.destroy(group_name)

    def group_list(self):
        return [self.groups[group].dict() for group in self.groups.list()]

    def group_include_user(self, group_name, user_name, reencrypt_on_change=True):
        if not self.users.exists(user_name):
            raise HarpoUserNotFound("Can't add a non-existing user '{}' to group '{}'".format(user_name, group_name))
        pass
        if not self.groups.exists(group_name):
            raise HarpoGroupNotFound("Can't add user '{}' to a non-existing group '{}'".format(user_name, group_name))
        self.groups.include_user(group_name, user_name)
        if reencrypt_on_change:
            self._group_trigger_reencryption(group_name)

    def group_exclude_user(self, group_name, user_name, reencrypt_on_change=True):
        if not self.groups.exists(group_name):
            raise HarpoGroupNotFound(
                "Can't remove user '{}' from a non-existing group '{}'".format(user_name, group_name)
            )
        self.groups.exclude_user(group_name, user_name)
        if reencrypt_on_change:
            self._group_trigger_reencryption(group_name)

    def _group_trigger_reencryption(self, group_name):
        group = self.groups[group_name]
        for domain in self.domain_list():
            if group in domain.recipients_objects:
                self.logger.info("Triggering re-encryption for domain '%s'...", domain.name)
                domain.reencrypt()

    # Key ---------------------------------------------------------------------
    @property
    def keys(self):
        return KeyManager(harpo=self)

    def key_create(self, key_material):
        return self.keys.create(key_material)

    def key_destroy(self, key_fingerprint):
        return self.keys.destroy(key_fingerprint)

    def key_list(self):
        result = []
        for key in self.keys.list():
            data = {"uid": key["uids"][0], "fingerprint": key["fingerprint"]}
            result.append(data)
        return result

    # Secret ------------------------------------------------------------------
    def secret_create(self, domain_name, secret_name, secret_value, force=False):
        if not self.domains.exists(domain_name):
            raise HarpoDomainNotFound("Domain '{}' doesn't exist!".format(domain_name))
        self.domains[domain_name].secrets.encrypt(secret_name, secret_value)

    def secret_destroy(self, domain_name, secret_name):
        return self.domains[domain_name].secrets.destroy(secret_name)

    def secret_read(self, domain_name, secret_name):
        return str(self.domains[domain_name].secrets.decrypt(secret_name))

    def secret_list(self, domain_name):
        return sorted(self.domains[domain_name].secrets.list())

    # User --------------------------------------------------------------------
    @property
    def users(self):
        return UserManager(harpo=self)

    def user_create(self, user_name, key_fingerprint):
        return self.users.create(user_name, key_fingerprint)

    def user_destroy(self, user_name):
        return self.users.destroy(user_name)

    def user_list(self):
        return [self.users[user].dict() for user in self.users.list()]
