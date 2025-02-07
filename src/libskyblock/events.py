from libskyblock.api import Api
from msgspec import Struct


class Firesale(Struct):
    item_id: str
    start: int
    end: int
    amount: int
    price: int


class Events:
    def __init__(self, api: Api) -> None:
        self.client = api

    def fire_sales(self) -> list[Firesale]:
        return self.client.query("/firesales", model=list[Firesale])
