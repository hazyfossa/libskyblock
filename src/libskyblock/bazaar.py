from msgspec import Struct
from time import time
from typing import Literal

from libskyblock.api import Api, BaseResponseModel
from libskyblock.item import Tag


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
    product_id: str  # TODO: needed? Isn't that a key in the upper dict?
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

    def available(self, item: Tag) -> bool:
        return item in self.state.products

    def get_price(
        self,
        item: Tag,
        type: Literal["buy", "sell"],
        order: bool = False,
        optimistic: bool = False,
    ) -> float:
        if order:
            type = "buy" if type == "sell" else "sell"

        item_state = self.state.products[item]
        # TODO: Do not use getattr

        if optimistic:
            # TODO: make more stable by supplying quantity hints
            return getattr(item_state, f"{type}_summary")[0].pricePerUnit
        else:
            return getattr(item_state.quick_status, f"{type}Price")

    @property
    def timestamp(self) -> int:
        return self.state.lastUpdated
