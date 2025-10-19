from typing import Any, Optional
from httpx import AsyncClient, Response
import httpx 
from dataclasses import asdict, dataclass
from typing import TypeVar

T = TypeVar('T')

@dataclass
class Request():
    url: str
    headers: dict
    json: dict

def encode_key(input_str: str) -> str:
    encoded = ''

    for char in input_str:
        char_code = ord(char)
        new_char_code = char_code + 3
        encoded += chr(new_char_code)
    
    return encoded

class SDKHelper():
    def __init__(self, host: str, api_key: str, should_encode_key: Optional[bool] = False, without_https: Optional[bool] = False):
        self.host = host 
        self.api_key = api_key
        self.without_https = without_https

        if should_encode_key:
            self.api_key = encode_key(self.api_key) 

    def create_request(self, endpoint: str, task: Any) -> Request:
        payload = {
            "auth": self.api_key, 
            **asdict(task)
        }

        url = f"https://{self.host}{endpoint}"

        if self.without_https:
            url = f"http://{self.host}{endpoint}"

        return Request(
            url=url, 
            headers={'content-type': 'application/json'}, 
            json=payload, 
        )
    
    def parse_response(self, res: Response, solution: type[T]) -> T:
        body = res.json() 

        if body['error'] is not None and body['error'] is True:
            if body['message'] is None:
                body['message'] = body["cookie"]

            raise Exception(f"Api responded with error, error message: {body['message']}")

        return solution(**body)

class SDK(SDKHelper):
    _client: Optional[httpx.Client]

    def __init__(self, host: str, api_key: str, should_encode_key: Optional[bool] = False, without_https: Optional[bool] = False):
        super().__init__(api_key=api_key, host=host, without_https=without_https, should_encode_key=should_encode_key)
        self._client = None

    def close(self):
        if self._client is not None:
            self._client.close()

    def __enter__(self):
        self._client = httpx.Client()
        return self
    
    def init_client(self):
        self._client = httpx.Client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def api_call(self, endpoint: str, task: Any, solution: type[T]) -> T:
        if self._client is None:
            self.init_client()

        assert self._client is not None

        req = self.create_request(endpoint=endpoint, task=task)
        res = self._client.post(url=req.url, headers=req.headers, json=req.json)

        return self.parse_response(res=res, solution=solution)

class AsyncSDK(SDKHelper):
    _client: Optional[AsyncClient]

    def __init__(self, host: str, api_key: str, should_encode_key: Optional[bool] = False, without_https: Optional[bool] = False):
        super().__init__(api_key=api_key, host=host, without_https=without_https, should_encode_key=should_encode_key)
        
        self._client = None
    
    async def aclose(self):
        if self._client is not None:
            await self._client.aclose()

    async def __aenter__(self):
        await self.init_client()
        return self
    
    async def init_client(self):
        self._client = AsyncClient()

    async def __aexit__(self, exc_type, exc_val, exc_tb): 
        await self.aclose()

    async def api_call(self, endpoint: str, task: Any, solution: type[T]) -> T:
        if self._client is None:
            await self.init_client()

        assert self._client is not None

        req = self.create_request(endpoint=endpoint, task=task)
        res = await self._client.post(url=req.url, headers=req.headers, json=req.json)

        return self.parse_response(res=res, solution=solution)
