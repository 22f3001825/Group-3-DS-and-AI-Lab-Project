import json
import tempfile
import unittest
from pathlib import Path

from discourse_exporter.profiles import (
    ProfileSelectionError,
    build_chrome_launch_args,
    find_profile,
    format_windows_command,
    load_profiles_from_local_state,
)


class ProfileTests(unittest.TestCase):
    def write_local_state(self, payload):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "Local State"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_load_profiles_reads_folder_name_and_email(self):
        path = self.write_local_state(
            {
                "profile": {
                    "info_cache": {
                        "Default": {"name": "Person 1", "user_name": "user@example.com"},
                        "Profile 4": {
                            "name": "ds.study.iitm.ac.in",
                            "user_name": "21f1001895@ds.study.iitm.ac.in",
                        },
                    }
                }
            }
        )

        profiles = load_profiles_from_local_state(path)

        self.assertEqual([profile.folder for profile in profiles], ["Default", "Profile 4"])
        self.assertEqual(profiles[1].name, "ds.study.iitm.ac.in")
        self.assertEqual(profiles[1].email, "21f1001895@ds.study.iitm.ac.in")

    def test_find_profile_matches_folder_name_or_email(self):
        path = self.write_local_state(
            {
                "profile": {
                    "info_cache": {
                        "Profile 4": {
                            "name": "ds.study.iitm.ac.in",
                            "user_name": "21f1001895@ds.study.iitm.ac.in",
                        },
                    }
                }
            }
        )
        profiles = load_profiles_from_local_state(path)

        self.assertEqual(find_profile(profiles, "Profile 4").folder, "Profile 4")
        self.assertEqual(find_profile(profiles, "ds.study").folder, "Profile 4")
        self.assertEqual(find_profile(profiles, "21f1001895").folder, "Profile 4")

    def test_find_profile_reports_ambiguous_matches(self):
        path = self.write_local_state(
            {
                "profile": {
                    "info_cache": {
                        "Profile 4": {"name": "ds.study.iitm.ac.in"},
                        "Profile 7": {"name": "jessin ds.study.iitm.ac.in"},
                    }
                }
            }
        )
        profiles = load_profiles_from_local_state(path)

        with self.assertRaises(ProfileSelectionError) as caught:
            find_profile(profiles, "ds.study")

        self.assertIn("Profile 4", str(caught.exception))
        self.assertIn("Profile 7", str(caught.exception))

    def test_build_launch_command_quotes_profile_folder(self):
        args = build_chrome_launch_args(
            chrome_path=Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            profile_folder="Profile 4",
            port=9222,
            start_url="https://discourse.onlinedegree.iitm.ac.in",
            user_data_dir=None,
        )

        self.assertEqual(args[1], "--remote-debugging-port=9222")
        self.assertEqual(args[2], "--remote-debugging-address=127.0.0.1")
        self.assertEqual(args[3], "--profile-directory=Profile 4")
        rendered = format_windows_command(args)
        self.assertIn('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"', rendered)
        self.assertIn('"--profile-directory=Profile 4"', rendered)

    def test_build_launch_command_can_use_non_standard_user_data_dir(self):
        args = build_chrome_launch_args(
            chrome_path=Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            profile_folder="Profile 1",
            port=9222,
            start_url="https://discourse.onlinedegree.iitm.ac.in",
            user_data_dir=Path(r"C:\temp\discourse-debug-chrome"),
        )

        self.assertIn(r"--user-data-dir=C:\temp\discourse-debug-chrome", args)
        rendered = format_windows_command(args)
        self.assertIn("--user-data-dir=C:\\temp\\discourse-debug-chrome", rendered)


if __name__ == "__main__":
    unittest.main()
