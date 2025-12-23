import argparse
import json
import re
from pathlib import Path


def extract_first_jsonld(html: str) -> str:
    match = re.search(
        r"<script[^>]+type\s*=\s*(?:\"application/ld\+json\"|'application/ld\+json'|application/ld\+json)[^>]*>([\s\S]*?)</script>",
        html,
        flags=re.IGNORECASE,
    )
    if not match:
        raise SystemExit("No JSON-LD <script type=application/ld+json> found")
    return match.group(1).strip()


def collect_jsonld_scripts(html: str) -> list[str]:
    return [
        m.group(1).strip()
        for m in re.finditer(
            r"<script[^>]+type\s*=\s*(?:\"application/ld\+json\"|'application/ld\+json'|application/ld\+json)[^>]*>([\s\S]*?)</script>",
            html,
            flags=re.IGNORECASE,
        )
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect JSON-LD @graph in a built Hugo HTML page")
    parser.add_argument(
        "page",
        nargs="?",
        default="public/blog/lvad/index.html",
        help="Path to built HTML file (default: public/blog/lvad/index.html)",
    )
    args = parser.parse_args()

    page = Path(args.page)
    html = page.read_text(encoding="utf-8")

    scripts = collect_jsonld_scripts(html)
    if not scripts:
        raise SystemExit("No JSON-LD <script type=application/ld+json> found")

    print("page:", page.as_posix())
    print("jsonld_scripts:", len(scripts))

    total_faq = 0
    all_faq_ids: list[str] = []

    for i, raw in enumerate(scripts, start=1):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"script_{i}: invalid_json ({e})")
            continue

        script_faq = 0
        script_faq_ids: list[str] = []
        type_counts: dict[str, int] = {}

        def add_type(tt: str) -> None:
            nonlocal type_counts
            type_counts[tt] = type_counts.get(tt, 0) + 1

        # Case A: consolidated graph
        graph = data.get("@graph") if isinstance(data, dict) else None
        if isinstance(graph, list):
            for node in graph:
                if not isinstance(node, dict):
                    continue
                t = node.get("@type")
                node_types: list[str]
                if isinstance(t, list):
                    node_types = [x for x in t if isinstance(x, str)]
                elif isinstance(t, str):
                    node_types = [t]
                else:
                    node_types = []

                for tt in node_types:
                    add_type(tt)

                if "FAQPage" in node_types:
                    script_faq += 1
                    node_id = node.get("@id")
                    if isinstance(node_id, str):
                        script_faq_ids.append(node_id)
        # Case B: single node JSON-LD
        elif isinstance(data, dict):
            t = data.get("@type")
            node_types: list[str]
            if isinstance(t, list):
                node_types = [x for x in t if isinstance(x, str)]
            elif isinstance(t, str):
                node_types = [t]
            else:
                node_types = []

            for tt in node_types:
                add_type(tt)

            if "FAQPage" in node_types:
                script_faq += 1
                node_id = data.get("@id")
                if isinstance(node_id, str):
                    script_faq_ids.append(node_id)

        total_faq += script_faq
        all_faq_ids.extend(script_faq_ids)

        graph_len = len(graph) if isinstance(graph, list) else 0
        print(f"script_{i}: graph_len={graph_len} faq_count={script_faq}")
        if script_faq_ids:
            for fid in script_faq_ids:
                print("  faq_id:", fid)

    print("faq_total_across_scripts:", total_faq)
    if all_faq_ids:
        print("faq_ids_all:")
        for fid in all_faq_ids:
            print("-", fid)


if __name__ == "__main__":
    main()
