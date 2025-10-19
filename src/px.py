from .sdk import SDK, AsyncSDK
from .solutions import GenerateHoldCaptchaSolution, GenerateUserAgentSolution, GeneratePXCookiesSolution
from .tasks import TaskGenerateHoldCaptcha, TaskGeneratePXCookies, TaskGenerateUserAgent

class PerimeterxSDK(SDK):
    def __init__(self, host: str, api_key: str):
        super().__init__(host, api_key, should_encode_key=True)
    
    def generate_cookies(self, task: TaskGeneratePXCookies) -> GeneratePXCookiesSolution:
        return self.api_call("/gen", task, GeneratePXCookiesSolution)

    def generate_hold_captcha(self, task: TaskGenerateHoldCaptcha) -> GenerateHoldCaptchaSolution:
        return self.api_call("/holdcaptcha", task, GenerateHoldCaptchaSolution)
    
class AsyncPerimeterxSDK(AsyncSDK):
    def __init__(self, host: str, api_key: str):
        super().__init__(host, api_key, should_encode_key=True)
    
    async def __aenter__(self): 
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb): 
        await self.aclose()
    
    async def generate_cookies(self, task: TaskGeneratePXCookies) -> GeneratePXCookiesSolution:
        return await self.api_call("/gen", task, GeneratePXCookiesSolution)

    async def generate_hold_captcha(self, task: TaskGenerateHoldCaptcha) -> GenerateHoldCaptchaSolution:
        return await self.api_call("/holdcaptcha", task, GenerateHoldCaptchaSolution)