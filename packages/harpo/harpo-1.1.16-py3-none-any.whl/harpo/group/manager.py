import six

from harpo.exceptions import HarpoGroupAlreadyExists, HarpoGroupNotFound
from harpo.log import get_logger
from harpo.meta import MetaData
from harpo.user import UserManager
from harpo.util import ParametricSingleton, with_lock

from .group import Group


class GroupManager(six.with_metaclass(ParametricSingleton, object)):
    def __init__(self, harpo):
        self.logger = get_logger()
        self.harpo = harpo
        self.groups_metadata = self.metadata.groups
        self.users = UserManager(harpo=self.harpo)
        self.logger.debug3("%s initialized: %s", self.__class__, self.__dict__)

    @property
    def metadata(self):
        return MetaData(harpo=self.harpo)

    def exists(self, group_name):
        return group_name in self.metadata.groups.keys()

    @with_lock
    def create(self, group_name):
        if self.exists(group_name):
            raise HarpoGroupAlreadyExists("Group with name '{}' already exists".format(group_name))

        self.logger.info("Creating group '%s'", group_name)
        group_metadata = {
            "name": group_name,
            "members": [],
        }
        group = Group(**group_metadata)

        metadata = self.metadata.groups
        metadata.update({group_name: group.dict()})
        self.metadata.groups = metadata

    @with_lock
    def destroy(self, group_name):
        if not self.exists(group_name):
            raise HarpoGroupNotFound("Group doesn't exist: " + group_name)

        self.logger.info("Destroying group %s", group_name)
        metadata = self.metadata.groups
        metadata.pop(group_name)
        self.logger.info("Updating group metadata...")
        self.metadata.groups = metadata

    def list(self):
        return list(self.metadata.groups.keys())

    @with_lock
    def include_user(self, group_name, user_name):
        self.logger.info("Adding user '%s' to group '%s'", user_name, group_name)
        group_metadata = self.metadata.groups[group_name]
        group_members = group_metadata.get("members", [])
        if user_name not in group_members:
            group_members.append(user_name)
            group_members = sorted(list(set(group_members)))
            group_metadata["members"] = group_members
            group = Group(**group_metadata)

            metadata = self.metadata.groups
            metadata.update({group_name: group.dict()})
            self.logger.info("Updating group metadata...")
            self.metadata.groups = metadata

    @with_lock
    def exclude_user(self, group_name, user_name):
        self.logger.info("Removing user '%s' from group '%s'", user_name, group_name)
        group_metadata = self.metadata.groups[group_name]
        group_members = group_metadata.get("members", [])
        if user_name in group_members:
            group_members.remove(user_name)
            group_members = list(set(group_members))
            group_metadata["members"] = group_members
            group = Group(**group_metadata)

            metadata = self.metadata.groups
            metadata.update({group_name: group.dict()})
            self.logger.info("Updating group metadata...")
            self.metadata.groups = metadata

    def _group_from_metadata(self, metadata):
        metadata_copy = metadata.copy()
        users = metadata_copy.get("members", [])
        users_objects = [self.users[user] for user in users]
        metadata_copy["members"] = users_objects
        return Group(**metadata_copy)

    def __getitem__(self, group_name):
        try:
            metadata = self.metadata.groups[group_name]
        except KeyError as exc:
            raise HarpoGroupNotFound("Can't find group: '{}'; {}".format(group_name, exc))

        return self._group_from_metadata(metadata)
