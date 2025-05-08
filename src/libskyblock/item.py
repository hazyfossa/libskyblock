from enum import StrEnum
from typing import Literal

from libskyblock.types import ItemTag


class tier(StrEnum):
    common = "COMMON"
    uncommon = "UNCOMMON"
    rare = "RARE"
    epic = "EPIC"
    legendary = "LEGENDARY"
    mythic = "MYTHIC"
    divine = "SUPREME"  # TODO: verify
    special = "SPECIAL"
    very_special = "VERY_SPECIAL"


def tagify(item: str) -> ItemTag:
    return item.replace(" ", "_").upper()


class Item:
    def __init__(self, name: str, tag_override=None) -> None:
        self.name = name
        self.tag: ItemTag = tag_override or tagify(name)

    def __str__(self) -> str:
        return self.name


GemstoneTier = Literal["rough", "flawed", "fine", "flawless", "perfect"]
Gemstone = Literal[
    "jade",
    "amber",
    "topaz",
    "sapphire",
    "amethyst",
    "jasper",
    "ruby",
    "opal",
    "onyx",
    "aquamarine",
    "citrine",
    "peridot",
]


def gem(tier: GemstoneTier, item: Gemstone) -> Item:
    name = tier + " " + item
    return Item(name, tagify(name + " gem"))


EnchantmentTier = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def enchantment(name: str, tier: EnchantmentTier, ultimate: bool = False) -> Item:
    name = name + " " + str(tier)
    return Item(name, tagify("enchantment " + "ultimate " if ultimate else "" + name))
