# <img src="logo.png" alt="Parallax Logo" width="30" height="30" style="vertical-align: middle;"> ParallaxAPIs Python SDK: Datadome & Perimeterx

**Python SDK for bypassing DataDome and PerimeterX anti-bot protection.**

## Overview

ParallaxAPIs provides a **request-based solution** for bypassing DataDome and PerimeterX anti-bot systems. Instead of relying on slow, resource-heavy browser automation, our API generates valid cookies and tokens in **200-400ms** through direct HTTP requests.

**What We Solve:**
- ✅ **DataDome** - Slider captchas, interstitial pages, cookie generation, tags payload
- ✅ **PerimeterX** - Cookie generation (_px3), challenge solver, vid & cts tokens

**Key Benefits:**
- **Lightning Fast** - 200-400ms response times vs 2-5+ seconds for browsers
- **Simple Integration** - Clean API, no browser management required
- **Highly Scalable** - Handle thousands of concurrent requests with minimal resources
- **Cost Effective** - Lightweight infrastructure, minimal proxy usage
- **Always Updated** - We handle all reverse engineering and updates for you

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
    host="host.com", # optional
    api_key="Key"
)

# Advanced configuration with timeout and proxy
cfg = SDKConfig(
    host="host.com", # optional
    api_key="Key",
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
    host="host.com", # optional
    api_key="Key"
)

