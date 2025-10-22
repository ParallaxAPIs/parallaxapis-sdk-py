from typing import Any, Optional
from httpx import AsyncClient, Request, Response
import httpx
from dataclasses import asdict, dataclass
from typing import TypeVar
from .constants import DEFAULT_DATADOME_API_HOST, DEFAULT_PX_API_HOST

T = TypeVar("T")


@dataclass
class SDKConfig:
    api_key: str
    host: str | None = None
    timeout: int | None = 30
    proxy: str | None = None


class SDKHelper:
    def __init__(self, host: str | None, api_key: str):
        self.api_key = api_key
        self.host = self.resolve_default_host(host, api_key)

    def resolve_default_host(self, host: str | None, api_key: str) -> str:
        if host:
            return host
        if api_key.upper().startswith("PX-"):
            return DEFAULT_PX_API_HOST
        if api_key.upper().startswith("DD-"):
            return DEFAULT_DATADOME_API_HOST
        raise ValueError("No host provided and unable to determine from API key prefix")

    def create_request(self, endpoint: str, task: Any) -> Request:
        payload = {"auth": self.api_key, **asdict(task)}

        url = f"https://{self.host}{endpoint}"

        return Request(
            "POST",
            url,
            headers={"content-type": "application/json"},
            json=payload,
        )

    def parse_response(self, res: Response, solution: type[T]) -> T:
        if res.status_code != 200:
            text = res.text
            raise Exception(f"HTTP {res.status_code}: {text[:400]}")
        try:
            body = res.json()
        except Exception:
            raise Exception("Invalid JSON response")
        if isinstance(body, dict) and body.get("error") is True:
            if body.get("message") is None:
                body["message"] = body.get("cookie")
            raise Exception(
                f"Api responded with error, error message: {body['message']}"
            )
        return solution(**body)


class SDK(SDKHelper):
    _client: httpx.Client | None

    def __init__(self, cfg: SDKConfig):
        super().__init__(
            api_key=cfg.api_key,
            host=cfg.host,
        )

        self._client = None
        self.cfg = cfg

    def close(self):
        if self._client is not None:
            self._client.close()

    def __enter__(self):
        self._client = httpx.Client(timeout=self.cfg.timeout, proxy=self.cfg.proxy)

        return self

    def init_client(self):
        self._client = httpx.Client(timeout=self.cfg.timeout, proxy=self.cfg.proxy)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def api_call(self, endpoint: str, task: Any, solution: type[T]) -> T:
        if self._client is None:
            self.init_client()

        assert self._client is not None

        req = self.create_request(endpoint=endpoint, task=task)
        res = self._client.send(req)

        return self.parse_response(res=res, solution=solution)


class AsyncSDK(SDKHelper):
    _client: AsyncClient | None

    def __init__(self, cfg: SDKConfig):
        super().__init__(
            api_key=cfg.api_key,
            host=cfg.host,
        )

        self.cfg: SDKConfig = cfg
        self._client = None

    async def aclose(self):
        if self._client is not None:
            await self._client.aclose()

    async def __aenter__(self):
        await self.init_client()
        return self

    async def init_client(self):
        self._client = AsyncClient(timeout=self.cfg.timeout, proxy=self.cfg.proxy)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()

    async def api_call(self, endpoint: str, task: Any, solution: type[T]) -> T:
        if self._client is None:
            await self.init_client()

        assert self._client is not None

        req = self.create_request(endpoint=endpoint, task=task)
        res = await self._client.send(req)

        return self.parse_response(res=res, solution=solution)
