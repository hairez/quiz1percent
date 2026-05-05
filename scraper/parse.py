"""Parse cached comingsoon.net HTML into structured question records.

Output: data/questions-raw.json — one record per question, with raw answer text
and image URLs (not yet downloaded).

The HTML has a consistent shape per article:

  <div class="entry-content">
    ...
    <h3>Episode N Questions and Answers ...</h3>
    <h4>90% Question & Answer</h4>
    [<img src="...question image...">]
    <p>Q: ... [image above]</p>
    [<ul>(A) X (B) Y (C) Z</ul>]
    <details><summary>Answer to 90% Question</summary>– (A) X. Explanation.</details>
    <h4>80% Question & Answer</h4>
    ...
  </div>
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "questions-raw.json"

SOURCES = {
    "uk-s4": {
        "show_version": "uk", "season": 4,
        "url": "https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025",
    },
    "uk-s5": {
        "show_version": "uk", "season": 5,
        "url": "https://www.comingsoon.net/guides/features/2041778-1-percent-club-uk-questions-answers-season-5-2025-solutions-series-five",
    },
    "us-s1": {
        "show_version": "us", "season": 1,
        "url": "https://www.comingsoon.net/guides/features/1788741-1-percent-club-questions-answers-tonight-last-night-tv-show",
    },
    "us-s2": {
        "show_version": "us", "season": 2,
        "url": "https://www.comingsoon.net/guides/features/1987178-1-percent-club-questions-answers-season-2-2025-solutions-joel-mchale",
    },
}

EPISODE_RE = re.compile(r"Episode\s+(\d+)", re.I)
DIFFICULTY_RE = re.compile(r"(\d+)\s*%\s*Question", re.I)
# Accept (A), A), A. — at least one bracket/dot to mark the letter as a label
OPTION_RE = re.compile(r"^\(?([A-E])[\)\.\]]\s*(.+)$")
ANSWER_LETTER_RE = re.compile(r"\(?([A-E])[\)\.\]]\s*([^.]+)\.?")


def text_of(el) -> str:
    return el.get_text(" ", strip=True)


def parse_options_from_ul(ul) -> list[str] | None:
    """Try to read (A) X (B) Y options from a <ul>."""
    items = [text_of(li) for li in ul.find_all("li", recursive=False)]
    full_text = text_of(ul)
    # First, try parsing the full ul text — handles both no-li and single-li-with-all-options.
    multi = parse_options_from_text(full_text)
    if multi and len(multi) >= 2:
        return multi
    if not items:
        return None
    parsed = []
    for item in items:
        m = OPTION_RE.match(item)
        if not m:
            return None
        parsed.append(f"({m.group(1)}) {m.group(2).strip()}")
    return parsed if len(parsed) >= 2 else None


def parse_options_from_text(text: str) -> list[str] | None:
    """Extract '(A) X (B) Y' or 'A) X B) Y' style options from a single string.

    Requires at least 2 lettered options. Stops on the first paren/dot-letter
    (so plain prose with '(a)' lowercase or '(B)' inside the question text won't trigger).
    """
    # Match (A) X, A) X, A. X with at least one delimiter
    parts = re.findall(r"\(?([A-E])[\)\.\]]\s+([^()]+?)(?=\s*\(?[A-E][\)\.\]]\s|$)", text)
    if len(parts) < 2:
        return None
    cleaned = []
    for letter, body in parts:
        body = body.strip().rstrip(",. ")
        # Stop the body at common end markers like "or" trailing the last option
        body = re.sub(r"\s+or\s*$", "", body, flags=re.I).strip().rstrip(",. ")
        if not body:
            return None
        cleaned.append(f"({letter}) {body}")
    return cleaned


def split_answer(details_text: str) -> tuple[str, str]:
    """Split 'Answer to 90% Question – (A) X. Explanation.' into (answer_segment, explanation).

    The leading 'Answer to N% Question' is removed, then we split on the dash separator,
    then on the first sentence boundary.
    """
    text = details_text.strip()
    # Strip the summary portion
    text = re.sub(r"^Answer\s+to\s+\d+%\s+Question\s*", "", text, flags=re.I)
    # Strip leading dash variants (–, —, -)
    text = re.sub(r"^[–—\-:\s]+", "", text)
    # Split on first sentence boundary (period followed by space + capital, or end)
    # Be conservative: just take everything before the first period as the answer.
    m = re.match(r"(.+?[.!?])\s+(.+)$", text, flags=re.S)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return text.strip(), ""


def parse_article(slug: str, info: dict, html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    article = soup.find("div", class_="entry-content")
    if not article:
        print(f"[{slug}] no entry-content div found")
        return []

    questions: list[dict] = []
    current_episode: int | None = None
    current_episode_id: str | None = None  # may include 'b','c' suffix on duplicate Ep N headers
    seen_episodes: dict[int, int] = {}  # episode_num -> occurrence count
    pending: dict | None = None

    def finalize():
        nonlocal pending
        if pending and pending.get("question_text") and pending.get("answer_raw"):
            questions.append(pending)
        pending = None

    # Walk all relevant tags in document order
    for el in article.find_all(["h2", "h3", "h4", "img", "p", "ul", "ol", "details"]):
        name = el.name
        if name in ("h2", "h3"):
            t = text_of(el)
            m = EPISODE_RE.search(t)
            if m:
                finalize()
                current_episode = int(m.group(1))
                seen_episodes[current_episode] = seen_episodes.get(current_episode, 0) + 1
                n = seen_episodes[current_episode]
                current_episode_id = str(current_episode) if n == 1 else f"{current_episode}{chr(ord('a') + n - 1)}"
            continue
        if name == "h4":
            t = text_of(el)
            m = DIFFICULTY_RE.search(t)
            if m and current_episode is not None:
                finalize()
                pending = {
                    "id": f"{slug}-e{current_episode_id}-{m.group(1)}",
                    "show_version": info["show_version"],
                    "season": info["season"],
                    "episode": current_episode,
                    "difficulty": int(m.group(1)),
                    "question_text": "",
                    "question_extra": [],  # extra paragraphs (e.g. number sequence)
                    "image_url": None,
                    "options": None,
                    "answer_raw": None,
                    "source_url": info["url"],
                }
            continue
        if pending is None:
            continue
        if name == "img":
            if pending["image_url"] is None:
                src = el.get("src") or el.get("data-src")
                if src and "comingsoon.net" in src and "/uploads/" in src:
                    pending["image_url"] = src
            continue
        if name == "details":
            pending["answer_raw"] = text_of(el)
            continue
        if name in ("ul", "ol"):
            opts = parse_options_from_ul(el)
            if opts:
                pending["options"] = opts
            else:
                # Treat as part of the question (rare)
                pending["question_extra"].append(text_of(el))
            continue
        if name == "p":
            t = text_of(el)
            if not t:
                continue
            if pending["question_text"] == "":
                # First paragraph after the h4 header — should start with Q:
                pending["question_text"] = re.sub(r"^Q[:\s]+", "", t).strip()
                # If options are inline, extract them
                inline = parse_options_from_text(pending["question_text"])
                if inline and pending["options"] is None:
                    pending["options"] = inline
            else:
                # Could be additional question content (e.g. a number sequence)
                # Skip if it looks like it's really an "answer" or "ad" paragraph
                if any(skip in t.lower() for skip in ("answer to", "advertisement", "subscribe")):
                    continue
                inline = parse_options_from_text(t)
                if inline and pending["options"] is None:
                    pending["options"] = inline
                else:
                    pending["question_extra"].append(t)
            continue

    finalize()
    return questions


def main():
    all_questions: list[dict] = []
    for slug, info in SOURCES.items():
        path = RAW / f"{slug}.html"
        if not path.exists():
            print(f"missing: {path}")
            continue
        html = path.read_text(encoding="utf-8")
        qs = parse_article(slug, info, html)
        print(f"{slug}: {len(qs)} questions")
        all_questions.extend(qs)

    OUT.write_text(json.dumps(all_questions, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nTotal: {len(all_questions)} questions -> {OUT}")

    # Quick stats
    from collections import Counter
    by_show = Counter(q["show_version"] for q in all_questions)
    by_diff = Counter(q["difficulty"] for q in all_questions)
    has_image = sum(1 for q in all_questions if q["image_url"])
    has_opts = sum(1 for q in all_questions if q["options"])
    print(f"  by show: {dict(by_show)}")
    print(f"  with image: {has_image}/{len(all_questions)}")
    print(f"  with options: {has_opts}/{len(all_questions)}")
    print(f"  difficulty distribution: {dict(sorted(by_diff.items()))}")


if __name__ == "__main__":
    main()
