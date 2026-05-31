"""Turn questions-raw.json into the final questions.json + download images.

Steps:
  1. Parse each raw question's answer text into (correct_letter|correct_text, explanation).
  2. For MC: find correct_index from options. For free-text: build accepted_answers.
  3. Download images to public/questions/.
  4. Deduplicate near-identical questions (UK/US share question bank).
  5. Drop low-quality records and produce questions.json + validation-report.md.
"""
import hashlib
import json
import re
import time
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "questions-raw.json"
IMG_DIR = ROOT / "public" / "questions"
IMG_DIR.mkdir(parents=True, exist_ok=True)
OUT_JSON = ROOT / "public" / "questions.json"
OUT_REPORT = ROOT / "validation-report.md"
OUT_SOURCES = ROOT / "SOURCES.md"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Hand-curated overrides for questions where the source text fights every
# heuristic we have. Keyed by canonical question id. Each entry is merged into
# the canonicalized record (last). Add an entry only after confirming the
# question is unplayable as parsed. See CLAUDE.md "Parser gotchas".
#
# Recurring failure mode for the entries below: comingsoon writes the answer
# as a full prose sentence ("The hybrid instrument is part trombone and part
# tambourine, so it's a 'Trombourine'"). parse_answer takes that sentence as
# the answer segment, expand_accepted stores it verbatim, and the player has
# to type the whole thing to score. The fix is either to register the real
# MC options here (when the source <li> options weren't picked up) or to
# replace the answer with the bare word/letter buried in the prose.
_PLACEHOLDER_NOTE = "Options visible in image only — pick the lettered choice"

MANUAL_OVERRIDES: dict[str, dict] = {
    # Image shows 3 trays (A/B/C); source answer is "Answer B is the only tray..."
    "us-s2-e13-80": {
        "type": "mc",
        "options": ["(A)", "(B)", "(C)"],
        "correct_index": 1,
        "accepted_answers": None,
        "correct_text": "(B)",
        "explanation": "Tray B is the only one with three different vegetables, milk, and no bread.",
        "notes": _PLACEHOLDER_NOTE,
    },
    # Answer "N" is buried in the explanation, not the first sentence.
    "us-s2-e9-25": {
        "type": "text",
        "options": None,
        "correct_index": None,
        "accepted_answers": ["n"],
        "correct_text": "N",
        "explanation": "The letters are currently P, R, N, D, S, L. In alphabetical order, the letters are D, L, N, P, R, S – so N is in the same position.",
    },
    # Free-text answer is the word COMB-OVER; source stores the explanation sentence.
    "us-s2-e6-50": {
        "type": "text",
        "options": None,
        "correct_index": None,
        "accepted_answers": ["comb-over", "comb over", "combover"],
        "correct_text": "COMB-OVER",
        "explanation": "The word “COMB-OVER” is revealed when you move the combo over and interlock the teeth.",
    },
    # 3-option compass image, correct = B.
    "uk-s4-e8-40": {
        "type": "mc",
        "options": ["(A)", "(B)", "(C)"],
        "correct_index": 1,
        "accepted_answers": None,
        "correct_text": "(B)",
        "explanation": "In B, when the N and the S come into the right positions, the E and the W are back to front and in the wrong positions.",
        "notes": _PLACEHOLDER_NOTE,
    },
    # Real MC with text options; source <li>s weren't picked up by parse.py.
    "us-s1-e1-50": {
        "type": "mc",
        "options": ["One with 5 petals", "One with 50 petals", "One with 555 petals"],
        "correct_index": 1,
        "accepted_answers": None,
        "correct_text": "One with 50 petals",
        "explanation": "“He loves me not” is said when plucking even-numbered petals, and the only even-numbered flower has 50 petals.",
        "notes": "",
    },
    # Free-text numeric answer ($2,015) buried in the explanation.
    "us-s2-e2-1": {
        "type": "text",
        "options": None,
        "correct_index": None,
        "accepted_answers": ["2015", "2,015", "$2015", "$2,015"],
        "correct_text": "$2,015",
        "explanation": "Jerry takes the first digit of the year and doubles it to get the first number. Then he adds the remaining numbers together to get the rest of the price. Doubling the 1 in 1951 gets you 2, and 9 + 5 + 1 = 15, for a total of $2,015.",
    },
    # Real MC with text options.
    "us-s2-e4-50": {
        "type": "mc",
        "options": [
            "Senior ticket purchased June 29",
            "General Admission ticket purchased June 28",
            "VIP ticket purchased June 27",
            "Meet and Greet ticket purchased June 25",
        ],
        "correct_index": 0,
        "accepted_answers": None,
        "correct_text": "Senior ticket purchased June 29",
        "explanation": "The Senior ticket, even without the discount, is the cheapest, at $115. General Admission with no discount would be $125, VIP with discount is $175, and a Meet and Greet ticket with discount is $250.",
        "notes": "",
    },
    "us-s2-e6-90": {
        "type": "mc",
        "options": ["Saxaccordion", "Flutanjo", "Trombourine"],
        "correct_index": 2,
        "accepted_answers": None,
        "correct_text": "Trombourine",
        "explanation": "The hybrid instrument is part trombone and part tambourine, so it’s a “Trombourine”.",
        "notes": "",
    },
    "us-s2-e6-80": {
        "type": "mc",
        "options": ["Jane", "Billy", "Frank"],
        "correct_index": 1,
        "accepted_answers": None,
        "correct_text": "Billy",
        "explanation": "The only person whose smile would make that shape of bite is Billy, since he’s missing his two front teeth.",
        "notes": "",
    },
    # Image has 2 lettered pairs (A, B); answer = the second pair.
    "us-s2-e6-70": {
        "type": "mc",
        "options": ["(A)", "(B)"],
        "correct_index": 1,
        "accepted_answers": None,
        "correct_text": "(B)",
        "explanation": "Only the second pair has the character with the triangle chest piece.",
        "notes": _PLACEHOLDER_NOTE,
    },
    # Image has 3 invitations (A, B, C); answer = Taylor and Morgan = C.
    "us-s2-e6-40": {
        "type": "mc",
        "options": ["(A)", "(B)", "(C)"],
        "correct_index": 2,
        "accepted_answers": None,
        "correct_text": "(C)",
        "explanation": "Taylor and Morgan’s wedding date is February 30th, and no one will be able to make it on that date since it doesn’t exist.",
        "notes": _PLACEHOLDER_NOTE,
    },
    # Free-text; answer is two letters (R and I).
    "us-s2-e9-80": {
        "type": "text",
        "options": None,
        "correct_index": None,
        "accepted_answers": ["r and i", "i and r", "r, i", "i, r", "ri", "ir"],
        "correct_text": "R and I",
        "explanation": "The only two letters that make a word are R and I, making the pendant read “100% THAT RICH”.",
    },
    # Source recap omitted the question stem entirely; restore it.
    "uk-s4-e13-1": {
        "question_text": "What new word links the capitalised words below?\n\nMy SON TED ate raw FOOD and got SICK, then went to BED with me by his SIDE.",
    },
}


