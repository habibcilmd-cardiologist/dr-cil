#!/usr/bin/env python3
"""Check shared navigation/dialog contracts in a production Hugo output.

This checks rendered HTML semantics, not computed layout, focus behavior or WCAG.
"""
import argparse
import collections
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = collections.defaultdict(list)
        self.labels = []
        self.language = ""
        self.refresh = False
        self.links = []
        self.main_links = []
        self.in_main = False
        self.h1 = []
        self.in_h1 = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        attrs["tag"] = tag
        if attrs.get("id"):
            self.ids[attrs["id"]].append(attrs)
        if tag == "main":
            self.in_main = True
        if tag == "html":
            self.language = attrs.get("lang", "").split("-")[0]
        if tag == "label":
            self.labels.append(attrs.get("for"))
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.refresh = True
        if tag == "a":
            self.links.append(attrs.get("href", ""))
            if self.in_main:
                self.main_links.append(attrs.get("href", ""))
        if tag == "h1":
            self.in_h1 = True

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
        if tag == "main":
            self.in_main = False

    def handle_data(self, data):
        if self.in_h1:
            self.h1.append(data)


def check(root):
    errors = []
    tested = 0
    aliases = 0
    for file in sorted(root.rglob("*.html")):
        page = Page()
        page.feed(file.read_text(encoding="utf-8"))
        if page.refresh:
            aliases += 1
            continue
        tested += 1
        route = file.relative_to(root).as_posix()

        def require(condition, message):
            if not condition:
                errors.append({"file": route, "issue": message})

        def element(name):
            matches = page.ids[name]
            require(len(matches) == 1, f"Expected one #{name}; got {len(matches)}")
            return matches[0] if matches else {}

        opener = element("menu-button")
        require(opener.get("tag") == "button" and opener.get("type") == "button", "Mobile opener must be a native non-submit button")
        require(opener.get("aria-expanded") == "false" and opener.get("aria-controls") == "menu-wrapper", "Mobile opener state/control association")
        require(bool(opener.get("aria-label")), "Mobile opener needs an accessible name")
        closer = element("menu-close-button")
        require(closer.get("tag") == "button" and bool(closer.get("aria-label")), "Mobile closer must be a named button")
        menu = element("menu-wrapper")
        require(menu.get("role") == "dialog" and menu.get("aria-modal") == "true" and "hidden" in menu, "Mobile dialog must start hidden")
        require(bool(page.ids[menu.get("aria-labelledby")]), "Mobile dialog title must exist")

        wrapper = element("search-wrapper")
        require("hidden" in wrapper, "Search must start hidden")
        require(all(wrapper.get("data-" + key) for key in ["loading", "error", "empty", "count"]), "Search requires localized state text")
        modal = element("search-modal")
        require(modal.get("role") == "dialog" and modal.get("aria-modal") == "true", "Search dialog semantics")
        require(bool(page.ids[modal.get("aria-labelledby")]), "Search dialog title must exist")
        element("search-query")
        require("search-query" in page.labels, "Search input requires a real associated label")
        require(element("search-status").get("role") == "status", "Search feedback must be a live status")

        appointment = element("appointment-button")
        require(appointment.get("tag") == "a", "Appointment opener needs a real navigation fallback")
        contact_path = "/iletisim/" if page.language == "tr" else f"/{page.language}/contact/"
        require(urlsplit(appointment.get("href", "")).path == contact_path, "Appointment fallback must preserve the page language")

        if route.endswith("404.html"):
            home = "/" if page.language == "tr" else f"/{page.language}/"
            require(home in page.main_links and contact_path in page.main_links, "404 main recovery links must preserve the page language")
            if page.language == "ar":
                require(any("\u0600" <= c <= "\u06ff" for c in "".join(page.h1)), "Arabic 404 heading must be Arabic")

    return {"html_tested": tested, "aliases_skipped": aliases, "errors": errors,
            "scope": "Rendered HTML contract only; browser layout/focus/keyboard/contrast/native zoom are separate tests"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check(args.root)
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({"html_tested": result["html_tested"], "aliases_skipped": result["aliases_skipped"], "error_count": len(result["errors"])}, ensure_ascii=False))
    raise SystemExit(1 if result["errors"] else 0)
