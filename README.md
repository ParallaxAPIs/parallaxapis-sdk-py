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

#### Async Client
```python
from parallax_sdk_py.src.datadome import AsyncDatadomeSDK

# Option 1: Context manager (Recommended) - automatic cleanup
async with AsyncDatadomeSDK(host="dd.parallaxsystems.io", api_key="key") as sdk:
    # Your code here
    pass

# Option 2: Manual close - remember to call aclose()
sdk = AsyncDatadomeSDK(host="dd.parallaxsystems.io", api_key="key")
try:
    # Your code here
    pass
finally:
    await sdk.aclose()
```

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK

# Option 1: Basic initialization
sdk = DatadomeSDK(host="dd.parallaxsystems.io", api_key="key")

# Option 2: Manual close - call close() when done
sdk = DatadomeSDK(host="dd.parallaxsystems.io", api_key="key")
try:
    # Your code here
    pass
finally:
    sdk.close()
```

### 🕵️‍♂️ Generate New User Agent

#### Async Client
```python
from parallax_sdk_py.src.datadome import AsyncDatadomeSDK
from parallax_sdk_py.src.tasks import TaskGenerateUserAgent

async with AsyncDatadomeSDK(host="dd.parallaxsystems.io", api_key="key") as sdk:
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

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.tasks import TaskGenerateUserAgent

sdk = DatadomeSDK(host="dd.parallaxsystems.io", api_key="key")

user_agent = sdk.generate_user_agent(TaskGenerateUserAgent(
    region="pl",
    site="vinted",
    pd="optional"
))

print(user_agent)
# Output: Same as async version
```

### 🔍 Get Task Data

#### Async Client
```python
from parallax_sdk_py.src.datadome import AsyncDatadomeSDK

async with AsyncDatadomeSDK(host="dd.parallaxsystems.io", api_key="key") as sdk:
    challenge_url = "https://geo.captcha-delivery.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=s&e=e"
    cookie = "cookie"
    task_data, product_type = sdk.parse_challenge_url(challenge_url, cookie)

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

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK

sdk = DatadomeSDK(host="dd.parallaxsystems.io", api_key="key")

challenge_url = "https://geo.captcha-delivery.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=s&e=e"
cookie = "cookie"
task_data, product_type = sdk.parse_challenge_url(challenge_url, cookie)

print(task_data, product_type)
# Output: Same as async version
```

### 🍪 Generate Cookie

#### Async Client
```python
from parallax_sdk_py.src.datadome import AsyncDatadomeSDK
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeCookie

async with AsyncDatadomeSDK(host="dd.parallaxsystems.io", api_key="key") as sdk:
    challenge_url = "https://geo.captcha-delivery.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=s&e=e"
    cookie = "cookie"
    task_data, product_type = sdk.parse_challenge_url(challenge_url, cookie)

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

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeCookie

sdk = DatadomeSDK(host="dd.parallaxsystems.io", api_key="key")

challenge_url = "https://geo.captcha-delivery.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=s&e=e"
cookie = "cookie"
task_data, product_type = sdk.parse_challenge_url(challenge_url, cookie)

cookie_response = sdk.generate_cookie(TaskGenerateDatadomeCookie(
    site="vinted",
    region="pl",
    data=task_data,
    pd=product_type,
    proxy="http://user:pas@addr:port",
    proxyregion="eu"
))

print(cookie_response)
# Output: Same as async version
```

---

## 🛡️ Perimeterx Usage

### ⚡ SDK Initialization

#### Async Client
```python
from parallax_sdk_py.src.perimeterx import AsyncPerimeterxSDK

# Option 1: Context manager (Recommended) - automatic cleanup
async with AsyncPerimeterxSDK(host="api.parallaxsystems.io", api_key="key") as sdk:
    # Your code here
    pass

# Option 2: Manual close - remember to call aclose()
sdk = AsyncPerimeterxSDK(host="api.parallaxsystems.io", api_key="key")
try:
    # Your code here
    pass
finally:
    await sdk.aclose()
```

#### Sync Client
```python
from parallax_sdk_py.src.perimeterx import PerimeterxSDK

# Option 1: Basic initialization
sdk = PerimeterxSDK(host="api.parallaxsystems.io", api_key="key")

# Option 2: Manual close - call close() when done
sdk = PerimeterxSDK(host="api.parallaxsystems.io", api_key="key")
try:
    # Your code here
    pass
finally:
    sdk.close()
```

### 🍪 Generate PX Cookie

#### Async Client
```python
from parallax_sdk_py.src.perimeterx import AsyncPerimeterxSDK
from parallax_sdk_py.src.tasks import TaskGeneratePXCookies, TaskGenerateHoldCaptcha

async with AsyncPerimeterxSDK(host="api.parallaxsystems.io", api_key="key") as sdk:
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

#### Sync Client
```python
from parallax_sdk_py.src.perimeterx import PerimeterxSDK
from parallax_sdk_py.src.tasks import TaskGeneratePXCookies, TaskGenerateHoldCaptcha

sdk = PerimeterxSDK(host="api.parallaxsystems.io", api_key="key")

result = sdk.generate_cookies(TaskGeneratePXCookies(
    proxy="http://user:pas@addr:port",
    proxyregion="eu",
    region="com",
    site="stockx"
))

print(result)
# Output: Same as async version

hold_captcha_result = sdk.generate_hold_captcha(TaskGenerateHoldCaptcha(
    proxy="http://user:pas@addr:port",
    proxyregion="eu",
    region="com",
    site="stockx",
    data=result['data'],
    POW_PRO=None
))

print(hold_captcha_result)
# Output: Same as async version
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
