#!/usr/bin/env python3
"""Fix hardcoded blog links inside service pages to the blog's real permalinks.

Rules (per language):
1) If a service page links to a blog slug and that blog exists in the same language, rewrite the href to the blog's canonical permalink
    as computed by `hugo list all`.
2) If a service page links to a blog slug but a service counterpart exists, rewrite to the service URL.
    (Keep a small allowlist of legacy blog slugs that should point to a service.)

Dry-run by default. Use --apply to write changes.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit


FM_KEY_RE = re.compile(r"^\s*(url)\s*:\s*(.+?)\s*$")


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]

CONTENT_ROOT = WORKSPACE_ROOT / "content"

LANG_CFG = {
    "en": {
        "services": CONTENT_ROOT / "en" / "services",
        "blog": CONTENT_ROOT / "en" / "blog",
        "service_url_prefix": "/en/services/",
    },
    "tr": {
        "services": CONTENT_ROOT / "tr" / "hizmetler",
        "blog": CONTENT_ROOT / "tr" / "blog",
        "service_url_prefix": "/hizmetler/",
    },
    "ar": {
        "services": CONTENT_ROOT / "ar" / "services",
        "blog": CONTENT_ROOT / "ar" / "blog",
        "service_url_prefix": "/ar/services/",
    },
}


ALLOWLIST_MAP = {
    # Legacy blog slugs that should point to services (mostly EN).
    "coronary-angioplasty": "angioplasty",
    "cardiac-angiography": "angiography",
}


BLOG_LINK_RE = re.compile(r"\(((?:/en|/ar)?/blog/([^)/\s]+))/?\)")


def _service_slugs(services_root: Path) -> set[str]:
    slugs: set[str] = set()
    for md_path in services_root.glob("**/index.md"):
        if md_path.parent.name == "_index.md":
            continue
        slugs.add(md_path.parent.name)
    return slugs


def _read_front_matter_url(md_path: Path) -> str | None:
    """Best-effort: read `url:` from YAML front matter."""
    try:
        text = md_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = md_path.read_text(encoding="utf-8-sig")

    lines = text.splitlines()
    if not lines or not lines[0].strip().startswith("---"):
        return None
    for line in lines[1:300]:
        if line.strip().startswith("---"):
            break
        m = FM_KEY_RE.match(line)
        if not m:
            continue
        raw = m.group(2).strip()
        if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
            raw = raw[1:-1]
        raw = raw.strip()
        if raw:
            return raw
    return None


def _blog_slug_to_canonical_url(lang: str, blog_root: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    if not blog_root.exists():
        return mapping

    # Use Hugo itself to compute canonical permalinks (handles slug/title/ugly paths).
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    proc = subprocess.run(
        ["hugo", "list", "all"],
        cwd=str(WORKSPACE_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=env,
    )
    if proc.returncode == 0 and proc.stdout:
        for line in proc.stdout.splitlines():
            if ",blog" not in line:
                continue
            parts = line.split(",")
            if not parts:
                continue
            rel = parts[0].strip().replace("\\", "/")
            if not rel.startswith(f"content/{lang}/blog/"):
                continue
            if not rel.endswith("/index.md"):
                continue
            folder = rel.split("/")[-2]
            url = parts[7].strip() if len(parts) > 7 else ""
            if not url:
                continue
            # url in list output is absolute (baseURL + lang); normalize to path.
            path = urlsplit(url).path
            if path:
                mapping[folder] = path

        if mapping:
            return mapping

    # Fallback: infer by front matter; less accurate than hugo list.
    for md_path in blog_root.glob("**/index.md"):
        # Hugo uses folder name as slug by default, but may be overridden.
        folder = md_path.parent.name
        slug = folder
        try:
            text = md_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = md_path.read_text(encoding="utf-8-sig")
        m = re.search(r"^\s*slug\s*:\s*(.+?)\s*$", text, flags=re.MULTILINE)
        if m:
            raw = m.group(1).strip()
            if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
                raw = raw[1:-1]
            raw = raw.strip()
            if raw:
                slug = raw

        # EN permalinks are configured as /blog/:slug/ but may include /en prefix depending on build.
        url = f"/blog/{slug}/"
        fm_url = _read_front_matter_url(md_path)
        if fm_url and fm_url.startswith("/"):
            url = fm_url
        # Map both folder name and resolved slug to the same canonical URL to support legacy links.
        mapping[folder] = url
        mapping[slug] = url
    return mapping


def _rewrite_text(text: str, service_slugs: set[str], blog_map: dict[str, str]) -> tuple[str, int]:
    rewrites = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal rewrites
        full = match.group(0)
        blog_slug = match.group(2)

        # Prefer real EN blog permalinks when the blog exists.
        if blog_slug in blog_map:
            rewrites += 1
            return full.replace(match.group(1), blog_map[blog_slug].rstrip("/"))

        # Otherwise, fall back to service mapping only when it exists.
        target_slug = None
        if blog_slug in service_slugs:
            target_slug = blog_slug
        else:
            mapped = ALLOWLIST_MAP.get(blog_slug)
            if mapped and mapped in service_slugs:
                target_slug = mapped

        if target_slug:
            # The caller will have passed service_slugs for the target language and will rewrite
            # the prefix appropriately in a second pass.
            rewrites += 1
            return full.replace(match.group(1), f"__SERVICE__/{target_slug}")

        return full

    new_text = BLOG_LINK_RE.sub(repl, text)
    return new_text, rewrites


def _apply_service_prefix(text: str, prefix: str) -> str:
    return text.replace("__SERVICE__/", prefix)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--langs", default="en,tr,ar")
    args = parser.parse_args()

    langs = [x.strip() for x in (args.langs or "").split(",") if x.strip()]
    changed_files = 0
    total_rewrites = 0

    for lang in langs:
        cfg = LANG_CFG.get(lang)
        if not cfg:
            print(f"Unknown lang: {lang}")
            return 2

        services_root: Path = cfg["services"]
        blog_root: Path = cfg["blog"]
        service_prefix: str = cfg["service_url_prefix"]

        if not services_root.exists():
            print(f"Missing services root for {lang}: {services_root}")
            continue

        service_slugs = _service_slugs(services_root)
        blog_map = _blog_slug_to_canonical_url(lang, blog_root)

        for md_path in sorted(services_root.glob("**/index.md")):
            if md_path.parent.name == "_index.md":
                continue
            original = md_path.read_text(encoding="utf-8")
            updated, rewrites = _rewrite_text(original, service_slugs, blog_map)
            if rewrites:
                updated = _apply_service_prefix(updated, service_prefix)
                total_rewrites += rewrites
                changed_files += 1
                print(f"{md_path.relative_to(WORKSPACE_ROOT)}: {rewrites} rewrite(s)")
                if args.apply:
                    md_path.write_text(updated, encoding="utf-8")

    print(f"Changed files: {changed_files}")
    print(f"Total rewrites: {total_rewrites}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
