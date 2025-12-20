import json
import re
from pathlib import Path

# Turkish-aware ASCII slugifier (URL-safe)
TR_MAP = str.maketrans(
    {
        "ç": "c",
        "Ç": "c",
        "ğ": "g",
        "Ğ": "g",
        "ı": "i",
        "İ": "i",
        "ö": "o",
        "Ö": "o",
        "ş": "s",
        "Ş": "s",
        "ü": "u",
        "Ü": "u",
    }
)


def slugify_tr(text: str) -> str:
    # Preserve hyphen-separated words but normalize everything to ASCII.
    text = (text or "").strip().translate(TR_MAP).lower()
    # Any non alnum becomes '-'
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    src = root / "scripts" / "_encoded_tr_taxonomy_terms.json"
    if not src.exists():
        raise SystemExit(f"Missing {src}. Run the extraction step first.")

    items = json.loads(src.read_text(encoding="utf-8"))

    mapping = {}
    collisions = {}

    for item in items:
        kind = item["kind"]
        term = item["term"]
        slug = slugify_tr(term)
        mapping.setdefault(kind, {})
        if slug in mapping[kind].values():
            collisions.setdefault(kind, []).append({"term": term, "slug": slug})
        mapping[kind][term] = slug

    out = root / "scripts" / "_taxonomy_slug_map_tr.json"
    out.write_text(json.dumps({"mapping": mapping, "collisions": collisions}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out} ({sum(len(v) for v in mapping.values())} mappings)")
    if any(collisions.values()):
        print("WARNING: collisions detected:")
        print(json.dumps(collisions, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