NUMBER_WORDS = {
    "0": ["zero"], "1": ["one"], "2": ["two"], "3": ["three"], "4": ["four"],
    "5": ["five"], "6": ["six"], "7": ["seven"], "8": ["eight"], "9": ["nine"],
    "10": ["ten"], "11": ["eleven"], "12": ["twelve"], "13": ["thirteen"],
    "14": ["fourteen"], "15": ["fifteen"], "16": ["sixteen"], "17": ["seventeen"],
    "18": ["eighteen"], "19": ["nineteen"], "20": ["twenty"], "21": ["twenty-one", "twenty one"],
    "22": ["twenty-two", "twenty two"], "23": ["twenty-three", "twenty three"],
    "24": ["twenty-four", "twenty four"], "25": ["twenty-five", "twenty five"],
    "30": ["thirty"], "40": ["forty"], "50": ["fifty"], "60": ["sixty"],
    "70": ["seventy"], "80": ["eighty"], "90": ["ninety"], "100": ["one hundred", "hundred"],
}


def normalize_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def build_question_text(raw: dict) -> str:
    parts = [raw["question_text"]]
    if raw.get("question_extra"):
        parts.extend(raw["question_extra"])
    text = "\n\n".join(p for p in parts if p)
    # Strip [image above] / (image above) / (photo above) markers — image renders separately.
    text = re.sub(r"\s*[\[\(](?:image|photo)\s+above[\]\)]\s*", "", text, flags=re.I)
    # Strip trailing meta-option lists like "(A), (B), or (C)" / "(A) or (B) or (C) or (D)"
    text = re.sub(
        r"\s*(?:\(?[A-E][\)\.\]],?\s*(?:or\s+)?){2,}\(?[A-E][\)\.\]]?\.?\s*$",
        "",
        text,
        flags=re.I,
    ).strip()
    return text.strip()


