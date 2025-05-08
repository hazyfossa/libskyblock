from typing import Literal
from msgspec import field, Struct
from libskyblock.types import ProfileID, PlayerID
from .api import UseApi


class Member(Struct):
    player_id: PlayerID
    # TODO: support deletion notice


class Transaction(Struct):
    timestamp: int # TODO: datetime
    amount: int
    action: Literal["DEPOSIT", "WITHDRAW"] # TODO: verify withdraw
    initiator_name: str # TODO: PlayerID?


class Banking(Struct):
    balance: int


class Profile(Struct):
    id: ProfileID = field(name="profile_id")
    members: list[Member]
    profile_name: str = field(name="cute_name")
    community_upgrades: dict  # TODO
    
    _game_mode: Literal["island", "ironman", "bingo"] | None = field(name="game_mode")
    @property
    def game_mode(self) -> Literal["normal", "ironman", "stranded", "bingo"]: # type: ignore
        # NOTE: Simpler than the official API naming
        match self._game_mode:
            case None:
                return "normal"
            case "island":
                return "stranded"

            case *other: # technically we can specify ironman & bingo here to satisfy typing
                return other

class MultiProfile(Profile):
    selected: bool


class Profiles(UseApi):
    def query_id[T](self, id: ProfileID, view: type[T] = Profile) -> T:
        return self.client.query(f"/profile", params={"uuid": id}, model=view)
    
    def query_player[T](self, player_id: PlayerID, view: type[T] = MultiProfile) -> list[T]:
        return self.client.query(f"/profiles", params={"uuid": player_id}, model=list[view])