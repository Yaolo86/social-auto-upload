# Language: 中文
import unittest

from uploader.baijiahao_uploader.main import (
    ForegroundWindowClosedError,
    HumanVerificationRequiredError,
    wait_for_baijiahao_publish_result,
)


class _FakeLocator:
    def __init__(self, page, kind):
        self._page = page
        self._kind = kind

    @property
    def first(self):
        return self

    async def count(self):
        if self._kind == "captcha":
            return int(self._page.captcha_visible)
        return 0

    async def is_visible(self):
        return False

    async def inner_text(self):
        return ""


class _FakePage:
    def __init__(
        self,
        *,
        captcha_visible=True,
        complete_after_wait=False,
        complete_after_wait_count=1,
        close_after_wait=False,
    ):
        self.url = "https://baijiahao.baidu.com/builder/rc/edit?type=videoV2"
        self.captcha_visible = captcha_visible
        self.complete_after_wait = complete_after_wait
        self.complete_after_wait_count = complete_after_wait_count
        self.close_after_wait = close_after_wait
        self.wait_count = 0
        self._closed = False

    def is_closed(self):
        return self._closed

    def locator(self, selector):
        if selector == 'text="百度安全验证"':
            return _FakeLocator(self, "captcha")
        return _FakeLocator(self, "other")

    async def wait_for_timeout(self, _milliseconds):
        self.wait_count += 1
        if self.close_after_wait:
            self._closed = True
            raise RuntimeError("Target page, context or browser has been closed")
        if self.complete_after_wait and self.wait_count >= self.complete_after_wait_count:
            self.captcha_visible = False
            self.url = "https://baijiahao.baidu.com/builder/rc/content?type=video"


class BaijiahaoHumanVerificationTests(unittest.IsolatedAsyncioTestCase):
    async def test_foreground_captcha_waits_for_manual_completion_instead_of_failing(self):
        page = _FakePage(complete_after_wait=True)

        await wait_for_baijiahao_publish_result(
            page,
            headless=False,
            normal_timeout_seconds=1,
            human_timeout_seconds=1,
            poll_interval_ms=1,
        )

        self.assertGreaterEqual(page.wait_count, 1)

    async def test_background_captcha_requires_a_foreground_human_verification_run(self):
        page = _FakePage()

        with self.assertRaisesRegex(HumanVerificationRequiredError, "SAU_REQUIRES_HUMAN"):
            await wait_for_baijiahao_publish_result(
                page,
                headless=True,
                normal_timeout_seconds=1,
                human_timeout_seconds=1,
                poll_interval_ms=1,
            )

    async def test_foreground_captcha_has_no_automatic_timeout(self):
        page = _FakePage(complete_after_wait=True, complete_after_wait_count=3)

        await wait_for_baijiahao_publish_result(
            page,
            headless=False,
            normal_timeout_seconds=0,
            human_timeout_seconds=None,
            poll_interval_ms=1,
        )

        self.assertEqual(page.wait_count, 3)

    async def test_closing_foreground_window_during_captcha_stops_the_upload(self):
        page = _FakePage(close_after_wait=True)

        with self.assertRaisesRegex(ForegroundWindowClosedError, "SAU_FOREGROUND_WINDOW_CLOSED"):
            await wait_for_baijiahao_publish_result(
                page,
                headless=False,
                normal_timeout_seconds=1,
                human_timeout_seconds=1,
                poll_interval_ms=1,
            )


if __name__ == "__main__":
    unittest.main()
