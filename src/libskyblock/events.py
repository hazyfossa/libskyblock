from enum import Enum
from libskyblock.api import Api, BaseResponseModel
from msgspec import Struct


class Firesale(Struct):
    item_id: str
    start: int
    end: int
    amount: int
    price: int


class BingoModifier(Enum):
    NORMAL = "NORMAL"
    EXTREME = "EXTREME"
    SECRET = "SECRET"


class BingoGoal(Struct):
    id: str
    name: str
    lore: str
    fullLore: list  # TODO: stricter type

    tiers: list[int]
    progress: int
    requiredAmount: int


class Bingo(BaseResponseModel):
    id: int
    name: str
    start: int
    end: int
    modifier: BingoModifier
    goals: list[BingoGoal]


class Events:
    def __init__(self, api: Api) -> None:
        self.client = api

    def fire_sales(self) -> list[Firesale]:
        return self.client.query("/firesales", model=list[Firesale])

    def current_bingo(self) -> Bingo:
        return self.client.query("/bingo", model=Bingo)
