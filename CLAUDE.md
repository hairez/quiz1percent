# CLAUDE.md

Orientation for an AI agent picking this project up. Terse on purpose — read the
code for detail, this file just flags the non-obvious.

## What it is

A localhost-only practice quiz for *The 1% Club*. Single-page vanilla-JS app
served by Python's `http.server` on port 3003. The interesting work isn't the UI
— it's the question bank and the parser that produces it.

## Mental model in 30 seconds

```
data/raw/*.html         primary sources (comingsoon.net Q&A recaps), cached
   │
   ▼  scraper/parse.py
data/questions-raw.json one record per Q (raw fields, including question_extra and answer_raw)
   │
   ▼  scraper/build.py
public/questions.json   final, deduped, validated; loaded by the app
public/questions/*.jpg  downloaded question images (named by question id)
   │
   ▼  scraper/smoke.js  (sanity check: every Q can be answered correctly)
   ▼  public/index.html + public/app.js  (no build step, Tailwind via CDN)
```

The app is **vanilla JS, no build step, no framework**. State lives in one
module-scoped `game` object inside `app.js`. Renders are pure innerHTML rewrites
of `<main id="app">`. Don't add a build pipeline without a strong reason.

## Running it

```bash
./serve.sh                          # http://localhost:3003/
./serve.sh ?autostart=full          # skip start screen — handy for testing
```

## Re-running the scrape

```bash
python3 -m venv .venv && .venv/bin/pip install requests beautifulsoup4 lxml pillow
.venv/bin/python scraper/fetch.py    # cached — only re-fetches missing pages
.venv/bin/python scraper/parse.py    # raw HTML → questions-raw.json
.venv/bin/python scraper/build.py    # canonical questions.json + image download
node scraper/smoke.js                # sanity check
```

`fetch.py` is idempotent (it skips files >5 KB that already exist). Delete a file
in `data/raw/` to force a refetch.

## Question schema (public/questions.json)

```jsonc
{
  "id": "uk-s4-e1-90",                // <show>-s<season>-e<episode[a|b|c…]>-<difficulty>
  "show_version": "uk" | "us",
  "season": 4,
  "episode": 1,
  "difficulty": 90,                   // one of 90,80,70,60,50,45,40,35,30,25,20,15,10,5,1
  "type": "mc" | "text",
  "question_text": "…",               // may contain \n\n for paragraph breaks
  "question_image": "questions/<id>.jpg" | null,
  "options": ["EXPLORE", "EXAMINE", …] | null,   // MC only; never letter-prefixed
  "correct_index": 0 | null,           // MC only
  "accepted_answers": ["fifty", "50"] | null,    // text only; case-insensitive match list
  "correct_text": "EXPLORE",          // canonical answer for display
  "explanation": "…",
  "source_url": "https://…",
  "confidence": "high" | "medium" | "low",
  "notes": ""
}
```

**"Placeholder MC"**: when the show puts the option labels inside the image
(e.g. four photos labelled A/B/C/D), `options` is `["(A)", "(B)", "(C)", "(D)"]`
and the player picks a lettered tile. The app detects this via
`isPlaceholderMC()` and renders the four big lettered buttons instead of the
normal text-options layout.

## Parser gotchas (the painful ones)

These are real bugs that bit me; if you change `parse.py` or `build.py`, keep them in mind.

1. **`<details>` bleed.** Some source articles (US S1 in particular) have
   malformed `<details>` tags that aren't properly closed, so the answer text of
   one question swallows the next question's full content. `parse_answer()` in
   `build.py` truncates at any `\d+%\s+Question\s*&\s*Answer` or `Answer to N% Question`
   marker that appears mid-answer. Don't remove that.

