"""Bounded public-web collection: seeds + sitemaps + HTML/PDF links.

No login, directory guessing, access-control bypass, or external search API.
Edit sources.json to add public sources. Every skipped URL is recorded.
"""

import heapq
import json
import re
import time
import xml.etree.ElementTree as ET
from collections import deque
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader

from nu_chat.config import DATA_DIR, ROOT

AGENT = "NileGuideStudentProject/1.0"
MAX_BYTES = 20 * 1024 * 1024
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
    ".xlsx",
}


def canonical_url(url: str, domains: list[str]) -> str | None:
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
        if any(
            word in host.split(".")[0] for word in ("stage", "register", "portal", "moodle", "mail")
        ):
            return None
        if re.search(r"/(user|admin|login|search|node/\d+/edit)(/|$)", parts.path, re.I):
            return None
        if Path(parts.path).suffix.lower() in SKIP_EXTENSIONS:
            return None
        # Pagination is useful; tracking/search/filter query combinations are not.
        query = parts.query if re.fullmatch(r"page=\d{1,3}", parts.query) else ""
        return urlunsplit((parts.scheme, host, parts.path or "/", query, ""))
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

    def robot_policy(self, url: str) -> RobotFileParser:
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if origin not in self.robots:
            robot = RobotFileParser(origin + "/robots.txt")
            # Robots redirects also remain inside the configured domain scope.
            response = self.fetch(origin + "/robots.txt", check_robots=False)
            robot.parse(response[1].decode("utf-8", errors="replace").splitlines())
            self.robots[origin] = robot
        return self.robots[origin]

    def fetch(self, url: str, check_robots: bool = True) -> tuple[str, bytes, str]:
        for _ in range(6):
            safe = canonical_url(url, self.domains)
            if not safe:
                raise ValueError("URL or redirect outside public source scope")
            delay = self.delay
            if check_robots:
                policy = self.robot_policy(safe)
                if not policy.can_fetch(AGENT, safe):
                    raise ValueError("Disallowed by robots.txt")
                delay = max(delay, policy.crawl_delay(AGENT) or 0)
            host = urlsplit(safe).netloc
            time.sleep(max(0, delay - (time.monotonic() - self.last_request.get(host, 0))))
            self.last_request[host] = time.monotonic()
            with self.client.stream("GET", safe) as response:
                if response.is_redirect:
                    url = urljoin(safe, response.headers["location"])
                    continue
                if not check_robots and response.status_code == 404:
                    return safe, b"User-agent: *\nAllow: /", "text/plain"
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
                while pending and len(seen) < 4:
                    sitemap = pending.popleft()
                    if sitemap in seen:
                        continue
                    seen.add(sitemap)
                    _, body, _ = self.fetch(sitemap)
                    root = ET.fromstring(body)
                    locations = [
                        e.text.strip() for e in root.iter() if e.tag.endswith("}loc") and e.text
                    ]
                    if root.tag.endswith("sitemapindex"):
                        pending.extend(locations)
                    else:
                        urls.extend(locations)
            except (httpx.HTTPError, ValueError, ET.ParseError) as exc:
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
    # Keep each table row together so values retain their column order.
    for table in soup.select("table"):
        rows = [
            " | ".join(cell.get_text(" ", strip=True) for cell in row.select("th,td"))
            for row in table.select("tr")
        ]
        table.replace_with(soup.new_string("\n" + "\n".join(rows) + "\n"))
    main = soup.select_one("main") or soup.select_one("#content") or soup.body or soup
    lines = [re.sub(r"\s+", " ", line).strip() for line in main.get_text("\n").splitlines()]
    text = "\n".join(line for line in lines if line)
    return title, text, links


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
    max_pages: int = 100, use_sitemaps: bool = True, config_path: Path = ROOT / "sources.json"
) -> dict:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    collector = Collector(config["allowed_domains"])
    documents, visited, hashes = [], set(), set()
    seeds = config["seeds"]
    discovered = collector.discover_sitemaps(seeds) if use_sitemaps else []
    pending, queued = [], set()

    def enqueue(url: str, rank: int | None = None):
        safe = canonical_url(url, config["allowed_domains"])
        if safe and safe not in queued:
            queued.add(safe)
            heapq.heappush(pending, (priority(safe) if rank is None else rank, len(queued), safe))

    for seed in seeds:
        enqueue(seed, -1)
    for url in discovered:
        enqueue(url)
    fetched_at = datetime.now(timezone.utc).isoformat()
    try:
        # Bound attempts as well as successes, so broken sites cannot cause endless crawls.
        while pending and len(visited) < max_pages:
            url = heapq.heappop(pending)[2]
            if not url or url in visited:
                continue
            visited.add(url)
            print(f"[{len(visited)}/{max_pages}] {url}", flush=True)
            try:
                final, body, content_type = collector.fetch(url)
                is_pdf = "application/pdf" in content_type or body.startswith(b"%PDF")
                archive = "oldwebsite." in final
                if is_pdf:
                    reader = PdfReader(BytesIO(body))
                    title = str(
                        (reader.metadata or {}).get("/Title") or Path(urlsplit(final).path).name
                    )
                    sections = [
                        (number, page.extract_text() or "")
                        for number, page in enumerate(reader.pages, 1)
                    ]
                    links = []
                elif "html" in content_type:
                    title, text, links = extract_html(body, final)
                    sections = [(None, text)]
                else:
                    raise ValueError("Unsupported source type (HTML and text-based PDF only)")
                count = 0
                for page, text in sections:
                    text = re.sub(r"[ \t]+", " ", text).strip()
                    digest = sha256(text.encode()).hexdigest()
                    if len(text) < 120 or digest in hashes:
                        continue
                    hashes.add(digest)
                    documents.append(
                        {
                            "id": sha256(f"{final}#{page}".encode()).hexdigest()[:16],
                            "url": final,
                            "title": title,
                            "text": text,
                            "page": page,
                            "kind": "pdf" if is_pdf else "html",
                            "fetched_at": fetched_at,
                            "archived": archive,
                        }
                    )
                    count += 1
                if not count:
                    collector.skipped.append(
                        {"url": final, "reason": "No new extractable text; scan may require OCR"}
                    )
                # Include public embedded PDFs before the rest of the crawl queue.
                safe_links = sorted(
                    {
                        u
                        for link in links
                        if (u := canonical_url(link, config["allowed_domains"]))
                        and u not in visited
                    },
                    key=priority,
                )
                for link in safe_links:
                    enqueue(link)
            except Exception as exc:
                collector.skipped.append({"url": url, "reason": str(exc)})
    finally:
        collector.client.close()
    if not documents:
        raise RuntimeError(
            "No documents collected. Existing corpus was preserved. Check network access and source URLs."
        )
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    corpus = DATA_DIR / "documents.jsonl"
    temporary = corpus.with_suffix(".tmp")
    temporary.write_text(
        "\n".join(json.dumps(d, ensure_ascii=False) for d in documents), encoding="utf-8"
    )
    temporary.replace(corpus)
    report = {
        "fetched_at": fetched_at,
        "attempted": len(visited),
        "documents": len(documents),
        "unique_urls": len({d["url"] for d in documents}),
        "sitemap_urls_discovered": len(discovered),
        "pending_urls": len(pending),
        "skipped": collector.skipped,
    }
    (DATA_DIR / "collection_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    inventory = [{k: v for k, v in d.items() if k not in {"text", "id"}} for d in documents]
    (DATA_DIR / "source_inventory.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report
