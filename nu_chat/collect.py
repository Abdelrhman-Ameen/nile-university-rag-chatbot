"""Bounded public-web collection: seeds + sitemaps + HTML/PDF links.

No login, directory guessing, access-control bypass, or external search API.
Edit sources.json to add public sources. Every skipped URL is recorded.
"""

import re
import threading
import time
import xml.etree.ElementTree as ET
from collections import deque
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlencode, urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup

from nu_chat.config import ROOT

AGENT = "NileGuideStudentProject/1.0"
MAX_BYTES = 20 * 1024 * 1024


class SourceBlocked(RuntimeError):
    """Pause this host when it asks for verification or refuses automated requests."""


SKIP_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".webp",
    ".zip",
    ".mp4",
    ".mp3",
    ".css",
    ".js",
    ".ico",
}


def canonical_url(url: str, domains: list[str], assets: bool = False) -> str | None:
    try:
        parts = urlsplit(url)
        host = (parts.hostname or "").lower()
        if host == "www.nu.edu.eg":
            host = "nu.edu.eg"
        if parts.scheme not in {"https", "http"} or parts.username or parts.password:
            return None
        if parts.port not in {None, 80, 443}:
            return None
        if not any(host == d or host.endswith("." + d) for d in domains):
            return None
        if (
            any(
                word in host.split(".")[0]
                for word in ("stage", "register", "portal", "moodle", "mail", "localhost")
            )
            or re.fullmatch(r"main\d+", host.split(".")[0])
            or host.split(".")[0].endswith("-new")
        ):
            return None
        if re.search(
            r"/(user|admin|login|search|wp-admin|wp-login.php|node/\d+/edit)(/|$)|(?:^|[-/])test(?:[-/]|$)",
            parts.path,
            re.I,
        ):
            return None
        suffix = Path(unquote(parts.path)).suffix.lower()
        if suffix in SKIP_EXTENSIONS and not (
            assets and suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"}
        ):
            return None
        # Preserve public catalogue identifiers and pagination, discard tracking/filter loops.
        query = urlencode(
            sorted(
                (k, v)
                for k, v in parse_qsl(parts.query)
                if k in {"page", "paged", "biblionumber", "id", "p"} and re.fullmatch(r"\d{1,7}", v)
            )
        )
        path = re.sub(r"/+", "/", parts.path) or "/"
        return urlunsplit(("https", host, path, query, ""))
    except ValueError:
        return None


class Collector:
    def __init__(self, domains: list[str], delay: float = 0.4):
        self.domains = domains
        self.delay = delay
        self.client = httpx.Client(timeout=20, headers={"User-Agent": AGENT})
        self.robots: dict[str, RobotFileParser] = {}
        self.last_request: dict[str, float] = {}
        self.skipped: list[dict] = []
        self.policy_locks = {}
        self.request_locks = {}
        self.slots = {}
        self.blocked = {}

    def robot_policy(self, url: str) -> RobotFileParser:
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        with self.policy_locks.setdefault(origin, threading.RLock()):
            if origin not in self.robots:
                robot = RobotFileParser(origin + "/robots.txt")
                response = self.fetch(origin + "/robots.txt", check_robots=False)
                robot.parse(response[1].decode("utf-8", errors="replace").splitlines())
                self.robots[origin] = robot
        return self.robots[origin]

    def fetch(
        self, url: str, check_robots: bool = True, assets: bool = False
    ) -> tuple[str, bytes, str]:
        for _ in range(6):
            safe = canonical_url(url, self.domains, assets=assets)
            if not safe:
                raise ValueError("URL or redirect outside public source scope")
            host = urlsplit(safe).netloc
            if host in self.blocked:
                raise SourceBlocked(self.blocked[host])
            delay = self.delay
            if check_robots:
                policy = self.robot_policy(safe)
                if not policy.can_fetch(AGENT, safe):
                    raise ValueError("Disallowed by robots.txt")
                delay = max(delay, policy.crawl_delay(AGENT) or 0)
            with self.request_locks.setdefault(host, threading.Lock()):
                time.sleep(max(0, delay - (time.monotonic() - self.last_request.get(host, 0))))
                self.last_request[host] = time.monotonic()
            with (
                self.slots.setdefault(host, threading.BoundedSemaphore(2)),
                self.client.stream("GET", safe) as response,
            ):
                if response.is_redirect:
                    url = urljoin(safe, response.headers["location"])
                    continue
                if not check_robots and response.status_code == 404:
                    return safe, b"User-agent: *\nAllow: /", "text/plain"
                if response.status_code in {403, 405, 429, 503}:
                    reason = f"HTTP {response.status_code}: host paused; access challenge, throttling or service unavailable. Retry after the site permits access."
                    self.blocked[host] = reason
                    raise SourceBlocked(reason)
                response.raise_for_status()
                data = bytearray()
                for block in response.iter_bytes():
                    data.extend(block)
                    if len(data) > MAX_BYTES:
                        raise ValueError("Source exceeds 20 MB download limit")
                return safe, bytes(data), response.headers.get("content-type", "")
        raise ValueError("Too many redirects")

    def discover_sitemaps(self, seeds: list[str]) -> list[str]:
        urls = []
        origins = list(dict.fromkeys(f"{urlsplit(s).scheme}://{urlsplit(s).netloc}" for s in seeds))
        for origin in origins:
            try:
                maps = self.robot_policy(origin).site_maps() or [origin + "/sitemap.xml"]
                pending = deque(maps)
                seen = set()
                while pending and len(seen) < 100:
                    sitemap = pending.popleft()
                    if sitemap in seen:
                        continue
                    seen.add(sitemap)
                    _, body, _ = self.fetch(sitemap)
                    root = ET.fromstring(body)
                    locations = [
                        e.text.strip()
                        for e in root.iter()
                        if e.tag.split("}")[-1] == "loc" and e.text
                    ]
                    if root.tag.endswith("sitemapindex"):
                        pending.extend(locations)
                    else:
                        urls.extend(locations)
            except (httpx.HTTPError, ValueError, SourceBlocked, ET.ParseError) as exc:
                self.skipped.append({"url": origin + "/sitemap.xml", "reason": str(exc)})
        return urls


