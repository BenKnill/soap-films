// Relax the frame films with the page's own minimiser and write them out for Blender: vertices, triangles, a
// film-thickness field (nm), the wires, the triple lines and the junctions.
require("../docs/surface.js"); require("../docs/catenoid.js"); require("../docs/film3d.js");
const fs = require("fs"), { tetrahedron, cube } = globalThis.Surface;
const thickness = (V, top = 250, bottom = 1100) => { let lo = Infinity, hi = -Infinity; for (const v of V) { lo = Math.min(lo, v[1]); hi = Math.max(hi, v[1]); }
  return V.map(v => { const u = (hi - v[1]) / (hi - lo + 1e-9); return top + (bottom - top) * Math.pow(u, 1.6) + 90 * Math.sin(3.1 * v[0] + 2.0 * Math.sin(2.3 * v[2])) * Math.sin(2.7 * v[2] + 1.7 * Math.sin(1.9 * v[1])); }); };
function dump(name, f, maxIt) {
  let it = 0; for (; it < maxIt; it++) if (f.step() < 1e-8) break;
  const lines = globalThis.Film3D.tripleLines(f);
  const out = { V: f.V, tris: f.tris, D: thickness(f.V), wires: f.wires, lines, junctions: f.junctions.map(j => f.V[j]), area: f.area() };
  fs.writeFileSync(`blender/${name}.json`, JSON.stringify(out)); console.log(name, "iters", it, "verts", f.V.length, "area", out.area.toFixed(4));
}
dump("tetra", tetrahedron(20), 40000);
dump("cube", cube(16), 60000);
