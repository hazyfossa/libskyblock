from time import time
from typing import Literal

from msgspec import Struct

from libskyblock.types import ItemTag

from .api import CachedResponseModel, UseApi


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


class BazaarResponse(CachedResponseModel):
    products: dict[str, BazaarItem]


class Bazaar(UseApi):
    def on_load(self):
        self.refresh()

    def refresh(self):
        self.state = self.client.query("/bazaar", model=BazaarResponse)
        self.local_update_timestamp = time()

    def available(self, item: ItemTag) -> bool:
        return item in self.state.products

    def get_price(
        self,
        item: ItemTag,
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
