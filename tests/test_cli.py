import io
import unittest
from unittest.mock import patch

import requests

from discourse_exporter.cli import build_parser, main


class CliTests(unittest.TestCase):
    def test_doctor_reports_closed_cdp_port_without_traceback(self):
        with patch(
            "discourse_exporter.cli.check_cdp_endpoint",
            side_effect=requests.exceptions.ConnectionError("connection refused"),
        ), patch("sys.stderr", new_callable=io.StringIO) as stderr:
            code = main(["doctor"])

        self.assertEqual(code, 2)
        self.assertIn("Could not connect to Chrome DevTools", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

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

    def test_launch_accepts_debug_user_data_dir(self):
        args = build_parser().parse_args(
            ["launch", "--profile", "Profile 1", "--debug-user-data-dir", "debug-profile"]
        )

        self.assertEqual(str(args.debug_user_data_dir), "debug-profile")


if __name__ == "__main__":
    unittest.main()
