import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { polygon, rng, wilson, validTree, settle, cell } from './success.mjs';

const fixtures = [
  { pins: polygon(3), expected: 3, count: 1 },
  { pins: [{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 1, y: 1 }, { x: 0, y: 1 }], expected: 1 + Math.sqrt(3), count: 3 },
  { pins: [{ x: -1, y: 0 }, { x: 1, y: 0 }, { x: 0, y: 0.1 }], expected: 2 * Math.hypot(1, 0.1), count: 1 },
  { pins: polygon(6), expected: 5, count: 105 },
];
const oracle = spawnSync(fileURLToPath(new URL('../.venv/bin/python', import.meta.url)),
  [fileURLToPath(new URL('./optimum.py', import.meta.url))], {
    input: JSON.stringify(fixtures.map(f => f.pins.map(p => [p.x, p.y]))), encoding: 'utf8', timeout: 120000,
  });
assert.equal(oracle.status, 0, oracle.stderr);
const references = JSON.parse(oracle.stdout);
for (let i = 0; i < fixtures.length; i++) {
  const { pins, expected, count } = fixtures[i], ref = references[i];
  assert.equal(ref.topologies, count);
  assert.ok(ref.lower <= expected + 1e-9 && ref.upper >= expected - 1e-9);
  assert.ok(ref.upper - ref.lower < 1e-7);
  const net = Steiner.Network(pins, rng(42)).dip();
  settle(net);
  assert.ok(validTree(net));
  assert.ok(net.length() >= ref.lower - 1e-8);
  net.edges.pop();
  assert.equal(validTree(net), false);
}
assert.ok(wilson(0, 1000)[1] < 0.004);
assert.ok(wilson(1000, 1000)[0] > 0.996);
assert.deepEqual(cell({ n: 3, shake: 0.15, dips: 10, reference: references[0] }),
  cell({ n: 3, shake: 0.15, dips: 10, reference: references[0] }));
assert.equal(settle(Steiner.Network(polygon(3), rng(42)).dip(), 0).converged, false);
console.log('PASS: independent optimum fixtures, degeneracy, topology counts, tree validity, seeded reproducibility, Wilson boundaries and iteration cap');
