import io
import asyncio
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import httpx

from discourse_exporter.cli import build_parser, main
from discourse_exporter.profiles import ChromeProfile


class FakeBrowserCookieSession:
    entered_without_running_loop = False

    def __init__(self, base_url, cdp_url):
        self.base_url = base_url
        self.cdp_url = cdp_url

    def __enter__(self):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            FakeBrowserCookieSession.entered_without_running_loop = True
            return self
        raise AssertionError("BrowserCookieSession entered inside a running event loop")

    def __exit__(self, exc_type, exc, traceback):
        return None

    async def is_logged_in(self):
        return True

    async def aclose(self):
        return None


class CliTests(unittest.TestCase):
    def test_doctor_reports_closed_cdp_port_without_traceback(self):
        with patch(
            "discourse_exporter.cli.check_cdp_endpoint",
            new=AsyncMock(side_effect=httpx.ConnectError("connection refused")),
        ), patch("sys.stderr", new_callable=io.StringIO) as stderr:
            code = main(["doctor"])

        self.assertEqual(code, 2)
        self.assertIn("Could not connect to Chrome DevTools", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_doctor_enters_browser_cookie_session_outside_async_loop(self):
        FakeBrowserCookieSession.entered_without_running_loop = False

        with patch(
            "discourse_exporter.cli.check_cdp_endpoint",
            new=AsyncMock(return_value={"Browser": "Chrome/126"}),
        ), patch(
            "discourse_exporter.cli.BrowserCookieSession",
            FakeBrowserCookieSession,
        ), patch("sys.stdout", new_callable=io.StringIO):
            code = main(["doctor"])

        self.assertEqual(code, 0)
        self.assertTrue(FakeBrowserCookieSession.entered_without_running_loop)

    def test_scrape_enters_browser_cookie_session_outside_async_loop(self):
        FakeBrowserCookieSession.entered_without_running_loop = False
        export = {
            "metadata": {
                "topic_count": 0,
                "post_count": 0,
                "user_count": 0,
            }
        }

        with patch(
            "discourse_exporter.cli.BrowserCookieSession",
            FakeBrowserCookieSession,
        ), patch(
            "discourse_exporter.cli.scrape_category_async",
            new=AsyncMock(return_value=export),
        ), patch("sys.stdout", new_callable=io.StringIO):
            code = main(["scrape"])

        self.assertEqual(code, 0)
        self.assertTrue(FakeBrowserCookieSession.entered_without_running_loop)

    def test_scrape_accepts_llm_fallback_mode(self):
        args = build_parser().parse_args(["scrape", "--llm-fallback", "missing"])

        self.assertEqual(args.llm_fallback, "missing")

    def test_scrape_llm_fallback_defaults_to_off(self):
        args = build_parser().parse_args(["scrape"])

        self.assertEqual(args.llm_fallback, "off")

    def test_scrape_accepts_llm_config_path(self):
        args = build_parser().parse_args(["scrape", "--llm-config", "my_llm.json"])

        self.assertEqual(str(args.llm_config), "my_llm.json")

    def test_scrape_accepts_topic_retry_options(self):
        args = build_parser().parse_args(
            ["scrape", "--topic-retries", "4", "--topic-retry-delay-seconds", "0.25"]
        )

        self.assertEqual(args.topic_retries, 4)
        self.assertEqual(args.topic_retry_delay_seconds, 0.25)

    def test_scrape_accepts_max_concurrent_requests(self):
        args = build_parser().parse_args(["scrape", "--max-concurrent-requests", "7"])

        self.assertEqual(args.max_concurrent_requests, 7)

    def test_launch_accepts_debug_user_data_dir(self):
        args = build_parser().parse_args(
            ["launch", "--profile", "Profile 1", "--debug-user-data-dir", "debug-profile"]
        )

        self.assertEqual(str(args.debug_user_data_dir), "debug-profile")

    def test_launch_accepts_launch_timeout_seconds(self):
        args = build_parser().parse_args(
            ["launch", "--profile", "Profile 1", "--launch-timeout-seconds", "12"]
        )

        self.assertEqual(args.launch_timeout_seconds, 12)

    def test_launch_waits_for_cdp_endpoint_after_starting_chrome(self):
        process = Mock()
        process.poll.return_value = None

        with patch(
            "discourse_exporter.cli.load_profiles_from_local_state",
            return_value=[ChromeProfile("Profile 1", "student.onlinedegree.iitm.ac.in")],
        ), patch(
            "discourse_exporter.cli.find_chrome_executable",
            return_value=Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        ), patch(
            "discourse_exporter.cli.subprocess.Popen",
            return_value=process,
        ), patch(
            "discourse_exporter.cli.check_cdp_endpoint",
            new=AsyncMock(return_value={"Browser": "Chrome/126"}),
        ), patch("sys.stdout", new_callable=io.StringIO) as stdout:
            code = main(["launch", "--profile", "Profile 1", "--launch-timeout-seconds", "0"])

        self.assertEqual(code, 0)
        self.assertIn("Chrome DevTools: ready", stdout.getvalue())

    def test_launch_reports_when_chrome_exits_before_cdp_ready(self):
        process = Mock()
        process.poll.return_value = 21

        with patch(
            "discourse_exporter.cli.load_profiles_from_local_state",
            return_value=[ChromeProfile("Profile 1", "student.onlinedegree.iitm.ac.in")],
        ), patch(
            "discourse_exporter.cli.find_chrome_executable",
            return_value=Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        ), patch(
            "discourse_exporter.cli.subprocess.Popen",
            return_value=process,
        ), patch(
            "discourse_exporter.cli.check_cdp_endpoint",
            new=AsyncMock(side_effect=httpx.ConnectError("connection refused")),
        ), patch("sys.stderr", new_callable=io.StringIO) as stderr:
            code = main(["launch", "--profile", "Profile 1", "--launch-timeout-seconds", "0"])

        self.assertEqual(code, 2)
        self.assertIn("Chrome exited before DevTools became available", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
