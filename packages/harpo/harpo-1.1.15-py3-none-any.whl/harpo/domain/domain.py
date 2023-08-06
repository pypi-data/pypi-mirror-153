import six

from harpo.exceptions import HarpoException
from harpo.group.group import Group
from harpo.log import get_logger
from harpo.user.user import User
from harpo.util import ParametricSingleton


class Domain(six.with_metaclass(ParametricSingleton, object)):
    __tunable__ = ["inherit_recipients", "aliases", "comment"]

    def __init__(
        self,
        harpo,
        name,
        parent,
        secrets_manager=None,
        allow=None,
        deny=None,
        aliases=None,
        comment=None,
        inherit_recipients=True,
        **_
    ):
        self.logger = get_logger()
        self.name = name
        self.secrets = secrets_manager

        self.children = []  # back-populated by children
        self.parent = parent

        self.allow = allow
        self.deny = deny
        self.aliases = aliases
        self.comment = comment
        self.inherit_recipients = inherit_recipients
        self.recipients_objects = set()
        self.denied_recipients_objects = set()
        self.logger.debug3("%s initialized: %s", self.__class__, self.__dict__)

    @staticmethod
    def _entities_to_users(entities_list):
        result = []
        for entity in entities_list:
            if type(entity) is User:
                result.append(entity)
            elif type(entity) is Group:
                for user in entity.members:
                    result.append(user)
            else:
                raise HarpoException("Unexpected recipient type: '{}'! This should never happen!".format(type(entity)))
        return result

    @property
    def recipients(self):
        recipients = self._entities_to_users(self.recipients_objects)
        if self.parent is not None and self.inherit_recipients:
            denied_parent_recipients = self._entities_to_users(self.parent.denied_recipients_objects)
            recipients = list(set(recipients + self.parent.recipients) - set(denied_parent_recipients))
        recipients = set(recipients) - set(self._entities_to_users(self.denied_recipients_objects))
        return list(recipients)

    def reencrypt(self, recurse=True):
        # Reencrypt own secrets
        for secret in self.secrets.list():
            self.logger.info("Re-encrypting %s::%s", self.name, secret)
            value = self.secrets.decrypt(secret)
            self.secrets.encrypt(secret, str(value))

        if recurse:
            self.logger.debug2("Reencrypting children of %s: %s", self.name, self.children)
            for child in self.children:
                if child.inherit_recipients:
                    self.logger.info(
                        "Triggering re-encryption for domain '%s' (recurse=True)...",
                        child.name,
                    )
                    child.reencrypt()
                else:
                    self.logger.debug1(
                        "Skipping reencryption of domain '%s' because it doesn't inherit recipients",
                        child.name,
                    )
        else:
            self.logger.debug1("Skipping reencryption of children domains (recurse=False)")

    def dict(self):
        result = {
            "name": self.name,
            "parent": str(self.parent) if self.parent else None,
            "allow": sorted(list(set(self.allow or []))),
            "deny": sorted(list(set(self.deny or []))),
            "inherit_recipients": self.inherit_recipients,
            "comment": self.comment,
        }
        return result

    def __repr__(self):
        return self.name
