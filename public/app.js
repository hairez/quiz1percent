// The 1% Club — practice quiz. Vanilla JS, no build step.
// Loads ./questions.json, picks 15 questions (one per difficulty tier in full-game mode,
// or random shuffle), runs through the play/answer/done state machine.

(() => {
  const TIERS = [90, 80, 70, 60, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 1];
  const QUESTION_COUNT = 15;
  const TIMER_SECONDS = 30;
  const STORAGE_KEY = 'one-percent-club:v1';

  /** @type {{questions: any[], settings: any, stats: any}} */
  const store = loadStore();

  /** Mutable game state — replaced when starting a new game. */
  let game = null; // { mode, items, idx, timerOn, paused, deadline, paused_at, answers }
  let timerHandle = null;

  // ---------- Storage ----------
  function loadStore() {
    let s = {};
    try { s = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch {}
    return {
      questions: [],
      settings: Object.assign({ timerOn: true, mode: 'full' }, s.settings || {}),
      stats: Object.assign({ played: 0, answered: 0, correct: 0 }, s.stats || {}),
    };
  }
  function saveStore() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ settings: store.settings, stats: store.stats }));
    } catch {}
  }

  // ---------- Utilities ----------
  function tierColor(d) {
    if (d >= 70) return { bg: 'bg-emerald-500/10', text: 'text-emerald-300', border: 'border-emerald-400/20', solid: '#10b981' };
    if (d >= 40) return { bg: 'bg-amber-500/10', text: 'text-amber-300', border: 'border-amber-400/20', solid: '#f59e0b' };
    if (d >= 15) return { bg: 'bg-orange-500/10', text: 'text-orange-300', border: 'border-orange-400/20', solid: '#f97316' };
    return { bg: 'bg-rose-500/10', text: 'text-rose-300', border: 'border-rose-400/20', solid: '#f43f5e' };
  }
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }
  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
  function normalize(s) {
    return (s || '').toString().toLowerCase().replace(/['’]/g, '').replace(/[^\w\s]/g, ' ').replace(/\s+/g, ' ').trim();
  }
  function escHtml(s) {
    return (s || '').toString()
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function formatQuestion(text) {
    // Preserve paragraph breaks; escape HTML
    return escHtml(text).replace(/\n\n+/g, '</p><p class="mt-3">').replace(/\n/g, '<br>');
  }
  function isPlaceholderMC(q) {
    return q.type === 'mc' && Array.isArray(q.options)
      && q.options.every(o => /^\([A-E]\)$/.test(String(o).trim()));
  }
  function checkTextAnswer(input, accepted) {
    if (!accepted || !accepted.length) return false;
    const n = normalize(input);
    if (!n) return false;
    return accepted.some(a => normalize(a) === n);
  }

  // ---------- Game construction ----------
  function buildFullGame(qs) {
    const out = [];
    for (const tier of TIERS) {
      const pool = qs.filter(q => q.difficulty === tier);
      if (pool.length === 0) continue;
      out.push(pick(pool));
    }
    return out; // already in descending difficulty (90 first)
  }
  function buildRandomGame(qs) {
    return shuffle(qs).slice(0, QUESTION_COUNT);
  }

  function startGame(mode) {
    const items = mode === 'random' ? buildRandomGame(store.questions) : buildFullGame(store.questions);
    if (!items.length) {
      alert('No questions loaded.');
      return;
    }
    game = {
      mode,
      items,
      idx: 0,
      viewIdx: 0,
      timerOn: !!store.settings.timerOn,
      paused: false,
      deadline: 0,
      pausedRemaining: 0,
      answers: [], // { id, correct, user, time_left, locked }
    };
    store.stats.played = (store.stats.played || 0) + 1;
    saveStore();
    renderCurrent();
  }

  // Render whichever screen is appropriate for game.viewIdx.
  function renderCurrent() {
    if (!game) return;
    if (!game.done && game.viewIdx === game.idx && !game.answers[game.idx]) {
      renderPlay();
    } else {
      renderAnswered();
    }
  }
  function gotoView(newIdx) {
    if (!game) return;
    const max = game.done ? game.items.length - 1 : game.idx;
    if (newIdx < 0 || newIdx > max) return;
    const wasLive = !game.done && game.viewIdx === game.idx && !game.answers[game.idx];
    const willBeLive = !game.done && newIdx === game.idx && !game.answers[game.idx];
    if (wasLive && !willBeLive) pauseTimer();
    game.viewIdx = newIdx;
    renderCurrent();
    if (!wasLive && willBeLive) resumeTimer();
  }

  // ---------- Timer ----------
  function startTimer() {
    if (!game.timerOn) return;
    game.deadline = Date.now() + TIMER_SECONDS * 1000;
    tickTimer();
  }
  function tickTimer() {
    if (timerHandle) cancelAnimationFrame(timerHandle);
    const update = () => {
      const bar = document.getElementById('timer-bar');
      const label = document.getElementById('timer-label');
      if (!bar || !game) return;
      if (game.paused) return;
      const remaining = Math.max(0, game.deadline - Date.now());
      const frac = remaining / (TIMER_SECONDS * 1000);
      bar.style.transform = `scaleX(${frac})`;
      if (label) label.textContent = `${(remaining / 1000).toFixed(1)}s`;
      if (remaining <= 0) {
        lockAnswer({ timedOut: true });
        return;
      }
      timerHandle = requestAnimationFrame(update);
    };
    update();
  }
  function pauseTimer() {
    if (!game || !game.timerOn) return;
    game.paused = true;
    game.pausedRemaining = Math.max(0, game.deadline - Date.now());
    if (timerHandle) cancelAnimationFrame(timerHandle);
  }
  function resumeTimer() {
    if (!game || !game.timerOn) return;
    game.paused = false;
    game.deadline = Date.now() + game.pausedRemaining;
    tickTimer();
  }
  function stopTimer() {
    if (timerHandle) cancelAnimationFrame(timerHandle);
    timerHandle = null;
  }

  // ---------- Answer handling ----------
  let pendingAnswer = null; // { type: 'mc'|'text', value }

  function lockAnswer(opts = {}) {
    if (!game) return;
    const q = game.items[game.idx];
    const tier = tierColor(q.difficulty);
    const remainingMs = game.timerOn ? Math.max(0, game.deadline - Date.now()) : null;
    stopTimer();
    let userAnswer = null, correct = false, timedOut = !!opts.timedOut;

    if (timedOut) {
      userAnswer = pendingAnswer ? pendingAnswer.value : null;
    } else if (pendingAnswer) {
      userAnswer = pendingAnswer.value;
    }

    if (q.type === 'mc') {
      if (typeof userAnswer === 'number') {
        correct = userAnswer === q.correct_index;
      }
    } else {
      if (typeof userAnswer === 'string' && userAnswer.trim()) {
        correct = checkTextAnswer(userAnswer, q.accepted_answers || []);
      }
    }

    game.answers.push({
      id: q.id,
      difficulty: q.difficulty,
      type: q.type,
      user: userAnswer,
      correct,
      timedOut,
      time_left_ms: remainingMs,
    });
    store.stats.answered = (store.stats.answered || 0) + 1;
    if (correct) store.stats.correct = (store.stats.correct || 0) + 1;
    saveStore();
    pendingAnswer = null;
    game.viewIdx = game.idx;
    renderAnswered();
  }

  function next() {
    if (!game) return;
    game.idx += 1;
    game.viewIdx = game.idx;
    game.deadline = 0;
    game.paused = false;
    if (game.idx >= game.items.length) {
      game.done = true;
      renderDone();
      return;
    }
    renderPlay();
  }

  // ---------- Rendering ----------
  const app = () => document.getElementById('app');

  function renderHeaderStats() {
    const el = document.getElementById('header-stats');
    if (!el) return;
    const s = store.stats;
    if (s.answered) {
      const pct = s.answered ? Math.round((100 * s.correct) / s.answered) : 0;
      el.textContent = `lifetime ${s.correct}/${s.answered} · ${pct}%`;
    } else {
      el.textContent = '';
    }
  }

  function renderStart() {
    renderHeaderStats();
    const total = store.questions.length;
    const tiers = new Set(store.questions.map(q => q.difficulty));
    const withImage = store.questions.filter(q => q.question_image).length;
    app().innerHTML = `
      <section class="pt-12 slide-up">
        <h1 class="font-display text-[2.4rem] sm:text-5xl leading-[1.05] tracking-tight text-stone-100">
          Train for the <span class="text-amber-400">1%</span>.
        </h1>
        <p class="mt-5 text-stone-400 leading-relaxed max-w-md">
          ${total} verified questions sourced from past UK and US episodes &mdash;
          ${withImage} with original on-screen visuals, all 15 difficulty tiers from 90% down to 1%.
        </p>

        <div class="mt-10 space-y-3">
          <button id="start-full"
            class="w-full text-left rounded-md border border-amber-400/30 bg-amber-500/[0.04] hover:bg-amber-500/[0.08] hover:border-amber-400/60 transition px-5 py-4 group">
            <div class="font-display text-lg text-stone-100">Full game</div>
            <div class="text-xs text-stone-500 mt-1 font-mono">90 → 80 → 70 → … → 5 → 1 &nbsp;·&nbsp; 15 questions</div>
          </button>
          <button id="start-random"
            class="w-full text-left rounded-md border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] hover:border-white/20 transition px-5 py-4">
            <div class="font-display text-lg text-stone-100">Random shuffle</div>
            <div class="text-xs text-stone-500 mt-1 font-mono">15 questions, any order</div>
          </button>
        </div>

        <div class="mt-10 flex items-center gap-3 text-sm">
          <label class="inline-flex items-center gap-2 cursor-pointer select-none text-stone-400">
            <input id="timer-toggle" type="checkbox" ${store.settings.timerOn ? 'checked' : ''}
              class="appearance-none w-9 h-5 rounded-full bg-ink-700 border border-white/10 relative cursor-pointer
                     checked:bg-amber-500/40 transition before:content-[''] before:absolute before:top-[2px] before:left-[2px]
                     before:w-[14px] before:h-[14px] before:rounded-full before:bg-stone-300 before:transition
                     checked:before:translate-x-4 checked:before:bg-amber-300" />
            <span class="font-mono text-xs uppercase tracking-wider">${TIMER_SECONDS}s timer</span>
          </label>
          ${tiers.size < TIERS.length ? `<span class="font-mono text-[10px] text-rose-400/80">missing tiers: ${TIERS.filter(t => !tiers.has(t)).join(', ')}</span>` : ''}
        </div>

        ${store.stats.answered > 0 ? `
        <div class="mt-12 pt-6 border-t border-white/5 text-stone-500 text-xs font-mono">
          you've answered ${store.stats.correct}/${store.stats.answered} correctly across ${store.stats.played} sessions
        </div>` : ''}
      </section>
    `;
    document.getElementById('start-full').onclick = () => startGame('full');
    document.getElementById('start-random').onclick = () => startGame('random');
    document.getElementById('timer-toggle').onchange = (e) => {
      store.settings.timerOn = !!e.target.checked;
      saveStore();
    };
  }

  function renderPlay() {
    pendingAnswer = null;
    const q = game.items[game.idx];
    const tier = tierColor(q.difficulty);
    const isMC = q.type === 'mc';
    const optionLetters = ['A', 'B', 'C', 'D', 'E'];

    app().innerHTML = `
      <div class="pt-4 slide-up">
        <div class="flex items-center justify-between gap-3 mb-4">
          <div class="flex items-center gap-3 min-w-0">
            ${game.idx > 0 ? `<button id="prev" aria-label="review previous" class="font-mono text-[11px] text-stone-500 hover:text-stone-200 uppercase tracking-wider">← prev</button>` : ''}
            <span class="difficulty-badge ${tier.bg} ${tier.text} border ${tier.border}">${q.difficulty}% question</span>
            <span class="font-mono text-[11px] text-stone-500 truncate">
              ${q.show_version.toUpperCase()} · S${q.season} · E${q.episode} &nbsp;·&nbsp; ${game.idx + 1}/${game.items.length}
            </span>
          </div>
          <button id="quit" class="text-[11px] font-mono text-stone-500 hover:text-stone-300 uppercase tracking-wider">quit</button>
        </div>

        <div class="relative h-[3px] bg-white/5 rounded-full overflow-hidden mb-6 ${game.timerOn ? '' : 'invisible'}">
          <div id="timer-bar" class="timer-bar w-full" style="transform: scaleX(1)"></div>
          <button id="timer-pause" aria-label="pause timer"
            class="absolute -right-1 -top-2 w-5 h-5 rounded-full bg-ink-700 border border-white/10 flex items-center justify-center text-stone-400 hover:text-stone-200 hover:border-white/30">
            <svg id="pause-icon" width="8" height="10" viewBox="0 0 8 10" fill="currentColor"><rect width="2.5" height="10" rx="0.5"/><rect x="5.5" width="2.5" height="10" rx="0.5"/></svg>
          </button>
        </div>
        <div class="flex justify-end -mt-5 mb-3 ${game.timerOn ? '' : 'hidden'}">
          <span id="timer-label" class="font-mono text-[10px] text-stone-500"></span>
        </div>

        <h2 class="font-display text-[1.55rem] sm:text-3xl leading-snug text-stone-100 tracking-tight">
          <p>${formatQuestion(q.question_text)}</p>
        </h2>

        ${q.question_image ? `
          <div class="mt-6">
            <img src="./${q.question_image}" alt="Question visual" class="question-image" onerror="this.outerHTML='<div class=\\'rounded border border-rose-400/20 bg-rose-500/[0.04] text-rose-300/80 px-4 py-3 font-mono text-xs\\'>image unavailable</div>'" />
          </div>` : ''}

        <div class="mt-8" id="answer-zone">
          ${isMC ? (isPlaceholderMC(q) ? `
            <p class="font-mono text-[11px] text-stone-500 mb-3 uppercase tracking-wider">Pick the lettered choice from the image</p>
            <div class="grid gap-2" style="grid-template-columns: repeat(${Math.min(q.options.length, 4)}, minmax(0, 1fr))">
              ${q.options.map((_opt, i) => `
                <button class="ans-btn rounded-md py-5 text-center font-display text-2xl" data-idx="${i}">
                  ${optionLetters[i]}
                </button>
              `).join('')}
            </div>
          ` : `
            <div class="grid gap-2">
              ${q.options.map((opt, i) => `
                <button class="ans-btn rounded-md px-4 py-3 text-left flex items-start gap-3" data-idx="${i}">
                  <span class="font-mono text-xs text-stone-500 mt-1">${optionLetters[i]}</span>
                  <span class="font-display text-lg leading-snug">${escHtml(opt)}</span>
                </button>
              `).join('')}
            </div>
          `) : `
            <form id="text-form" class="flex items-stretch gap-2">
              <input id="text-input" type="text" autocomplete="off" autocapitalize="off" spellcheck="false"
                class="text-answer flex-1 rounded-md px-4 py-3 font-display text-lg" placeholder="Your answer…" />
            </form>
            <p class="mt-2 text-[11px] font-mono text-stone-500">case-insensitive · press <kbd>↵</kbd> to lock in</p>
          `}
        </div>

        <div class="mt-8">
          <button id="lock"
            class="w-full rounded-md px-5 py-3 font-display text-lg transition bg-amber-500 text-ink-950 hover:bg-amber-400 disabled:bg-ink-700 disabled:text-stone-500 disabled:cursor-not-allowed"
            disabled>Lock in answer</button>
        </div>
      </div>
    `;

    document.getElementById('quit').onclick = () => {
      if (confirm('End this game?')) { stopTimer(); game = null; renderStart(); }
    };
    const prevBtn = document.getElementById('prev');
    if (prevBtn) prevBtn.onclick = () => gotoView(game.viewIdx - 1);

    const lockBtn = document.getElementById('lock');

    if (isMC) {
      const buttons = app().querySelectorAll('.ans-btn');
      buttons.forEach(btn => {
        btn.onclick = () => {
          const idx = Number(btn.dataset.idx);
          pendingAnswer = { type: 'mc', value: idx };
          buttons.forEach(b => b.classList.remove('selected'));
          btn.classList.add('selected', 'pulse-once');
          setTimeout(() => btn.classList.remove('pulse-once'), 600);
          lockBtn.disabled = false;
        };
      });
    } else {
      const form = document.getElementById('text-form');
      const input = document.getElementById('text-input');
      input.addEventListener('input', () => {
        pendingAnswer = { type: 'text', value: input.value };
        lockBtn.disabled = !input.value.trim();
      });
      form.onsubmit = (e) => { e.preventDefault(); if (pendingAnswer && pendingAnswer.value) lockAnswer(); };
      setTimeout(() => input.focus(), 50);
    }

    lockBtn.onclick = () => { if (pendingAnswer) lockAnswer(); };

    if (game.timerOn) {
      const pauseBtn = document.getElementById('timer-pause');
      pauseBtn.onclick = () => {
        if (game.paused) { resumeTimer(); pauseBtn.querySelector('#pause-icon').innerHTML = '<rect width="2.5" height="10" rx="0.5"/><rect x="5.5" width="2.5" height="10" rx="0.5"/>'; }
        else { pauseTimer(); pauseBtn.querySelector('#pause-icon').innerHTML = '<polygon points="0,0 8,5 0,10" />'; }
      };
      startTimer();
    }
  }

  function renderAnswered() {
    const idx = game.viewIdx;
    const q = game.items[idx];
    const a = game.answers[idx];
    const tier = tierColor(q.difficulty);
    const isMC = q.type === 'mc';
    const optionLetters = ['A', 'B', 'C', 'D', 'E'];
    const inReview = game.done || idx < game.idx;

    const userDisplay = (() => {
      if (a.timedOut && a.user == null) return 'No answer (time up)';
      if (isMC) return typeof a.user === 'number' ? `(${optionLetters[a.user]}) ${q.options[a.user]}` : '—';
      return a.user || '—';
    })();
    const correctDisplay = isMC
      ? `(${optionLetters[q.correct_index]}) ${q.options[q.correct_index]}`
      : (q.correct_text || (q.accepted_answers || [])[0] || '—');

    app().innerHTML = `
      <div class="pt-4 slide-up">
        <div class="flex items-center justify-between gap-3 mb-4">
          <div class="flex items-center gap-3 min-w-0">
            ${idx > 0 ? `<button id="prev" aria-label="previous" class="font-mono text-[11px] text-stone-500 hover:text-stone-200 uppercase tracking-wider">← prev</button>` : ''}
            <span class="difficulty-badge ${tier.bg} ${tier.text} border ${tier.border}">${q.difficulty}% question</span>
            <span class="font-mono text-[11px] text-stone-500 truncate">
              ${q.show_version.toUpperCase()} · S${q.season} · E${q.episode} &nbsp;·&nbsp; ${idx + 1}/${game.items.length}
            </span>
          </div>
          ${inReview ? `<span class="font-mono text-[10px] text-amber-400/70 uppercase tracking-wider">reviewing</span>` : ''}
        </div>

        <h2 class="font-display text-[1.4rem] sm:text-2xl leading-snug text-stone-400 tracking-tight">
          <p>${formatQuestion(q.question_text)}</p>
        </h2>

        ${q.question_image ? `
          <div class="mt-5">
            <img src="./${q.question_image}" alt="Question visual" class="question-image opacity-70" onerror="this.style.display='none'" />
          </div>` : ''}

        <div class="mt-6 grid gap-2" ${isMC && isPlaceholderMC(q) ? `style="grid-template-columns: repeat(${Math.min(q.options.length, 4)}, minmax(0, 1fr))"` : ''} aria-hidden="true">
          ${isMC ? q.options.map((opt, i) => {
            const isCorrect = i === q.correct_index;
            const isUser = i === a.user;
            const cls = isCorrect ? 'correct' : (isUser ? 'wrong' : 'dim');
            if (isPlaceholderMC(q)) {
              return `<div class="ans-btn rounded-md py-5 text-center font-display text-2xl ${cls}">
                ${optionLetters[i]}${isCorrect ? '<div class="font-mono text-[9px] text-emerald-300 mt-1">CORRECT</div>' : (isUser && !isCorrect ? '<div class="font-mono text-[9px] text-rose-300 mt-1">YOUR PICK</div>' : '')}
              </div>`;
            }
            return `<div class="ans-btn rounded-md px-4 py-3 flex items-start gap-3 ${cls}">
              <span class="font-mono text-xs text-stone-500 mt-1">${optionLetters[i]}</span>
              <span class="font-display text-lg leading-snug flex-1">${escHtml(opt)}</span>
              ${isCorrect ? '<span class="font-mono text-[10px] text-emerald-300 mt-1">CORRECT</span>' : (isUser && !isCorrect ? '<span class="font-mono text-[10px] text-rose-300 mt-1">YOUR PICK</span>' : '')}
            </div>`;
          }).join('') : ''}
        </div>

        <div class="mt-7 rounded-md border border-white/10 bg-white/[0.03] p-5 slide-up">
          <div class="flex items-center gap-3 mb-3">
            <span class="font-display text-2xl ${a.correct ? 'text-emerald-400' : 'text-rose-400'}">
              ${a.correct ? '✓ Correct' : (a.timedOut && a.user == null ? '⏱ Time up' : '✗ Incorrect')}
            </span>
          </div>
          ${!isMC ? `
            <dl class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1 text-sm">
              <dt class="text-stone-500 font-mono text-[11px] uppercase tracking-wider">your answer</dt>
              <dd class="${a.correct ? 'text-emerald-300' : 'text-rose-300'}">${escHtml(userDisplay)}</dd>
              <dt class="text-stone-500 font-mono text-[11px] uppercase tracking-wider">correct</dt>
              <dd class="text-stone-200">${escHtml(correctDisplay)}</dd>
            </dl>` : ''}
          ${q.explanation ? `
            <p class="mt-3 text-sm text-stone-400 leading-relaxed">${escHtml(q.explanation)}</p>
          ` : ''}
          ${q.notes ? `<p class="mt-2 text-[11px] font-mono text-stone-500">${escHtml(q.notes)}</p>` : ''}
        </div>

        <div class="mt-8 grid ${game.done ? 'grid-cols-[1fr_auto] gap-2' : 'grid-cols-1'}">
          <button id="next-btn" class="rounded-md px-5 py-3 font-display text-lg transition ${inReview ? 'border border-white/15 bg-white/[0.03] hover:bg-white/[0.06] text-stone-200' : 'bg-amber-500 text-ink-950 hover:bg-amber-400'}">
            ${(() => {
              if (game.done) {
                return idx + 1 < game.items.length ? 'Forward →' : 'Back to results 🏆';
              }
              if (inReview) {
                return idx + 1 < game.idx ? 'Forward →' : `Back to question ${game.idx + 1} →`;
              }
              return game.idx + 1 >= game.items.length ? 'See results 🏆' : 'Next question →';
            })()}
          </button>
          ${game.done ? `<button id="results-btn" class="rounded-md px-4 py-3 font-mono text-xs uppercase tracking-wider border border-white/10 hover:border-white/30 text-stone-400 hover:text-stone-200">Results</button>` : ''}
        </div>
      </div>
    `;
    const prevBtn = document.getElementById('prev');
    if (prevBtn) prevBtn.onclick = () => gotoView(idx - 1);
    document.getElementById('next-btn').onclick = (() => {
      if (game.done) {
        return idx + 1 < game.items.length ? () => gotoView(idx + 1) : renderDone;
      }
      return inReview ? () => gotoView(idx + 1) : next;
    })();
    const resultsBtn = document.getElementById('results-btn');
    if (resultsBtn) resultsBtn.onclick = renderDone;
  }

  function verdictLine(answers) {
    const items = game.items;
    if (game.mode === 'random') {
      const c = answers.filter(a => a.correct).length;
      if (c === items.length) return "Perfect run. Bring this energy to Stockholm.";
      if (c >= 12) return "Strong run. You'd hold your own on the show.";
      if (c >= 8) return "Solid mid-game. Sharpen the trickier ones.";
      if (c >= 4) return "Warming up. The patterns will start to click.";
      return "Early days. Keep training.";
    }
    // Full-game mode: how deep did you go before stumbling?
    let deepest = null;
    for (const a of answers) {
      if (a.correct) deepest = a;
      else break;
    }
    if (deepest && deepest.difficulty === 1) {
      return "You'd win the show. You are the 1%.";
    }
    if (deepest) {
      const next = items.find(q => q.difficulty < deepest.difficulty);
      if (next) return `You'd be a finalist. Eliminated at the ${next.difficulty}% question.`;
      return `You cleared every tier from 90% down to ${deepest.difficulty}%.`;
    }
    return "Eliminated at the very first question. Shake it off, run it again.";
  }

  function renderDone() {
    stopTimer();
    const correct = game.answers.filter(a => a.correct).length;
    const total = game.items.length;
    const pct = Math.round((100 * correct) / total);
    app().innerHTML = `
      <div class="pt-8 slide-up">
        <div class="text-stone-500 font-mono text-xs uppercase tracking-[0.18em]">final score</div>
        <div class="font-display text-7xl sm:text-8xl tracking-tight text-stone-100 mt-2">
          ${correct}<span class="text-stone-600">/${total}</span>
        </div>
        <div class="font-mono text-stone-500 mt-1">${pct}%</div>
        <p class="mt-6 font-display text-xl text-amber-300 leading-snug">${verdictLine(game.answers)}</p>

        <p class="mt-10 mb-3 font-mono text-[11px] text-stone-500 uppercase tracking-wider">Tap a row to review &middot; ←/→ to navigate</p>
        <div class="space-y-1.5">
          ${game.items.map((q, i) => {
            const a = game.answers[i];
            const tier = tierColor(q.difficulty);
            const ok = a && a.correct;
            return `
              <button data-review="${i}" class="recap-row w-full text-left rounded border ${tier.border} ${tier.bg} px-3 py-2.5 flex items-start gap-3 hover:border-white/30 hover:brightness-125 transition">
                <span class="font-mono text-[11px] ${tier.text} w-9 text-right pt-0.5">${q.difficulty}%</span>
                <span class="font-mono text-[11px] mt-0.5 ${ok ? 'text-emerald-400' : 'text-rose-400'}">${ok ? '✓' : '✗'}</span>
                <span class="font-display text-sm leading-snug text-stone-300 flex-1 line-clamp-2">${escHtml(q.question_text.split('\n')[0].slice(0, 140))}</span>
                <span class="font-mono text-[10px] text-stone-500 mt-0.5 hidden sm:inline">review →</span>
              </button>`;
          }).join('')}
        </div>

        <div class="mt-10 grid grid-cols-2 gap-3">
          <button id="play-again" class="rounded-md px-5 py-3 font-display text-lg bg-amber-500 text-ink-950 hover:bg-amber-400 transition">
            Play again
          </button>
          <button id="back-home" class="rounded-md px-5 py-3 font-display text-lg border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] hover:border-white/20 text-stone-200 transition">
            Home
          </button>
        </div>
      </div>
    `;
    document.getElementById('play-again').onclick = () => startGame(game.mode);
    document.getElementById('back-home').onclick = () => { game = null; renderStart(); };
    app().querySelectorAll('.recap-row').forEach(btn => {
      btn.onclick = () => gotoView(Number(btn.dataset.review));
    });
  }

  // ---------- Boot ----------
  async function boot() {
    try {
      const res = await fetch('./questions.json', { cache: 'no-store' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      store.questions = await res.json();
    } catch (err) {
      app().innerHTML = `
        <div class="pt-12">
          <h1 class="font-display text-3xl text-rose-400">Couldn't load questions</h1>
          <p class="mt-3 text-stone-400">${escHtml(err.message)}</p>
          <p class="mt-2 text-stone-500 text-sm">Make sure questions.json is present and you're loading via the local server.</p>
        </div>`;
      return;
    }
    // ?autostart=full or ?autostart=random skips the start screen.
    const params = new URLSearchParams(location.search);
    const auto = params.get('autostart');
    if (auto === 'full' || auto === 'random') { startGame(auto); return; }
    renderStart();
  }

  // Keyboard shortcuts (only meaningful during play / answered)
  window.addEventListener('keydown', (e) => {
    if (!game) return;
    const tag = (e.target.tagName || '').toLowerCase();
    const isInput = tag === 'input' || tag === 'textarea';

    // Left arrow always reviews the previous question (when one exists).
    if (e.key === 'ArrowLeft' && !isInput && game.viewIdx > 0) {
      e.preventDefault(); gotoView(game.viewIdx - 1); return;
    }

    const inReview = game.viewIdx < game.idx;
    const onAnswered = inReview || !!game.answers[game.idx];

    if (onAnswered) {
      // Enter/Space/Right advances. In review: forward. On freshly-answered: next.
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowRight') {
        e.preventDefault();
        if (inReview) gotoView(game.viewIdx + 1);
        else next();
      }
      return;
    }

    const q = game.items[game.idx];
    if (!q) return;
    if (q.type === 'mc' && !isInput) {
      const i = ['a','b','c','d','e'].indexOf(e.key.toLowerCase());
      if (i >= 0 && i < q.options.length) {
        const btn = document.querySelector(`.ans-btn[data-idx="${i}"]`);
        if (btn) { btn.click(); }
      } else if (e.key === 'Enter' && pendingAnswer) {
        e.preventDefault(); lockAnswer();
      }
    }
  });

  boot();
})();
