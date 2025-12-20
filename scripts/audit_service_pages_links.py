from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


FM_DELIM_RE = re.compile(r"^---\s*$")
KEY_RE = re.compile(r"^\s*translationKey\s*:\s*(.+?)\s*$")


@dataclass(frozen=True)
class ServicePage:
    lang: str
    translation_key: str | None
    slug: str
    source_path: str

    @property
    def expected_path(self) -> str:
        if self.lang == "tr":
            return f"/hizmetler/{self.slug}/"
        if self.lang == "en":
            return f"/en/services/{self.slug}/"
        if self.lang == "ar":
            return f"/ar/services/{self.slug}/"
        return f"/{self.lang}/services/{self.slug}/"


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def _iter_front_matter_lines(md_text: str) -> list[str] | None:
    lines = md_text.splitlines()
    if not lines or not FM_DELIM_RE.match(lines[0]):
        return None

    end = None
    for i in range(1, min(len(lines), 800)):
        if FM_DELIM_RE.match(lines[i]):
            end = i
            break
    if end is None:
        return None

    return lines[1:end]


def _parse_translation_key(front_matter_lines: list[str]) -> str | None:
    for line in front_matter_lines:
        m = KEY_RE.match(line)
        if not m:
            continue
        raw = m.group(1).strip()
        if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
            raw = raw[1:-1]
        raw = raw.strip()
        return raw or None
    return None


def iter_service_pages(repo_root: Path) -> list[ServicePage]:
    specs: list[tuple[str, str]] = [
        ("tr", "content/tr/hizmetler/**/index.md"),
        ("en", "content/en/services/**/index.md"),
        ("ar", "content/ar/services/**/index.md"),
    ]

    pages: list[ServicePage] = []
    for lang, pattern in specs:
        for md_path in sorted(repo_root.glob(pattern)):
            if md_path.name != "index.md":
                continue
            if md_path.parent.name == "_index":
                continue
            if md_path.parent.name == "_index.md":
                continue
            if md_path.name == "_index.md":
                continue

            slug = md_path.parent.name
            txt = _read_text(md_path)
            fm_lines = _iter_front_matter_lines(txt)
            translation_key = _parse_translation_key(fm_lines) if fm_lines else None

            pages.append(
                ServicePage(
                    lang=lang,
                    translation_key=translation_key,
                    slug=slug,
                    source_path=md_path.as_posix(),
                )
            )

    return pages


def normalize_base_url(base_url: str) -> str:
    base_url = base_url.strip()
    if not base_url:
        raise ValueError("base_url must not be empty")
    if not (base_url.startswith("http://") or base_url.startswith("https://")):
        raise ValueError("base_url must start with http:// or https://")
    return base_url.rstrip("/")


def normalize_href_to_path(href: str) -> str | None:
    """Return a normalized site-relative path like '/en/foo/' or None to skip."""
    href = href.strip()
    if not href:
        return None

    lowered = href.lower()
    if lowered.startswith("mailto:") or lowered.startswith("tel:") or lowered.startswith("javascript:"):
        return None

    # Absolute URL? Convert to path if possible.
    if lowered.startswith("http://") or lowered.startswith("https://"):
        parsed = urllib.parse.urlsplit(href)
        if not parsed.path:
            return None
        path = parsed.path
    else:
        path = href

    if not path.startswith("/"):
        # Not site-relative.
        return None

    # Strip query and fragment if present in the original href.
    path = urllib.parse.urlsplit(path).path
    if not path.startswith("/"):
        return None

    return path


def urljoin_base(base_url: str, path: str) -> str:
    return urllib.parse.urljoin(base_url + "/", path.lstrip("/"))


