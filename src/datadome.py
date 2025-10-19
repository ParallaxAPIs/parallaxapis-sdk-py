import ast
import json
import re
from typing import Any, Optional, Tuple
import urllib.parse
from .sdk import SDK, AsyncSDK
from .solutions import GenerateUserAgentSolution, GenerateDatadomeCookieSolution
from .tasks import ProductType, TaskGenerateDatadomeCookie, TaskGenerateDatadomeTagsCookie, TaskGenerateUserAgent, GenerateDatadomeCookieData
from .exceptions import NoDatadomeValuesInHtmlException, PermanentlyBlockedException, UnknownChallengeTypeException, UnparsableHtmlDatadomeBodyException, UnparsableJsonDatadomeBodyException

class DatadomeChallengeParser():
    _dd_object_re: re.Pattern = re.compile("dd={[^}]+}")
    _dd_url_re: re.Pattern = re.compile('''geo\\.captcha\\-delivery\\.com\\/(interstitial|captcha)''')
  
    def parse_challenge_url(self, url: str, datadome_cookie: str) -> Tuple[GenerateDatadomeCookieData, ProductType]:
        parsed_url = urllib.parse.urlparse(url)

        pd: ProductType

        if parsed_url.path.startswith("/captcha"):
            pd = ProductType.Captcha
        elif parsed_url.path.startswith("/interstitial"):
            pd = ProductType.Interstitial
        elif parsed_url.path.startswith("/init"):
            pd = ProductType.Init
        else: 
            raise UnknownChallengeTypeException
        
        parsed_queries = urllib.parse.parse_qs(parsed_url.query)

        if parsed_queries.get("t") is not None and parsed_queries.get("t", "")[0] == "bv":
            raise PermanentlyBlockedException

        return GenerateDatadomeCookieData(
            b=parsed_queries.get("b", "0")[0],
            s=parsed_queries.get("s", "")[0],
            e=parsed_queries.get("e", "")[0],
            cid=datadome_cookie,
            initialCid=parsed_queries.get("initialCid", "")[0]
        ), pd
    
    def parse_challenge_json(self, json_body: str, datadome_cookie: str) -> Tuple[GenerateDatadomeCookieData, ProductType]:
        loaded_body = json.loads(json_body)

        if 'url' not in loaded_body:
            raise UnparsableJsonDatadomeBodyException

        return self.parse_challenge_url(url=loaded_body['url'], datadome_cookie=datadome_cookie)

    def parse_challenge_html(self, html_body: str, datadome_cookie: str) -> Tuple[GenerateDatadomeCookieData, ProductType]:
        dd_values_match = self._dd_object_re.search(html_body)

        if dd_values_match is None:
            raise NoDatadomeValuesInHtmlException
        
        dd_values_object: Any

        try:
            dd_values_object_string = dd_values_match.group(0)[3:]
            dd_values_object = ast.literal_eval(dd_values_object_string)
        except:
            raise UnparsableHtmlDatadomeBodyException

        pd: ProductType

        if dd_values_object['t'] == "it":
            pd = ProductType.Interstitial
        elif dd_values_object['t'] == "fe":
            pd = ProductType.Captcha
        elif dd_values_object['t'] == "bv":
            raise PermanentlyBlockedException
        else: 
            raise UnknownChallengeTypeException
        
        b = ""

        if 'b' in dd_values_object:
            b = dd_values_object['b']

        return GenerateDatadomeCookieData(
            b=b,
            s=str(dd_values_object['s']),
            e=dd_values_object['e'],
            cid=datadome_cookie,
            initialCid=dd_values_object['cid']
        ), pd
    
    def detect_challenge_and_parse(self, body: str, datadome_cookie: str) -> Tuple[bool, Optional[GenerateDatadomeCookieData], Optional[ProductType]]:
        if self._dd_object_re.search(body):
            return (True, *self.parse_challenge_html(html_body=body, datadome_cookie=datadome_cookie))
        elif self._dd_url_re.search(body):
            return (True, *self.parse_challenge_json(json_body=body, datadome_cookie=datadome_cookie))
       
        return (False, None, None)

class DatadomeSDK(SDK, DatadomeChallengeParser):
    def __init__(self, host: str, api_key: str):
        super().__init__(host, api_key)

    def generate_user_agent(self, task: TaskGenerateUserAgent) -> GenerateUserAgentSolution:
        return self.api_call("/useragent", task, GenerateUserAgentSolution)
    
    def generate_cookie(self, task: TaskGenerateDatadomeCookie) -> GenerateDatadomeCookieSolution:
        return self.api_call("/gen", task, GenerateDatadomeCookieSolution)
    
    def generate_tags_cookie(self, task: TaskGenerateDatadomeTagsCookie) -> GenerateDatadomeCookieSolution:
        return self.api_call(
            "/gen", 
            TaskGenerateDatadomeCookie(
                site=task.site, 
                region=task.region, 
                pd=ProductType.Init, 
                proxy=task.proxy, 
                data=GenerateDatadomeCookieData(cid=task.data.cid, e="", s="", b="", initialCid="")
            ), 
            GenerateDatadomeCookieSolution, 
        )
    
class AsyncDatadomeSDK(AsyncSDK, DatadomeChallengeParser):
    def __init__(self, host: str, api_key: str):
        super().__init__(host, api_key)

    async def __aenter__(self): 
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb): 
        await self.aclose()

    async def generate_user_agent(self, task: TaskGenerateUserAgent) -> GenerateUserAgentSolution:
        return await self.api_call("/useragent", task, GenerateUserAgentSolution)
    
    async def generate_cookie(self, task: TaskGenerateDatadomeCookie) -> GenerateDatadomeCookieSolution:
        return await self.api_call("/gen", task, GenerateDatadomeCookieSolution)
    
    async def generate_tags_cookie(self, task: TaskGenerateDatadomeTagsCookie) -> GenerateDatadomeCookieSolution:
        return await self.api_call(
            "/gen", 
            TaskGenerateDatadomeCookie(
                site=task.site, 
                region=task.region, 
                pd=ProductType.Init, 
                proxy=task.proxy, 
                data=GenerateDatadomeCookieData(cid=task.data.cid, e="", s="", b="", initialCid="")
            ), 
            GenerateDatadomeCookieSolution, 
        )