from libskyblock.util.construct import Module

from .api import Api
from .bazaar import Bazaar
from .profiles import Profiles
from .events import Events


class Hypixel:
    bazaar = Module(Bazaar)
    profiles = Module(Profiles)
    events = Module(Events)

    def __init__(self, key: str = "-") -> None:
        self.api = Api(key)
