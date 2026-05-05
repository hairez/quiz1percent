# The 1% Club — practice quiz

A localhost-only practice app for *The 1% Club* game show. **639 verified
questions** sourced from publicly available episode recaps (UK seasons 4–5,
US seasons 1–2), **362 of them with the original on-screen visuals**, all 15
difficulty tiers from 90% down to 1%.

Single-page vanilla-JS app. No build step. No framework. Tailwind via CDN.

## Run it

```bash
./serve.sh
# then open http://localhost:3003/
```

Stop with Ctrl-C. Override the port with `PORT=4000 ./serve.sh`.

## Game modes

- **Full game** — picks one question from each of the 15 difficulty tiers
  (90% → 80% → 70% → … → 5% → 1%) and plays them in show order, easiest first.
- **Random shuffle** — 15 questions from any tier in any order.
- **30-second timer** per question, toggleable on the start screen, pausable mid-question.
- **Free-text answers** are case-insensitive and lenient: numbers accept word
  forms (`50` ↔ `fifty`), letter-sequence answers accept `C, A, D, B` / `CADB` /
  `C A D B` interchangeably, leading articles are stripped.

## Reviewing previously-answered questions

- Click **`← prev`** in the top-left of the play screen or the answered screen,
  or press **←**, to step back through questions you've already locked in. The
  timer pauses while you're reviewing and resumes when you return.
- After the game ends, **tap any row in the recap** to jump back into review for
  that question. Use **←/→** to step through, or click **RESULTS** to return to
  the score screen.

## Project layout

```
public/                 # everything the static server hands out
  index.html            # UI shell + Tailwind via CDN, font links
  app.js                # game state machine, timer, navigation, answer checking
  questions.json        # the question bank
  questions/*.jpg       # downloaded question images
scraper/                # one-shot Python pipeline (only re-run to add data)
  fetch.py              # download primary-source HTML to data/raw/
  parse.py              # raw HTML  →  data/questions-raw.json
  build.py              # canonicalize, dedupe, download images, validate
  smoke.js              # node-side sanity check on questions.json
data/raw/               # cached source HTML
SOURCES.md              # primary-source URLs & counts
validation-report.md    # what was dropped during the validation pass
CLAUDE.md               # orientation for an AI agent picking this up
```

## Re-running the scrape

```bash
python3 -m venv .venv && .venv/bin/pip install requests beautifulsoup4 lxml pillow
.venv/bin/python scraper/fetch.py    # respects local cache
.venv/bin/python scraper/parse.py    # raw HTML  →  questions-raw.json
.venv/bin/python scraper/build.py    # canonical questions.json + image download
node scraper/smoke.js                # sanity check
```

Add new sources by appending to `SOURCES` in `scraper/fetch.py` and `scraper/parse.py`.

## Useful URLs

- `http://localhost:3003/?autostart=full` — skip start screen, jump into a full game.
- `http://localhost:3003/?autostart=random` — same, random-shuffle mode.

## Disclaimer

Unofficial fan tool. *The 1% Club* format is owned by BBC Studios. Practice
questions are sourced from publicly available episode recap articles — every
record carries a `source_url` field linking back to its origin.
