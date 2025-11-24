from dataclasses import dataclass
from enum import Enum


class ProductType(str, Enum):
    Captcha = "captcha"
    Interstitial = "interstitial"
    Init = "init"


@dataclass
class TaskGenerateUserAgent:
    site: str
    region: str
    pd: str | None = ""


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
    proxyregion: str
    pd: ProductType
    data: GenerateDatadomeCookieData


@dataclass
class TagsData:
    cid: str


@dataclass
class TaskGenerateDatadomeTagsCookie:
    site: str
    region: str
    proxyregion: str
    proxy: str
    data: TagsData


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
    POW_PRO: str | None
