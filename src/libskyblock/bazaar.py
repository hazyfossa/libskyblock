from msgspec import Struct
from time import time
from typing import Literal

from libskyblock.api import Api, BaseResponseModel
from libskyblock.item import Item


class QuickStatus(Struct):
    productId: str

    sellPrice: float
    sellVolume: int
    sellMovingWeek: int
    sellOrders: int

    buyPrice: float
    buyVolume: int
    buyMovingWeek: int
    buyOrders: int


class OrderSummary(Struct):
    amount: int
    pricePerUnit: float
    orders: int


class BazaarItem(Struct):
    product_id: str
    sell_summary: list[OrderSummary]
    buy_summary: list[OrderSummary]
    quick_status: QuickStatus


class BazaarResponse(BaseResponseModel):
    products: dict[str, BazaarItem]


class Bazaar:
    def __init__(self, api: Api) -> None:
        self.client = api
        self.refresh()

    def refresh(self):
        self.state = self.client.query("/bazaar", model=BazaarResponse)
        self.local_update_timestamp = time()

    def get_price(
        self, item: Item, type: Literal["buy", "sell"], order: bool = False
    ) -> int:
        if order:
            type = "buy" if type == "sell" else "sell"

        # TODO: Do not use getattr
        return getattr(self.state.products[item.tag].quick_status, f"{type}Price")

    @property
    def timestamp(self) -> int:
        return self.state.lastUpdated


class OptimisticBazaar(Bazaar):  # TODO: This probably isn't necessary
    def get_price(
        self, item: Item, type: Literal["buy", "sell"], order: bool = False
    ) -> int:
        if order:
            type = "buy" if type == "sell" else "sell"

        # TODO: Do not use getattr
        return getattr(self.state.products[item.tag], f"{type}_summary")[0].pricePerUnit
