from typing import Callable


class EntityRegistry(object):
    registry = {}

    @classmethod
    def register(cls, entity: str) -> Callable:
        def inner_wrapper(wrapped_class):
            cls.registry[entity] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def get_class(cls, entity: str, **kwargs):
        if entity not in cls.registry:
            return None
        exec_class = cls.registry[entity]
        return exec_class
