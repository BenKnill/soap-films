import assert from 'node:assert/strict';
import '../docs/steiner.js';
import '../docs/surface.js';
import '../docs/live-model.js';
const M = SoapModels;
// These are independent geometry checks, not copied display strings.
for (let i = 0; i < 2; i++) {
  const net = M.network(i), seen = new Set([0]);
  for (let j = 0; j < net.pins.length + net.jx.length; j++) for (const [a, b] of net.edges) {
    if (seen.has(a)) seen.add(b); if (seen.has(b)) seen.add(a);
  }
  assert.equal(seen.size, net.pins.length + net.jx.length, 'network must connect every pin and junction');
  assert.equal(net.edges.length, seen.size - 1, 'network is a connected tree');
  assert.ok(net.jx.every((_, j) => net.nbrs(net.pins.length + j).length === 3));
}
const first = M.network(0), second = M.network(1);
assert.ok(Math.abs(first.length() - Math.sqrt(27)) < 1e-6);
assert.ok(Math.abs(second.length() - 5) < 1e-6);
assert.ok(first.length() > M.referenceLength + .1);
assert.ok(Math.abs(M.referenceLength - 5) < 1e-12);
// Interior free junctions should have approximately 120-degree turns after relaxation.
for (let i = 0; i < first.jx.length; i++) {
  const p = first.jx[i], neighbours = first.nbrs(first.pins.length + i).map(first.P);
  for (let a = 0; a < neighbours.length; a++) for (let b = a + 1; b < neighbours.length; b++) {
    const u = [neighbours[a].x - p.x, neighbours[a].y - p.y], v = [neighbours[b].x - p.x, neighbours[b].y - p.y];
    const cosine = (u[0]*v[0] + u[1]*v[1]) / Math.hypot(...u) / Math.hypot(...v);
    assert.ok(Math.abs(cosine + .5) < 1e-4, 'balanced equal-tension junction');
  }
}
const results = { firstLength: first.length(), secondLength: second.length(), referenceLength: M.referenceLength, films: {} };
for (const kind of ['tetrahedron', 'cube']) {
  const f = M.film(kind), model = f.model;
  assert.ok(model.V.flat().every(Number.isFinite));
  assert.ok(model.area() < f.initialArea, 'existing relaxation decreases area');
  assert.ok(model.tripleEdges.length > 0);
  assert.equal(model.junctions.length, kind === 'tetrahedron' ? 1 : 4);
  model.wires.flat().forEach(p => assert.ok(model.V.some(v => Math.hypot(...v.map((x, i) => x-p[i])) < 1e-10), 'wire endpoints remain represented'));
  results.films[kind] = { vertices: model.V.length, triangles: model.tris.length, tripleEdges: model.tripleEdges.length, junctions: model.junctions.length, initialArea: f.initialArea, area: model.area(), digest: M.digest(model.V) };
}
console.log(JSON.stringify({ status: 'PASS', ...results }, null, 2));
