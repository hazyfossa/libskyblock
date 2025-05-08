from typing import Any, Callable, Protocol, cast


class Provides[T](Protocol):
    api: T


class ModuleBase[T]:
    def __init__(self, api: T) -> None:
        self.client = api
        self.on_load: Callable | None = None


# This is a python descriptor
# that performs api dependency injection
# and transparently overwrites itself with a real instance on first access
class Module[T: ModuleBase, Api = Any]:  # To constrain T by Api we need HKT's
    __slots__ = "prototype"

    def __init__(
        self,
        prototype: type[T],
    ) -> None:
        self.prototype = cast(type[T], prototype)

    def __get__(self, api_accessor: Provides[Api], owner=None):
        if api_accessor is None:
            # If accessed via the class, return the descriptor as is, unbound
            return self

        instance = self.inject(api_accessor.api)
        attr_key = self._get_attribute_name(owner)
        setattr(api_accessor, attr_key, instance)

        return instance

    def inject(self, api: Api):
        instance = self.prototype(api)

        if instance.on_load is not None:
            instance.on_load()

        return instance

    def _get_attribute_name(self, owner: object):
        for name, value in owner.__dict__.items():
            if value is self:
                return name
        raise AttributeError("Descriptor not found in the owner class.")
