from pydantic import BaseModel

class GenerateUserAgentSolution(BaseModel):
    UserAgent: str
    secHeader: str
    secFullVersionList: str
    secPlatform: str
    secArch: str

class GenerateDatadomeCookieSolution(BaseModel):
    cookie: str
    userAgent: str
    
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