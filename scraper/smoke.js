// Headless smoke test: simulate the answer-checking logic against the canonical answer
// for every question to ensure 100% of questions can be answered correctly.
const fs = require('fs');
const path = require('path');

const TIERS = [90, 80, 70, 60, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 1];

const qs = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'public', 'questions.json'), 'utf-8'));

function normalize(s) {
  return (s || '').toString().toLowerCase().replace(/['’]/g, '').replace(/[^\w\s]/g, ' ').replace(/\s+/g, ' ').trim();
}
function checkText(input, accepted) {
  if (!accepted || !accepted.length) return false;
  const n = normalize(input);
  return accepted.some(a => normalize(a) === n);
}

let issues = 0;
const samples = [];
for (const q of qs) {
  if (q.type === 'mc') {
    if (!Array.isArray(q.options) || q.options.length < 2) {
      console.log(`MC missing options: ${q.id}`); issues++;
    }
    if (typeof q.correct_index !== 'number' || q.correct_index < 0 || q.correct_index >= q.options.length) {
      console.log(`MC bad correct_index: ${q.id} idx=${q.correct_index} options=${q.options.length}`); issues++;
    }
  } else if (q.type === 'text') {
    if (!Array.isArray(q.accepted_answers) || q.accepted_answers.length === 0) {
      console.log(`text missing accepted_answers: ${q.id}`); issues++;
      continue;
    }
    // The "official" answer (correct_text) should be accepted by checkText
    const ok = checkText(q.correct_text, q.accepted_answers);
    if (!ok) {
      issues++;
      if (samples.length < 8) samples.push({id: q.id, correct: q.correct_text, accept: q.accepted_answers});
    }
  } else {
    console.log(`unknown type: ${q.id} = ${q.type}`); issues++;
  }
}
if (samples.length) {
  console.log('\nText answers where checkText(correct_text, accepted) failed:');
  for (const s of samples) console.log(` - ${s.id}: correct=${JSON.stringify(s.correct)} accept=${JSON.stringify(s.accept)}`);
}

// Tier coverage
const byDiff = new Map();
for (const q of qs) byDiff.set(q.difficulty, (byDiff.get(q.difficulty) || 0) + 1);
const missingTiers = TIERS.filter(t => (byDiff.get(t) || 0) === 0);
if (missingTiers.length) {
  console.log(`Missing tiers: ${missingTiers.join(', ')}`);
  issues++;
}

// Pick one per tier — full-game build
const game = [];
for (const t of TIERS) {
  const pool = qs.filter(q => q.difficulty === t);
  if (pool.length) game.push(pool[Math.floor(Math.random() * pool.length)]);
}
console.log(`Full-game build picks: ${game.length}/${TIERS.length} tiers`);

console.log(`\nTotal: ${qs.length} questions, ${issues} issues`);
process.exit(issues > 0 ? 1 : 0);
