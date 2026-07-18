"""Minimal FreshRSS Google-Reader-API client (stdlib only)."""

import html
import json
import re
import urllib.parse
import urllib.request

from . import config

READING_LIST = "user/-/state/com.google/reading-list"
READ_STATE = "user/-/state/com.google/read"
STARRED = "user/-/state/com.google/starred"

_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(text: str, limit: int = 600) -> str:
    text = html.unescape(_TAG_RE.sub(" ", text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


class Client:
    def __init__(self):
        self.auth = self._login()

    def _login(self) -> str:
        qs = urllib.parse.urlencode(
            {"Email": config.FRESH_USER, "Passwd": config.FRESH_API_PASS}
        )
        with urllib.request.urlopen(
            f"{config.FRESH_URL}/accounts/ClientLogin?{qs}", timeout=20
        ) as r:
            body = r.read().decode()
        for line in body.splitlines():
            if line.startswith("Auth="):
                return line[5:].strip()
        raise RuntimeError(f"FreshRSS login failed: {body[:200]}")

    def _get(self, path: str, params: dict) -> dict:
        params = {"output": "json", **params}
        url = f"{config.FRESH_URL}/reader/api/0/{path}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(
            url, headers={"Authorization": f"GoogleLogin auth={self.auth}"}
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())

    def _stream(self, stream: str, n: int, exclude: str | None = None,
                newer_than_unix: int | None = None, max_items: int = 2000):
        """Yield items from a stream, following continuations."""
        fetched = 0
        cont = None
        while fetched < max_items:
            params = {"n": min(n, max_items - fetched)}
            if exclude:
                params["xt"] = exclude
            if newer_than_unix:
                params["ot"] = newer_than_unix
            if cont:
                params["c"] = cont
            data = self._get(
                f"stream/contents/{urllib.parse.quote(stream, safe='')}", params
            )
            items = data.get("items", [])
            if not items:
                return
            for it in items:
                yield self._normalize(it)
                fetched += 1
            cont = data.get("continuation")
            if not cont:
                return

    @staticmethod
    def _normalize(it: dict) -> dict:
        url = ""
        for key in ("canonical", "alternate"):
            links = it.get(key) or []
            if links and links[0].get("href"):
                url = links[0]["href"]
                break
        category = ""
        for c in it.get("categories", []):
            if "/label/" in c:
                category = c.split("/label/", 1)[1]
                break
        content = (it.get("summary") or it.get("content") or {}).get("content", "")
        return {
            "id": it.get("id", ""),
            "title": _strip_html(it.get("title", ""), 300),
            "url": url,
            "published": int(it.get("published", 0)),
            "feed": (it.get("origin") or {}).get("title", ""),
            "category": category,
            "snippet": _strip_html(content),
        }

    def unread(self, newer_than_unix: int | None = None, max_items: int = 2000):
        return self._stream(READING_LIST, 200, exclude=READ_STATE,
                            newer_than_unix=newer_than_unix, max_items=max_items)

    def starred(self, max_items: int = 60):
        return self._stream(STARRED, 60, max_items=max_items)
