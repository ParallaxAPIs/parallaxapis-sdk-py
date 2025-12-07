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


class GeneratePXCookiesSolution(BaseModel):
    cookie: str
    vid: str
    cts: Optional[str] = None
    uuid: Optional[str] = None
    isFlagged: Optional[bool] = None
    isMaybeFlagged: Optional[bool] = None
    UserAgent: str
    model: Optional[str] = None
    device_fp: Optional[str] = None
    data: str


class GenerateHoldCaptchaSolution(GeneratePXCookiesSolution):
    flaggedPOW: bool


class ResponseGetUsage(BaseModel):
    usedRequests: str
    requestsLeft: int
