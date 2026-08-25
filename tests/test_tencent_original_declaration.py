import asyncio
import tempfile
import unittest
from pathlib import Path

from patchright.async_api import async_playwright

from uploader.tencent_uploader.main import TencentVideo


class TencentOriginalDeclarationTests(unittest.TestCase):
    def test_apply_original_declaration_checks_the_wechat_channels_control(self):
        async def scenario(tmp_path: Path):
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True, channel="chrome")
                page = await browser.new_page()
                await page.set_content(
                    """
                    <label class="weui-desktop-form__check-label">
                      <input type="checkbox" />
                      <span>声明原创</span>
                    </label>
                    """
                )
                uploader = TencentVideo(
                    title="标题",
                    file_path=str(tmp_path / "video.mp4"),
                    tags=[],
                    publish_date=0,
                    account_file=str(tmp_path / "account.json"),
                    declare_original=True,
                )

                await uploader.apply_original_declaration(page)
                self.assertTrue(await page.locator('input[type="checkbox"]').is_checked())
                await browser.close()

        with tempfile.TemporaryDirectory() as tmp_dir:
            asyncio.run(scenario(Path(tmp_dir)))

    def test_apply_original_declaration_leaves_the_control_untouched_when_disabled(self):
        async def scenario(tmp_path: Path):
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True, channel="chrome")
                page = await browser.new_page()
                await page.set_content(
                    """
                    <label class="weui-desktop-form__check-label">
                      <input type="checkbox" />
                      <span>声明原创</span>
                    </label>
                    """
                )
                uploader = TencentVideo(
                    title="标题",
                    file_path=str(tmp_path / "video.mp4"),
                    tags=[],
                    publish_date=0,
                    account_file=str(tmp_path / "account.json"),
                    declare_original=False,
                )

                await uploader.apply_original_declaration(page)
                self.assertFalse(await page.locator('input[type="checkbox"]').is_checked())
                await browser.close()

        with tempfile.TemporaryDirectory() as tmp_dir:
            asyncio.run(scenario(Path(tmp_dir)))


if __name__ == "__main__":
    unittest.main()
