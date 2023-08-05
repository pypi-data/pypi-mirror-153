from __future__ import annotations
from abc import ABCMeta
from typing import TypeVar


SingletonInstance = TypeVar("SingletonInstance")


class SingletonMeta(type):
    """Singleton metaclass for implementing singleton patterns. 
    Source: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python

    TODO: Change usage example compliant to Singleton(metaclass=SingletonMeta) class.
    Usage:
    ```
    class MySingleInstanceClass(metaclass=Singleton): ...
    ```
    """
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]


class Singleton(metaclass=SingletonMeta):
    """Singleton base class."""
    @classmethod
    def instance(cls: type[SingletonInstance]) -> SingletonInstance:
        return cls()
