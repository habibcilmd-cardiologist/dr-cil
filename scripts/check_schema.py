import json
import re
from pathlib import Path


def extract_first_jsonld(html: str) -> str:
    match = re.search(
        r"<script[^>]+type=\"application/ld\+json\"[^>]*>([\s\S]*?)</script>",
        html,
        flags=re.IGNORECASE,
    )
    if not match:
        raise SystemExit("No JSON-LD <script type=application/ld+json> found")
    return match.group(1).strip()


def main() -> None:
    page = Path("public/hizmetler/sol-ana-koroner-stent/index.html")
    html = page.read_text(encoding="utf-8")
    raw = extract_first_jsonld(html)
    data = json.loads(raw)

    print("keys:", list(data.keys()))
    graph = data.get("@graph", [])
    print("graph_len:", len(graph))

    types: set[str] = set()
    for node in graph:
        t = node.get("@type")
        if isinstance(t, list):
            types.update(t)
        elif isinstance(t, str):
            types.add(t)

    print("types:")
    for t in sorted(types):
        print("-", t)


if __name__ == "__main__":
    main()
