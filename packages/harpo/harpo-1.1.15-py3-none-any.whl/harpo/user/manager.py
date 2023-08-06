import six

from harpo.exceptions import HarpoUserAlreadyExists, HarpoUserException, HarpoUserNotFound
from harpo.key import KeyManager
from harpo.log import get_logger
from harpo.meta import MetaData
from harpo.util import ParametricSingleton, with_lock

from .user import User


class UserManager(six.with_metaclass(ParametricSingleton, object)):
    def __init__(self, harpo):
        self.logger = get_logger()
        self.harpo = harpo
        self.users_metadata = self.metadata.users
        self.keys = KeyManager(harpo=self.harpo)
        self.logger.debug3("%s initialized: %s", self.__class__, self.__dict__)

    @property
    def metadata(self):
        return MetaData(harpo=self.harpo)

    def exists(self, user_name):
        return user_name in self.metadata.users.keys()

    @with_lock
    def create(self, user_name, key_fingerprint):
        if self.exists(user_name):
            raise HarpoUserAlreadyExists("User with name '{}' already exists".format(user_name))

        keys = self.keys[key_fingerprint]
        if keys:
            key_real_fingerprint = keys[0]["fingerprint"]
        else:
            raise HarpoUserException("Can't create a new user")

        self.logger.info(
            "Creating user '%s' identified by key with fingerprint '%s'",
            user_name,
            key_real_fingerprint,
        )
        user_metadata = {
            "name": user_name,
            "key_fingerprint": key_real_fingerprint,
        }
        user = User(**user_metadata)

        metadata = self.metadata.users
        metadata.update({user_name: user.dict()})
        self.metadata.users = metadata

    @with_lock
    def destroy(self, user_name):
        if not self.exists(user_name):
            raise HarpoUserNotFound("User doesn't exist: " + user_name)
        self.logger.info("Destroying user %s", user_name)
        metadata = self.users_metadata
        metadata.pop(user_name)
        self.logger.info("Updating domain metadata...")
        self.metadata.users = metadata

    def list(self):
        return list(self.metadata.users.keys())

    def __getitem__(self, user_name):
        try:
            metadata = self.metadata.users[user_name]
        except KeyError as exc:
            raise HarpoUserNotFound("Can't find user: '{}'".format(user_name)) from exc
        return User(**metadata)
