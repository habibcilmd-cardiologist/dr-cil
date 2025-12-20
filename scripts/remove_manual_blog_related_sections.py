#!/usr/bin/env python3
"""Remove manually added 'related' sections at the end of blog posts.

This repo has two different "related" concepts:
1) Theme-driven related cards (Blowfish partial `related.html`) controlled via config.
2) Manually added Markdown sections like:
   - "## Related Cardiology Services"
   - "## İlgili Kardiyoloji Hizmetleri"

This script targets (2) only.

It removes:
  - A heading that matches known variants
  - The following bullet list block (lines starting with '-', '*', or '+')
  - Optional surrounding horizontal rules

Dry-run by default. Use --apply to write changes.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOT = WORKSPACE_ROOT / "content"


HEADING_RE = re.compile(
    r"^##\s*(?:"
    r"Related\s+(?:Cardiology\s+Services|Articles|Valve\s+Treatments)"
    r"|İlgili\s+(?:Kardiyoloji\s+Hizmetleri|Yazılar|Kapak\s+Tedavileri)"
    r")\s*$",
    flags=re.IGNORECASE,
)

BULLET_RE = re.compile(r"^\s*[-*+]\s+")
HR_RE = re.compile(r"^\s*(?:---|\*\*\*|___)\s*$")


@dataclass
class Change:
    path: Path
    removed_blocks: int


def _iter_blog_posts() -> list[Path]:
    posts: list[Path] = []
    for md in CONTENT_ROOT.glob("**/blog/**/index.md"):
        if md.name != "index.md":
            continue
        posts.append(md)
    return sorted(posts)


def _remove_block(lines: list[str], heading_idx: int) -> list[str]:
    """Remove the heading + following bullet list block, with optional HRs."""

    start = heading_idx

    # Optionally remove an HR and blank lines immediately above the heading.
    while start > 0 and lines[start - 1].strip() == "":
        start -= 1
    if start > 0 and HR_RE.match(lines[start - 1]):
        start -= 1
        while start > 0 and lines[start - 1].strip() == "":
            start -= 1

    end = heading_idx + 1

    # Consume blank lines after heading
    while end < len(lines) and lines[end].strip() == "":
        end += 1

    # Consume bullet list (allow blank lines inside once bullets started)
    bullet_seen = False
    while end < len(lines) and (BULLET_RE.match(lines[end]) or (bullet_seen and lines[end].strip() == "")):
        if BULLET_RE.match(lines[end]):
            bullet_seen = True
        end += 1

    # Optionally consume trailing blank lines + HR
    end2 = end
    while end2 < len(lines) and lines[end2].strip() == "":
        end2 += 1
    if end2 < len(lines) and HR_RE.match(lines[end2]):
        end2 += 1
        while end2 < len(lines) and lines[end2].strip() == "":
            end2 += 1

    return lines[:start] + lines[end2:]


def process_file(path: Path) -> tuple[Change, str] | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    removed = 0

    idx = 0
    while idx < len(lines):
        if HEADING_RE.match(lines[idx]):
            lines = _remove_block(lines, idx)
            removed += 1
            idx = max(0, idx - 2)
            continue
        idx += 1

    if removed == 0:
        return None

    new_text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return Change(path=path, removed_blocks=removed), new_text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    changed_files = 0
    removed_blocks = 0

    for md_path in _iter_blog_posts():
        result = process_file(md_path)
        if not result:
            continue
        change, new_text = result
        changed_files += 1
        removed_blocks += change.removed_blocks
        rel = md_path.relative_to(WORKSPACE_ROOT)
        print(f"{rel}: removed {change.removed_blocks} related section(s)")
        if args.apply:
            md_path.write_text(new_text, encoding="utf-8")

    print(f"Changed files: {changed_files}")
    print(f"Removed blocks: {removed_blocks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
