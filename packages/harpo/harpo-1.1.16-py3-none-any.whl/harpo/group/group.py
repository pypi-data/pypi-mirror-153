import six

from harpo.util import ParametricSingleton


class Group(six.with_metaclass(ParametricSingleton, object)):
    def __init__(self, name, members):
        self.name = name
        self.members = members

    def dict(self):
        result = {
            "name": self.name,
            "members": [str(member) for member in self.members],
        }
        return result

    def __repr__(self):
        return "%" + self.name
