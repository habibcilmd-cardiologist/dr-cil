from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KeyUse:
    key: str
    lang: str
    section: str
    path: Path


FM_DELIM_RE = re.compile(r"^---\s*$")
KEY_RE = re.compile(r"^\s*translationKey\s*:\s*(.+?)\s*$")


def iter_front_matter_lines(md_text: str) -> list[str] | None:
    lines = md_text.splitlines()
    if not lines or not FM_DELIM_RE.match(lines[0]):
        return None

    end = None
    for i in range(1, min(len(lines), 600)):
        if FM_DELIM_RE.match(lines[i]):
            end = i
            break
    if end is None:
        return None

    return lines[1:end]


def parse_translation_key(front_matter_lines: list[str]) -> str | None:
    for line in front_matter_lines:
        m = KEY_RE.match(line)
        if not m:
            continue
        raw = m.group(1).strip()
        if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
            raw = raw[1:-1]
        return raw.strip() or None
    return None


def infer_lang_and_section(path: Path) -> tuple[str, str]:
    parts = path.parts
    # content/<lang>/...
    lang = parts[1] if len(parts) > 1 else "?"
    section = parts[2] if len(parts) > 2 else ""
    return lang, section


def load_uses(content_root: Path) -> list[KeyUse]:
    uses: list[KeyUse] = []
    for p in content_root.rglob("*.md"):
        try:
            txt = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            txt = p.read_text(encoding="utf-8-sig")

        fm_lines = iter_front_matter_lines(txt)
        if not fm_lines:
            continue
        key = parse_translation_key(fm_lines)
        if not key:
            continue

        lang, section = infer_lang_and_section(p)
        uses.append(KeyUse(key=key, lang=lang, section=section, path=p))

    return uses


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit translationKey collisions in Hugo content")
    parser.add_argument("--root", default="content", help="content root folder")
    parser.add_argument("--max", type=int, default=200, help="max collisions to print")
    args = parser.parse_args()

    content_root = Path(args.root)
    if not content_root.exists():
        print(f"ERROR: content root not found: {content_root}")
        return 2

    uses = load_uses(content_root)
    by_key: dict[str, list[KeyUse]] = defaultdict(list)
    for u in uses:
        by_key[u.key].append(u)

    collisions: list[tuple[str, list[KeyUse], set[str]]] = []
    for key, key_uses in by_key.items():
        sections = {u.section for u in key_uses}
        if len(sections) <= 1:
            continue
        collisions.append((key, key_uses, sections))

    collisions.sort(key=lambda x: (-len(x[1]), x[0]))

    print(f"Found {len(by_key)} translationKey values.")
    print(f"Found {len(collisions)} cross-section translationKey collisions.")

    for idx, (key, key_uses, _sections) in enumerate(collisions[: args.max], start=1):
        print(f"\n{idx}. translationKey={key} ({len(key_uses)} files)")
        for u in sorted(key_uses, key=lambda k: (k.lang, k.section, k.path.as_posix())):
            rel = u.path.as_posix()
            print(f"   - {u.lang:2s}  {u.section:14s}  {rel}")

    if len(collisions) > args.max:
        print(f"\n... plus {len(collisions) - args.max} more")

    # Exit with 1 if collisions exist so it can be used in CI
    return 1 if collisions else 0


if __name__ == "__main__":
    raise SystemExit(main())
