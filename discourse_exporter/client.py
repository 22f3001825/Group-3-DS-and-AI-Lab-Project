from __future__ import annotations

import json
from http.cookiejar import Cookie, CookieJar
from typing import Any
from urllib.parse import urljoin

import httpx


class MissingPlaywrightError(RuntimeError):
    pass


class BrowserCookieSession:
    """Async HTTP client populated with cookies from a Chrome CDP connection."""

    def __init__(self, base_url: str, cdp_url: str = "http://127.0.0.1:9222", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.cdp_url = cdp_url.rstrip("/")
        self.timeout = timeout
        self.cookies = CookieJar()
        self.headers = {
            "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
            "User-Agent": "CodexDiscourseExporter/0.1",
        }
        self._playwright = None
        self._browser = None
        self._client: httpx.AsyncClient | None = None

    def __enter__(self) -> "BrowserCookieSession":
        try:
            from playwright.sync_api import Error, sync_playwright
        except ImportError as exc:
            raise MissingPlaywrightError(
                "Playwright is required to read cookies from Chrome. "
                "Run: python -m pip install -r requirements.txt"
            ) from exc

        try:
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
                self.cookies.set_cookie(_to_cookiejar_cookie(cookie))
        finally:
            # Playwright's synchronous CDP adapter keeps an event loop active.
            # The scraper only needs the copied cookies, so disconnect before
            # entering asyncio.run for the HTTP export.
            self._disconnect_playwright()
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self._disconnect_playwright()

    def _disconnect_playwright(self) -> None:
        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None
            self._browser = None

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def get_json(self, path_or_url: str) -> dict[str, Any]:
        response = await self._request(path_or_url)
        return response.json()

    async def get_bytes(self, path_or_url: str) -> tuple[bytes, str]:
        response = await self._request(path_or_url)
        return response.content, response.headers.get("content-type", "")

    async def is_logged_in(self) -> bool:
        response = await self._client_or_create().get(f"{self.base_url}/session/current.json")
        if response.status_code != 200:
            return False
        try:
            payload = response.json()
        except json.JSONDecodeError:
            return False
        return bool(payload.get("current_user"))

    async def _request(self, path_or_url: str) -> httpx.Response:
        response = await self._client_or_create().get(self._url(path_or_url))
        response.raise_for_status()
        return response

    def _client_or_create(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                cookies=self.cookies,
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=True,
            )
        return self._client

    def _url(self, path_or_url: str) -> str:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return path_or_url
        return urljoin(self.base_url + "/", path_or_url.lstrip("/"))


async def check_cdp_endpoint(cdp_url: str = "http://127.0.0.1:9222", timeout: int = 5) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(cdp_url.rstrip("/") + "/json/version")
        response.raise_for_status()
        return response.json()


def _to_cookiejar_cookie(cookie: dict[str, Any]) -> Cookie:
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
