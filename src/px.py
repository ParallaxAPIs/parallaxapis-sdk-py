from .sdk import SDK
from .solutions import GenerateHoldCaptchaSolution, GenerateUserAgentSolution, GeneratePXCookiesSolution
from .tasks import TaskGenerateHoldCaptcha, TaskGeneratePXCookies, TaskGenerateUserAgent

class PerimeterxSDK(SDK):
    def __init__(self, host: str, api_key: str):
        super().__init__(host, api_key, should_encode_key=True)
    
    async def generate_cookies(self, task: TaskGeneratePXCookies):
        return await self.api_call("/gen", task, GeneratePXCookiesSolution)

    async def generate_hold_captcha(self, task: TaskGenerateHoldCaptcha):
        return await self.api_call("/holdcaptcha", task, GenerateHoldCaptchaSolution)