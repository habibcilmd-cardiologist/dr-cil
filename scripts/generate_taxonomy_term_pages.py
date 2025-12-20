import json
from pathlib import Path


def write_term_page(base_dir: Path, term: str, slug: str) -> None:
    base_dir.mkdir(parents=True, exist_ok=True)
    # Use a deterministic filename so reruns overwrite the same file.
    filename = f"{slug}.md" if slug else "term.md"
    path = base_dir / filename

    # Title remains human-readable; slug controls URL.
    content = (
        "---\n"
        f'title: "{term}"\n'
        f'slug: "{slug}"\n'
        "---\n"
    )
    path.write_text(content, encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    src = root / "scripts" / "_taxonomy_slug_map_tr.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    mapping = data.get("mapping", {})

    # Hugo multilingual content roots
    tr_root = root / "content" / "tr"

    kind_to_dir = {
        "tags": tr_root / "tags",
        "categories": tr_root / "categories",
    }

    count = 0
    for kind, term_map in mapping.items():
        if kind not in kind_to_dir:
            continue
        out_dir = kind_to_dir[kind]
        for term, slug in term_map.items():
            write_term_page(out_dir, term, slug)
            count += 1

    print(f"Wrote/updated {count} taxonomy term pages under content/tr/")


if __name__ == "__main__":
    main()
