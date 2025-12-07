from typing import Union
from typing_extensions import override
from .sdk import SDK, AsyncSDK, SDKConfig, SDKKind
from .solutions import (
    GenerateHoldCaptchaSolution,
    GeneratePXCookiesSolution,
    GeneratePXCookiesSolutionMobile,
)

from .tasks import TaskGenerateHoldCaptcha, TaskGeneratePXCookies, TaskGenerateUserAgent

class PerimeterxSDK(SDK):
    def __init__(self, cfg: SDKConfig):
        super().__init__(cfg=cfg, sdk_kind=SDKKind.PERIMETERX)

    def generate_cookies(
        self, task: TaskGeneratePXCookies
    ) -> Union[GeneratePXCookiesSolution, GeneratePXCookiesSolutionMobile]:
        if "mobile" in task.region.lower():
            return self.api_call("/gen", task, GeneratePXCookiesSolutionMobile)
        else:
            return self.api_call("/gen", task, GeneratePXCookiesSolution)

    def generate_hold_captcha(
        self, task: TaskGenerateHoldCaptcha
    ) -> GenerateHoldCaptchaSolution:
        return self.api_call("/holdcaptcha", task, GenerateHoldCaptchaSolution)


class AsyncPerimeterxSDK(AsyncSDK):
    def __init__(self, cfg: SDKConfig):
        super().__init__(cfg=cfg, sdk_kind=SDKKind.PERIMETERX)

    @override
    async def __aenter__(self):
        return self

    @override
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()

    async def generate_cookies(
        self, task: TaskGeneratePXCookies
    ) -> Union[GeneratePXCookiesSolution, GeneratePXCookiesSolutionMobile]:
        if "mobile" in task.region.lower():
            return await self.api_call("/gen", task, GeneratePXCookiesSolutionMobile)
        else:
            return await self.api_call("/gen", task, GeneratePXCookiesSolution)

    async def generate_hold_captcha(
        self, task: TaskGenerateHoldCaptcha
    ) -> GenerateHoldCaptchaSolution:
        return await self.api_call("/holdcaptcha", task, GenerateHoldCaptchaSolution)
