from httpx import Client
from msgspec import Struct, json


class SkyblockApiError(Exception):
    def __init__(self, code: int, reason: str) -> None:
        super().__init__(f"[{code}]: {reason}")


class SkyblockApiErrorModel(Struct):
    # success: Literal[False] #NOTE: This is obvious, so we do not decode the field
    cause: str


class BaseResponseModel(Struct):
    success: bool  # TODO: is this necessary for us?


class CachedResponseModel(BaseResponseModel):
    lastUpdated: int


class Api:
    def __init__(self, key: str) -> None:
        self._http = Client(
            base_url="https://api.hypixel.net/v2/skyblock/", params={"key": key}
        )

    def query[T](
        self,
        path: str,
        params: dict[str, str] | None = None,
        model: type[T] = dict,
    ) -> T:
        response = self._http.get(path, params=params)

        if response.status_code != 200:
            err = json.decode(response.read(), type=SkyblockApiErrorModel)
            raise SkyblockApiError(response.status_code, err.cause)

        return json.decode(response.read(), type=model)
