import asyncio
import time
from typing import Optional
import pytest
from src.datadome import DatadomeSDK
from dataclasses import dataclass
from src.exceptions import PermanentlyBlockedException
from src.sdk import SDK, AsyncSDK
from src.tasks import ProductType
from fastapi import FastAPI
from pytest_httpserver import HTTPServer

@dataclass
class TestResult():
    __test__ = False
    ok: bool 
    error: str

@dataclass
class TestTask():
    __test__ = False
    foo: str

@pytest.mark.asyncio
async def test_async_requests(httpserver: HTTPServer):
    @dataclass
    class TestCase:
        sdk: AsyncSDK
        requests_count: int
        max_expected_exec_time: int

    httpserver.expect_request("/test").respond_with_json({'ok': True, 'error': False})

    test_cases: list[TestCase] = [
        TestCase(
            sdk=AsyncSDK(f"{httpserver.host}:{httpserver.port}", "", without_https=True), 
            requests_count=250,
            max_expected_exec_time=100,
        )
    ]

    for test_case in test_cases:
        tasks = []

        start = time.time()

        for _ in range(test_case.requests_count):
            task = asyncio.create_task(test_case.sdk.api_call("/test", TestTask(foo="bar"), TestResult))
            tasks.append(task)

        await asyncio.gather(*tasks)
        await test_case.sdk.aclose()

        seconds_taken = time.time() - start
        print("seconds_taken", seconds_taken)

        assert seconds_taken < 5


def test_sync_requests(httpserver: HTTPServer):
    @dataclass
    class TestCase:
        sdk: SDK
        requests_count: int
        max_expected_exec_time: int

    httpserver.expect_request("/test").respond_with_json({'ok': True, 'error': False})

    test_cases: list[TestCase] = [
        TestCase(
            sdk=SDK(f"{httpserver.host}:{httpserver.port}", "", without_https=True), 
            requests_count=250,
            max_expected_exec_time=100,
        )
    ]

    for test_case in test_cases:
        start = time.time()

        for _ in range(test_case.requests_count):
            test_case.sdk.api_call("/test", TestTask(foo="bar"), TestResult)

        seconds_taken = time.time() - start
        print("seconds_taken", seconds_taken)

        assert seconds_taken < 5
