# 🚀 Parallax SDK: Datadome & Perimeterx (Python)

Easily interact with Datadome and Perimeterx anti-bot solutions using a simple Python SDK. Fast integration, clear API! ✨

---

## 📦 Installation

### pip
```bash
 pip install parallax-sdk-py
```

### uv
```bash
 uv add parallax-sdk-py
```

---

## 🧑‍💻 Datadome Usage

### ⚡ SDK Initialization

```python
from parallax_sdk_py.src.datadome import DatadomeSDK

# Basic initialization with API key and host
sdk = DatadomeSDK(host="dd.parallaxsystems.io", api_key="key")
```

### 🕵️‍♂️ Generate New User Agent

```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.tasks import TaskGenerateUserAgent

sdk = DatadomeSDK(host="dd.parallaxsystems.io", api_key="key")

user_agent = await sdk.generate_user_agent(TaskGenerateUserAgent(
    region="pl",
    site="vinted",
    pd="optional"
))

print(user_agent)
# Output:
# {
#     'UserAgent': 'Mozilla/5.0 ...',
#     'secHeader': '...',
#     'secFullVersionList': '...',
#     'secPlatform': '...',
#     'secArch': '...'
# }
```

### 🔍 Get Task Data

```python
from parallax_sdk_py.src.datadome import DatadomeSDK

sdk = DatadomeSDK(host="dd.parallaxsystems.io", api_key="key")

challenge_url = "https://geo.captcha-delivery.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=s&e=e"
cookie = "cookie"
task_data, product_type = await sdk.parse_challenge_url(challenge_url, cookie)

print(task_data, product_type)
# Output:
# GenerateDatadomeCookieData(
#     cid="cookie",
#     b="",
#     e="e",
#     s="s",
#     initialCid="initialCid"
# ), ProductType.Captcha
```

### 🍪 Generate Cookie

```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeCookie

sdk = DatadomeSDK(host="dd.parallaxsystems.io", api_key="key")

challenge_url = "https://geo.captcha-delivery.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=s&e=e"
cookie = "cookie"
task_data, product_type = await sdk.parse_challenge_url(challenge_url, cookie)

cookie_response = await sdk.generate_cookie(TaskGenerateDatadomeCookie(
    site="vinted",
    region="pl",
    data=task_data,
    pd=product_type,
    proxy="http://user:pas@addr:port",
    proxyregion="eu"
))

print(cookie_response)
# Output:
# {
#     'cookie': 'datadome=cookie_value',
#     'userAgent': 'Mozilla/5.0 ...'
# }
```

---

## 🛡️ Perimeterx Usage

### ⚡ SDK Initialization

```python
from parallax_sdk_py.src.px import PerimeterxSDK

# Basic initialization with API key and host
sdk = PerimeterxSDK(host="api.parallaxsystems.io", api_key="key")
```

### 🍪 Generate PX Cookie

```python
from parallax_sdk_py.src.px import PerimeterxSDK
from parallax_sdk_py.src.tasks import TaskGeneratePXCookies, TaskGenerateHoldCaptcha

sdk = PerimeterxSDK(host="api.parallaxsystems.io", api_key="key")

result = await sdk.generate_cookies(TaskGeneratePXCookies(
    proxy="http://user:pas@addr:port",
    proxyregion="eu",
    region="com",
    site="stockx"
))

print(result)
# Output:
# {
#     'cookie': '_px3=d3sswjaltwxgAd...',
#     'vid': '514d7e11-6962-11f0-810f-88cc16043287',
#     'cts': '514d8e28-6962-11f0-810f-51b6xf2786b0',
#     'isFlagged': False,
#     'isMaybeFlagged': True,
#     'UserAgent': 'Mozilla/5.0 ...',
#     'data': '==WlrBti6vpO6rshP1CFtBsiocoO8...'
# }

hold_captcha_result = await sdk.generate_hold_captcha(TaskGenerateHoldCaptcha(
    proxy="http://user:pas@addr:port",
    proxyregion="eu",
    region="com",
    site="stockx",
    data=result['data'],
    POW_PRO=None
))

print(hold_captcha_result)
# Output:
# {
#     'cookie': '_px3=d3sswjaltwxgAd...',
#     'vid': '514d7e11-6962-11f0-810f-88cc16043287',
#     'cts': '514d8e28-6962-11f0-810f-51b6xf2786b0',
#     'isFlagged': False,
#     'isMaybeFlagged': True,
#     'UserAgent': 'Mozilla/5.0 ...',
#     'data': '==WlrBti6vpO6rshP1CFtBsiocoO8...',
#     'flaggedPOW': False
# }
```

---

## 📚 Documentation & Help

- Full API docs: [GitHub](https://github.com/parallaxsystems/parallax-sdk-py)
- Issues & support: [GitHub Issues](https://github.com/parallaxsystems/parallax-sdk-py/issues)

---

## 📝 License

MIT

---

Made with ❤️ by Parallax Systems
