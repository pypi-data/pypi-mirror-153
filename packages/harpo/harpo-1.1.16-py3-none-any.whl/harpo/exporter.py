import os
from shutil import copyfile

from .exceptions import HarpoAlreadyInitialized, HarpoDomainAlreadyExists, HarpoExportError
from .log import get_logger
from .main import Harpo


class Exporter(object):
    def __init__(self, src_base_dir, dst_base_dir, gpg_home, secrets_export_method="copy"):
        self.logger = get_logger()
        self.src_base_dir = src_base_dir
        self.dst_base_dir = dst_base_dir
        self.gpg_home = gpg_home
        self.harpo = Harpo(src_base_dir, gpg_home)
        self.dst_harpo = Harpo(dst_base_dir, os.path.join(src_base_dir, "keystore"))
        self.secrets_export_method = secrets_export_method

    def export(self, domain_name, recurse=True):
        self.logger.info("Exporting to %s...", self.dst_base_dir)
        try:
            self.dst_harpo.initialize()
        except HarpoAlreadyInitialized as exc:
            self.logger.warning(exc)
        domain = self.harpo.domains[domain_name]
        self.export_domain(domain.name, recurse)

    def export_domain(self, domain_name, recurse=True):
        self.logger.info("Exporting Domain: %s", domain_name)
        domain = self.harpo.domains[domain_name]
        parent = domain.parent
        if parent:
            self.export_domain(parent.name, recurse=False)
        try:
            dst_domain = self.dst_harpo.domain_create(domain_name, inherit_recipients=domain.inherit_recipients)
        except HarpoDomainAlreadyExists as exc:
            self.logger.debug1(exc)
            dst_domain = self.dst_harpo.domains[domain_name]
        self.export_gpg_keys(domain.recipients)
        allow_users = [member for member in domain.allow if not member.startswith("%")]
        deny_users = [member for member in domain.deny if not member.startswith("%")]
        reencrypt = False if self.secrets_export_method == "copy" else True
        for recipient in allow_users:
            self.export_user(recipient)
            self.dst_harpo.domain_allow(domain_name, recipient, reencrypt)
        for recipient in deny_users:
            self.export_user(recipient)
            self.dst_harpo.domain_deny(domain_name, recipient, reencrypt)

        allow_groups = [member for member in domain.allow if member.startswith("%")]
        deny_groups = [member for member in domain.deny if member.startswith("%")]
        for recipient in allow_groups:
            self.export_group(recipient[1:])
            self.dst_harpo.domain_allow(domain_name, recipient, reencrypt)
        for recipient in deny_groups:
            self.export_group(recipient[1:])
            self.dst_harpo.domain_deny(domain_name, recipient, reencrypt)

        for key in domain.secrets.list():
            self.logger.info(
                "Exporting secret %s::%s (method=%s)",
                domain_name,
                key,
                self.secrets_export_method,
            )
            if self.secrets_export_method == "copy":
                src = domain.secrets.locate(key)
                dst = dst_domain.secrets.locate(key)
                self.logger.debug1("Copy secret %s::%s: SRC=%s DST=%s", domain_name, key, src, dst)
                copyfile(src, dst)
            elif self.secrets_export_method == "reencrypt":
                value = str(domain.secrets.decrypt(key))
                dst_domain.secrets.encrypt(key, value)
            else:
                raise HarpoExportError("Unsupported secrets export method: {}".format(self.secrets_export_method))

        if recurse:
            for child in domain.children:
                self.export_domain(child.name, recurse=True)

    def export_gpg_keys(self, recipients):
        for recipient in recipients:
            if not self.dst_harpo.keys.get(recipient.key_fingerprint):
                self.logger.info("Exporting GPG key: %s (%s)", recipient.key_fingerprint, recipient)
                result = self.harpo.keys.gpg.export_keys(keyids=recipient.key_fingerprint)
                self.dst_harpo.key_create(result.strip())

    def export_user(self, user_name):
        user = self.harpo.users[user_name]
        if self.dst_harpo.users.exists(user.name):
            self.logger.warning("User already exists in destination: %s. Skipping...", user.name)
        else:
            self.logger.info("Exporting user: %s", user.name)
            self.dst_harpo.user_create(user.name, user.key_fingerprint)

    def export_group(self, group_name):
        group = self.harpo.groups[group_name]
        if self.dst_harpo.groups.exists(group.name):
            self.logger.warning("Group already exists in destination: %s. Skipping...", group.name)
        else:
            self.logger.info("Exporting group: %s", group)
            self.dst_harpo.group_create(group.name)
            members = group.members[:]
            for user in members:
                self.export_user(user.name)
                # It's very important to disable automatic reencryption
                # because not all users may exist at this point yet
                self.dst_harpo.group_include_user(group.name, user.name, reencrypt_on_change=False)
