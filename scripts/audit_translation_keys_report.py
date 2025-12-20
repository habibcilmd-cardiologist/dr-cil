from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KeyUse:
    key: str
    lang: str
    section: str
    path: str


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
        raw = raw.strip()
        return raw or None
    return None


def infer_lang_and_section(path: Path) -> tuple[str, str]:
    parts = path.parts
    lang = parts[1] if len(parts) > 1 else "?"
    section = parts[2] if len(parts) > 2 else ""
    return lang, section


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    content_root = repo_root / "content"
    out_path = repo_root / "agent-logs" / "translationKey-collisions.json"

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
        uses.append(
            KeyUse(
                key=key,
                lang=lang,
                section=section,
                path=p.relative_to(repo_root).as_posix(),
            )
        )

    by_key: dict[str, list[KeyUse]] = defaultdict(list)
    for u in uses:
        by_key[u.key].append(u)

    collisions = []
    for key, key_uses in by_key.items():
        sections = sorted({u.section for u in key_uses})
        if len(sections) <= 1:
            continue
        collisions.append(
            {
                "translationKey": key,
                "sections": sections,
                "count": len(key_uses),
                "uses": [u.__dict__ for u in sorted(key_uses, key=lambda x: (x.lang, x.section, x.path))],
            }
        )

    collisions.sort(key=lambda c: (-c["count"], c["translationKey"]))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "translationKeyCount": len(by_key),
                "collisionCount": len(collisions),
                "collisions": collisions,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {out_path}")
    return 1 if collisions else 0


if __name__ == "__main__":
    raise SystemExit(main())
