import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

NS = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xhtml": "http://www.w3.org/1999/xhtml",
}

DEFAULT_FILES = [
    Path("public/sitemap.xml"),
    Path("public/en/sitemap.xml"),
    Path("public/ar/sitemap.xml"),
]


def infer_lang_from_loc(loc: str) -> str:
    if "/en/" in loc:
        return "en"
    if "/ar/" in loc:
        return "ar"
    return "tr"


def validate_file(path: Path) -> list[str]:
    problems: list[str] = []
    if not path.exists():
        return [f"MISSING: {path}"]

    tree = ET.parse(path)
    root = tree.getroot()

    for url_el in root.findall("sm:url", NS):
        loc_el = url_el.find("sm:loc", NS)
        if loc_el is None or not (loc_el.text or "").strip():
            problems.append(f"{path}: url without <loc>")
            continue
        loc = (loc_el.text or "").strip()
        page_lang = infer_lang_from_loc(loc)

        alts = url_el.findall("xhtml:link", NS)
        hreflang_to_hrefs: dict[str, set[str]] = defaultdict(set)
        for a in alts:
            hl = (a.attrib.get("hreflang") or "").strip()
            href = (a.attrib.get("href") or "").strip()
            if not hl or not href:
                continue
            hreflang_to_hrefs[hl].add(href)

        for hl, hrefs in hreflang_to_hrefs.items():
            if len(hrefs) > 1:
                problems.append(
                    f"{path}: DUP hreflang={hl} for loc={loc} -> {sorted(hrefs)}"
                )

        # Lightweight leakage heuristic: EN loc should not point to /tags or /categories without /en/
        if page_lang == "en":
            for hl, hrefs in hreflang_to_hrefs.items():
                for href in hrefs:
                    if (
                        ("/tags/" in href or "/categories/" in href)
                        and "/en/" not in href
                        and "drcil" in href
                    ):
                        problems.append(
                            f"{path}: EN loc has taxonomy alternate without /en/: loc={loc} href={href}"
                        )

    return problems


def main() -> int:
    args = [Path(a) for a in sys.argv[1:]]
    paths = args if args else DEFAULT_FILES

    all_problems: list[str] = []
    for p in paths:
        all_problems.extend(validate_file(p))

    if all_problems:
        print("SITEMAP VALIDATION: FAIL")
        for pr in all_problems[:200]:
            print(pr)
        if len(all_problems) > 200:
            print(f"... plus {len(all_problems) - 200} more")
        return 1

    print("SITEMAP VALIDATION: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
