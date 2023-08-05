# pylint: disable=unused-argument
from .structs import ConfigDict


class ReadOnlyDict(ConfigDict):
    def __init__(self, src):
        super().__init__(src)
        self.readonly = True

    def __setitem__(self, key, item):
        if hasattr(self, "readonly"):
            raise TypeError("Key `{}` is read only!".format(key))
        if isinstance(item, ConfigDict):
            item = ReadOnlyDict(item)
        return super().__setitem__(key, item)

    def __delitem__(self, key):
        raise TypeError

    def clear(self):
        raise TypeError

    def pop(self, key, *args):
        raise TypeError

    def popitem(self):
        raise TypeError

    def __copy__(self):
        """We can only create a new ReadOnlyDict
        via initialization, so to make a copy we
        need to revert to ConfigDict and then
        create a new ReadOnlyDict from it.

        """
        new_copy = ConfigDict(self)
        return ReadOnlyDict(new_copy)