def parse_answer(answer_raw: str) -> tuple[str, str]:
    """Return (answer_segment, explanation).

    answer_segment is the bare answer (e.g. '(A) EXPLORE' or '22' or 'Great minds think alike.')
    explanation is the rest of the details text after the first sentence.

    Also defends against bleed: some source HTML has malformed <details> elements that
    accidentally swallow subsequent question/answer text. Truncate at the next
    "% Question & Answer" or "Answer to N% Question" marker.
    """
    if not answer_raw:
        return "", ""
    text = answer_raw.strip()
    # Strip leading section header (e.g. "Answer to 90% Question")
    text = re.sub(r"^Answer\s+to\s+\d+%\s+Question\s*", "", text, flags=re.I)
    # Truncate at any further question/answer header that bled in from a sibling.
    text = re.split(
        r"\s*(?:\d+\s*%\s+Question\s*&\s*Answer|Answer\s+to\s+\d+%\s+Question)\b",
        text,
        maxsplit=1,
        flags=re.I,
    )[0]
    text = re.sub(r"^[–—\-:\s]+", "", text).strip()
    # Split first sentence (answer) from remainder (explanation).
    m = re.match(r"(.+?[.!?])\s+(.+)$", text, flags=re.S)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return text.strip(), ""


_LETTER_PREFIX_RE = re.compile(r"^\(?([A-E])[\)\.\]:]\s*(.+)$", re.I)
# Bare-letter answer ("A", "A.", "(B)") with nothing meaningful after.
_BARE_LETTER_RE = re.compile(r"^\(?([A-E])[\)\.\]:]?\.?\s*$", re.I)
# "Answer B is the only tray..." / "Answer B: explanation" — source prose
# where the letter is followed by an "is"/"was" verb or a colon/equals. Used
# only as a last-resort fallback after the other letter extractors fail.
# The trailing verb/punctuation guard keeps us from false-positive matching
# prose like "Answer A is wrong because B is right" — the first sentence
# would still resolve to A, so anything looser than this is unsafe.
_ANSWER_PROSE_RE = re.compile(r"^Answer\s+([A-E])\b(?:\s+(?:is|was)\b|\s*[:=])", re.I)
_INLINE_OPTS_RE = re.compile(r"\(?([A-E])[\)\.\]]\s+([^()]+?)(?=\s*\(?[A-E][\)\.\]]\s|$)")


def parse_inline_options(text: str) -> list[str] | None:
    """Extract '(A) X (B) Y' / 'A) X B) Y' style options from a paragraph string."""
    parts = _INLINE_OPTS_RE.findall(text)
    if len(parts) < 2:
        return None
    cleaned = []
    for letter, body in parts:
        body = re.sub(r"\s+or\s*$", "", body.strip().rstrip(",. "), flags=re.I).strip().rstrip(",. ")
        if not body:
            return None
        cleaned.append(f"({letter}) {body}")
    return cleaned


def extract_correct_letter(answer_seg: str) -> str | None:
    """Return 'A'-'E' if the answer is a labelled letter ('(A)', 'A) X', 'A.', 'B: Red', 'A', 'Answer B ...')."""
    s = answer_seg.strip()
    m = _BARE_LETTER_RE.match(s)
    if m:
        return m.group(1).upper()
    m = _LETTER_PREFIX_RE.match(s)
    if m:
        return m.group(1).upper()
    m = _ANSWER_PROSE_RE.match(s)
    if m:
        return m.group(1).upper()
    return None


def strip_letter_prefix(answer_seg: str) -> str:
    """'(A) EXPLORE' -> 'EXPLORE'. Also handles 'B: Red.' -> 'Red'."""
    m = _LETTER_PREFIX_RE.match(answer_seg.strip())
    inner = (m.group(2) if m else answer_seg).strip()
    return inner.rstrip(".!?,;:")


