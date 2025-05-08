from typing import Callable, Protocol
from libskyblock.api import Api


class ProvidesApi(Protocol):
    api: Api


class Module:
    def __init__(self, api: Api) -> None:
        self.client = api
        self.on_load: Callable | None = None


class Lazy[T: Module]:
    def __init__(self, prototype: type[T]) -> None:
        self.prototype = prototype
        self.loaded: T | None = None

    def __get__(self, library: ProvidesApi, owner=None) -> T:
        if not self.loaded:
            self.loaded = self.load(library.api)

        return self.loaded

    def load(self, api: Api) -> T:
        instance = self.prototype(api)

        if instance.on_load is not None:
            instance.on_load()

        return instance
