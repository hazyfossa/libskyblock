from msgspec import Struct

from libskyblock.item import tier
from libskyblock.types import PlayerID, ProfileID

from .api import CachedResponseModel, UseApi


class ItemData(Struct):
    type: int
    data: bytes


class Bid(Struct):
    auction_id: str  # TODO: Irrelevant to us most likely
    bidder: PlayerID
    profile_id: ProfileID
    amount: int
    timestamp: int  # TODO: datetime


class Auction(Struct):
    uuid: str
    auctioneer: PlayerID
    profile_id: ProfileID
    coop: list[str]
    start: int  # TODO: datetime
    end: int  # TODO: datetime
    item_name: str
    item_lore: str
    extra: str
    category: str  # TODO: literal
    tier: tier
    starting_bid: int
    claimed: bool
    claimed_bidders: list[PlayerID]  # TODO: verify str
    highest_bid_amount: int


class ActiveAuctionsResponse(CachedResponseModel):
    page: int
    totalPages: int
    totalAuctions: int
    auctions: list[Auction]


class EndedAuction(Struct):
    auction_id: str

    seller: PlayerID
    seller_profile: ProfileID
    buyer: PlayerID
    buyer_profile: ProfileID
    timestamp: int  # TODO: datetime
    price: int
    bin: bool
    item_bytes: bytes


class RecentlyEndedAuctionsResponse(CachedResponseModel):
    auctions: list[EndedAuction]


class AuctionHouse(UseApi): ...
