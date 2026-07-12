from __future__ import annotations

import argparse
import asyncio
import subprocess
import sys
import time
from pathlib import Path

import httpx

from .client import BrowserCookieSession, MissingPlaywrightError, check_cdp_endpoint
from .exporter import scrape_category_async
from .llm import MissingLLMConfigError, OpenAICompatibleLLMClient
from .profiles import (
    ProfileSelectionError,
    build_chrome_launch_args,
    find_chrome_executable,
    find_profile,
    format_windows_command,
    load_profiles_from_local_state,
)


DEFAULT_BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
DEFAULT_CATEGORY_PATH = "/c/courses/mlt-kb/32"
DEFAULT_CDP_URL = "http://127.0.0.1:9222"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return args.func(args)
    except (
        ConnectionError,
        FileNotFoundError,
        PermissionError,
        ProfileSelectionError,
        MissingPlaywrightError,
        MissingLLMConfigError,
        httpx.HTTPError,
    ) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Repeatable authenticated Discourse category exporter.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    profiles = subparsers.add_parser("profiles", help="List Chrome profiles and matching launch commands.")
    profiles.add_argument("--profile", help="Filter/select a profile by folder, display name, or email substring.")
    profiles.add_argument("--port", type=int, default=9222)
    profiles.add_argument("--start-url", default=DEFAULT_BASE_URL)
    profiles.add_argument(
        "--debug-user-data-dir",
        type=Path,
        default=_default_debug_user_data_dir(),
        help="Persistent non-standard Chrome user data directory required for remote debugging.",
    )
    profiles.set_defaults(func=cmd_profiles)

    launch = subparsers.add_parser("launch", help="Launch Chrome with remote debugging for one selected profile.")
    launch.add_argument("--profile", required=True, help="Profile folder/name/email substring, e.g. ds.study or Profile 4.")
    launch.add_argument("--port", type=int, default=9222)
    launch.add_argument("--start-url", default=DEFAULT_BASE_URL)
    launch.add_argument(
        "--launch-timeout-seconds",
        type=float,
        default=15,
        help="How long launch waits for Chrome DevTools to become reachable.",
    )
    launch.add_argument(
        "--debug-user-data-dir",
        type=Path,
        default=_default_debug_user_data_dir(),
        help="Persistent non-standard Chrome user data directory required for remote debugging.",
    )
    launch.set_defaults(func=cmd_launch)

    doctor = subparsers.add_parser("doctor", help="Check Chrome CDP connection and Discourse login.")
    doctor.add_argument("--cdp-url", default=DEFAULT_CDP_URL)
    doctor.add_argument("--base-url", default=DEFAULT_BASE_URL)
    doctor.set_defaults(func=cmd_doctor)

    scrape = subparsers.add_parser("scrape", help="Export category topics, posts, users, and images.")
    scrape.add_argument("--cdp-url", default=DEFAULT_CDP_URL)
    scrape.add_argument("--base-url", default=DEFAULT_BASE_URL)
    scrape.add_argument("--category-path", default=DEFAULT_CATEGORY_PATH)
    scrape.add_argument("--output-dir", type=Path, default=_default_output_dir())
    scrape.add_argument("--state-path", type=Path, default=_default_state_path())
    scrape.add_argument("--max-pages", type=int)
    scrape.add_argument("--rate-limit-seconds", type=float, default=0.5)
    scrape.add_argument("--refresh-users", action="store_true")
    scrape.add_argument(
        "--topic-retries",
        type=int,
        default=2,
        help="Extra retries for each topic JSON fetch after the first failed attempt.",
    )
    scrape.add_argument(
        "--topic-retry-delay-seconds",
        type=float,
        default=1.0,
        help="Delay between topic fetch retries.",
    )
    scrape.add_argument(
        "--llm-fallback",
        choices=("off", "missing", "always"),
        default="off",
        help="Use an OpenAI-compatible LLM fallback. Reads --llm-config first, then LLM_* env vars.",
    )
    scrape.add_argument(
        "--llm-config",
        type=Path,
        default=_default_llm_config_path(),
        help="JSON file for LLM settings. File values are used first, then env vars fill missing values.",
    )
    scrape.add_argument(
        "--max-concurrent-requests",
        type=int,
        default=10,
        help="Maximum concurrent HTTP requests across topics, images, user profiles, and LLM calls.",
    )
    scrape.set_defaults(func=cmd_scrape)

    return parser


def cmd_profiles(args) -> int:
    profiles = load_profiles_from_local_state()
    chrome_path = find_chrome_executable()

    if args.profile:
        selected = find_profile(profiles, args.profile)
        launch_args = build_chrome_launch_args(
            chrome_path,
            selected.folder,
            args.port,
            args.start_url,
            user_data_dir=args.debug_user_data_dir,
        )
        print(selected.label())
        print(format_windows_command(launch_args))
        return 0

    for index, profile in enumerate(profiles, start=1):
        launch_args = build_chrome_launch_args(
            chrome_path,
            profile.folder,
            args.port,
            args.start_url,
            user_data_dir=args.debug_user_data_dir,
        )
        print(f"{index}. {profile.label()}")
        print(f"   {format_windows_command(launch_args)}")
    return 0


