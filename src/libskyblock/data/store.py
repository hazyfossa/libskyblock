from collections.abc import Generator
from pathlib import Path
from dulwich.repo import Repo
from dulwich import porcelain as git
from msgspec import json

from libskyblock.data import item

NEU_DATA_SOURCE = "https://github.com/NotEnoughUpdates/NotEnoughUpdates-REPO.git"


class DataDirectory[View]:
    def __init__(self, path: Path, view: type[View] = dict):
        self.path = path

        if not self.path.exists():
            raise FileNotFoundError(
                f"Invalid data repo: data directory not found: {self.path}"
            )

        self._view = view

    def query(self, query: str) -> View:
        return json.decode(
            (self.path / query).read_bytes(),
            type=self._view,
        )

    def iter_all(self) -> Generator[View, None, None]:
        for path in self.path.iterdir():
            data = self.query(path.name)
            yield data

    def view[NewView](self, view: type[NewView]) -> "DataDirectory[NewView]":
        return DataDirectory(self.path, view)


# TODO: support rebuild to lmdb


class DataStore:
    def __init__(
        self,
        path: str | Path,
    ):
        self.path = Path(path)
        self.repo = Repo(str(self.path))

        self.constants = DataDirectory(self.path / "constants")
        self.items = DataDirectory(self.path / "items", view=item.RecipeData)
        self.mobs = DataDirectory(self.path / "mobs")

    @classmethod
    def new(cls, path: str | Path, source: str = NEU_DATA_SOURCE):
        path = Path(path)

        path.mkdir(exist_ok=False)
        git.clone(source, str(path))

        return cls(path)

    def update(self):
        git.pull(self.repo)
