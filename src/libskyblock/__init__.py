from .api import Api
from .bazaar import Bazaar, OptimisticBazaar


class Skyblock:
    def __init__(self, key: str = "-") -> None:
        api = Api(key)

        self.raw_api = api
        self.bazaar = OptimisticBazaar(api)
