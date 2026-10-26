"""Check the small static site without third-party dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links = path, set(), []
        self.h1 = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f"Duplicate id: {self.path}"
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "html":
            assert attrs.get("lang") == "en", f"Missing language: {self.path}"
        if tag == "img":
            assert attrs.get("alt"), f"Missing image description: {self.path}"
            assert attrs.get("width") and attrs.get("height"), "Reserve image space"
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])


pages = {path: Page(path) for path in ROOT.glob("*.html")}
assert len(pages) == 3, "Expected product, support and privacy pages"
for path, page in pages.items():
    assert page.h1 == 1, f"Expected one main heading: {path}"
    assert "—" not in path.read_text(), f"Unexpected em dash: {path}"
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
print(f"Passed: {len(pages)} pages, local assets, links, anchors and basic semantics")