def cmd_launch(args) -> int:
    profiles = load_profiles_from_local_state()
    selected = find_profile(profiles, args.profile)
    chrome_path = find_chrome_executable()
    args.debug_user_data_dir.mkdir(parents=True, exist_ok=True)
    launch_args = build_chrome_launch_args(
        chrome_path,
        selected.folder,
        args.port,
        args.start_url,
        user_data_dir=args.debug_user_data_dir,
    )
    print(f"Launching {selected.label()}")
    print(f"Debug user data dir: {args.debug_user_data_dir}")
    print(format_windows_command(launch_args))
    process = subprocess.Popen(launch_args)
    cdp_url = f"http://127.0.0.1:{args.port}"
    version = asyncio.run(_wait_for_cdp_endpoint(cdp_url, process, args.launch_timeout_seconds))
    print(f"Chrome DevTools: ready at {cdp_url} ({version.get('Browser', 'connected')})")
    return 0


async def _wait_for_cdp_endpoint(cdp_url: str, process, timeout_seconds: float) -> dict:
    deadline = time.monotonic() + max(0, timeout_seconds)
    last_error: Exception | None = None

    while True:
        try:
            return await check_cdp_endpoint(cdp_url, timeout=1)
        except httpx.HTTPError as exc:
            last_error = exc

        exit_code = process.poll()
        if exit_code is not None:
            raise ConnectionError(
                "Chrome exited before DevTools became available "
                f"at {cdp_url} (exit code {exit_code}). "
                "Close any Chrome windows using the scraper debug profile and run launch again. "
                "If it keeps happening, try a fresh --debug-user-data-dir."
            ) from last_error

        if time.monotonic() >= deadline:
            raise ConnectionError(
                f"Chrome DevTools did not become reachable at {cdp_url} "
                f"within {timeout_seconds:g} seconds. "
                "Chrome may have reused an existing window that was not launched with remote debugging. "
                "Close the scraper Chrome window or use a fresh --debug-user-data-dir, then run launch again."
            ) from last_error

        await asyncio.sleep(0.25)


def cmd_doctor(args) -> int:
    version = asyncio.run(_check_cdp_for_doctor_async(args))
    print(f"Chrome CDP: {version.get('Browser', 'connected')}")
    with BrowserCookieSession(args.base_url, args.cdp_url) as client:
        return asyncio.run(_cmd_doctor_login_async(args, client))


async def _check_cdp_for_doctor_async(args) -> dict:
    try:
        return await check_cdp_endpoint(args.cdp_url)
    except httpx.HTTPError as exc:
        raise ConnectionError(
            f"Could not connect to Chrome DevTools at {args.cdp_url}. "
            "Run `python scrape_discourse.py profiles`, copy the launch command for your DS profile, "
            "then run `python scrape_discourse.py doctor` again."
        ) from exc


async def _cmd_doctor_login_async(args, client) -> int:
    try:
        if await client.is_logged_in():
            print(f"Discourse login: authenticated for {args.base_url}")
            return 0
        print(f"Discourse login: not authenticated for {args.base_url}", file=sys.stderr)
        return 1
    finally:
        await client.aclose()


def cmd_scrape(args) -> int:
    llm_client = None
    if args.llm_fallback != "off":
        llm_client = OpenAICompatibleLLMClient.from_file_then_env(args.llm_config)

    with BrowserCookieSession(args.base_url, args.cdp_url) as client:
        return asyncio.run(_cmd_scrape_async(args, llm_client, client))


async def _cmd_scrape_async(args, llm_client, client) -> int:
    try:
        if not await client.is_logged_in():
            raise PermissionError(
                f"Chrome is reachable, but not logged in to {args.base_url}. "
                "Open that site in the selected profile and try again."
            )
        export = await scrape_category_async(
            client=client,
            base_url=args.base_url,
            category_path=args.category_path,
            output_dir=args.output_dir,
            state_path=args.state_path,
            max_pages=args.max_pages,
            rate_limit_seconds=args.rate_limit_seconds,
            refresh_users=args.refresh_users,
            llm_fallback=args.llm_fallback,
            llm_client=llm_client,
            topic_retries=args.topic_retries,
            topic_retry_delay_seconds=args.topic_retry_delay_seconds,
            max_concurrent_requests=args.max_concurrent_requests,
        )
    finally:
        await client.aclose()
        if llm_client is not None:
            await llm_client.aclose()
    print(
        "Exported "
        f"{export['metadata']['topic_count']} topics, "
        f"{export['metadata']['post_count']} posts, "
        f"{export['metadata']['user_count']} users."
    )
    print(f"Output: {args.output_dir}")
    print(f"State: {args.state_path}")
    return 0


def _default_output_dir() -> Path:
    return Path(__file__).resolve().parents[3] / "outputs"


def _default_state_path() -> Path:
    return Path(__file__).resolve().parents[1] / "state.json"


def _default_llm_config_path() -> Path:
    return Path(__file__).resolve().parents[1] / "llm_config.json"


def _default_debug_user_data_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "chrome_debug_user_data"