def expand_accepted(answer_segment: str) -> list[str]:
    """Generate a list of acceptable user answers (case-insensitive matching).

    Strips leading articles, strips trailing punctuation, adds number-word and
    letter-sequence variants, and accepts the bare number from "<n> <unit>"
    answers ("60 days" → also accept "60", "sixty", "sixty days").
    """
    base = answer_segment.strip().rstrip(".!?,;: ")
    answers = {base}

    # Strip leading 'The '
    if base.lower().startswith("the "):
        answers.add(base[4:])
    # If it's a pure integer, add the word form (and vice-versa).
    for num, words in NUMBER_WORDS.items():
        if base.strip() == num:
            answers.update(words)
            break
        for w in words:
            if base.strip().lower() == w:
                answers.add(num)
                break
    # "<integer> <unit>" answers — also accept the bare integer and the
    # number-word form. So "60 days" → "60", "sixty", "sixty days".
    # Only the integer-first form is handled: a word-first branch would
    # over-match band/title answers like "One Direction" or "Four Seasons"
    # and let users score by typing "1" or "4". The unit must be lowercase
    # (no re.I) so Title Case proper nouns like "10 Downing Street" do not
    # match — bare "10" is wrong when the street name is part of the answer.
    # The unit character class includes both straight and smart apostrophes
    # so "10 o'clock" works.
    m = re.fullmatch(r"\s*(\d{1,3}(?:,\d{3})*|\d+)\s+([a-z][a-z'’ ]*)", base)
    if m:
        num_raw, unit = m.group(1), m.group(2).strip()
        unit_no_quotes = re.sub(r"['’]", "", unit)
        num_plain = num_raw.replace(",", "")
        answers.add(num_raw)
        answers.add(num_plain)
        for word in NUMBER_WORDS.get(num_plain, []):
            answers.add(word)
            answers.add(f"{word} {unit}")
            if unit_no_quotes != unit:
                answers.add(f"{word} {unit_no_quotes}")
    # Strip quotes/apostrophes
    answers.add(re.sub(r"['’\"“”]", "", base))
    # Letter-sequence answers ("C, A, D, B") — also accept concatenated form.
    if re.fullmatch(r"\s*[A-E](?:\s*,\s*[A-E]){1,5}\s*\.?", base, flags=re.I):
        letters = "".join(re.findall(r"[A-E]", base, flags=re.I))
        answers.add(letters.lower())
        answers.add(letters.upper())
        answers.add(", ".join(letters.upper()))
        answers.add(" ".join(letters.upper()))
    # Lowercase
    answers = {a.lower() for a in answers if a}
    return sorted(answers)


def options_match_letter(options: list[str], letter: str) -> int | None:
    for i, opt in enumerate(options):
        m = re.match(r"^\(([A-E])\)", opt.strip())
        if m and m.group(1) == letter:
            return i
    return None


def clean_option(opt: str) -> str:
    """'(A) EXPLORE' -> 'EXPLORE'. Trim trailing puncutation."""
    m = re.match(r"^\(([A-E])\)\s*(.+)$", opt.strip())
    if m:
        return m.group(2).strip().rstrip(".,;: ")
    return opt.strip()


