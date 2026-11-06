"""Check the small static site without third-party dependencies.

Usage: python3 scripts/check_site.py
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://cloudlatch.chrominsky.dev/"
BLOCK_TAGS = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "div", "section",
              "summary", "td", "th", "figcaption", "br", "ul", "ol", "details", "dt", "dd"}
TEXT_ATTRS = ("content", "alt", "aria-label", "title")
REQUIRED_META = ("og:title", "og:description", "og:image")

# Phrases that must not appear on public root pages.
FORBIDDEN = [
    ("apps.apple.com", re.compile(r"apps\.apple\.com", re.I)),
    ("dollar price", re.compile(r"\$\d")),
    ("euro price", re.compile(r"€\d")),
    ("em dash", re.compile("—")),
]
# Allowed only inside a sentence that also contains "not".
NEGATION_ONLY = [re.compile(r"Identity Center", re.I), re.compile(r"\bSSO\b")]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links = path, set(), []
        self.h1, self.last_level, self.in_title = 0, 0, False
        self.title, self.canonical, self.meta = "", None, {}
        self.chunks = []
        self.text = path.read_text()
        self.feed(self.text)
        self.visible = "".join(self.chunks)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag in BLOCK_TAGS:
            self.chunks.append("\n")

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        self.chunks.append(data)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in BLOCK_TAGS:
            self.chunks.append("\n")
        for key in TEXT_ATTRS:
            if attrs.get(key):
                self.chunks.append("\n" + attrs[key] + "\n")
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f"Duplicate id: {self.path}"
            self.ids.add(attrs["id"])
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key and "content" in attrs:
                self.meta[key] = attrs["content"]
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if len(tag) == 2 and tag[0] == "h" and tag[1] in "123456":
            level = int(tag[1])
            assert level <= self.last_level + 1, f"Heading level skips: {self.path} h{level}"
            self.last_level = level
            if level == 1:
                self.h1 += 1
        if tag == "html":
            assert attrs.get("lang") == "en", f"Missing language: {self.path}"
        if tag == "img":
            assert attrs.get("alt"), f"Missing image description: {self.path}"
            assert attrs.get("width") and attrs.get("height"), "Reserve image space"
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])
        if attrs.get("srcset"):
            for candidate in attrs["srcset"].split(","):
                if candidate.strip():
                    self.links.append(candidate.split()[0])


pages = {path: Page(path) for path in ROOT.glob("*.html") if path.name != "404.html"}
assert len(pages) == 3, "Expected product, support and privacy pages"
for path, page in pages.items():
    assert page.h1 == 1, f"Expected one main heading: {path}"
    assert page.title.strip(), f"Missing title: {path}"
    assert page.meta.get("description", "").strip(), f"Missing meta description: {path}"
    expected = BASE_URL if path.name == "index.html" else BASE_URL + path.name
    assert page.canonical == expected, f"Wrong canonical: {path}: {page.canonical}"
    assert page.meta.get("og:url") == page.canonical, f"og:url differs from canonical: {path}"
    assert page.meta.get("og:image", "").startswith(BASE_URL), f"og:image off-site: {path}"
    for key in REQUIRED_META:
        assert page.meta.get(key, "").strip(), f"Missing {key}: {path}"
    for label, pattern in FORBIDDEN:
        assert not pattern.search(page.text) and not pattern.search(page.visible), f"Forbidden {label}: {path}"
    for sentence in re.split(r"(?<=[.!?])\s+|\n", page.visible):
        for pattern in NEGATION_ONLY:
            if pattern.search(sentence):
                assert re.search(r"\bnot\b", sentence, re.I), f"Unnegated claim '{pattern.pattern}': {path}: {sentence.strip()[:80]}"
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            assert url.scheme == "https", f"Unexpected external link: {link}"
            continue
        assert not url.path.startswith("/"), f"Project-path-unsafe link: {link}"
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        assert target.is_relative_to(ROOT), f"Link leaves site: {link}"
        if target.is_dir():
            target = target / "index.html"
        assert target.is_file(), f"Missing local target: {link}"
        if url.fragment and target in pages:
            assert unquote(url.fragment) in pages[target].ids, f"Missing anchor: {link}"

# The previous site is kept only as a backup and must stay out of search results.
old_pages = sorted((ROOT / "_old").rglob("*.html"))
for path in old_pages:
    assert "noindex" in path.read_text(), f"Backup page missing noindex: {path}"


OLD_HOST = "chrominskyy.github.io"


def check_published_host(root, base):
    """No published file may point at the old github.io project URL."""
    for path in [*root.glob("*.html"), root / "robots.txt", root / "sitemap.xml"]:
        assert OLD_HOST not in path.read_text(), f"Old host {OLD_HOST} in {path.name}"


def check_sitemap(root, base):
    locs = set(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", (root / "sitemap.xml").read_text()))
    expected = {base, base + "support.html", base + "privacy.html"}
    assert locs == expected, f"Sitemap URLs: {sorted(locs)}, expected {sorted(expected)}"


def check_robots(root, base):
    lines = [line.strip() for line in (root / "robots.txt").read_text().splitlines()]
    assert f"Sitemap: {base}sitemap.xml" in lines, "robots.txt must point to this host's sitemap"
    assert not any(line.lower().startswith("disallow") for line in lines), \
        "robots.txt must not Disallow: _old pages rely on a readable noindex"


def check_local_asset(root, base, url, where):
    """An absolute URL on this host must resolve to a file in the repository."""
    if url.startswith(base):
        rel = urlsplit(url).path[len(urlsplit(base).path):] or "index.html"
        assert (root / unquote(rel)).is_file(), f"Missing local file for {url} in {where}"


def check_404(root, base):
    """404.html is served at any depth, so every reference must be absolute."""
    path = root / "404.html"
    assert path.is_file(), "Missing 404.html"
    text = path.read_text()
    assert re.search(r'<meta name="robots" content="noindex">', text), "404.html needs noindex"
    assert '<html lang="en">' in text, "404.html needs lang=en"
    assert len(re.findall(r"<h1[\s>]", text)) == 1, "404.html needs one h1"
    for ref in re.findall(r'(?:href|src)="([^"]*)"', text):
        assert ref.startswith((base, "https://", "#", "data:", "mailto:")), f"Relative reference in 404.html: {ref}"
        check_local_asset(root, base, ref, "404.html")
    page = Page(path)
    for label, pattern in FORBIDDEN:
        assert not pattern.search(page.text) and not pattern.search(page.visible), f"Forbidden {label}: 404.html"
    assert f'href="{base}"' in text, "404.html must link to the home page"


check_published_host(ROOT, BASE_URL)
check_sitemap(ROOT, BASE_URL)
check_robots(ROOT, BASE_URL)
check_404(ROOT, BASE_URL)
for path, page in pages.items():
    check_local_asset(ROOT, BASE_URL, page.meta["og:image"], path.name)


def check_favicon_ico(root):
    """Browsers and crawlers request /favicon.ico by default; serve a real ICO there."""
    path = root / "favicon.ico"
    assert path.is_file(), "Missing favicon.ico in the site root"
    assert path.read_bytes()[:4] == b"\x00\x00\x01\x00", "favicon.ico is not an ICO file"


check_favicon_ico(ROOT)

print(f"Passed (strict): {len(pages)} pages, {len(old_pages)} backup pages, local assets, links, anchors and basic semantics")
