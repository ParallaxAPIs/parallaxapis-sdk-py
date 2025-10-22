from typing_extensions import override
from .sdk import SDK, AsyncSDK, SDKConfig
from .solutions import (
    GenerateHoldCaptchaSolution,
    GeneratePXCookiesSolution,
)
from .tasks import TaskGenerateHoldCaptcha, TaskGeneratePXCookies, TaskGenerateUserAgent


class PerimeterxSDK(SDK):
    def __init__(self, cfg: SDKConfig):
        super().__init__(cfg=cfg)

    def generate_cookies(
        self, task: TaskGeneratePXCookies
    ) -> GeneratePXCookiesSolution:
        return self.api_call("/gen", task, GeneratePXCookiesSolution)

    def generate_hold_captcha(
        self, task: TaskGenerateHoldCaptcha
    ) -> GenerateHoldCaptchaSolution:
        return self.api_call("/holdcaptcha", task, GenerateHoldCaptchaSolution)


class AsyncPerimeterxSDK(AsyncSDK):
    def __init__(self, cfg: SDKConfig):
        super().__init__(cfg=cfg)

    @override
    async def __aenter__(self):
        return self

    @override
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()

    async def generate_cookies(
        self, task: TaskGeneratePXCookies
    ) -> GeneratePXCookiesSolution:
        return await self.api_call("/gen", task, GeneratePXCookiesSolution)

    async def generate_hold_captcha(
        self, task: TaskGenerateHoldCaptcha
    ) -> GenerateHoldCaptchaSolution:
        return await self.api_call("/holdcaptcha", task, GenerateHoldCaptchaSolution)
