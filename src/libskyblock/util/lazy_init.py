from typing import Protocol
from libskyblock.api import Api


class ProvidesApi(Protocol):
    api: Api


class UsesApi(Protocol):
    def __init__(self, api: Api) -> None: ...


class Lazy[T: UsesApi]:
    def __init__(self, prototype: type[T]) -> None:
        self.prototype = prototype
        self.loaded: T | None = None

    def __get__(self, instance: ProvidesApi, owner=None) -> T:
        if not self.loaded:
            self.loaded = self.prototype(instance.api)

        return self.loaded
