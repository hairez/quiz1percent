"""Diff public/questions.json against data/questions-fandom.json.

Writes data/audit-fandom.md with:

  1. Conflicts on UK S4 (per-question side-by-side, categorised)
  2. New content available from the wiki (S1-S3 + specials)
  3. Parse warnings (wiki records flagged confidence: low)

No modifications are made to public/questions.json or to MANUAL_OVERRIDES.
"""
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OURS_PATH = ROOT / "public" / "questions.json"
WIKI_PATH = ROOT / "data" / "questions-fandom.json"
OUT_PATH = ROOT / "data" / "audit-fandom.md"


def normalize_text(s: str | None) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.lower()
    # Curly quotes -> straight
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    # Drop whitespace and most punctuation for set-style comparison
    s = re.sub(r"[\s\.,;:!\?\-'\"\(\)\[\]\{\}]+", " ", s)
    return s.strip()


def options_set(opts):
    if not opts:
        return set()
    return {normalize_text(o) for o in opts}


def categorise(ours: dict, wiki: dict) -> list[str]:
    """Return the list of conflict categories that apply, or [] for clean match."""
    cats = []

    # Compare question text
    if normalize_text(ours.get("question_text")) != normalize_text(wiki.get("question_text")):
        # Tolerate the case where the wiki added a duplicated stem or
        # where our text contains more (the comingsoon Q often pads with examples).
        ours_norm = normalize_text(ours.get("question_text"))
        wiki_norm = normalize_text(wiki.get("question_text"))
        if ours_norm and wiki_norm and (
            ours_norm in wiki_norm or wiki_norm in ours_norm
        ):
            # one is a substring of the other -> usually means one side captured
            # extra context. Flag as enrichment, not a conflict.
            if len(wiki_norm) > len(ours_norm) + 20:
                cats.append("richer_question_on_wiki")
        else:
            cats.append("different_question_text")

    # Compare options
    our_opts = options_set(ours.get("options"))
    wiki_opts = options_set(wiki.get("options"))
    placeholder = {"(a)", "(b)", "(c)", "(d)", "(e)"}
    if our_opts <= placeholder and wiki_opts and not (wiki_opts <= placeholder):
        cats.append("we_have_placeholder_wiki_has_real_options")
    elif our_opts and wiki_opts and our_opts != wiki_opts:
        common = our_opts & wiki_opts
        if not common:
            cats.append("different_options")
        elif len(wiki_opts) > len(our_opts):
            cats.append("missing_options")
        elif len(our_opts) > len(wiki_opts):
            cats.append("extra_options")
        else:
            cats.append("different_options")
    elif our_opts and not wiki_opts:
        # we have options, wiki didn't have a table -> wiki may have parsed it as text
        cats.append("wiki_missing_options")

    # Compare correct answer
    our_ans = normalize_text(ours.get("correct_text"))
    wiki_ans = normalize_text(wiki.get("correct_text"))
    if our_ans and wiki_ans and our_ans != wiki_ans:
        if our_ans not in wiki_ans and wiki_ans not in our_ans:
            cats.append("different_correct_answer")
        else:
            cats.append("answer_substring_mismatch")
    elif our_ans and not wiki_ans:
        cats.append("wiki_missing_answer")
    elif wiki_ans and not our_ans:
        cats.append("we_have_no_answer")

    # Explanation length
    our_exp = (ours.get("explanation") or "").strip()
    wiki_exp = (wiki.get("explanation") or "").strip()
    if wiki_exp and len(wiki_exp) > len(our_exp) + 40:
        cats.append("richer_explanation_on_wiki")

    return cats


def fmt_block(label: str, value):
    if isinstance(value, list):
        if not value:
            return f"  {label}: (none)"
        return f"  {label}: {value}"
    if value is None or value == "":
        return f"  {label}: (none)"
    text = str(value).replace("\n", " ")
    if len(text) > 240:
        text = text[:237] + "..."
    return f"  {label}: {text}"


def render_conflict(qid: str, cats: list[str], ours: dict | None, wiki: dict | None) -> str:
    lines = [f"### `{qid}`", ""]
    lines.append(f"Category: **{', '.join(cats)}**")
    lines.append("")
    if ours:
        lines.append(f"**Ours** ({ours.get('source_url', '')})")
        lines.append("```")
        lines.append(fmt_block("Q", ours.get("question_text")))
        lines.append(fmt_block("opts", ours.get("options")))
        lines.append(fmt_block("ans", ours.get("correct_text")))
        lines.append(fmt_block("expl", ours.get("explanation")))
        lines.append(fmt_block("img", ours.get("question_image")))
        lines.append("```")
    else:
        lines.append("**Ours**: (no record)")
    lines.append("")
    if wiki:
        lines.append(f"**Wiki** ({wiki.get('source_url', '')})")
        lines.append("```")
        lines.append(fmt_block("Q", wiki.get("question_text")))
        lines.append(fmt_block("opts", wiki.get("options")))
        lines.append(fmt_block("ans", wiki.get("correct_text")))
        lines.append(fmt_block("expl", wiki.get("explanation")))
        lines.append(fmt_block("img", wiki.get("image_filename")))
        if wiki.get("confidence") == "low":
            lines.append(f"  parse_notes: {wiki.get('notes')}")
        lines.append("```")
    else:
        lines.append("**Wiki**: (no record)")
    return "\n".join(lines) + "\n"


