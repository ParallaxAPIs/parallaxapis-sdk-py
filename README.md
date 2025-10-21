# 🚀 ParallaxAPIs SDK: Datadome & Perimeterx (Python)

**Powerful Python SDK for bypassing DataDome and PerimeterX anti-bot protection.**

Built with both async and sync support, this SDK is perfect for Python developers who need flexibility. Whether you're building async web scrapers with aiohttp/httpx or traditional synchronous applications, this SDK has you covered.

## ✨ Why Choose the Python SDK?

- **🔄 Dual Mode Support**: Both async (`AsyncDatadomeSDK`) and sync (`DatadomeSDK`) clients for maximum flexibility
- **⚡ Async-First Design**: Native asyncio support with context managers for efficient concurrent operations
- **🎯 Type Hints**: Full type annotations with dataclass-based models for better IDE support
- **🛠️ Pythonic API**: Clean, intuitive interfaces following Python best practices
- **📦 Easy Integration**: Works seamlessly with popular HTTP libraries (aiohttp, httpx, requests)
- **🔧 Flexible Configuration**: Context manager support with automatic resource cleanup

---

## 🚀 Quick Start

Get started with ParallaxAPIs SDK's in under 5 minutes:

1. **Join our [Discord](https://www.parallaxsystems.io/join?s=gh)** - Connect with our community
2. **Create a ticket** - Request your API key
3. **Get your free trial** - Start testing immediately
4. **[Install the SDK](#-installation)** - Choose your preferred language
5. **Solve all anti-bots in seconds** - Start bypassing DataDome, PerimeterX & more

---

## 📦 Installation

### pip
```bash
 pip install parallaxapis-sdk-py
```

![Pip Install Demo](pipinstallsdk.gif)

---

## 🧑‍💻 Datadome Usage

### ⚡ SDK Initialization

#### Async Client
```python
from parallax_sdk_py.src.datadome import AsyncDatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig

# Basic configuration
cfg = SDKConfig(
    host="dd.parallaxsystems.io",
    api_key="key"
)

# Advanced configuration with timeout and proxy
cfg = SDKConfig(
    host="dd.parallaxsystems.io",
    api_key="key",
    timeout=60,  # Optional: request timeout in seconds (default: 30)
    proxy="http://user:pass@proxy.example.com:8080"  # Optional: proxy URL
)

# Option 1: Context manager (Recommended) - automatic cleanup
async with AsyncDatadomeSDK(cfg=cfg) as sdk:
    # Your code here
    pass

# Option 2: Manual close - remember to call aclose()
sdk = AsyncDatadomeSDK(cfg=cfg)
try:
    # Your code here
    pass
finally:
    await sdk.aclose()
```

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig

# Basic configuration
cfg = SDKConfig(
    host="dd.parallaxsystems.io",
    api_key="key"
)

# Advanced configuration with timeout and proxy
cfg = SDKConfig(
    host="dd.parallaxsystems.io",
    api_key="key",
    timeout=60,  # Optional: request timeout in seconds (default: 30)
    proxy="http://user:pass@proxy.example.com:8080"  # Optional: proxy URL
)

# Option 1: Context manager - automatic cleanup
with DatadomeSDK(cfg=cfg) as sdk:
    # Your code here
    pass

# Option 2: Manual close - call close() when done
sdk = DatadomeSDK(cfg=cfg)
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
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateUserAgent

cfg = SDKConfig(host="dd.parallaxsystems.io", api_key="key")

async with AsyncDatadomeSDK(cfg=cfg) as sdk:
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
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateUserAgent

cfg = SDKConfig(host="dd.parallaxsystems.io", api_key="key")

with DatadomeSDK(cfg=cfg) as sdk:
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
from parallax_sdk_py.src.sdk import SDKConfig

cfg = SDKConfig(host="dd.parallaxsystems.io", api_key="key")

async with AsyncDatadomeSDK(cfg=cfg) as sdk:
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
from parallax_sdk_py.src.sdk import SDKConfig

cfg = SDKConfig(host="dd.parallaxsystems.io", api_key="key")

with DatadomeSDK(cfg=cfg) as sdk:
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
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeCookie

cfg = SDKConfig(
    host="dd.parallaxsystems.io",
    api_key="key",
    timeout=60,  # Optional: custom timeout
    proxy="http://user:pass@proxy.example.com:8080"  # Optional: SDK-level proxy
)

async with AsyncDatadomeSDK(cfg=cfg) as sdk:
    challenge_url = "https://geo.captcha-delivery.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=s&e=e"
    cookie = "cookie"
    task_data, product_type = sdk.parse_challenge_url(challenge_url, cookie)

    cookie_response = await sdk.generate_cookie(TaskGenerateDatadomeCookie(
        site="vinted",
        region="pl",
        data=task_data,
        pd=product_type,
        proxy="http://user:pas@addr:port",  # Task-level proxy (for solving)
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
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeCookie

cfg = SDKConfig(
    host="dd.parallaxsystems.io",
    api_key="key",
    timeout=60,  # Optional: custom timeout
    proxy="http://user:pass@proxy.example.com:8080"  # Optional: SDK-level proxy
)

with DatadomeSDK(cfg=cfg) as sdk:
    challenge_url = "https://geo.captcha-delivery.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=s&e=e"
    cookie = "cookie"
    task_data, product_type = sdk.parse_challenge_url(challenge_url, cookie)

    cookie_response = sdk.generate_cookie(TaskGenerateDatadomeCookie(
        site="vinted",
        region="pl",
        data=task_data,
        pd=product_type,
        proxy="http://user:pas@addr:port",  # Task-level proxy (for solving)
        proxyregion="eu"
    ))

    print(cookie_response)
    # Output: Same as async version
```

### 🏷️ Generate Tags Cookie

The `generate_tags_cookie` method is used to generate initial Datadome tags cookies (uses `ProductType.Init`). This is typically used for the initial page load before any challenge is encountered.

#### Async Client
```python
from parallax_sdk_py.src.datadome import AsyncDatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeTagsCookie, GenerateDatadomeTagsCookieData

cfg = SDKConfig(host="dd.parallaxsystems.io", api_key="key")

async with AsyncDatadomeSDK(cfg=cfg) as sdk:
    tags_cookie_response = await sdk.generate_tags_cookie(TaskGenerateDatadomeTagsCookie(
        site="vinted",
        region="pl",
        data=GenerateDatadomeTagsCookieData(cid="your_datadome_cookie_value"),
        proxy="http://user:pas@addr:port",
        proxyregion="eu"
    ))

    print(tags_cookie_response)
    # Output:
    # {
    #     'cookie': 'datadome=tags_cookie_value',
    #     'userAgent': 'Mozilla/5.0 ...'
    # }
```

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeTagsCookie, GenerateDatadomeTagsCookieData

cfg = SDKConfig(host="dd.parallaxsystems.io", api_key="key")

with DatadomeSDK(cfg=cfg) as sdk:
    tags_cookie_response = sdk.generate_tags_cookie(TaskGenerateDatadomeTagsCookie(
        site="vinted",
        region="pl",
        data=GenerateDatadomeTagsCookieData(cid="your_datadome_cookie_value"),
        proxy="http://user:pas@addr:port",
        proxyregion="eu"
    ))

    print(tags_cookie_response)
    # Output: Same as async version
```

---

## 🛡️ Perimeterx Usage

### ⚡ SDK Initialization

#### Async Client
```python
from parallax_sdk_py.src.perimeterx import AsyncPerimeterxSDK
from parallax_sdk_py.src.sdk import SDKConfig

# Basic configuration
cfg = SDKConfig(
    host="api.parallaxsystems.io",
    api_key="key"
)

# Advanced configuration with timeout and proxy
cfg = SDKConfig(
    host="api.parallaxsystems.io",
    api_key="key",
    timeout=60,  # Optional: request timeout in seconds (default: 30)
    proxy="http://user:pass@proxy.example.com:8080"  # Optional: proxy URL
)

# Option 1: Context manager (Recommended) - automatic cleanup
async with AsyncPerimeterxSDK(cfg=cfg) as sdk:
    # Your code here
    pass

# Option 2: Manual close - remember to call aclose()
sdk = AsyncPerimeterxSDK(cfg=cfg)
try:
    # Your code here
    pass
finally:
    await sdk.aclose()
```

#### Sync Client
```python
from parallax_sdk_py.src.perimeterx import PerimeterxSDK
from parallax_sdk_py.src.sdk import SDKConfig

# Basic configuration
cfg = SDKConfig(
    host="api.parallaxsystems.io",
    api_key="key"
)

# Advanced configuration with timeout and proxy
cfg = SDKConfig(
    host="api.parallaxsystems.io",
    api_key="key",
    timeout=60,  # Optional: request timeout in seconds (default: 30)
    proxy="http://user:pass@proxy.example.com:8080"  # Optional: proxy URL
)

# Option 1: Context manager - automatic cleanup
with PerimeterxSDK(cfg=cfg) as sdk:
    # Your code here
    pass

# Option 2: Manual close - call close() when done
sdk = PerimeterxSDK(cfg=cfg)
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
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGeneratePXCookies, TaskGenerateHoldCaptcha

cfg = SDKConfig(
    host="api.parallaxsystems.io",
    api_key="key",
    timeout=60  # Optional: custom timeout
)

async with AsyncPerimeterxSDK(cfg=cfg) as sdk:
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
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGeneratePXCookies, TaskGenerateHoldCaptcha

cfg = SDKConfig(
    host="api.parallaxsystems.io",
    api_key="key",
    timeout=60  # Optional: custom timeout
)

with PerimeterxSDK(cfg=cfg) as sdk:
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

- Full API docs & support: [Discord](https://www.parallaxsystems.io/join?s=gh)



## 🌟 Contributing

Got feedback or found a bug? Feel free to open an issue or send us a pull request!



## 🏢 Enterprise

Unlock enterprise-grade performance with custom solutions, expanded limits, and expert support. [Contact us](https://www.parallaxsystems.io/join?s=gh) to learn more.



## 📝 License

MIT

---

## 🔑 Keywords

**DataDome bypass** • **PerimeterX bypass** • **Anti-bot bypass** • **Bot detection bypass** • **CAPTCHA solver** • **Cookie generator** • **Python web scraping** • **Python bot automation** • **Async Python anti-bot** • **DataDome Python SDK** • **PerimeterX Python SDK** • **Headless browser alternative** • **Request-based bypass** • **Python automation** • **Web scraping Python** • **Bot mitigation bypass** • **Sensor data generation** • **Challenge solver** • **asyncio anti-bot** • **pip anti-bot**
