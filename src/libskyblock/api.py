from httpx import Client
from msgspec import Struct, json


class SkyblockApiError(Exception):
    def __init__(self, code: int, reason: str) -> None:
        super().__init__(f"[{code}]: {reason}")


class SkyblockApiErrorModel(Struct):
    # success: Literal[False] #NOTE: This is obvious, so we do not decode the field
    cause: str


class BaseResponseModel(Struct):
    success: bool
    lastUpdated: int


class Api:
    def __init__(self, key: str) -> None:
        self._http = Client(
            base_url="https://api.hypixel.net/v2/skyblock/", params={"key": key}
        )

    def query[T](self, path: str, model: type[T] = dict) -> T:
        response = self._http.get(path)

        if response.status_code != 200:
            err = json.decode(response.read(), type=SkyblockApiErrorModel)
            raise SkyblockApiError(response.status_code, err.cause)

        return json.decode(response.read(), type=model)
