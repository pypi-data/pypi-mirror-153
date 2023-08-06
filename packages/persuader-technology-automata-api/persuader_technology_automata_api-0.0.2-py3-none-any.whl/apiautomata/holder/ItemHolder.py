from typing import Optional, Type, TypeVar

from apiautomata.holder.Items import Items

T = TypeVar('T')


class ItemHolder:
    __instance: Optional[Items] = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = Items()
        return cls.__instance

    @staticmethod
    def get(name):
        return ItemHolder.__instance.get(name)

    @staticmethod
    def get_entity(cls: Type[T]) -> T:
        return ItemHolder.__instance.get_entity(cls)
