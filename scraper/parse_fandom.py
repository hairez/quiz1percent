"""Parse cached Fandom wikitext into structured question records.

Input:  data/raw/fandom/*.wiki
Output: data/questions-fandom.json

This is the audit-side parser. It produces records with the same field shape
as the main pipeline so audit_fandom.py can do a straight join on `id`.

Wikitext shape (samples in data/raw/fandom/):

  == 90% ==                          # or ==90%==, no space
  [[File:Image.png|frameless]]       # optional, can come before OR after table
  {| class="fandom-table"
  ! colspan="3" |Question text       # cell can also be '''bold''' wrapped
  |-
  |Option A
  |'''Correct option'''              # fully-bold cell marks the answer
  |Option C
  |}
  Explanation paragraph.

For text questions there is no table; the answer is the line containing a
fully-bold token (`'''ANSWER'''`), often followed by `: explanation`.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "fandom"
OUT = ROOT / "data" / "questions-fandom.json"

WIKI_BASE = "https://only-connect-questions.fandom.com/wiki/"

# Difficulty headings: == 90% ==, ==90%==, == 1% ==
HEADING_RE = re.compile(r"^==\s*(\d+)%\s*==\s*$")
# Non-difficulty heading like "== Example Question =="
NON_NUMERIC_HEADING_RE = re.compile(r"^==\s*([^=]+?)\s*==\s*$")
FILE_RE = re.compile(r"\[\[File:([^\|\]]+?)(?:\|[^\]]*)?\]\]")
# A "fully bold" string: starts and ends with ''' and has no other ''' inside.
FULLY_BOLD_RE = re.compile(r"^'''([^']+(?:'[^']+)*)'''$")


def page_title_from_slug(slug: str) -> str:
    """Reverse fetch_fandom.slug() back into a wiki page title."""
    return slug.replace("_", " ").replace("pct", "%")


def page_url(slug: str) -> str:
    title = slug.replace("pct", "%25")
    return WIKI_BASE + title


def classify_page(slug: str):
    """Return (show_version, season, episode, special_label, id_prefix)."""
    m = re.match(r"1pct_Club_Season_(\d+)_Episode_(\d+)$", slug)
    if m:
        season, ep = int(m.group(1)), int(m.group(2))
        return "uk", season, ep, None, f"uk-s{season}-e{ep}"
    m = re.match(r"1pct_Club_(Christmas_\d+|Soccer_Aid_\d+)$", slug)
    if m:
        label = m.group(1).replace("_", "-").lower()
        return "uk", 0, 0, label, f"uk-special-{label}"
    return None


def strip_wiki_inline(s: str) -> str:
    """Remove wikitext formatting, leaving plain text."""
    # Files (shouldn't appear inline in question text usually, but be safe)
    s = FILE_RE.sub("", s)
    # Internal links [[Target|Display]] -> Display, [[Target]] -> Target
    s = re.sub(r"\[\[([^\]\|]+)\|([^\]]+)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    # HTML tags: keep <br> as space, drop <s>, <u>
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"</?(?:s|u|strike|del|ins|sup|sub|small)>", "", s, flags=re.I)
    # Bold + italic markers -> nothing
    s = re.sub(r"'''''", "", s)
    s = re.sub(r"'''", "", s)
    s = re.sub(r"''", "", s)
    return re.sub(r"\s+", " ", s).strip()


def is_fully_bold(cell: str) -> bool:
    """A cell is the 'correct' one when its entire content is wrapped in '''…'''.

    Tolerates a trailing punctuation char after the closing ''' (none have been
    seen but cheap to allow) and strips outer whitespace.
    """
    s = cell.strip().rstrip(".,;:")
    return bool(FULLY_BOLD_RE.match(s))


def parse_table(table_block: str):
    """Return (question_text, options, correct_indices, n_columns) or None.

    table_block is the wikitext between '{|' and '|}', inclusive.
    """
    lines = [ln for ln in table_block.splitlines() if ln.strip()]
    if not lines:
        return None
    # First line is `{| class="..."`, drop it. Last is `|}`, drop it.
    if lines[0].lstrip().startswith("{|"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "|}":
        lines = lines[:-1]

    question_text = None
    n_columns = None
    rows: list[list[str]] = []
    current_row: list[str] = []

    for ln in lines:
        s = ln.rstrip()
        if s.startswith("!"):
            # Header cell. Look for "colspan=N | text".
            body = s[1:].lstrip()
            colspan_m = re.match(r'colspan\s*=\s*"?(\d+)"?\s*\|\s*(.*)$', body)
            if colspan_m:
                n_columns = int(colspan_m.group(1))
                question_text = colspan_m.group(2).strip()
            else:
                # Plain header cell without colspan — treat as question text.
                question_text = body.lstrip("|").strip()
        elif s.strip() == "|-":
            if current_row:
                rows.append(current_row)
                current_row = []
        elif s.startswith("|"):
            # Could be one cell `|X` or multiple cells on one line `|A||B||C`.
            body = s[1:]
            cells = re.split(r"\|\|", body)
            current_row.extend(c for c in cells)
    if current_row:
        rows.append(current_row)

    # Bold-wrapped question text: strip and remember.
    if question_text:
        qm = FULLY_BOLD_RE.match(question_text.strip())
        if qm:
            question_text = qm.group(1)
        question_text = strip_wiki_inline(question_text)

    # Detect "label + text" pattern: 2-col table where every row's first cell is
    # a single letter A-E (optionally bold). Merge col1+col2 into one option.
    is_label_text = (
        len(rows) >= 2
        and all(len(r) == 2 for r in rows)
        and all(re.match(r"^\s*'*([A-E])'*\s*$", r[0]) for r in rows)
    )

    options = []
    correct = []
    if is_label_text:
        for row in rows:
            label_cell, text_cell = row[0].strip(), row[1].strip()
            idx = len(options)
            # Correct if either cell is fully bold (the wiki uses both together).
            if is_fully_bold(label_cell) or is_fully_bold(text_cell):
                correct.append(idx)
            options.append(strip_wiki_inline(text_cell))
    else:
        for row in rows:
            for cell in row:
                cell_stripped = cell.strip()
                if not cell_stripped:
                    continue
                idx = len(options)
                if is_fully_bold(cell_stripped):
                    correct.append(idx)
                options.append(strip_wiki_inline(cell_stripped))

    return {
        "question_text": question_text or "",
        "options": options,
        "correct_indices": correct,
        "n_columns": n_columns,
    }


def find_first_fully_bold_token(text: str) -> str | None:
    """Find the first '''...''' run in a piece of free wikitext."""
    m = re.search(r"'''([^']+(?:'[^']+)*)'''", text)
    return m.group(1).strip() if m else None


def parse_text_question(body: str):
    """A question section with no MC table. Extract question, answer, explanation."""
    lines = [ln.rstrip() for ln in body.splitlines()]
    image = None
    question_lines: list[str] = []
    answer_line_idx = None

    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s:
            question_lines.append("")
            continue
        fm = FILE_RE.search(s)
        if fm:
            image = fm.group(1).strip()
            # Drop the file marker from the line if it's all that's there.
            remainder = FILE_RE.sub("", s).strip()
            if remainder:
                question_lines.append(remainder)
            continue
        # First line containing a fully-bold token is the answer line.
        if "'''" in s and answer_line_idx is None:
            answer_line_idx = i
            break
        question_lines.append(s)

    question_text = strip_wiki_inline("\n".join(question_lines).strip())

    answer = None
    explanation = ""
    if answer_line_idx is not None:
        ans_line = lines[answer_line_idx].strip()
        # Pattern: '''ANSWER''': explanation OR '''ANSWER'''
        m = re.match(r"^\s*'''([^']+(?:'[^']+)*)'''\s*[:–-]\s*(.+)$", ans_line)
        if m:
            answer = m.group(1).strip()
            explanation = strip_wiki_inline(m.group(2))
        else:
            answer = find_first_fully_bold_token(ans_line)
            # The non-bold remainder of the line might still be informative.
            stripped = strip_wiki_inline(ans_line)
            if answer and stripped and stripped != answer:
                explanation = stripped
        # Anything after the answer line is more explanation.
        extra = [strip_wiki_inline(l) for l in lines[answer_line_idx + 1:] if l.strip()]
        if extra:
            extra_text = "\n".join(e for e in extra if e)
            explanation = (explanation + ("\n" + extra_text if explanation else extra_text)).strip()

    return {
        "question_text": question_text,
        "answer": answer,
        "explanation": explanation,
        "image_filename": image,
    }


def split_into_sections(wikitext: str):
    """Yield (difficulty_int, section_body_str) for each scored question section.

    Skips non-numeric headings (e.g. 'Example Question') and the implicit
    'Category' suffix wikitext that some pages end with.
    """
    lines = wikitext.splitlines()
    current_diff = None
    current_body: list[str] = []
    for ln in lines:
        m = HEADING_RE.match(ln.strip())
        nm = NON_NUMERIC_HEADING_RE.match(ln.strip())
        if m or nm:
            if current_diff is not None:
                yield current_diff, "\n".join(current_body)
            current_body = []
            current_diff = int(m.group(1)) if m else None
        else:
            current_body.append(ln)
    if current_diff is not None:
        yield current_diff, "\n".join(current_body)


def split_table_and_rest(body: str):
    """If body contains `{| ... |}`, return (before, table_block, after)."""
    start = body.find("{|")
    if start == -1:
        return body, None, ""
    end = body.find("|}", start)
    if end == -1:
        return body, None, ""
    end += 2  # include the closing
    return body[:start], body[start:end], body[end:]


def parse_section(slug: str, diff: int, body: str, classification):
    show_version, season, episode, special, id_prefix = classification
    qid = f"{id_prefix}-{diff}"
    page_title = page_title_from_slug(slug)
    url = page_url(slug) + f"#{diff}pct"

    before, table_block, after = split_table_and_rest(body)
    confidence = "high"
    notes_parts: list[str] = []

    # Find image anywhere in the section body
    image_filename = None
    img_m = FILE_RE.search(body)
    if img_m:
        image_filename = img_m.group(1).strip()

    if table_block is not None:
        parsed = parse_table(table_block)
        if parsed is None:
            return {
                "id": qid, "show_version": show_version, "season": season,
                "episode": episode, "special": special, "difficulty": diff,
                "type": "mc", "question_text": "", "options": [], "correct_index": None,
                "correct_text": "", "explanation": "", "image_filename": image_filename,
                "source_url": url, "confidence": "low",
                "notes": "table parse failed",
            }
        # Combine pre-table prose into question text if the table's header cell is empty.
        pre = strip_wiki_inline(FILE_RE.sub("", before))
        if not parsed["question_text"] and pre:
            parsed["question_text"] = pre
        elif parsed["question_text"] and pre:
            # Some MCs have a stem before the table AND a "what is X?" in the table header.
            parsed["question_text"] = (pre + "\n\n" + parsed["question_text"]).strip()
        explanation = strip_wiki_inline(FILE_RE.sub("", after))

        correct_idx = None
        correct_text = ""
        if len(parsed["correct_indices"]) == 1:
            correct_idx = parsed["correct_indices"][0]
            correct_text = parsed["options"][correct_idx]
        elif len(parsed["correct_indices"]) == 0:
            confidence = "low"
            notes_parts.append("no bolded correct cell")
        else:
            confidence = "low"
            notes_parts.append(
                f"multiple bolded cells ({len(parsed['correct_indices'])})"
            )
            correct_idx = parsed["correct_indices"][0]
            correct_text = parsed["options"][correct_idx]
        return {
            "id": qid, "show_version": show_version, "season": season,
            "episode": episode, "special": special, "difficulty": diff,
            "type": "mc",
            "question_text": parsed["question_text"],
            "options": parsed["options"],
            "correct_index": correct_idx,
            "correct_text": correct_text,
            "explanation": explanation,
            "image_filename": image_filename,
            "source_url": url,
            "confidence": confidence,
            "notes": "; ".join(notes_parts),
        }

    # Text question
    parsed = parse_text_question(body)
    if not parsed["question_text"]:
        confidence = "low"
        notes_parts.append("empty question text")
    if not parsed["answer"]:
        confidence = "low"
        notes_parts.append("no bolded answer")
    return {
        "id": qid, "show_version": show_version, "season": season,
        "episode": episode, "special": special, "difficulty": diff,
        "type": "text",
        "question_text": parsed["question_text"],
        "options": None,
        "correct_index": None,
        "correct_text": parsed["answer"] or "",
        "explanation": parsed["explanation"] or "",
        "image_filename": parsed["image_filename"],
        "source_url": url,
        "confidence": confidence,
        "notes": "; ".join(notes_parts),
    }


def parse_file(path: Path):
    slug = path.stem
    classification = classify_page(slug)
    if not classification:
        print(f"skip  {slug} (unrecognised page name)")
        return []
    wikitext = path.read_text(encoding="utf-8")
    records = []
    for diff, body in split_into_sections(wikitext):
        if not body.strip():
            # Empty section, still emit a stub so the audit can flag it.
            show_version, season, episode, special, id_prefix = classification
            records.append({
                "id": f"{id_prefix}-{diff}", "show_version": show_version,
                "season": season, "episode": episode, "special": special,
                "difficulty": diff, "type": "text", "question_text": "",
                "options": None, "correct_index": None, "correct_text": "",
                "explanation": "", "image_filename": None,
                "source_url": page_url(slug) + f"#{diff}pct",
                "confidence": "low", "notes": "empty section on wiki",
            })
            continue
        rec = parse_section(slug, diff, body, classification)
        records.append(rec)
    return records


def main():
    all_records = []
    files = sorted(RAW.glob("*.wiki"))
    for f in files:
        recs = parse_file(f)
        all_records.extend(recs)
        low = sum(1 for r in recs if r["confidence"] == "low")
        print(f"{f.stem}: {len(recs)} records ({low} low-confidence)")
    OUT.write_text(json.dumps(all_records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {len(all_records)} records to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
