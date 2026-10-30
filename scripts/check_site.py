"""Check the small static site without third-party dependencies.

Usage: python3 scripts/check_site.py
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://chrominskyy.github.io/cloudlatch-site/"
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


pages = {path: Page(path) for path in ROOT.glob("*.html")}
assert len(pages) == 3, "Expected product, support and privacy pages"
for path, page in pages.items():
    assert page.h1 == 1, f"Expected one main heading: {path}"
    assert page.title.strip(), f"Missing title: {path}"
    assert page.meta.get("description", "").strip(), f"Missing meta description: {path}"
    expected = BASE_URL if path.name == "index.html" else BASE_URL + path.name
    assert page.canonical == expected, f"Wrong canonical: {path}: {page.canonical}"
    assert page.meta.get("og:url") == page.canonical, f"og:url differs from canonical: {path}"
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
        assert target.is_file(), f"Missing local target: {link}"
        if url.fragment and target in pages:
            assert unquote(url.fragment) in pages[target].ids, f"Missing anchor: {link}"

# The previous site is kept only as a backup and must stay out of search results.
old_pages = sorted((ROOT / "_old").glob("*.html"))
for path in old_pages:
    assert "noindex" in path.read_text(), f"Backup page missing noindex: {path}"

print(f"Passed (strict): {len(pages)} pages, {len(old_pages)} backup pages, local assets, links, anchors and basic semantics")
