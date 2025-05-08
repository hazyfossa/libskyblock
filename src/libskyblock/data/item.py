from msgspec import UNSET, Struct, UnsetType, field

# Why the heck are npc items???


class Meta(Struct):
    mc_itemid: str = field(name="itemid")
    nbttag: str
    internalname: str  # TODO: Can this differ from id?
    crafttext: str
    # modver: str # NOTE: irrelevant
    # clickcommand: str # NOTE: irrelevant


class Info(Struct):
    infoType: str
    info: list[str]


class Display(Struct):
    displayname: str
    damage: int
    lore: list[str]


class ItemInput(str):
    def parse(self) -> tuple[str, int]:
        id, quantity = self.split(":")
        return id, int(quantity)


class Recipe(Struct):
    type: str
    inputs: list[ItemInput]
    count: int
    output: str = field(name="overrideOutputId")
    duration: int


class RecipeData(Struct):
    advanced_recipes: dict[str, Recipe] | UnsetType = field(
        default=UNSET, name="recipes"
    )
    simple_recipe: dict[str, ItemInput] | UnsetType = field(
        default=UNSET, name="recipe"
    )


# class FullView(Meta, Info, Display, RecipeData): ...