def main():
    ours = json.load(OURS_PATH.open(encoding="utf-8"))
    wiki = json.load(WIKI_PATH.open(encoding="utf-8"))

    ours_by_id = {q["id"]: q for q in ours}
    wiki_by_id = {q["id"]: q for q in wiki}

    # Section 1: UK S4 overlap
    s4_ours_ids = {q["id"] for q in ours if q["show_version"] == "uk" and q["season"] == 4}
    s4_wiki_ids = {q["id"] for q in wiki if q["show_version"] == "uk" and q["season"] == 4}
    s4_shared = sorted(s4_ours_ids & s4_wiki_ids)
    s4_only_ours = sorted(s4_ours_ids - s4_wiki_ids)
    s4_only_wiki = sorted(s4_wiki_ids - s4_ours_ids)

    conflicts: list[tuple[str, list[str]]] = []
    clean = 0
    for qid in s4_shared:
        cats = categorise(ours_by_id[qid], wiki_by_id[qid])
        if cats:
            conflicts.append((qid, cats))
        else:
            clean += 1

    # Section 2: new content (UK S1-3 + specials)
    new_records = [r for r in wiki if (
        (r["show_version"] == "uk" and 1 <= r["season"] <= 3)
        or r.get("special")
    )]
    by_page: dict[str, list[dict]] = defaultdict(list)
    for r in new_records:
        if r.get("special"):
            key = f"Special: {r['special']}"
        else:
            key = f"UK S{r['season']} E{r['episode']}"
        by_page[key].append(r)

    # Section 3: parse warnings
    warnings = [r for r in wiki if r["confidence"] == "low"]

    # Render
    out: list[str] = []
    out.append("# Fandom wiki audit")
    out.append("")
    out.append(
        f"Compared **{len(ours)}** records in `public/questions.json` "
        f"against **{len(wiki)}** records parsed from "
        f"`data/raw/fandom/` (only-connect-questions.fandom.com)."
    )
    out.append("")
    out.append(
        f"Headline: **{len(conflicts)} conflicts on UK S4** ({clean} clean), "
        f"**{len(new_records)} new questions available** "
        f"(UK S1-S3 + specials), **{len(warnings)} parse warnings**."
    )
    out.append("")
    out.append("---")
    out.append("")

    out.append("## 1. UK S4 conflicts")
    out.append("")
    out.append(
        "Each entry lists the categories that fired, then prints the two records "
        "side-by-side so you can decide if the wiki version should override "
        "(via `MANUAL_OVERRIDES` in `scraper/build.py`)."
    )
    out.append("")
    cat_counter: dict[str, int] = defaultdict(int)
    for _, cats in conflicts:
        for c in cats:
            cat_counter[c] += 1
    if cat_counter:
        out.append("Conflicts by category:")
        out.append("")
        for c, n in sorted(cat_counter.items(), key=lambda kv: -kv[1]):
            out.append(f"- **{c}**: {n}")
        out.append("")
    if s4_only_ours:
        out.append(f"Records present in ours but not on wiki ({len(s4_only_ours)}):")
        out.append("")
        for qid in s4_only_ours:
            out.append(f"- `{qid}`")
        out.append("")
    if s4_only_wiki:
        out.append(f"Records present on wiki but not in ours ({len(s4_only_wiki)}):")
        out.append("")
        for qid in s4_only_wiki:
            out.append(f"- `{qid}`")
        out.append("")
    for qid, cats in conflicts:
        out.append(render_conflict(qid, cats, ours_by_id.get(qid), wiki_by_id.get(qid)))

    out.append("---")
    out.append("")
    out.append("## 2. New questions available")
    out.append("")
    out.append(
        f"The wiki covers UK Seasons 1-3 and three specials, which the current "
        f"build does not include. **{len(new_records)} questions** total. To import, "
        f"add a follow-up pass to `scraper/build.py` that ingests "
        f"`data/questions-fandom.json` and matches the public schema (the wiki "
        f"records use `image_filename` and have no downloaded images)."
    )
    out.append("")
    out.append("| Page | Questions | High-confidence | Low-confidence |")
    out.append("|------|-----------|-----------------|----------------|")
    for key in sorted(by_page.keys(), key=_page_sort_key):
        recs = by_page[key]
        high = sum(1 for r in recs if r["confidence"] == "high")
        low = sum(1 for r in recs if r["confidence"] == "low")
        out.append(f"| {key} | {len(recs)} | {high} | {low} |")
    out.append("")

    out.append("---")
    out.append("")
    out.append("## 3. Parse warnings")
    out.append("")
    out.append(
        "Wiki records the parser flagged as low-confidence. Most are wiki-side "
        "issues (no bolded answer, picture-only answers, multi-row letter grids) "
        "rather than parser bugs."
    )
    out.append("")
    warn_by_reason: dict[str, list[str]] = defaultdict(list)
    for r in warnings:
        warn_by_reason[r["notes"] or "(no note)"].append(r["id"])
    for reason in sorted(warn_by_reason.keys(), key=lambda k: -len(warn_by_reason[k])):
        ids = warn_by_reason[reason]
        out.append(f"### {reason} ({len(ids)})")
        out.append("")
        out.append(", ".join(f"`{i}`" for i in ids[:60]))
        if len(ids) > 60:
            out.append(f"\n... and {len(ids) - 60} more")
        out.append("")

    OUT_PATH.write_text("\n".join(out), encoding="utf-8")
    print(
        f"{len(conflicts)} conflicts, {len(new_records)} new questions available, "
        f"{len(warnings)} parse warnings -> {OUT_PATH.relative_to(ROOT)}"
    )


def _page_sort_key(key: str):
    """Sort 'UK S1 E1' before 'UK S1 E10' and specials last."""
    if key.startswith("Special:"):
        return (9, key)
    m = re.match(r"UK S(\d+) E(\d+)", key)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (0, key)


if __name__ == "__main__":
    main()
