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
    cts: str
    isFlagged: bool
    isMaybeFlagged: bool
    UserAgent: str
    data: str


class GenerateHoldCaptchaSolution(GeneratePXCookiesSolution, BaseModel):
    flaggedPOW: bool


class ResponseGetUsage(BaseModel):
    usedRequests: str
    requestsLeft: int
