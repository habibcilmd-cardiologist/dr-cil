"""Reproduce this audit's local content evidence; never modifies application files."""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.forms = []
        self.canonical = ""
        self.jsonld = []
        self.ld = False
        self.buf = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "form":
            self.forms.append(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href", "")
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.ld, self.buf = True, []

    def handle_data(self, data):
        if self.ld:
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.ld:
            try:
                self.jsonld.append(json.loads("".join(self.buf)))
            except ValueError:
                pass
            self.ld = False


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--build-root", default="/tmp/dr-cil-audit-2026-11-24/public")
    args = args.parse_args()
    build = Path(args.build_root)
    repo = Path(__file__).resolve().parents[5]
    paths = [
        "index.html", "hakkimda/index.html", "en/about/index.html", "ar/about/index.html",
        "iletisim/index.html", "en/contact/index.html", "ar/contact/index.html",
        "yayinlar/index.html", "hizmetler/index.html",
        "hizmetler/dizalti-damar-tikanikligi/index.html", "hizmetler/periferik-damar/index.html",
        "blog/diyabetik-ayak/index.html", "blog/periferik-arter-hastaligi/index.html",
        "blog/koroner-anjiyoplasti/index.html", "hizmetler/anjiyoplasti/index.html",
    ]
    targets = {
        "/hizmetler/dizalti-damar-tikanikligi/", "/hizmetler/periferik-damar/",
        "/blog/diyabetik-ayak/", "/blog/periferik-arter-hastaligi/",
    }
    pages = {}
    for name in paths:
        page = Page()
        page.feed((build / name).read_text())
        links = {
            href for href in page.links
            if urlsplit(href).netloc in {"", "docdrhabibcil.com"}
            and urlsplit(href).path in targets
        }
        info = {"canonical": page.canonical, "forms": page.forms,
                "target_links": sorted(links), "clinic_hours": []}
        for script in page.jsonld:
            for node in script.get("@graph", []) if isinstance(script, dict) else []:
                if isinstance(node, dict) and node.get("@type") == "MedicalBusiness":
                    info["clinic_hours"] = node.get("openingHoursSpecification", [])
        pages[name] = info
    sources = [
        "content/tr/blog/diyabetik-ayak/index.md",
        "content/tr/blog/periferik-arter-hastaligi/index.md",
        "content/tr/hizmetler/dizalti-damar-tikanikligi/index.md",
        "content/tr/hizmetler/periferik-damar/index.md",
    ]
    metrics = {}
    for name in sources:
        source = (repo / name).read_text()
        lines = list(enumerate(source.splitlines(), 1))
        excerpt = lambda condition: [{"line": n, "text": text} for n, text in lines if condition(text)]
        metrics[name] = {
            "lines": len(lines), "http_urls": re.findall(r"https?://[^\s)<>]+", source),
            "reference_headings": excerpt(lambda text: re.match(r"^#+\s+(Kaynak|Referans)", text, re.I)),
            "percentage_lines": excerpt(lambda text: re.search(r"%\s*\d|\d\s*%", text)),
            "related_source_links": excerpt(lambda text: "relref" in text or re.search(r"/(?:hizmetler|blog)/", text)),
        }
    source = (repo / "content/tr/yayinlar/_index.md").read_text()
    counts = {
        section.splitlines()[0]: len(re.findall(r"(?m)^\d+\. ", section))
        for section in re.split(r"(?m)^## ", source)
        if section[:2] in {"A.", "B.", "C.", "D.", "E."}
    }
    data = {
        "date": "2026-11-24", "build_root": str(build),
        "scope": "Static source and rendered production output only; HTTP/live profiles/clinical truth not tested",
        "pages": pages, "source_metrics": metrics, "publication_list_counts": counts,
        "publication_list_total": sum(counts.values()),
        "publication_doi_tokens": len(re.findall(r"\bDOI\s*:", source, re.I)),
    }
    destination = Path(__file__).with_name("recheck-content-evidence.json")
    destination.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print("Wrote", destination, "; pages:", len(pages), "; publication entries:", sum(counts.values()))


if __name__ == "__main__":
    main()
