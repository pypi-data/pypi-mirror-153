from typing import TypeVar, Type

T = TypeVar('T')


class Items:

    def __init__(self):
        self.items = {}

    def add(self, value, name):
        self.items[name] = value

    def get(self, name):
        return self.items[name]

    def add_entity(self, entity: T):
        name = type(entity).__name__
        self.items[name] = entity

    def get_entity(self, cls: Type[T]) -> T:
        name = cls.__name__
        return self.items[name]
