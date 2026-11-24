#!/usr/bin/env python3
"""Targeted whole-output schema regression checks, not an official validator.

Reads the actual HTML and all JSON-LD scripts. It never sends HTTP requests or
claims to validate the complete Schema.org vocabulary or clinical facts.
"""
import argparse
import collections
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


def normalized(value):
    return " ".join(html.unescape(str(value)).split())


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.scripts = []
        self.canonical = ""
        self.alias = False
        self.single = False
        self._ld = None
        self._ignored = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and a.get("http-equiv", "").lower() == "refresh":
            self.alias = True
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonical = a.get("href", "")
        if a.get("id") == "single_header":
            self.single = True
        if tag in {"script", "style", "template"}:
            self._ignored += 1
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._ld = []

    def handle_endtag(self, tag):
        if tag == "script" and self._ld is not None:
            self.scripts.append("".join(self._ld))
            self._ld = None
        if tag in {"script", "style", "template"}:
            self._ignored = max(0, self._ignored - 1)

    def handle_data(self, value):
        if self._ld is not None:
            self._ld.append(value)
        if not self._ignored:
            self.text.append(value)


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def types(node):
    value = node.get("@type", [])
    return [value] if isinstance(value, str) else value if isinstance(value, list) else []


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path, help="Built output directory or one HTML file")
    ap.add_argument("--json", type=Path, help="Optional machine-readable report")
    args = ap.parse_args()
    root = args.path if args.path.is_dir() else None
    files = sorted(args.path.rglob("*.html")) if root else [args.path]
    errors = []
    counts = collections.Counter()
    type_counts = collections.Counter()
    examples = {}

    def fail(file, code, detail):
        errors.append({"file": str(file.relative_to(root)) if root else str(file),
                       "code": code, "detail": detail})

    for file in files:
        counts["html"] += 1
        doc = Document()
        doc.feed(file.read_text(encoding="utf-8"))
        if doc.alias:
            counts["aliases"] += 1
            continue
        if not doc.scripts:
            fail(file, "JSONLD_MISSING", "Non-alias HTML has no JSON-LD")
            continue
        counts["pages_with_jsonld"] += 1
        nodes = []
        top = []
        for script in doc.scripts:
            counts["scripts"] += 1
            try:
                value = json.loads(script)
            except (ValueError, TypeError) as exc:
                fail(file, "JSON_PARSE", str(exc))
                continue
            nodes.extend(walk(value))
            if isinstance(value, dict):
                top.extend(value.get("@graph", [value]))
            elif isinstance(value, list):
                top.extend(value)
        content = normalized(" ".join(doc.text))
        defined = {}
        faq_count = 0
        for node in nodes:
            ts = types(node)
            type_counts.update(ts)
            if node.get("@id") and len(node) > 1:
                entity_id = node["@id"]
                prior = defined.setdefault(entity_id, {})
                for key, value in node.items():
                    if key in prior and prior[key] != value:
                        fail(file, "CONFLICTING_ID", {"id": entity_id, "property": key})
                    prior[key] = value
            if "performer" in node and "Event" not in ts:
                fail(file, "PERFORMER_DOMAIN", {"types": ts})
            if "procedureType" in node:
                allowed = {"https://schema.org/NoninvasiveProcedure", "https://schema.org/PercutaneousProcedure"}
                value = node["procedureType"]
                value = value.get("@id", "") if isinstance(value, dict) else value
                if not isinstance(value, str) or value not in allowed:
                    fail(file, "PROCEDURE_ENUM", node["procedureType"])
            for key in ["lastReviewed", "reviewedBy", "recognizingAuthority", "openingHoursSpecification", "geo", "priceRange"]:
                if key in node:
                    counts["fields_requiring_external_proof:" + key] += 1
            if "Person" in ts and "Physician" in ts:
                fail(file, "PERSON_OFFICE_SEPARATION_POLICY", node.get("@id"))
            if any(t in ts for t in ["Article", "BlogPosting", "MedicalScholarlyArticle"]) and not doc.single:
                fail(file, "ARTICLE_ON_NONARTICLE_TEMPLATE", ts)
            if "BreadcrumbList" in ts:
                counts["breadcrumbs"] += 1
                items = node.get("itemListElement", [])
                if [x.get("position") for x in items] != list(range(1, len(items) + 1)):
                    fail(file, "BREADCRUMB_POSITION", [x.get("position") for x in items])
                for item in items:
                    target = item.get("item", "")
                    target = target.get("@id", target.get("url", "")) if isinstance(target, dict) else target
                    if root and target and not target_exists(root, target):
                        fail(file, "BREADCRUMB_TARGET", target)
            if "ItemList" in ts and not node.get("itemListElement"):
                fail(file, "EMPTY_ITEMLIST", node.get("@id"))
            if "FAQPage" in ts:
                faq_count += 1
                for qa in node.get("mainEntity", []):
                    for label, value in [("question", qa.get("name", "")),
                                         ("answer", qa.get("acceptedAnswer", {}).get("text", ""))]:
                        plain = normalized(re.sub(r"<[^>]*>", " ", str(value)))
                        if not plain or plain not in content:
                            fail(file, "FAQ_NOT_RENDERED", {label: plain[:120]})
            if root and "image" in node:
                images = node["image"] if isinstance(node["image"], list) else [node["image"]]
                for image in images:
                    url = image.get("contentUrl", image.get("url", "")) if isinstance(image, dict) else image
                    if url and urlsplit(str(url)).netloc == urlsplit(doc.canonical).netloc and not target_exists(root, str(url)):
                        fail(file, "IMAGE_TARGET", url)
        if faq_count > 1:
            fail(file, "DUPLICATE_FAQ", faq_count)
        counts["faq_pages"] += int(faq_count > 0)
        page_nodes = [n for n in top if any(t in types(n) for t in ["WebPage", "MedicalWebPage", "ProfilePage", "ContactPage", "CollectionPage"])]
        if len(page_nodes) != 1:
            fail(file, "PAGE_ENTITY_COUNT", len(page_nodes))
        elif page_nodes[0].get("url") != doc.canonical or page_nodes[0].get("@id") != doc.canonical + "#webpage":
            fail(file, "PAGE_CANONICAL_MISMATCH", {"canonical": doc.canonical, "page": page_nodes[0]})
        for n in top:
            for t in types(n):
                if t not in examples:
                    examples[t] = {"file": str(file.relative_to(root)) if root else str(file), "url": doc.canonical}

    result = {"scope": "targeted output regressions; not full vocabulary, official validator, HTTP or clinical truth",
              "input": str(args.path), "counts": dict(counts), "types_including_nested": dict(type_counts),
              "examples": examples, "error_count": len(errors),
              "errors_by_code": dict(collections.Counter(x["code"] for x in errors)), "errors": errors,
              "official_schema_validator": "NOT_RUN", "google_rich_results_test": "NOT_RUN"}
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in {"errors", "examples"}}, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


def target_exists(root, url):
    path = unquote(urlsplit(url).path).lstrip("/")
    target = root / path
    return (target / "index.html").is_file() if path.endswith("/") or not path else target.is_file() or (target / "index.html").is_file()


if __name__ == "__main__":
    main()
