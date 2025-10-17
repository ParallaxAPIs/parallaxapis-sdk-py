import ast
import json
import re
from typing import Any, Optional, Tuple
import urllib
import urllib.parse
from .sdk import SDK
from .solutions import GenerateUserAgentSolution, GenerateDatadomeCookieSolution
from .tasks import ProductType, TaskGenerateDatadomeCookie, TaskGenerateDatadomeTagsCookie, TaskGenerateUserAgent, GenerateDatadomeCookieData
from .exceptions import NoDatadomeValuesInHtmlException, PermanentlyBlockedException, UnknownChallangeTypeException, UnparasbleHtmlDatadomeBodyException, UnparasbleJsonDatadomeBodyException

class DatadomeSDK(SDK):
    _dd_object_re: re.Pattern = re.compile("dd={[^}]+}")
    _dd_url_re: re.Pattern = re.compile('''geo\\.captcha\\-delivery\\.com\\/(interstitial|captcha)''')
  
    def __init__(self, host: str, api_key: str):
        super().__init__(host, api_key)

    async def generate_user_agent(self, task: TaskGenerateUserAgent):
        return await self.api_call("/useragent", task, GenerateUserAgentSolution)
    
    async def generate_cookie(self, task: TaskGenerateDatadomeCookie):
        return await self.api_call("/gen", task, GenerateDatadomeCookieSolution)
    
    async def generate_tags_cookie(self, task: TaskGenerateDatadomeTagsCookie):
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

    async def parse_challenge_url(self, url: str, datadome_cookie: str) -> Tuple[GenerateDatadomeCookieData, ProductType]:
        parsed_url = urllib.parse.urlparse(url)

        pd: ProductType

        if parsed_url.path.startswith("/captcha"):
            pd = ProductType.Captcha
        elif parsed_url.path.startswith("/interstitial"):
            pd = ProductType.Interstitial
        elif parsed_url.path.startswith("/init"):
            pd = ProductType.Init
        else: 
            raise UnknownChallangeTypeException
        
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
    
    async def parse_challange_json(self, json_body: str, datadome_cookie: str) -> Tuple[GenerateDatadomeCookieData, ProductType]:
        loaded_body = json.loads(json_body)

        if 'url' not in loaded_body:
            raise UnparasbleJsonDatadomeBodyException

        return await self.parse_challenge_url(url=loaded_body['url'], datadome_cookie=datadome_cookie)

    async def parse_challange_html(self, html_body: str, datadome_cookie: str) -> Tuple[GenerateDatadomeCookieData, ProductType]:
        dd_values_match = self._dd_object_re.search(html_body)

        if dd_values_match is None:
            raise NoDatadomeValuesInHtmlException
        
        dd_values_object: Any

        try:
            dd_values_object_string = dd_values_match.group(0)[3:]
            dd_values_object = ast.literal_eval(dd_values_object_string)
        except:
            raise UnparasbleHtmlDatadomeBodyException

        pd: ProductType

        if dd_values_object['t'] == "it":
            pd = ProductType.Interstitial
        elif dd_values_object['t'] == "fe":
            pd = ProductType.Captcha
        elif dd_values_object['t'] == "bv":
            raise PermanentlyBlockedException
        else: 
            raise UnknownChallangeTypeException
        
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
    
    async def detect_challange_and_parse(self, body: str, datadome_cookie: str) -> Tuple[bool, Optional[GenerateDatadomeCookieData], Optional[ProductType]]:
        if self._dd_object_re.search(body):
            return (True, *await self.parse_challange_html(html_body=body, datadome_cookie=datadome_cookie))
        elif self._dd_url_re.search(body):
            return (True, *await self.parse_challange_json(json_body=body, datadome_cookie=datadome_cookie))
       
        return (False, None, None)
        