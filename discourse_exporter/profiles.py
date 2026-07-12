from __future__ import annotations

import json
import os
import re
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


class ProfileSelectionError(ValueError):
    """Raised when a profile query cannot be resolved to one Chrome profile."""


@dataclass(frozen=True)
class ChromeProfile:
    folder: str
    name: str = ""
    email: str = ""

    def haystack(self) -> str:
        return " ".join([self.folder, self.name, self.email]).lower()

    def label(self) -> str:
        suffix = f" <{self.email}>" if self.email else ""
        return f"{self.folder}: {self.name}{suffix}".strip()


def default_local_state_path() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        raise FileNotFoundError("LOCALAPPDATA is not set; cannot find Chrome profile metadata.")
    return Path(local_app_data) / "Google" / "Chrome" / "User Data" / "Local State"


def load_profiles_from_local_state(path: Path | None = None) -> list[ChromeProfile]:
    path = path or default_local_state_path()
    if not path.exists():
        raise FileNotFoundError(f"Chrome Local State file not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))
    info_cache = payload.get("profile", {}).get("info_cache", {})
    profiles = [
        ChromeProfile(
            folder=folder,
            name=str(info.get("name") or ""),
            email=str(info.get("user_name") or ""),
        )
        for folder, info in info_cache.items()
    ]
    return sorted(profiles, key=_profile_sort_key)


def find_profile(profiles: Sequence[ChromeProfile], query: str) -> ChromeProfile:
    query = query.strip().lower()
    if not query:
        raise ProfileSelectionError("Profile query is empty.")

    exact = [
        profile
        for profile in profiles
        if query in {profile.folder.lower(), profile.name.lower(), profile.email.lower()}
    ]
    if len(exact) == 1:
        return exact[0]

    matches = [profile for profile in profiles if query in profile.haystack()]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        available = "\n".join(f"- {profile.label()}" for profile in profiles)
        raise ProfileSelectionError(f"No Chrome profile matched '{query}'. Available profiles:\n{available}")

    candidates = "\n".join(f"- {profile.label()}" for profile in matches)
    raise ProfileSelectionError(f"Profile query '{query}' is ambiguous. Matching profiles:\n{candidates}")


def find_chrome_executable() -> Path:
    candidates = [
        Path(os.environ.get("PROGRAMFILES", "")) / "Google" / "Chrome" / "Application" / "chrome.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Google" / "Chrome" / "Application" / "chrome.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "Application" / "chrome.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Could not find chrome.exe in the standard installation locations.")


def build_chrome_launch_args(
    chrome_path: Path,
    profile_folder: str,
    port: int,
    start_url: str,
    user_data_dir: Path | None = None,
) -> list[str]:
    args = [
        str(chrome_path),
        f"--remote-debugging-port={port}",
        "--remote-debugging-address=127.0.0.1",
        f"--profile-directory={profile_folder}",
    ]
    if user_data_dir is not None:
        args.append(f"--user-data-dir={user_data_dir}")
    args.extend(["--new-window", start_url])
    return args


def format_windows_command(args: Iterable[str]) -> str:
    rendered: list[str] = []
    for arg in args:
        if re.search(r"\s", arg):
            rendered.append(f'"{arg}"')
        else:
            rendered.append(arg)
    return " ".join(rendered)


def _profile_sort_key(profile: ChromeProfile) -> tuple[int, int, str]:
    if profile.folder == "Default":
        return (0, 0, profile.folder)
    match = re.fullmatch(r"Profile\s+(\d+)", profile.folder)
    if match:
        return (1, int(match.group(1)), profile.folder)
    return (2, 0, profile.folder)
