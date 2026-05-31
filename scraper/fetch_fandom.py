"""Fetch wikitext for every 1% Club page on only-connect-questions.fandom.com.

Uses the MediaWiki API (action=parse&prop=wikitext) which bypasses the
Cloudflare interactive challenge on the regular wiki pages. One file per page,
cached under data/raw/fandom/.

This is a second source: comingsoon.net stays primary for the live build, this
feeds the audit pipeline (parse_fandom.py + audit_fandom.py).
"""
import json
import time
import urllib.parse
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "fandom"
RAW.mkdir(parents=True, exist_ok=True)

API = "https://only-connect-questions.fandom.com/api.php"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Canonical page titles (discovered via action=query&list=allpages&apprefix=1%25_Club).
# 50 pages: S1-S4 regular episodes + 2 Christmas specials + Soccer Aid 2025.
PAGES = [
    "1% Club Christmas 2023",
    "1% Club Christmas 2024",
    "1% Club Soccer Aid 2025",
]
for season, n_eps in [(1, 8), (2, 8), (3, 16), (4, 15)]:
    for ep in range(1, n_eps + 1):
        PAGES.append(f"1% Club Season {season} Episode {ep}")


def slug(title: str) -> str:
    return title.replace(" ", "_").replace("%", "pct").replace("'", "")


def fetch_one(session: requests.Session, title: str) -> str | None:
    params = {
        "action": "parse",
        "page": title,
        "format": "json",
        "prop": "wikitext",
        "redirects": 1,
    }
    r = session.get(API, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        print(f"  api error: {data['error'].get('code')} {data['error'].get('info', '')[:80]}")
        return None
    return data["parse"]["wikitext"]["*"]


def main():
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"})
    ok = skip = fail = 0
    for title in PAGES:
        dest = RAW / f"{slug(title)}.wiki"
        if dest.exists() and dest.stat().st_size > 200:
            print(f"skip  {title}")
            skip += 1
            continue
        print(f"fetch {title} ...", end=" ", flush=True)
        try:
            wt = fetch_one(session, title)
            if wt is None:
                print("missing")
                fail += 1
            else:
                dest.write_text(wt, encoding="utf-8")
                print(f"ok ({len(wt)} bytes)")
                ok += 1
        except Exception as e:
            print(f"FAIL {e}")
            fail += 1
        time.sleep(1.0)
    print(f"\ndone: {ok} fetched, {skip} cached, {fail} failed")


if __name__ == "__main__":
    main()