def canonicalize(raw: dict) -> dict | None:
    """Convert one raw record to the final schema. Return None if invalid."""
    q_text = build_question_text(raw)
    if not q_text or len(q_text) < 15:
        return None
    if not raw.get("answer_raw"):
        return None

    # Drop "[Skipped because ...]" placeholders.
    if q_text.lstrip().startswith("[") and "skip" in q_text.lower()[:100]:
        return None
    # Bleed detection: drop if a leftover "% Question & Answer" header is in the text.
    if re.search(r"%\s+Question\s*&\s*Answer\b", q_text, flags=re.I):
        return None
    # Reject if the question text contains another full "Q:" — means we picked
    # up a sibling question's content.
    if q_text.lower().count("\nq:") + (1 if q_text.lower().startswith("q:") else 0) > 1:
        return None

    # Try to harvest inline options out of question_extra if the parser didn't
    # already extract them.
    if not raw.get("options"):
        for extra in list(raw.get("question_extra") or []):
            inline = parse_inline_options(extra)
            if inline:
                raw["options"] = inline
                # Strip the option line from the question text
                q_text = q_text.replace(extra, "").strip()
                break

    answer_seg, explanation = parse_answer(raw["answer_raw"])
    if not answer_seg:
        return None
    # Reject grossly long answer segments (bleed past truncation).
    if len(answer_seg) > 240:
        return None

    record = {
        "id": raw["id"],
        "show_version": raw["show_version"],
        "season": raw["season"],
        "episode": raw["episode"],
        "difficulty": raw["difficulty"],
        "question_text": q_text,
        "question_image": None,
        "image_url": raw.get("image_url"),  # carried for download stage
        "type": "text",
        "options": None,
        "correct_index": None,
        "accepted_answers": None,
        "correct_text": None,
        "explanation": explanation,
        "source_url": raw["source_url"],
        "confidence": "high",
        "notes": "",
    }

    letter = extract_correct_letter(answer_seg)
    options = raw.get("options")

    if options and letter:
        idx = options_match_letter(options, letter)
        if idx is None:
            return None
        record["type"] = "mc"
        record["options"] = [clean_option(o) for o in options]
        record["correct_index"] = idx
        record["correct_text"] = record["options"][idx]
    elif options and not letter:
        # Options listed but answer is e.g. "RED" (no letter prefix). Try to match by text.
        norm_answer = normalize_text(answer_seg)
        idx = next(
            (i for i, o in enumerate(options) if normalize_text(clean_option(o)) == norm_answer),
            None,
        )
        if idx is not None:
            record["type"] = "mc"
            record["options"] = [clean_option(o) for o in options]
            record["correct_index"] = idx
            record["correct_text"] = record["options"][idx]
        else:
            # Treat as free-text against the answer segment
            record["accepted_answers"] = expand_accepted(answer_seg)
            record["correct_text"] = answer_seg.rstrip(".!?,;: ")
    elif letter and not options:
        # MC question where the options were embedded in the question's image.
        # Without option text, we'd have to ask the user "pick A/B/C/D" — but we don't
        # know what they look like. Drop unless image is present (then user can see them).
        if not raw.get("image_url"):
            return None
        # Synthesize placeholder options A-D
        record["type"] = "mc"
        # Try to detect how many options are referenced by the question text
        letters_mentioned = sorted(set(re.findall(r"\(([A-E])\)", q_text)))
        if not letters_mentioned:
            letters_mentioned = ["A", "B", "C", "D"]
        record["options"] = [f"({L})" for L in letters_mentioned]
        try:
            record["correct_index"] = letters_mentioned.index(letter)
        except ValueError:
            return None
        record["correct_text"] = f"({letter})"
        record["notes"] = "Options visible in image only — pick the lettered choice"
    else:
        # Free-text answer
        record["accepted_answers"] = expand_accepted(answer_seg)
        record["correct_text"] = answer_seg.rstrip(".!?,;: ")

    if not record["correct_text"]:
        return None

    override = MANUAL_OVERRIDES.get(record["id"])
    if override:
        record.update(override)
        _validate_canonical(record)

    return record


def _validate_canonical(record: dict) -> None:
    """Raise if a canonical record violates the type/answer invariants.

    Cheap defense for MANUAL_OVERRIDES: an override that flips ``type`` but
    forgets to null out the opposite type's fields would silently produce a
    hybrid record that smoke.js does not catch.
    """
    rid = record["id"]
    rtype = record.get("type")
    if rtype == "mc":
        opts = record.get("options")
        idx = record.get("correct_index")
        if not opts or idx is None:
            raise ValueError(f"{rid}: mc record missing options/correct_index")
        if not (0 <= idx < len(opts)):
            raise ValueError(f"{rid}: correct_index {idx} out of range for {len(opts)} options")
        if record.get("accepted_answers") is not None:
            raise ValueError(f"{rid}: mc record must have accepted_answers=None")
        if opts[idx] != record.get("correct_text"):
            raise ValueError(
                f"{rid}: correct_text {record.get('correct_text')!r} != options[{idx}] {opts[idx]!r}"
            )
    elif rtype == "text":
        if not record.get("accepted_answers"):
            raise ValueError(f"{rid}: text record missing accepted_answers")
        if record.get("options") is not None or record.get("correct_index") is not None:
            raise ValueError(f"{rid}: text record must have options=None and correct_index=None")
    else:
        raise ValueError(f"{rid}: invalid type {rtype!r}")
    if not record.get("correct_text"):
        raise ValueError(f"{rid}: empty correct_text")