2. **Duplicate Episode N headers.** UK S1 has two "Episode 11"s on adjacent
   dates; US S2 has Episode 13 (Second Chance #1) and Episode 13 (Second Chance #2).
   `parse_article()` tracks `seen_episodes[N]` and appends `b`, `c`, … to the
   id of the second+ occurrence. So you'll see ids like `us-s2-e13-…` and
   `us-s2-e13b-…`. **Run `node scraper/smoke.js` after parser changes** — it asserts
   no duplicate ids would silently overwrite each other's images.

3. **Option-label styles vary.** `(A) X`, `A) X`, `A. X`, `A: X` are all in the
   wild, sometimes embedded as text inside a single `<li>` or paragraph instead
   of separate list items. `parse_options_from_ul`/`from_text` handle all four.
   `extract_correct_letter` matches the same set on the answer side.

4. **Answer letter without options.** Some MC answers like `B.` or `(B)` arrive
   with no extracted options because the options were image-only. The
   canonicalizer routes these into the placeholder-MC path **only** if a
   `question_image` was downloaded; otherwise the question is dropped (it would
   be unplayable).

5. **Source-article typos.** Comingsoon occasionally pastes the wrong answer
   under the wrong question heading. We don't try to detect this — there's no
   reliable signal. Expect 1–2 questionable questions per ~600. If we ever build
   a manual blocklist, put it at the top of `build.py`.

6. **`Answer X is …` prefix.** A few sources phrase the MC answer as prose:
   "Answer B is the only tray that has three different vegetables…". The
   `_ANSWER_WORD_RE` arm of `extract_correct_letter` catches this and routes
   the record into the placeholder-MC path. Only used as a last resort after
   the `(A)` / `A.` / `A:` matchers fail.

7. **`MANUAL_OVERRIDES` dict in `build.py`.** For the small number of questions
   where the source text fights every heuristic (e.g. the answer letter is buried
   in the explanation, or the image has fewer options than the default A–D),
   add an entry to `MANUAL_OVERRIDES` keyed by question id. The dict is merged
   into the canonicalized record as the last step of `canonicalize()`, so a
   re-scrape won't regress the fix. Only reach for this after confirming the
   parser can't be fixed generically.

## App architecture (public/app.js)

- `game` object holds: `items`, `idx` (live cursor), `viewIdx` (what's on screen),
  `done`, `answers`, `timerOn`, `paused`, `deadline`, `pausedRemaining`, `mode`.
- Five state-rendering functions: `renderStart`, `renderPlay`, `renderAnswered`,
  `renderDone`, plus `renderCurrent` which dispatches between play/answered based
  on `viewIdx` vs `idx` and the `done` flag.
- `gotoView(newIdx)` is the only legal way to change `viewIdx`. It pauses/resumes
  the timer when crossing in/out of the live question.
- `lockAnswer({timedOut})` is the only legal way to record an answer; it pushes
  to `game.answers` and re-syncs `viewIdx` to `idx`.
- Storage: `localStorage` under key `one-percent-club:v1`, holds settings + lifetime
  stats only. Game state is **not** persisted across reloads.

## Testing

There's no formal test runner. Useful commands:

```bash
node -c public/app.js                # JS syntax check
node scraper/smoke.js                # validate questions.json (run after every parser change)
```

For UI changes, **Chrome headless screenshots are the verification path**:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless=new --disable-gpu --hide-scrollbars \
  --user-data-dir=/tmp/chrome-test \
  --window-size=520,1500 --force-device-scale-factor=1 \
  --virtual-time-budget=4000 \
  --screenshot=/tmp/shot.png \
  "http://localhost:3003/?autostart=full"
```

Note: `--headless=new` viewport is **500px**, not whatever you pass to
`--window-size`. Set window-size to 500+ and design for that. The 375px overflow
I "saw" in screenshots was a Chrome headless artefact, not a real layout bug —
verify with a real browser before chasing layout fixes.

## Anti-goals

- ❌ No build step / bundler / framework. Tailwind is via CDN; that's fine.
- ❌ No external services or analytics. Everything is local.
- ❌ Don't fabricate "in the style of" questions — every question must have a real
  source URL. If a parsed question is unplayable, drop it.
- ❌ Don't add backwards-compat shims to the question schema; if you change the
  schema, re-run the build and bump the localStorage key.
