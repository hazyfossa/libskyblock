from pathlib import Path

from .api import Api
from .bazaar import Bazaar
from .data.store import DataStore
from .profiles import Profiles
from .util.lazy_init import Lazy


class Skyblock:
    bazaar = Lazy(Bazaar)
    profiles = Lazy(Profiles)

    def __init__(self, data_path: str | Path, key: str = "-") -> None:
        self.data = DataStore(Path(data_path))
        self.api = Api(key)
