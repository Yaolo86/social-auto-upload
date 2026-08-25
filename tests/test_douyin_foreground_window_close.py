# Language: 中文
import unittest
from unittest.mock import MagicMock

from uploader.douyin_uploader.main import (
    ForegroundWindowClosedError,
    raise_if_foreground_window_closed,
    raise_if_foreground_window_closed_error,
)


class DouyinForegroundWindowCloseTests(unittest.TestCase):
    def test_closed_foreground_page_stops_the_upload(self):
        page = MagicMock()
        page.is_closed.return_value = True

        with self.assertRaisesRegex(
            ForegroundWindowClosedError,
            "SAU_FOREGROUND_WINDOW_CLOSED",
        ):
            raise_if_foreground_window_closed(page, headless=False)

    def test_closed_background_page_remains_an_upstream_failure(self):
        page = MagicMock()
        page.is_closed.return_value = True

        raise_if_foreground_window_closed(page, headless=True)

    def test_page_close_error_outside_wait_loops_also_stops_foreground_upload(self):
        error = RuntimeError("Target page, context or browser has been closed")

        with self.assertRaisesRegex(
            ForegroundWindowClosedError,
            "SAU_FOREGROUND_WINDOW_CLOSED",
        ):
            raise_if_foreground_window_closed_error(error, headless=False)

    def test_page_close_error_is_not_reclassified_in_background_mode(self):
        error = RuntimeError("Target page, context or browser has been closed")

        raise_if_foreground_window_closed_error(error, headless=True)


if __name__ == "__main__":
    unittest.main()
