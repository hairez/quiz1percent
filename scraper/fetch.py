"""Fetch raw HTML from primary 1% Club question sources."""
import time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

SOURCES = [
    ("uk-s4", "https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025"),
    ("uk-s5", "https://www.comingsoon.net/guides/features/2041778-1-percent-club-uk-questions-answers-season-5-2025-solutions-series-five"),
    ("us-s1", "https://www.comingsoon.net/guides/features/1788741-1-percent-club-questions-answers-tonight-last-night-tv-show"),
    ("us-s2", "https://www.comingsoon.net/guides/features/1987178-1-percent-club-questions-answers-season-2-2025-solutions-joel-mchale"),
    ("tvguide-hardest", "https://www.tvguide.co.uk/articles/the-1-club-hardest-questions/"),
]


def main():
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"})
    for slug, url in SOURCES:
        dest = RAW / f"{slug}.html"
        if dest.exists() and dest.stat().st_size > 5000:
            print(f"skip  {slug} (already cached, {dest.stat().st_size} bytes)")
            continue
        print(f"fetch {slug} ...", end=" ", flush=True)
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            dest.write_text(r.text, encoding="utf-8")
            print(f"ok ({len(r.text)} bytes)")
        except Exception as e:
            print(f"FAIL {e}")
        time.sleep(1.5)


if __name__ == "__main__":
    main()
