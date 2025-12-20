from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LinkRef:
    file: str
    line: int
    href: str


MD_LINK_RE = re.compile(r"\]\((/[^)\s]+)\)")


def collect_links(md_path: Path) -> list[LinkRef]:
    links: list[LinkRef] = []
    try:
        txt = md_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        txt = md_path.read_text(encoding="utf-8-sig")

    for idx, line in enumerate(txt.splitlines(), start=1):
        for m in MD_LINK_RE.finditer(line):
            href = m.group(1)
            links.append(LinkRef(file=md_path.as_posix(), line=idx, href=href))
    return links


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit internal links inside service pages")
    parser.add_argument("--content", default="content", help="Path to content root")
    parser.add_argument(
        "--service-glob",
        default="**/services/**.md|**/services/**/index.md|**/hizmetler/**/index.md",
        help="Pipe-separated glob patterns under content root",
    )
    parser.add_argument(
        "--public",
        default="public",
        help="Path to built site output folder (used to verify link targets exist)",
    )
    parser.add_argument(
        "--mode",
        choices=["public", "server"],
        default="public",
        help="public: check targets exist in /public; server: HTTP-check via running hugo server",
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:55444",
        help="Base URL for --mode=server",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="HTTP timeout seconds for --mode=server",
    )
    parser.add_argument(
        "--out",
        default="agent-logs/service-link-audit.json",
        help="Output JSON report path",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    content_root = (repo_root / args.content).resolve()
    public_root = (repo_root / args.public).resolve()
    out_path = (repo_root / args.out).resolve()

    patterns = [p.strip() for p in args.service_glob.split("|") if p.strip()]

    md_files: set[Path] = set()
    for pat in patterns:
        # pathlib.glob() is strict: '**' must be its own path component.
        # Some patterns historically used '**.md' which is invalid on Python 3.12+.
        if pat.endswith("**.md"):
            pat = pat[: -len("**.md")] + "**/*.md"
        md_files.update(content_root.glob(pat))

    all_links: list[LinkRef] = []
    for md in sorted(md_files):
        all_links.extend(collect_links(md))

    def public_target_exists(href: str) -> bool:
        # Map /en/foo/ -> public/en/foo/index.html
        # Map /en/foo -> public/en/foo/index.html
        path = href
        if "?" in path:
            path = path.split("?", 1)[0]
        if "#" in path:
            path = path.split("#", 1)[0]
        if not path.startswith("/"):
            return True
        if path.endswith("/"):
            rel = path.lstrip("/") + "index.html"
        else:
            rel = path.lstrip("/") + "/index.html"
        return (public_root / rel).exists()

    def server_target_ok(href: str) -> tuple[bool, int]:
        path = href
        if "?" in path:
            path = path.split("?", 1)[0]
        if "#" in path:
            path = path.split("#", 1)[0]
        if not path.startswith("/"):
            return True, 200

        url = args.base_url.rstrip("/") + path
        req = urllib.request.Request(url, headers={"User-Agent": "drcil-link-audit/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=args.timeout) as resp:
                status = int(getattr(resp, "status", 200))
                # Treat any 2xx/3xx as OK for link validity.
                return 200 <= status < 400, status
        except urllib.error.HTTPError as e:
            return False, int(getattr(e, "code", 0) or 0)
        except urllib.error.URLError:
            # Connection refused / DNS / etc.
            return False, 0
        except Exception:
            return False, 0

    broken: list[dict] = []
    blog_links: list[dict] = []

    # Probe server once in server mode, fail fast if unreachable.
    if args.mode == "server":
        ok, status = server_target_ok("/")
        if not ok and status == 0:
            raise SystemExit(
                f"Server not reachable at {args.base_url}. Start hugo server first (e.g. hugo server -D --port 55444)."
            )

    for lr in all_links:
        href = lr.href
        if href.startswith("/en/blog/") or href.startswith("/ar/blog/") or href.startswith("/blog/"):
            blog_links.append(lr.__dict__)

        if not href.startswith("/"):
            continue

        if args.mode == "public":
            if not public_target_exists(href):
                broken.append({**lr.__dict__, "status": 404})
        else:
            ok, status = server_target_ok(href)
            if not ok:
                broken.append({**lr.__dict__, "status": status})

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "serviceFiles": len(md_files),
                "linksFound": len(all_links),
                "blogLinksFound": len(blog_links),
                "brokenLinksFound": len(broken),
                "brokenLinks": broken,
                "blogLinks": blog_links,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {out_path}")

    # Non-zero if broken links exist
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
