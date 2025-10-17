from typing import Any, Optional
import httpx 
from dataclasses import asdict
from typing import TypeVar

T = TypeVar('T')

class SDK:
    host: str
    api_key: str

    def __init__(self, host: str, api_key: str):
        self.host = host 
        self.api_key = api_key

    def encode_key(self, input_str: str) -> str:
        encoded = ''

        for char in input_str:
            char_code = ord(char)
            new_char_code = char_code + 3
            encoded += chr(new_char_code)
        
        return encoded


    async def api_call(self, endpoint: str, task: Any, solution: type[T]) -> T: 
        payload = {
            "auth": self.api_key, 
            **asdict(task)
        }

        url = f"https://{self.host}{endpoint}"

        res = httpx.post(url=url, verify=False, headers={
            'content-type': 'application/json'
        }, json=payload)

        body = res.json() 

        if body['error'] is not None and body['error'] is True:
            if body['message'] is None:
                body['message'] = body["cookie"]

            raise Exception(f"Api responded with error, error message: {body['message']}")

        return solution(**body)
