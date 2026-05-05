"""Quick structure inspection of a saved HTML page."""
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
slug = sys.argv[1] if len(sys.argv) > 1 else "uk-s4"
html = (ROOT / "data" / "raw" / f"{slug}.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "lxml")

# Find the article body
article = soup.find("article") or soup.find("div", class_=lambda c: c and "article" in c.lower())
if not article:
    article = soup.find("main") or soup.body

print(f"== {slug} ==")
print(f"title: {soup.title.string if soup.title else '?'}")
print()

# Print a flattened view: each h2/h3, p, ul, img in order, truncated
target = article or soup
for el in target.find_all(["h1", "h2", "h3", "h4", "p", "ul", "ol", "img", "details", "summary", "strong", "blockquote"], limit=300):
    tag = el.name
    if tag == "img":
        src = el.get("src") or el.get("data-src") or "?"
        alt = el.get("alt", "")
        print(f"  IMG  {src[:120]}  alt={alt[:60]!r}")
    elif tag in ("ul", "ol"):
        items = [li.get_text(" ", strip=True)[:120] for li in el.find_all("li", recursive=False)]
        if items:
            print(f"  {tag.upper():4s} ({len(items)} items): {items[0][:80]!r} ...")
    else:
        text = el.get_text(" ", strip=True)
        if text:
            print(f"  {tag.upper():4s} {text[:160]!r}")
