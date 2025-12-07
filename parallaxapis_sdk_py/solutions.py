from typing import Optional
from pydantic import BaseModel


class GenerateUserAgentSolution(BaseModel):
    UserAgent: str
    secHeader: str
    secFullVersionList: str
    secPlatform: str
    secArch: str


class GenerateDatadomeCookieSolution(BaseModel):
    message: str
    UserAgent: str

class BasePXCookieSolution(BaseModel):
    cookie: str
    vid: str
    cts: str
    isMaybeFlagged: bool
    UserAgent: str
    data: str


class GeneratePXCookiesSolution(BasePXCookieSolution):
    isFlagged: Optional[bool] = None

class GeneratePXCookiesSolutionMobile(BasePXCookieSolution):
    uuid: str
    model: str
    device_fp: str

class GenerateHoldCaptchaSolution(GeneratePXCookiesSolution):
    flaggedPOW: bool


class ResponseGetUsage(BaseModel):
    usedRequests: str
    requestsLeft: int
