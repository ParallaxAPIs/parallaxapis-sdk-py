from typing import Optional
import pytest
from parallaxapis_sdk_py.datadome import DatadomeSDK
from dataclasses import dataclass
from parallaxapis_sdk_py.exceptions import (
    PermanentlyBlockedException,
    UnknownChallengeTypeException,
)
from parallaxapis_sdk_py.sdk import SDKConfig
from parallaxapis_sdk_py.tasks import ProductType


@pytest.mark.asyncio
async def test_html_parsing():
    @dataclass
    class TestCase:
        html: str
        expected_b: str
        expected_cid: str
        expected_e: str
        expected_initial_cid: str
        expected_s: str
        expected_pd: ProductType
        expect_to_raise: bool

    test_cases: list[TestCase] = [
        TestCase(
            expect_to_raise=False,
            expected_b="",
            expected_cid="cid",
            expected_e="e",
            expected_initial_cid="cid",
            expected_s="1",
            expected_pd=ProductType.Interstitial,
            html="""<html lang="en"><head><title>seatgeek.com</title><style>#cmsg{animation: A 1.5s;}@keyframes A{0%{opacity:0;}99%{opacity:0;}100%{opacity:1;}}</style></head><body style="margin:0"><p id="cmsg">Please enable JS and disable any ad blocker</p><script data-cfasync="false">var dd={'rt':'rt','cid':'cid','hsh':'hsh','t':'it','qp':'qp','s':1,'e':'e','host':'geo.captcha-delivery.com','cookie':'cookie'}</script><script data-cfasync="false" src="https://ct.captcha-delivery.com/c.js"></script></body></html>""",
        ),
        TestCase(
            expect_to_raise=False,
            expected_b="",
            expected_cid="cid",
            expected_e="e",
            expected_initial_cid="cid",
            expected_s="1",
            expected_pd=ProductType.Captcha,
            html="""<html lang="en"><head><title>seatgeek.com</title><style>#cmsg{animation: A 1.5s;}@keyframes A{0%{opacity:0;}99%{opacity:0;}100%{opacity:1;}}</style></head><body style="margin:0"><p id="cmsg">Please enable JS and disable any ad blocker</p><script data-cfasync="false">var dd={'rt':'rt','cid':'cid','hsh':'hsh','t':'fe','qp':'qp','s':1,'e':'e','host':'geo.captcha-delivery.com','cookie':'cookie'}</script><script data-cfasync="false" src="https://ct.captcha-delivery.com/c.js"></script></body></html>""",
        ),
        TestCase(
            expect_to_raise=False,
            expected_b="",
            expected_cid="cid",
            expected_e="e",
            expected_initial_cid="cid",
            expected_s="1",
            expected_pd=ProductType.Captcha,
            html="""<html lang="en"><head><title>seatgeek.com</title><style>#cmsg{animation: A 1.5s;}@keyframes A{0%{opacity:0;}99%{opacity:0;}100%{opacity:1;}}</style></head><body style="margin:0"><p id="cmsg">Please enable JS and disable any ad blocker</p><script data-cfasync="false">var dd={'rt':'rt','cid':'cid','hsh':'hsh','t':'fe','qp':'qp','s':1,'e':'e','host':'geo.captcha-delivery.com','cookie':'cookie'}</script><script data-cfasync="false" src="https://ct.captcha-delivery.com/c.js"></script></body></html>""",
        ),
        TestCase(
            expect_to_raise=True,
            expected_b="",
            expected_cid="cid",
            expected_e="e",
            expected_initial_cid="cid",
            expected_s="1",
            expected_pd=ProductType.Captcha,
            html="""<html lang="en"><head><title>seatgeek.com</title><style>#cmsg{animation: A 1.5s;}@keyframes A{0%{opacity:0;}99%{opacity:0;}100%{opacity:1;}}</style></head><body style="margin:0"><p id="cmsg">Please enable JS and disable any ad blocker</p><script data-cfasync="false">var dd={'rt':'rt','cid':'cid','hsh':'hsh','t':'bv','qp':'qp','s':1,'e':'e','host':'geo.captcha-delivery.com','cookie':'cookie'}</script><script data-cfasync="false" src="https://ct.captcha-delivery.com/c.js"></script></body></html>""",
        ),
    ]

    for test_case in test_cases:
        sdk = DatadomeSDK(SDKConfig(api_key="dd-test"))

        if test_case.expect_to_raise:
            with pytest.raises(PermanentlyBlockedException):
                sdk.parse_challenge_html(test_case.html, test_case.expected_cid)
        else:
            task, pd = sdk.parse_challenge_html(test_case.html, test_case.expected_cid)

            assert task.b == test_case.expected_b
            assert task.cid == test_case.expected_cid
            assert task.e == test_case.expected_e
            assert task.initialCid == test_case.expected_initial_cid
            assert task.s == test_case.expected_s
            assert pd == test_case.expected_pd


