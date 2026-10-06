#!/usr/bin/env node
// Record the relaxation of one measured dip, step by step, for the film.
// The dip is the same seeded dip that tools/success.mjs scores (seed 0x51EA0000 + n*10000 + dip, no shake),
// so every network shown in the film is a sample from the measured grid.
//   node film/sims/steiner_traj.mjs N DIP [OUT.json]       one trajectory
//   node film/sims/steiner_traj.mjs --scan N COUNT          lengths and step counts of the first COUNT dips
//   node film/sims/steiner_traj.mjs --finals N COUNT OUT    settled networks of the first COUNT unshaken dips, scored
//                                                          exactly as tools/success.mjs scores them
// Run it where the grid was measured (bluestar26, Node 24): the relaxation is chaotic, and another Node/V8 build
// (the Mac's Node 26) gives different networks for some of the same seeds.
import '../../docs/steiner.js';
import { readFileSync, writeFileSync } from 'node:fs';
import { polygon, rng, settle, validTree } from '../../tools/success.mjs';

function trajectory(n, dip, limit = 8000) {
  const net = Steiner.Network(polygon(n), rng(0x51EA0000 + n * 10000 + dip)).dip();
  const frames = [{ ...net.snapshot(), L: net.length(), ev: 0 }];
  let converged = false;
  for (let i = 0; i < limit; i++) {
    const e0 = net.events.length, moved = net.step();
    frames.push({ ...net.snapshot(), L: net.length(), ev: net.events.length - e0 });
    if (moved < 1e-7 && e0 === net.events.length) { converged = true; break; }
  }
  return { n, dip, pins: net.pins, frames, events: net.events, converged, length: net.length() };
}

const a = process.argv.slice(2);
if (a[0] === '--finals') {
  const n = +a[1], count = +a[2];
  const grid = JSON.parse(readFileSync(new URL('../../results/success-grid.json', import.meta.url)));
  const ref = grid.references.find(r => r.n === n);
  const dips = [];
  for (let dip = 0; dip < count; dip++) {
    const net = Steiner.Network(polygon(n), rng(0x51EA0000 + n * 10000 + dip)).dip();
    settle(net); const r = settle(net);                      // the zero-shake control: two relaxation budgets
    const good = r.length <= ref.lower + 1e-4 * ref.upper;
    dips.push({ dip, length: r.length, converged: r.converged, valid: validTree(net), success: r.converged && good && validTree(net),
                jx: net.jx, edges: net.edges });
  }
  writeFileSync(a[3], JSON.stringify({ n, pins: polygon(n), reference: ref, dips }));
  console.log(`n=${n}: ${dips.filter(d => d.success).length} of the first ${count} unshaken dips found the shortest network`);
} else if (a[0] === '--scan') {
  const n = +a[1], count = +a[2];
  for (let d = 0; d < count; d++) {
    const t = trajectory(n, d);
    console.log(d, t.length.toFixed(6), t.frames.length - 1, t.converged ? 'conv' : 'UNRESOLVED', t.events.map(e => e.type[0]).join(''), 'jx', t.frames.at(-1).jx.length);
  }
} else {
  const t = trajectory(+a[0], +a[1]);
  if (a[2]) writeFileSync(a[2], JSON.stringify(t));
  console.log(`n=${t.n} dip=${t.dip} steps=${t.frames.length - 1} length=${t.length.toFixed(6)} converged=${t.converged} events=${t.events.length}`);
}
