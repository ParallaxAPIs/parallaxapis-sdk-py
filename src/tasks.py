from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ProductType(str, Enum):
    Captcha = "captcha"
    Interstitial = "interstitial"
    Init = "init"

@dataclass
class TaskGenerateUserAgent:
    site: str 
    region: str 
    pd: Optional[str] = ""

@dataclass
class GenerateDatadomeCookieData:
    cid: str
    e: str
    s: str
    b: str
    initialCid: str

@dataclass
class TaskGenerateDatadomeCookie:
    site: str 
    region: str 
    proxy: str
    pd: ProductType
    data: GenerateDatadomeCookieData

@dataclass
class TaskGenerateDatadomeTagsCookie:
    site: str 
    region: str 
    proxy: str

@dataclass
class TaskGeneratePXCookies:
    site: str 
    region: str 
    proxyregion: str
    proxy: str

@dataclass
class TaskGenerateHoldCaptcha:
    site: str 
    proxyregion: str
    region: str 
    proxy: str
    data: str 
    POW_PRO: Optional[str]