# Advanced configuration with timeout and proxy
cfg = SDKConfig(
    host="host.com", # optional
    api_key="Key",
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

cfg = SDKConfig(host="host.com", api_key="Key")

async with AsyncDatadomeSDK(cfg=cfg) as sdk:
    user_agent = await sdk.generate_user_agent(TaskGenerateUserAgent(
        region="com",
        site="site",
        pd="optional"
    ))

    print(user_agent)
```

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateUserAgent

cfg = SDKConfig(host="host.com", api_key="Key")

with DatadomeSDK(cfg=cfg) as sdk:
    user_agent = sdk.generate_user_agent(TaskGenerateUserAgent(
        region="com",
        site="site",
        pd="optional"
    ))

    print(user_agent)
```

### 🔍 Get Task Data

#### Async Client
```python
from parallax_sdk_py.src.datadome import AsyncDatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig

cfg = SDKConfig(host="host.com", api_key="Key")

async with AsyncDatadomeSDK(cfg=cfg) as sdk:
    challenge_url = "https://www.example.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=1&e=e"
    cookie = "cookie_value"
    task_data, product_type = sdk.parse_challenge_url(challenge_url, cookie)

    print(task_data, product_type)
```

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig

cfg = SDKConfig(host="host.com", api_key="Key")

with DatadomeSDK(cfg=cfg) as sdk:
    challenge_url = "https://www.example.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=s&e=e"
    cookie = "cookie_value"
    task_data, product_type = sdk.parse_challenge_url(challenge_url, cookie)

    print(task_data, product_type)
```

### 📄 Parse Challenge HTML

#### Async Client
```python
from parallax_sdk_py.src.datadome import AsyncDatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig

cfg = SDKConfig(host="host.com", api_key="Key")

async with AsyncDatadomeSDK(cfg=cfg) as sdk:
    # HTML body containing dd object
    html_body = "<html><script>dd={'b':'example'}</script></html>"
    prev_cookie = "cookie_value"
    
    # Parse HTML challenge
    task_data, product_type = sdk.parse_challenge_html(
        html_body=html_body, 
        datadome_cookie=prev_cookie
    )
    
    print(task_data, product_type)
```

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig

cfg = SDKConfig(host="host.com", api_key="Key")

with DatadomeSDK(cfg=cfg) as sdk:
    # HTML body containing dd object
    html_body = "<html><script>dd={'t':'it','s':123456,'e':'example','cid':'initialCid','b':'optional'}</script></html>"
    prev_cookie = "cookie_value"
    
    # Parse HTML challenge
    task_data, product_type = sdk.parse_challenge_html(
        html_body=html_body, 
        datadome_cookie=prev_cookie
    )
    
    print(task_data, product_type)
```

### 🍪 Generate Cookie

#### Async Client
```python
from parallax_sdk_py.src.datadome import AsyncDatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeCookie

cfg = SDKConfig(
    host="host.com", # Optional
    api_key="Key",
    timeout=60,  # Optional: custom timeout
    proxy="http://user:pass@proxy.example.com:8080"  # Optional: SDK-level proxy
)

async with AsyncDatadomeSDK(cfg=cfg) as sdk:
    challenge_url = "https://www.example.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=s&e=e"
    cookie = "cookie_value"
    task_data, product_type = sdk.parse_challenge_url(challenge_url, cookie)

    cookie_response = await sdk.generate_cookie(TaskGenerateDatadomeCookie(
        site="site",
        region="com",
        data=task_data,
        pd=product_type,
        proxy="http://user:pas@addr:port",  # Task-level proxy (for solving)
        proxyregion="eu"
    ))

    print(cookie_response)
```

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeCookie

cfg = SDKConfig(
    host="host.com", # Optional
    api_key="Key",
    timeout=60,  # Optional: custom timeout
    proxy="http://user:pass@proxy.example.com:8080"  # Optional: SDK-level proxy
)

with DatadomeSDK(cfg=cfg) as sdk:
    challenge_url = "https://www.example.com/captcha/?initialCid=initialCid&cid=cid&referer=referer&hash=hash&t=t&s=s&e=e"
    cookie = "cookie_value"
    task_data, product_type = sdk.parse_challenge_url(challenge_url, cookie)

    cookie_response = sdk.generate_cookie(TaskGenerateDatadomeCookie(
        site="site",
        region="com",
        data=task_data,
        pd=product_type,
        proxy="http://user:pas@addr:port",  # Task-level proxy (for solving)
        proxyregion="eu"
    ))

    print(cookie_response)
```

### 🏷️ Generate Tags Cookie

#### Async Client
```python
from parallax_sdk_py.src.datadome import AsyncDatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeTagsCookie, GenerateDatadomeTagsCookieData

cfg = SDKConfig(host="host.com", api_key="Key")

async with AsyncDatadomeSDK(cfg=cfg) as sdk:
    tags_cookie_response = await sdk.generate_tags_cookie(TaskGenerateDatadomeTagsCookie(
        site="site",
        region="com",
        data=GenerateDatadomeTagsCookieData(cid="your_datadome_cookie_value"),
        proxy="http://user:pas@addr:port",
        proxyregion="eu"
    ))

    print(tags_cookie_response)
```

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeTagsCookie, GenerateDatadomeTagsCookieData

cfg = SDKConfig(host="host.com", api_key="Key")

with DatadomeSDK(cfg=cfg) as sdk:
    tags_cookie_response = sdk.generate_tags_cookie(TaskGenerateDatadomeTagsCookie(
        site="site",
        region="com",
        data=GenerateDatadomeTagsCookieData(cid="your_datadome_cookie_value"),
        proxy="http://user:pas@addr:port",
        proxyregion="eu"
    ))

    print(tags_cookie_response)
```

### 🔍 Detect and Parse Challenge

#### Async Client
```python
from parallax_sdk_py.src.datadome import AsyncDatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeCookie

cfg = SDKConfig(host="host.com", api_key="Key")

async with AsyncDatadomeSDK(cfg=cfg) as sdk:
    # Response body from website (could be HTML or JSON)
    response_body = "<html>...</html>"  
    prev_cookie = "cookie_value"
    
    # Detect if challenge exists and parse it
    is_blocked, task_data, product_type = sdk.detect_challenge_and_parse(
        body=response_body, 
        datadome_cookie=prev_cookie
    )
    
    if is_blocked:
        # Generate new cookie using the parsed data
        cookie_resp = await sdk.generate_cookie(TaskGenerateDatadomeCookie(
            site="site",
            region="com",
            data=task_data,
            pd=product_type,
            proxy="http://user:pass@addr:port",
            proxyregion="eu"
        ))
        
        print(cookie_resp)
```

#### Sync Client
```python
from parallax_sdk_py.src.datadome import DatadomeSDK
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGenerateDatadomeCookie

cfg = SDKConfig(host="host.com", api_key="Key")

with DatadomeSDK(cfg=cfg) as sdk:
    # Response body from website (could be HTML or JSON)
    response_body = "<html>...</html>"  
    prev_cookie = "cookie_value"
    
    # Detect if challenge exists and parse it
    is_blocked, task_data, product_type = sdk.detect_challenge_and_parse(
        body=response_body, 
        datadome_cookie=prev_cookie
    )
    
    if is_blocked:
        # Generate new cookie using the parsed data
        cookie_resp = sdk.generate_cookie(TaskGenerateDatadomeCookie(
            site="site",
            region="com",
            data=task_data,
            pd=product_type,
            proxy="http://user:pass@addr:port",
            proxyregion="eu"
        ))
        
        print(cookie_resp)
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
    host="host.com",
    api_key="Key"
)

# Advanced configuration with timeout and proxy
cfg = SDKConfig(
    host="host.com",
    api_key="Key",
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
    host="host.com",
    api_key="Key"
)

# Advanced configuration with timeout and proxy
cfg = SDKConfig(
    host="host.com",
    api_key="Key",
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
    host="host.com",
    api_key="Key",
    timeout=60  # Optional: custom timeout
)

async with AsyncPerimeterxSDK(cfg=cfg) as sdk:
    result = await sdk.generate_cookies(TaskGeneratePXCookies(
        proxy="http://user:pas@addr:port",
        proxyregion="eu",
        region="com",
        site="site"
    ))

    print(result)


    hold_captcha_result = await sdk.generate_hold_captcha(TaskGenerateHoldCaptcha(
        proxy="http://user:pas@addr:port",
        proxyregion="eu",
        region="com",
        site="site",
        data=result['data'],
        POW_PRO=None
    ))

    print(hold_captcha_result)
```

#### Sync Client
```python
from parallax_sdk_py.src.perimeterx import PerimeterxSDK
from parallax_sdk_py.src.sdk import SDKConfig
from parallax_sdk_py.src.tasks import TaskGeneratePXCookies, TaskGenerateHoldCaptcha

cfg = SDKConfig(
    host="host.com",
    api_key="Key",
    timeout=60  # Optional: custom timeout
)

with PerimeterxSDK(cfg=cfg) as sdk:
    result = sdk.generate_cookies(TaskGeneratePXCookies(
        proxy="http://user:pas@addr:port",
        proxyregion="eu",
        region="com",
        site="site"
    ))

    print(result)


    hold_captcha_result = sdk.generate_hold_captcha(TaskGenerateHoldCaptcha(
        proxy="http://user:pas@addr:port",
        proxyregion="eu",
        region="com",
        site="site",
        data=result['data'],
        POW_PRO=None
    ))

    print(hold_captcha_result)
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