@pytest.mark.asyncio
async def test_detect_challenge_and_parse():
    @dataclass
    class TestCase:
        body: str
        expected_b: str
        expected_cid: str
        expected_e: str
        expected_initial_cid: str
        expected_s: str
        expected_pd: Optional[ProductType]
        expect_to_raise_permanent_block: bool
        expect_to_raise_unknown_challenge_type: bool
        expected_to_return_blocked: bool

    test_cases: list[TestCase] = [
        TestCase(
            expected_to_return_blocked=False,
            expect_to_raise_permanent_block=False,
            expect_to_raise_unknown_challenge_type=False,
            expected_b="",
            expected_cid="cid",
            expected_e="e",
            expected_initial_cid="cid",
            expected_s="1",
            expected_pd=ProductType.Interstitial,
            body="""example clean response""",
        ),
        TestCase(
            expected_to_return_blocked=True,
            expect_to_raise_permanent_block=False,
            expect_to_raise_unknown_challenge_type=False,
            expected_b="b",
            expected_cid="cid",
            expected_e="e",
            expected_initial_cid="cid",
            expected_s="1",
            expected_pd=ProductType.Captcha,
            body="""{
                    "url": "https://geo.captcha-delivery.com/captcha/?initialCid=cid&cid=cid&referer=referer&hash=hash&t=fe&s=1&e=e&b=b"
                }""",
        ),
        TestCase(
            expected_to_return_blocked=True,
            expect_to_raise_permanent_block=True,
            expect_to_raise_unknown_challenge_type=False,
            expected_b="",
            expected_cid="cid",
            expected_e="e",
            expected_initial_cid="cid",
            expected_s="1",
            expected_pd=None,
            body="""{
                    "url": "https://geo.captcha-delivery.com/captcha/?initialCid=cid&cid=cid&referer=referer&hash=hash&t=bv&s=1&e=e&b=b"
                }""",
        ),
        TestCase(
            expected_to_return_blocked=True,
            expect_to_raise_permanent_block=False,
            expect_to_raise_unknown_challenge_type=False,
            expected_b="",
            expected_cid="cid",
            expected_e="e",
            expected_initial_cid="cid",
            expected_s="1",
            expected_pd=ProductType.Captcha,
            body="""<html lang="en"><head><title>seatgeek.com</title><style>#cmsg{animation: A 1.5s;}@keyframes A{0%{opacity:0;}99%{opacity:0;}100%{opacity:1;}}</style></head><body style="margin:0"><p id="cmsg">Please enable JS and disable any ad blocker</p><script data-cfasync="false">var dd={'rt':'rt','cid':'cid','hsh':'hsh','t':'fe','qp':'qp','s':1,'e':'e','host':'geo.captcha-delivery.com','cookie':'cookie'}</script><script data-cfasync="false" src="https://ct.captcha-delivery.com/c.js"></script></body></html>""",
        ),
        TestCase(
            expected_to_return_blocked=True,
            expect_to_raise_permanent_block=False,
            expect_to_raise_unknown_challenge_type=False,
            expected_b="",
            expected_cid="cid",
            expected_e="e",
            expected_initial_cid="cid",
            expected_s="1",
            expected_pd=ProductType.Captcha,
            body="""<html lang="en"><head><title>seatgeek.com</title><style>#cmsg{animation: A 1.5s;}@keyframes A{0%{opacity:0;}99%{opacity:0;}100%{opacity:1;}}</style></head><body style="margin:0"><p id="cmsg">Please enable JS and disable any ad blocker</p><script data-cfasync="false">var dd={'rt':'rt','cid':'cid','hsh':'hsh','t':'fe','qp':'qp','s':1,'e':'e','host':'geo.captcha-delivery.com','cookie':'cookie'}</script><script data-cfasync="false" src="https://ct.captcha-delivery.com/c.js"></script></body></html>""",
        ),
        TestCase(
            expected_to_return_blocked=True,
            expect_to_raise_permanent_block=False,
            expect_to_raise_unknown_challenge_type=True,
            expected_b="",
            expected_cid="cid",
            expected_e="e",
            expected_initial_cid="cid",
            expected_s="1",
            expected_pd=None,
            body="""<html lang="en"><head><title>seatgeek.com</title><style>#cmsg{animation: A 1.5s;}@keyframes A{0%{opacity:0;}99%{opacity:0;}100%{opacity:1;}}</style></head><body style="margin:0"><p id="cmsg">Please enable JS and disable any ad blocker</p><script data-cfasync="false">var dd={'rt':'rt','cid':'cid','hsh':'hsh','t':'xd','qp':'qp','s':1,'e':'e','host':'geo.captcha-delivery.com','cookie':'cookie'}</script><script data-cfasync="false" src="https://ct.captcha-delivery.com/c.js"></script></body></html>""",
        ),
        TestCase(
            expected_to_return_blocked=True,
            expect_to_raise_permanent_block=True,
            expect_to_raise_unknown_challenge_type=False,
            expected_b="",
            expected_cid="cid",
            expected_e="e",
            expected_initial_cid="cid",
            expected_s="1",
            expected_pd=None,
            body="""<html lang="en"><head><title>seatgeek.com</title><style>#cmsg{animation: A 1.5s;}@keyframes A{0%{opacity:0;}99%{opacity:0;}100%{opacity:1;}}</style></head><body style="margin:0"><p id="cmsg">Please enable JS and disable any ad blocker</p><script data-cfasync="false">var dd={'rt':'rt','cid':'cid','hsh':'hsh','t':'bv','qp':'qp','s':1,'e':'e','host':'geo.captcha-delivery.com','cookie':'cookie'}</script><script data-cfasync="false" src="https://ct.captcha-delivery.com/c.js"></script></body></html>""",
        ),
    ]

    test_case_id = -1
    for test_case in test_cases:
        test_case_id = test_case_id + 1
        sdk = DatadomeSDK(SDKConfig(api_key="dd-test"))

        if test_case.expect_to_raise_unknown_challenge_type:
            with pytest.raises(UnknownChallengeTypeException):
                sdk.detect_challenge_and_parse(test_case.body, test_case.expected_cid)
        elif test_case.expect_to_raise_permanent_block:
            with pytest.raises(PermanentlyBlockedException):
                sdk.detect_challenge_and_parse(test_case.body, test_case.expected_cid)
        else:
            print(f"Test case: {test_case_id}")

            blocked, task, pd = sdk.detect_challenge_and_parse(
                test_case.body, test_case.expected_cid
            )

            assert blocked == test_case.expected_to_return_blocked

            if test_case.expected_to_return_blocked:
                assert task is not None
                assert task.b == test_case.expected_b
                assert task.cid == test_case.expected_cid
                assert task.e == test_case.expected_e
                assert task.initialCid == test_case.expected_initial_cid
                assert task.s == test_case.expected_s
                assert pd == test_case.expected_pd
            else:
                assert task is None
