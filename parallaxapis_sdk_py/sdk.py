from pydantic import BaseModel
from enum import Enum
from typing import Any, Optional
from httpx import AsyncClient, Request, Response
import httpx
from dataclasses import asdict, dataclass
from typing import TypeVar
from .constants import DEFAULT_DATADOME_API_HOST, DEFAULT_PX_API_HOST
from .solutions import ResponseGetUsage

T = TypeVar("T")

class SDKKind(Enum):
    PERIMETERX = "px"
    DATADOME = "dd"

@dataclass
class SDKConfig:
    api_key: str
    host: str | None = None
    timeout: int | None = 30
    proxy: str | None = None
    insecure: bool = False


class SDKHelper:
    def __init__(self, host: str | None, api_key: str, sdk_kind: SDKKind):
        self.api_key = api_key
        self.host = self.resolve_default_host(host, api_key)
        self.sdk_kind = sdk_kind

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
    
    def _format_additional_context_info(self, body: dict[Any, Any]):
        context_keys = [
            'isFlagged', 
            'isMaybeFlagged', 
            'flaggedPOW', 
        ]

        values = []

        for key in context_keys:
            value = body.get(key)
            if value is not None:
                values.append(f"{key}: {value}")

        return ", ".join(values)

    def parse_response(self, res: Response, solution: type[T]) -> T:
        if res.status_code != 200:
            text = res.text
            raise Exception(f"HTTP {res.status_code}: {text[:400]}")
        try:
            body = res.json()
        except Exception:
            raise Exception("Invalid JSON response")

        if isinstance(body, dict):
            body = {k: v for k, v in body.items() if v is not None}

        if isinstance(body, dict) and body.get("error") is True:
            if body.get("message") is None:
                body["message"] = body.get("cookie")

            if self.sdk_kind == SDKKind.PERIMETERX:
                additional_context = self._format_additional_context_info(body)
                body["message"] = f"{body['message']} {additional_context}"

            raise Exception(
                f"Api responded with error, error message: {body['message']}"
            )
        
        return solution(**body)


class SDK(SDKHelper):
    _client: httpx.Client | None

    def __init__(self, cfg: SDKConfig, sdk_kind: SDKKind):
        super().__init__(
            api_key=cfg.api_key,
            host=cfg.host,
            sdk_kind=sdk_kind, 
        )

        self._client = None
        self.cfg = cfg

    def close(self):
        if self._client is not None:
            self._client.close()

    def __enter__(self):
        self._client = httpx.Client(timeout=self.cfg.timeout, proxy=self.cfg.proxy, verify=not self.cfg.insecure)
        return self

    def _init_client(self):
        self._client = httpx.Client(timeout=self.cfg.timeout, proxy=self.cfg.proxy, verify=not self.cfg.insecure)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def api_call(self, endpoint: str, task: Any, solution: type[T]) -> T:
        if self._client is None:
            self._init_client()

        assert self._client is not None

        req = self.create_request(endpoint=endpoint, task=task)
        res = self._client.send(req)

        return self.parse_response(res=res, solution=solution)
    
    def check_usage(self, site: str) -> ResponseGetUsage:
        if self._client is None:
            self._init_client()

        assert self._client is not None

        url = f"https://{self.host}/usage"
        params = {"authToken": self.api_key, "site": site}
        res = self._client.get(url, params=params)

        return self.parse_response(res=res, solution=ResponseGetUsage)


class AsyncSDK(SDKHelper):
    _client: AsyncClient | None

    def __init__(self, cfg: SDKConfig, sdk_kind: SDKKind):
        super().__init__(
            api_key=cfg.api_key,
            host=cfg.host,
            sdk_kind=sdk_kind
        )

        self.cfg: SDKConfig = cfg
        self._client = None

    async def aclose(self):
        if self._client is not None:
            await self._client.aclose()

    async def __aenter__(self):
        await self._init_client()
        return self

    async def _init_client(self):
        self._client = AsyncClient(timeout=self.cfg.timeout, proxy=self.cfg.proxy, verify=not self.cfg.insecure)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()

    async def api_call(self, endpoint: str, task: Any, solution: type[T]) -> T:
        if self._client is None:
            await self._init_client()

        assert self._client is not None

        req = self.create_request(endpoint=endpoint, task=task)
        res = await self._client.send(req)

        return self.parse_response(res=res, solution=solution)

    async def check_usage(self, site: str) -> ResponseGetUsage:
        if self._client is None:
            await self._init_client()

        assert self._client is not None

        url = f"https://{self.host}/usage"
        params = {"authToken": self.api_key, "site": site}
        res = await self._client.get(url, params=params)

        return self.parse_response(res=res, solution=ResponseGetUsage)
