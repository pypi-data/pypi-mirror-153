from collections import OrderedDict
from .format import formatter


class ConfigDict(OrderedDict):
    """
    ConfigDict is an override of standard dictionary
    to allow dot-named access to nested dictionary
    values.

    The standard nested call:

        config['parent']['child']

    can also be accessed as:

        config['parent.child']

    """

    # def __init__(self, *args, **kwargs):
    # super().__init__(*args, **kwargs)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        if "." not in key:
            return super().__getitem__(key)
        segments = key.split(".")
        end = self
        for seg in segments:
            end = super(ConfigDict, end).__getitem__(seg)
        return end

    def __setitem__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, ConfigDict):
            value = ConfigDict(value)
        super().__setitem__(key, value)

    def __contains__(self, key):
        if "." not in key:
            return super().__contains__(key)
        segments = key.split(".")
        end = self
        contains = False
        for seg in segments:
            contains = super(ConfigDict, end).__contains__(seg)
            if not contains:
                return contains
            end = super(ConfigDict, end).__getitem__(seg)
        return contains

    def walk(self, full_key=False):
        def _recurse(section, parent_key):
            for key, value in section.items():
                if full_key and parent_key:
                    key = f"{parent_key}.{key}"
                if isinstance(value, ConfigDict):
                    yield from _recurse(value, key)
                else:
                    yield section, key, value

        yield from _recurse(self, None)

    def copy(self):
        "od.copy() -> a shallow copy of od"
        return self.__class__(self)

    def __str__(self):
        return formatter(self)


class ListNode:
    """Double Linked List Node"""

    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.previous = None
        self.next = None

    def __repr__(self):
        return '<ListNode "{}">'.format(self.name)

    def get_tail(self):
        node = self
        while node.next:
            node = node.next
        return node

    def get_root(self):
        node = self
        while node.previous:
            node = node.previous
        return node

    @property
    def is_root(self):
        return self.previous is None and self.next is not None

    @property
    def is_tail(self):
        return self.next is None and self.previous is not None

    @property
    def unlinked(self):
        return self.previous is None and self.next is None

    def append(self, node):
        _next = self.next
        if _next:
            _next.previous = node
        self.next = node
        self.next.previous = self
        self.next.next = _next
        return node

    def prepend(self, node):
        _previous = self.previous
        if _previous:
            _previous.next = node
        self.previous = node
        self.previous.next = self
        self.previous.previous = _previous
        return node

    def replace(self, node):
        self.name = node.name
        self.content = node.content
        return self

    def remove(self):
        if self.is_root:
            self.next.previous = None
        elif self.is_tail:
            self.previous.next = None
        elif not self.unlinked:
            self.next.previous = self.previous
            self.previous.next = self.next
        self.previous = None
        self.next = None

    def __eq__(self, node):
        return self.name == node.name and self.content == node.content


class DoubleLinkedDict:
    """
    Double Linked List

    """

    def __init__(self, *args):
        self.current = None
        self.root = None
        self._tail = None
        for name, content in args:
            self.append(name, content)

    @property
    def tail(self):
        if self.root:
            return self.root.get_tail()
        return None

    def __len__(self):
        count = 0
        for _ in self:  # noqa
            count += 1
        return count

    def __getitem__(self, index):
        for node in self:
            if node.name == index:
                return node
        return None

    def __setitem__(self, name, value):
        self.append(name, value)

    def __contains__(self, name):
        for node in self:
            if node.name == name:
                return True
        return False

    def replace(self, node_name, content):
        if node_name not in self:
            raise Exception(f"List does not contain '{node_name}'.")
        node = self[node_name]
        node.content = content

    def append(self, name, content):
        node = ListNode(name, content)

        if not self.root:
            self.root = node
        else:
            self.root.get_tail().append(node)

    def prepend(self, name, content):
        node = ListNode(name, content)
        if self.root:
            self.root.prepend(node)
        self.root = node

    def insert_before(self, node_name, name, content):
        node = self[node_name]
        new_node = ListNode(name, content)
        node.prepend(new_node)
        if self.root is node:
            self.root = new_node

    def insert_after(self, node_name, name, content):
        node = self[node_name]
        new_node = ListNode(name, content)
        node.append(new_node)

    def __iter__(self):
        node = self.root
        while node:
            yield node
            node = node.next

    def iter_names(self):
        for node in self:
            yield node.name

    def iter_values(self):
        for node in self:
            yield node.content