def extract_html(body: bytes, url: str) -> tuple[str, str, list[str]]:
    soup = BeautifulSoup(body, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else urlsplit(url).path
    links = [
        urljoin(url, tag.get("href", tag.get("src", tag.get("data", ""))))
        for tag in soup.select("a[href], iframe[src], embed[src], object[data]")
    ]
    for tag in soup.select(
        "script, style, nav, header, footer, noscript, form, .breadcrumb, .menu, .social-links, [class*='testimonial']"
    ):
        tag.decompose()
    for tag in soup.select('a[href^="mailto:"]'):
        tag.append(" (" + tag["href"].split(":", 1)[1].split("?")[0] + ")")
    for tag in soup.select("h1,h2,h3,h4,h5,h6"):
        tag.replace_with(soup.new_string("\n## " + tag.get_text(" ", strip=True) + "\n"))
    # Keep each table row together so values retain their column order.
    for table in soup.select("table"):
        rows = []
        headers = [c.get_text(" ", strip=True) for c in table.select("tr:first-child th")]
        for row in table.select("tr"):
            cells = [c.get_text(" ", strip=True) for c in row.select("th,td")]
            rows.append(
                " | ".join(
                    f"{headers[i]}: {v}"
                    if headers and len(headers) == len(cells) and not row.select("th")
                    else v
                    for i, v in enumerate(cells)
                )
            )
        table.replace_with(soup.new_string("\n" + "\n".join(rows) + "\n"))
    main = soup.select_one("main") or soup.select_one("#content") or soup.body or soup
    lines = [re.sub(r"\s+", " ", line).strip() for line in main.get_text("\n").splitlines()]
    text = "\n".join(line for line in lines if line)
    return title, text, links


def content_images(body: bytes, url: str) -> list[dict]:
    """Inventory informative images separately; photos and logos are not policy text."""
    soup = BeautifulSoup(body, "html.parser")
    main = soup.select_one("main") or soup.select_one("article") or soup.body or soup
    images = []
    for tag in main.select("img[src]"):
        src = urljoin(url, tag.get("data-src") or tag["src"])
        alt = tag.get("alt", "").strip()
        heading = tag.find_previous(["h1", "h2", "h3", "h4"])
        context = heading.get_text(" ", strip=True) if heading else alt
        candidate = "inline-images" in src or bool(
            re.search(
                r"fee|tuition|scholarship|schedule|calendar|criteria|stages|objectives|competenc|guideline",
                alt + " " + src,
                re.I,
            )
        )
        images.append({"url": src, "alt": alt, "section": context, "ocr_candidate": candidate})
    return images


def priority(url: str) -> int:
    if urlsplit(url).path.lower().endswith(".pdf"):
        return 0
    if any(
        term in url.lower() for term in ("/publications/", "/academic-staff/", "/news/", "/events/")
    ):
        return 3
    if any(
        term in url.lower()
        for term in (
            "admission",
            "scholarship",
            "program",
            "fees",
            "apply",
            "academic",
            "faq",
            "student",
            "library",
            "contact",
        )
    ):
        return 1
    return 2


def collect(
    max_pages: int = 0,
    use_sitemaps: bool = True,
    config_path: Path = ROOT / "sources.json",
    refresh: bool = False,
) -> dict:
    from nu_chat.crawl import collect as run_collection

    return run_collection(max_pages, use_sitemaps, config_path, refresh)
