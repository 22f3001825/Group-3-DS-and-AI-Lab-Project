from __future__ import annotations

import json
from http.cookiejar import Cookie
from typing import Any
from urllib.parse import urljoin

import requests


class MissingPlaywrightError(RuntimeError):
    pass


class BrowserCookieSession:
    """Requests session populated with cookies from a Chrome CDP connection."""

    def __init__(self, base_url: str, cdp_url: str = "http://127.0.0.1:9222", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.cdp_url = cdp_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self._playwright = None
        self._browser = None

    def __enter__(self) -> "BrowserCookieSession":
        try:
            from playwright.sync_api import Error, sync_playwright
        except ImportError as exc:
            raise MissingPlaywrightError(
                "Playwright is required to read cookies from Chrome. "
                "Run: python -m pip install -r requirements.txt"
            ) from exc

        try:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.connect_over_cdp(self.cdp_url)
        except Error as exc:
            raise ConnectionError(
                f"Could not connect to Chrome DevTools at {self.cdp_url}. "
                "Run the launch command printed by `python scrape_discourse.py profiles` first."
            ) from exc

        contexts = self._browser.contexts
        if not contexts:
            raise ConnectionError("Connected to Chrome, but no browser contexts were available.")

        cookies = contexts[0].cookies([self.base_url])
        if not cookies:
            raise PermissionError(
                f"No cookies were available for {self.base_url}. "
                "Open the Discourse site in the selected Chrome profile and confirm you are logged in."
            )

        for cookie in cookies:
            self.session.cookies.set_cookie(_to_requests_cookie(cookie))
        self.session.headers.update(
            {
                "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
                "User-Agent": "CodexDiscourseExporter/0.1",
            }
        )
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self._playwright is not None:
            self._playwright.stop()

    def get_json(self, path_or_url: str) -> dict[str, Any]:
        response = self.session.get(self._url(path_or_url), timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_bytes(self, path_or_url: str) -> tuple[bytes, str]:
        response = self.session.get(self._url(path_or_url), timeout=self.timeout)
        response.raise_for_status()
        return response.content, response.headers.get("content-type", "")

    def is_logged_in(self) -> bool:
        response = self.session.get(f"{self.base_url}/session/current.json", timeout=self.timeout)
        if response.status_code != 200:
            return False
        try:
            payload = response.json()
        except json.JSONDecodeError:
            return False
        return bool(payload.get("current_user"))

    def _url(self, path_or_url: str) -> str:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return path_or_url
        return urljoin(self.base_url + "/", path_or_url.lstrip("/"))


def check_cdp_endpoint(cdp_url: str = "http://127.0.0.1:9222", timeout: int = 5) -> dict[str, Any]:
    response = requests.get(cdp_url.rstrip("/") + "/json/version", timeout=timeout)
    response.raise_for_status()
    return response.json()


def _to_requests_cookie(cookie: dict[str, Any]) -> Cookie:
    return Cookie(
        version=0,
        name=cookie["name"],
        value=cookie["value"],
        port=None,
        port_specified=False,
        domain=cookie.get("domain") or "",
        domain_specified=bool(cookie.get("domain")),
        domain_initial_dot=str(cookie.get("domain") or "").startswith("."),
        path=cookie.get("path") or "/",
        path_specified=True,
        secure=bool(cookie.get("secure")),
        expires=cookie.get("expires") if cookie.get("expires", -1) != -1 else None,
        discard=False,
        comment=None,
        comment_url=None,
        rest={"HttpOnly": cookie.get("httpOnly")},
        rfc2109=False,
    )