def fetch_url(url: str, timeout_sec: float) -> tuple[int | None, str | None, str | None]:
    """Return (status_code, content_type, body_text_or_none)."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "drcil-link-auditor/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            status = getattr(resp, "status", None) or resp.getcode()
            content_type = resp.headers.get("Content-Type")
            raw = resp.read()

        # Best-effort decode.
        body = None
        if raw:
            body = raw.decode("utf-8", errors="replace")

        return status, content_type, body

    except urllib.error.HTTPError as e:
        # HTTPError is also a valid response with non-2xx code.
        return int(getattr(e, "code", 0) or 0), e.headers.get("Content-Type"), None
    except Exception as e:  # noqa: BLE001
        return None, None, f"{type(e).__name__}: {e}"


A_HREF_RE = re.compile(r"<a\s+[^>]*?href=(?:\"([^\"]+)\"|'([^']+)'|([^\s>]+))", re.IGNORECASE)


def iter_internal_link_paths(html: str) -> Iterable[str]:
    for m in A_HREF_RE.finditer(html):
        href = m.group(1) or m.group(2) or m.group(3) or ""
        path = normalize_href_to_path(href)
        if path:
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit broken internal links on Hugo service pages by crawling a running hugo server. "
            "Outputs JSON report to stdout."
        )
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:55444",
        help="Base URL of running hugo server (default: http://localhost:55444)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="HTTP request timeout in seconds (default: 10)",
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Also write JSON report to scripts/reports/service_link_audit.json",
    )
    parser.add_argument(
        "--report-path",
        default="scripts/reports/service_link_audit.json",
        help="Path to write report if --write-report is set",
    )
    parser.add_argument(
        "--max-links-per-page",
        type=int,
        default=0,
        help="Optional cap for internal links checked per page (0 = no cap)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    base_url = normalize_base_url(args.base_url)

    pages = iter_service_pages(repo_root)

    # Precompute expected absolute URLs.
    page_entries: list[dict] = []
    for p in pages:
        page_entries.append(
            {
                "lang": p.lang,
                "translationKey": p.translation_key,
                "slug": p.slug,
                "sourcePath": p.source_path,
                "expectedPath": p.expected_path,
                "pageUrl": urljoin_base(base_url, p.expected_path),
            }
        )

    checked_urls: dict[str, dict] = {}

    def check_url(url: str) -> dict:
        if url in checked_urls:
            return checked_urls[url]
        status, _ct, err = fetch_url(url, timeout_sec=args.timeout)
        result = {"url": url, "status": status, "error": err}
        checked_urls[url] = result
        return result

    results: list[dict] = []

    for entry in page_entries:
        page_url = entry["pageUrl"]
        status, content_type, body_or_err = fetch_url(page_url, timeout_sec=args.timeout)

        page_result: dict = {
            "page": entry,
            "fetch": {
                "status": status,
                "contentType": content_type,
                "error": None,
            },
            "internalLinksFound": 0,
            "internalLinksChecked": 0,
            "brokenInternalLinks": [],
        }

        if status != 200 or body_or_err is None:
            page_result["fetch"]["error"] = body_or_err if isinstance(body_or_err, str) else None
            results.append(page_result)
            continue

        internal_paths = list(dict.fromkeys(iter_internal_link_paths(body_or_err)))
        page_result["internalLinksFound"] = len(internal_paths)

        if args.max_links_per_page and args.max_links_per_page > 0:
            internal_paths = internal_paths[: args.max_links_per_page]

        broken: list[dict] = []
        for path in internal_paths:
            link_url = urljoin_base(base_url, path)
            link_check = check_url(link_url)
            page_result["internalLinksChecked"] += 1
            if link_check.get("status") != 200:
                broken.append(
                    {
                        "href": path,
                        "url": link_url,
                        "status": link_check.get("status"),
                        "error": link_check.get("error"),
                    }
                )

        page_result["brokenInternalLinks"] = broken
        results.append(page_result)

    report = {
        "baseUrl": base_url,
        "servicePages": len(page_entries),
        "uniqueInternalUrlsChecked": len(checked_urls),
        "pages": results,
        "summary": {
            "pagesNon200": sum(1 for r in results if (r.get("fetch") or {}).get("status") != 200),
            "pagesWithBrokenLinks": sum(1 for r in results if r.get("brokenInternalLinks")),
            "brokenLinksTotal": sum(len(r.get("brokenInternalLinks") or []) for r in results),
        },
    }

    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")

    if args.write_report:
        out_path = (repo_root / args.report_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Exit non-zero if any broken links found or service pages fail.
    has_failures = report["summary"]["pagesNon200"] > 0 or report["summary"]["brokenLinksTotal"] > 0
    return 1 if has_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
