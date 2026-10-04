#!/usr/bin/env node
import '../docs/steiner.js';
import { spawnSync } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { Worker, isMainThread, parentPort, workerData } from 'node:worker_threads';
import { fileURLToPath } from 'node:url';

export const polygon = n => Array.from({ length: n }, (_, i) => ({
  x: Math.cos(2 * Math.PI * i / n), y: Math.sin(2 * Math.PI * i / n),
}));
export function rng(seed) {
  return () => {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
export function wilson(success, total, z = 1.959963984540054) {
  const p = success / total, d = 1 + z * z / total;
  const centre = (p + z * z / (2 * total)) / d;
  const half = z / d * Math.sqrt(p * (1 - p) / total + z * z / (4 * total * total));
  return [Math.max(0, centre - half), Math.min(1, centre + half)];
}
export function pairedComparison(control, shaken) {
  if (control.length !== shaken.length || !control.length) throw Error('invalid paired sample');
  let gained = 0, lost = 0;
  for (let i = 0; i < control.length; i++) {
    if (!control[i] && shaken[i]) gained++;
    if (control[i] && !shaken[i]) lost++;
  }
  // Two 97.5% Wilson intervals give a conservative approximate 95% interval
  // for P(gained)-P(lost) by Bonferroni; no independence between cells assumed.
  const z = 2.241402727604947;
  const up = wilson(gained, control.length, z), down = wilson(lost, control.length, z);
  return { gained, lost, difference: (gained - lost) / control.length,
    ci: [up[0] - down[1], up[1] - down[0]] };
}
export function validTree(net) {
  const count = net.pins.length + net.jx.length;
  if (net.edges.length !== count - 1 || !Number.isFinite(net.length())) return false;
  const visited = new Set([0]);
  for (let i = 0; i < count; i++) for (const [a, b] of net.edges) {
    if (!Number.isInteger(a) || !Number.isInteger(b) || a < 0 || b < 0 || a >= count || b >= count || a === b) return false;
    if (visited.has(a)) visited.add(b);
    if (visited.has(b)) visited.add(a);
  }
  return visited.size === count;
}
export function settle(net, limit = 4000) {
  for (let i = 0; i < limit; i++) {
    const oldEvents = net.events.length;
    const moved = net.step();
    // step() reports pre-topology movement: a flip/peel can move nodes too.
    if (moved < 1e-7 && oldEvents === net.events.length) return { length: net.length(), converged: true };
  }
  return { length: net.length(), converged: false };
}
export function cell({ n, shake, dips, reference }) {
  let success = 0, unresolved = 0, invalid = 0, numericalAmbiguity = 0;
  let sumRatio = 0, maxRatio = 0;
  const outcomes = Array(dips).fill(false);
  for (let dip = 0; dip < dips; dip++) {
    // Pair initial dips across amplitudes. There are no hidden best-of retries.
    const net = Steiner.Network(polygon(n), rng(0x51EA0000 + n * 10000 + dip)).dip();
    settle(net);
    if (shake) {
      net.shake(shake);
    }
    const result = settle(net);
    if (!validTree(net)) { invalid++; continue; }
    if (!result.converged) unresolved++;
    const tolerance = 1e-4 * reference.upper;
    if (result.length < reference.lower - 1e-8) throw Error('film shorter than global lower bound');
    const good = result.length <= reference.lower + tolerance;
    const bad = result.length > reference.upper + tolerance;
    if (!good && !bad) numericalAmbiguity++;
    if (result.converged && good) { success++; outcomes[dip] = true; }
    const ratio = result.length / reference.upper;
    sumRatio += ratio; maxRatio = Math.max(maxRatio, ratio);
  }
  return { n, shake, dips, success, unresolved, invalid, numericalAmbiguity,
    rate: success / dips, ci: wilson(success, dips), meanRatio: sumRatio / (dips - invalid), maxRatio, outcomes };
}

async function grid(dips = 1000) {
  const ns = [3, 4, 5, 6, 7], shakes = [0, 0.15, 0.5];
  const oracle = spawnSync(fileURLToPath(new URL('../.venv/bin/python', import.meta.url)),
    [fileURLToPath(new URL('./optimum.py', import.meta.url))], {
      input: JSON.stringify(ns.map(n => polygon(n).map(p => [p.x, p.y]))), encoding: 'utf8', timeout: 120000,
    });
  if (oracle.error || oracle.status !== 0) throw Error(oracle.error?.message || oracle.stderr);
  const references = JSON.parse(oracle.stdout);
  if (references.length !== ns.length || references.some((r, i) => r.n !== ns[i] || !Number.isFinite(r.lower) || !Number.isFinite(r.upper) || r.upper - r.lower > 1e-7)) throw Error('malformed optimum results');
  const jobs = ns.flatMap((n, i) => shakes.map(shake => ({ n, shake, dips, reference: references[i] })));
  const results = [];
  await Promise.all(Array.from({ length: 4 }, async () => {
    while (jobs.length) {
      const data = jobs.shift();
      const result = await new Promise((resolve, reject) => {
        const worker = new Worker(new URL(import.meta.url), { workerData: data });
        let received = false;
        worker.once('message', value => { received = true; resolve(value); });
        worker.once('error', reject);
        worker.once('exit', code => { if (code || !received) reject(Error(`worker exited ${code} without a result`)); });
      });
      results.push(result);
      console.error(`CELL: n=${result.n} shake=${result.shake} ${result.success}/${dips}, unresolved=${result.unresolved}`);
    }
  }));
  results.sort((a, b) => a.n - b.n || a.shake - b.shake);
  const paired = results.filter(r => r.shake).map(r => ({ n: r.n, shake: r.shake,
    ...pairedComparison(results.find(c => c.n === r.n && c.shake === 0).outcomes, r.outcomes) }));
  for (const r of results) delete r.outcomes;
  const knees = shakes.map(shake => {
    const series = results.filter(r => r.shake === shake);
    const drops = series.slice(1).map((r, i) => ({ from: series[i].n, to: r.n, drop: series[i].rate - r.rate,
      separated: series[i].ci[0] > r.ci[1] }));
    const largest = drops.reduce((a, b) => a.drop >= b.drop ? a : b);
    return { shake, ...largest };
  });
  const pct = x => (100 * x).toFixed(1);
  const lines = ['# Film success grid', '',
    'Regular polygons of unit circumradius; 1,000 independent initial dips per cell (unless marked smoke).',
    'One shake after settling, then settle again. Success = converged connected tree within 0.01% of the exhaustive optimum.',
    'Unresolved and invalid outcomes count as failures. Intervals are marginal 95% Wilson intervals for simulation dip randomness.', '',
    '| n | shake amplitude | successes/dips | success % (95% CI) | unresolved | invalid | mean length/optimum |',
    '|---|---|---|---|---|---|---|'];
  for (const r of results) lines.push(`| ${r.n} | ${r.shake} | ${r.success}/${r.dips} | ${pct(r.rate)} (${pct(r.ci[0])}–${pct(r.ci[1])}) | ${r.unresolved} | ${r.invalid} | ${r.meanRatio.toFixed(6)} |`);
  lines.push('', 'Knee = largest adjacent decrease in success rate over the sampled pin counts.');
  for (const k of knees) lines.push(`- Shake ${k.shake}: n=${k.from}→${k.to}, drop ${pct(k.drop)} percentage points; ${k.separated ? 'non-overlapping' : 'overlapping'} marginal intervals.`);
  lines.push('', 'Paired shake effects versus the same initial dips without shaking; conservative approximate 95% intervals from Bonferroni-combined 97.5% Wilson intervals for gained/lost success probabilities.',
    '', '| n | shake | gained | lost | change in success, percentage points (95% CI) |', '|---|---|---|---|---|');
  for (const p of paired) lines.push(`| ${p.n} | ${p.shake} | ${p.gained} | ${p.lost} | ${pct(p.difference)} (${pct(p.ci[0])}–${pct(p.ci[1])}) |`);
  lines.push('', '| n | exhaustive topologies | optimum lower | optimum upper |', '|---|---|---|---|');
  for (const r of references) lines.push(`| ${r.n} | ${r.topologies} | ${r.lower.toFixed(10)} | ${r.upper.toFixed(10)} |`);
  lines.push('', 'These are simulated networks, not measurements of real soap films. Pin count is confounded with polygon geometry; the knee is specific to this layout family, solver and protocol.');
  const directory = dips === 1000 ? 'results' : 'runs/smoke';
  await mkdir(directory, { recursive: true });
  await writeFile(`${directory}/success-grid.md`, lines.join('\n') + '\n');
  await writeFile(`${directory}/success-grid.json`, JSON.stringify({ protocol: { dips, shakes, ns, tolerance: 1e-4, maxIterations: 4000, seed: '0x51EA0000 + n*10000 + dip' }, references, results, knees, paired }, null, 2) + '\n');
  if (results.some(r => r.invalid || r.numericalAmbiguity)) throw Error('invalid trees or ambiguous reference scoring');
  console.log(`${dips === 1000 ? 'PASS' : 'SMOKE PASS'}: ${results.length} cells × ${dips} dips; table ${directory}/success-grid.md; knees ${knees.map(k => `${k.shake}:${k.from}→${k.to}`).join(', ')}`);
}
if (!isMainThread) parentPort.postMessage(cell(workerData));
else if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const argument = process.argv[2];
  if (argument !== '--grid' && argument !== '--smoke') { console.error('Usage: node tools/success.mjs --grid|--smoke'); process.exitCode = 2; }
  else await grid(argument === '--smoke' ? 10 : 1000).catch(error => { console.error(`FAIL: ${error.message}`); process.exitCode = 1; });
}
