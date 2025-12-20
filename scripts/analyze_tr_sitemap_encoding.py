import re
from pathlib import Path
from urllib.parse import unquote


def main() -> None:
    path = Path(r"D:\PROGRAMMING\drcil\public\tr\sitemap.xml")
    xml = path.read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    enc = [u for u in locs if re.search(r"%[0-9A-Fa-f]{2}", u)]
    enc_tax = [u for u in enc if "/tags/" in u or "/categories/" in u]

    print("encoded_total", len(enc))
    print("encoded_tax", len(enc_tax))

    seen = set()
    for u in enc_tax:
        parts = u.split("/")
        if len(parts) < 5:
            continue
        kind = parts[3]
        seg = parts[4]
        dec = unquote(seg)
        key = (kind, dec)
        if key in seen:
            continue
        seen.add(key)
        print(f"{kind}\t{dec}")


if __name__ == "__main__":
    main()
