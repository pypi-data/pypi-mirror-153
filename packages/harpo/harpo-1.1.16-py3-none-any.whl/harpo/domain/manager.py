import os
from shutil import rmtree

import six

from harpo.exceptions import HarpoDomainAlreadyExists, HarpoDomainNotFound
from harpo.group import GroupManager
from harpo.log import get_logger
from harpo.meta import MetaData
from harpo.secret import SecretManager
from harpo.user import UserManager
from harpo.util import ParametricSingleton, mkdir_p, with_lock

from .domain import Domain


class DomainManager(six.with_metaclass(ParametricSingleton, object)):
    def __init__(self, harpo):
        self.harpo = harpo
        self.logger = get_logger()
        self.base_dir = self.harpo.base_dir
        self.data_dir = os.path.join(self.base_dir, "data")
        self.users = UserManager(harpo=self.harpo)
        self.groups = GroupManager(harpo=self.harpo)
        self.logger.debug2("%s initialized: %s", self.__class__, self.__dict__)

        self.list()  # TODO: come up with more elegant way of preloading domains

    @property
    def metadata(self):
        return MetaData(harpo=self.harpo)

    def list(self):
        return [self[domain] for domain in self.metadata.domains.keys()]

    def exists(self, domain_name):
        return domain_name in self.metadata.domains.keys()

    @with_lock
    def create(self, domain_name, inherit_recipients=True):
        self.logger.info("Creating domain %s", domain_name)
        domain_name = domain_name.strip()
        if self.exists(domain_name):
            raise HarpoDomainAlreadyExists("Domain already exists: '{}'".format(domain_name))

        splitted_domain_name = domain_name.split("/")
        if len(splitted_domain_name) > 1:
            parent = "/".join(splitted_domain_name[0:-1])
        else:
            parent = None
        self.logger.debug2("Domain parent: %s", parent)

        if parent is not None and not self.exists(parent):
            raise HarpoDomainNotFound("Can't find parent domain '{}' for domain '{}'".format(parent, domain_name))

        domain_dir = os.path.join(self.data_dir, *splitted_domain_name)
        domain_metadata = {
            "name": domain_name,
            "parent": parent,
            "inherit_recipients": inherit_recipients,
        }
        domain = self._domain_from_metadata(domain_metadata)
        self.logger.info("Creating domain data directory...")
        mkdir_p(domain_dir)

        metadata = self.metadata.domains
        metadata.update({domain_name: domain.dict()})
        self.logger.info("Updating domain metadata...")
        self.metadata.domains = metadata
        return domain

    @with_lock
    def destroy(self, domain_name):
        self.logger.info("Destroying domain %s", domain_name)
        domain_name = domain_name.strip()
        if not self.exists(domain_name):
            raise HarpoDomainNotFound("Domain doesn't exist: '{}'".format(domain_name))
        metadata = self.metadata.domains
        metadata.pop(domain_name)
        self.logger.info("Updating domain metadata...")
        self.metadata.domains = metadata
        self.logger.info("Destroying domain data directory...")
        rmtree(os.path.join(self.data_dir, domain_name))

    @with_lock
    def allow(self, domain_name, entity):
        if not self.exists(domain_name):
            raise HarpoDomainNotFound("Domain doesn't exist: '{}'".format(domain_name))
        metadata = self.metadata.domains.copy()
        domain_metadata = metadata.pop(domain_name)
        allow_list = domain_metadata.get("allow") or []
        allow_list.append(entity)
        deny_list = domain_metadata.get("deny") or []
        if entity in deny_list:
            deny_list.remove(entity)
        domain_metadata["allow"] = sorted(list(set(allow_list)))
        domain_metadata["deny"] = sorted(list(set(deny_list)))

        domain = self._domain_from_metadata(domain_metadata)
        metadata.update({domain_name: domain.dict()})
        self.logger.info("Updating domain metadata...")
        self.metadata.domains = metadata

    @with_lock
    def deny(self, domain_name, entity):
        if not self.exists(domain_name):
            raise HarpoDomainNotFound("Domain doesn't exist: '{}'".format(domain_name))
        metadata = self.metadata.domains.copy()
        domain_metadata = metadata.pop(domain_name)
        allow_list = domain_metadata.get("allow") or []
        if entity in allow_list:
            allow_list.remove(entity)
        deny_list = domain_metadata.get("deny") or []
        deny_list.append(entity)
        domain_metadata["allow"] = sorted(list(set(allow_list)))
        domain_metadata["deny"] = sorted(list(set(deny_list)))

        domain = self._domain_from_metadata(domain_metadata)
        metadata.update({domain_name: domain.dict()})
        self.logger.info("Updating domain metadata...")
        self.metadata.domains = metadata

    def _build_recipients_objects(self, members):
        recipients_objects = []
        for member in members:
            if member.startswith("%"):
                # it's a group!
                member_object = self.groups[member[1:]]
            else:
                # it's a user!
                member_object = self.users[member]
            recipients_objects.append(member_object)
        return recipients_objects

    def _domain_from_metadata(self, metadata):
        domain_metadata = metadata.copy()
        parent = domain_metadata.get("parent")
        if parent is not None and parent in self.metadata.domains.keys():
            parent_domain = self._domain_from_metadata(self.metadata.domains[parent].copy())
            domain_metadata["parent"] = parent_domain

        allow_set = set(domain_metadata.get("allow") or [])
        recipients_objects = self._build_recipients_objects(allow_set)

        deny_set = set(domain_metadata.get("deny") or [])
        denied_recipients_objects = self._build_recipients_objects(deny_set)
        recipients_objects = list(set(recipients_objects) - set(denied_recipients_objects))

        secrets_manager = SecretManager(harpo=self.harpo, domain_metadata=domain_metadata)

        domain = Domain(harpo=self.harpo, secrets_manager=secrets_manager, **domain_metadata)
        domain.recipients_objects = recipients_objects
        domain.denied_recipients_objects = denied_recipients_objects
        domain.allow = allow_set
        domain.deny = deny_set

        # back-populate children list in parent domain
        try:
            self.logger.debug2("Back-populating children for %s: append %s", parent_domain, domain)
            if domain not in parent_domain.children:
                parent_domain.children.append(domain)
            self.logger.debug2("%s children: %s", parent_domain, parent_domain.children)
        except NameError:
            pass
        return domain

    def __getitem__(self, domain_name):
        try:
            metadata = self.metadata.domains[domain_name]
        except KeyError as exc:
            raise HarpoDomainNotFound("Can't find domain: '{}'".format(domain_name)) from exc

        return self._domain_from_metadata(metadata)