def download_image(url: str, out_path: Path, session: requests.Session) -> tuple[bool, str]:
    """Download an image. Returns (success, error_or_path)."""
    try:
        r = session.get(url, timeout=30, stream=True)
        r.raise_for_status()
        ct = r.headers.get("content-type", "")
        if "image" not in ct:
            return False, f"non-image content-type: {ct}"
        out_path.write_bytes(r.content)
        # Verify it actually opens as an image
        try:
            with Image.open(out_path) as im:
                im.verify()
        except Exception as e:
            out_path.unlink(missing_ok=True)
            return False, f"corrupt image: {e}"
        return True, str(out_path)
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def near_duplicate(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()


def dedupe(records: list[dict], threshold: float = 0.88) -> tuple[list[dict], list[dict]]:
    """Group near-duplicate questions. Keep one per group (prefer image+UK)."""
    kept: list[dict] = []
    dropped: list[dict] = []
    # Bucket by difficulty for speed
    by_diff = defaultdict(list)
    for r in records:
        by_diff[r["difficulty"]].append(r)

    def rank(r):
        # Higher score wins. Prefer questions with images, then UK, then earlier seasons.
        return (
            1 if r.get("image_url") else 0,
            1 if r["show_version"] == "uk" else 0,
            -r["season"],
        )

    seen_kept: list[dict] = []
    for diff, group in by_diff.items():
        # Sort each difficulty bucket by rank (descending)
        group.sort(key=rank, reverse=True)
        local_kept: list[dict] = []
        for r in group:
            dup_of = None
            for k in local_kept:
                if near_duplicate(r["question_text"], k["question_text"]) >= threshold:
                    dup_of = k
                    break
            if dup_of:
                r["_dup_of"] = dup_of["id"]
                dropped.append(r)
            else:
                local_kept.append(r)
        seen_kept.extend(local_kept)
    return seen_kept, dropped


def main():
    raw_records = json.loads(RAW.read_text(encoding="utf-8"))
    print(f"loaded {len(raw_records)} raw questions")

    canonical: list[dict] = []
    canon_drops: list[tuple[str, str]] = []
    for r in raw_records:
        c = canonicalize(r)
        if c is None:
            canon_drops.append((r["id"], "could not canonicalize"))
        else:
            canonical.append(c)
    print(f"canonicalized: {len(canonical)} (dropped {len(canon_drops)})")

    # Fail loud if any MANUAL_OVERRIDES key never matched a canonicalized id
    # (typo, rename, or a question that was dropped earlier in canonicalize()
    # — without this check the override is silently ignored).
    applied = {r["id"] for r in canonical}
    missing = sorted(set(MANUAL_OVERRIDES) - applied)
    if missing:
        raise SystemExit(
            f"MANUAL_OVERRIDES has {len(missing)} ids that did not match any "
            f"canonicalized record: {missing}"
        )

    # Dedupe across editions
    kept, dups = dedupe(canonical)
    print(f"after dedupe: {len(kept)} (removed {len(dups)} duplicates)")

    # Download images
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Referer": "https://www.comingsoon.net/"})
    img_failures: list[tuple[str, str]] = []
    for rec in kept:
        url = rec.pop("image_url", None)
        if not url:
            continue
        # Strip query args (?w=1024) for filename, but fetch including them
        ext = ".jpg"
        clean_url = url.split("?")[0]
        if clean_url.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
            ext = "." + clean_url.rsplit(".", 1)[-1].lower()
            if ext == ".jpeg":
                ext = ".jpg"
        out_name = f"{rec['id']}{ext}"
        out_path = IMG_DIR / out_name
        if not out_path.exists() or out_path.stat().st_size < 1000:
            ok, info = download_image(url, out_path, session)
            if not ok:
                img_failures.append((rec["id"], info))
                rec["confidence"] = "low"
                rec["notes"] = (rec.get("notes") + " | " if rec.get("notes") else "") + f"image failed: {info}"
                continue
            time.sleep(0.3)
        rec["question_image"] = f"questions/{out_name}"
    print(f"image download failures: {len(img_failures)}")

    # Drop questions where image was required but failed
    final: list[dict] = []
    image_required_drops: list[tuple[str, str]] = []
    for rec in kept:
        # If question text references the image and we couldn't fetch it, drop.
        text = rec["question_text"].lower()
        looks_visual = any(
            kw in text
            for kw in [
                "spot the difference", "shown below", "shown above", "below is",
                "above is", "below.", "this image", "these images", "this picture",
                "[image above]",  # already stripped, but defensive
            ]
        )
        # If MC with placeholder options (image-only options) and no image -> drop
        placeholder_only = (
            rec.get("type") == "mc"
            and rec.get("options")
            and all(re.fullmatch(r"\([A-E]\)", o) for o in rec["options"])
        )
        if (looks_visual or placeholder_only) and rec.get("question_image") is None:
            image_required_drops.append((rec["id"], "visual question with no image"))
            continue
        final.append(rec)
    print(f"final after image-required check: {len(final)} (dropped {len(image_required_drops)})")

    # Sort: by show, season, episode, difficulty desc
    final.sort(key=lambda r: (r["show_version"], r["season"], r["episode"], -r["difficulty"]))

    OUT_JSON.write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT_JSON}")

    # Validation report
    from collections import Counter
    by_show = Counter(r["show_version"] for r in final)
    by_diff = Counter(r["difficulty"] for r in final)
    by_type = Counter(r["type"] for r in final)
    with_img = sum(1 for r in final if r.get("question_image"))

    report = []
    report.append("# Validation report\n")
    report.append(f"- Loaded raw questions: **{len(raw_records)}**")
    report.append(f"- Canonicalized successfully: **{len(canonical)}**")
    report.append(f"- After deduplication across editions: **{len(kept)}**")
    report.append(f"- Final after image-required check: **{len(final)}**")
    report.append("")
    report.append(f"- Final by show: {dict(by_show)}")
    report.append(f"- Final by type: {dict(by_type)}")
    report.append(f"- Final with images: **{with_img}/{len(final)}**")
    report.append("")
    report.append("## Difficulty distribution")
    report.append("| % | count |")
    report.append("|---|---|")
    for d in sorted(by_diff.keys(), reverse=True):
        report.append(f"| {d}% | {by_diff[d]} |")
    report.append("")
    if canon_drops:
        report.append(f"## Dropped during canonicalization ({len(canon_drops)})")
        for id_, reason in canon_drops[:30]:
            report.append(f"- `{id_}` — {reason}")
        if len(canon_drops) > 30:
            report.append(f"- ...and {len(canon_drops) - 30} more")
        report.append("")
    if dups:
        report.append(f"## Removed as duplicates ({len(dups)})")
        for r in dups[:20]:
            report.append(f"- `{r['id']}` ↔ `{r['_dup_of']}` ({r['difficulty']}%)")
        if len(dups) > 20:
            report.append(f"- ...and {len(dups) - 20} more")
        report.append("")
    if img_failures:
        report.append(f"## Image download failures ({len(img_failures)})")
        for id_, err in img_failures[:30]:
            report.append(f"- `{id_}` — {err}")
        if len(img_failures) > 30:
            report.append(f"- ...and {len(img_failures) - 30} more")
        report.append("")
    if image_required_drops:
        report.append(f"## Visual questions dropped (no image available) ({len(image_required_drops)})")
        for id_, reason in image_required_drops[:30]:
            report.append(f"- `{id_}` — {reason}")
        if len(image_required_drops) > 30:
            report.append(f"- ...and {len(image_required_drops) - 30} more")

    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"wrote {OUT_REPORT}")

    # Sources doc
    src_lines = [
        "# Sources",
        "",
        "All practice questions were extracted from publicly available episode recap pages.",
        "Each question's `source_url` field links back to its origin.",
        "",
        "## Primary sources",
        "",
        "- comingsoon.net — UK Season 4: <https://www.comingsoon.net/guides/features/1911071-1-percent-club-questions-answers-uk-season-4-series-2025>",
        "- comingsoon.net — UK Season 5: <https://www.comingsoon.net/guides/features/2041778-1-percent-club-uk-questions-answers-season-5-2025-solutions-series-five>",
        "- comingsoon.net — US Season 1: <https://www.comingsoon.net/guides/features/1788741-1-percent-club-questions-answers-tonight-last-night-tv-show>",
        "- comingsoon.net — US Season 2: <https://www.comingsoon.net/guides/features/1987178-1-percent-club-questions-answers-season-2-2025-solutions-joel-mchale>",
        "",
        "## Counts in final bank",
        "",
        f"- Total: **{len(final)}** questions",
        f"- UK: {by_show.get('uk', 0)} · US: {by_show.get('us', 0)}",
        f"- With image: {with_img}",
        f"- Multiple-choice: {by_type.get('mc', 0)} · Free-text: {by_type.get('text', 0)}",
        "",
        "Practice tool is unofficial. The 1% Club format is owned by BBC Studios.",
    ]
    OUT_SOURCES.write_text("\n".join(src_lines), encoding="utf-8")
    print(f"wrote {OUT_SOURCES}")


if __name__ == "__main__":
    main()
