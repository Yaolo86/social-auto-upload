import os
import unittest
from unittest.mock import patch

from uploader.baijiahao_uploader.main import _build_launch_kwargs


class BaijiahaoBrowserExecutableTest(unittest.TestCase):
    def test_uses_the_browser_executable_supplied_by_the_host(self):
        browser_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        with patch.dict(os.environ, {"SAU_BROWSER_EXECUTABLE": browser_path}):
            launch_kwargs = _build_launch_kwargs(headless=True)

        self.assertEqual(
            launch_kwargs,
            {
                "headless": True,
                "executable_path": browser_path,
            },
        )


if __name__ == "__main__":
    unittest.main()
