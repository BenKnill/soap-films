// The soap film between two coaxial rings of radius R, a distance h apart.
// A catenoid r(z) = a·cosh(z/a) spans them when R = a·cosh(h/2a). Writing x = h/2a, that is cosh x = (2R/h)·x:
// two solutions while h/R < 1.3255 (a fat, stable one and a thin, unstable one), none beyond — the film collapses
// into two flat disks. Its area is π a² (2x + sinh 2x); the two disks have 2πR². The fat catenoid has less area than
// the disks only for h/R < 1.0554; in between it is a local minimum, not the global one, and the film keeps it anyway.
(function (root) {
  const XSTAR = (() => { let x = 1.2; for (let i = 0; i < 60; i++) x -= (Math.tanh(x) - 1 / x) / (1 / Math.cosh(x) ** 2 + 1 / (x * x)); return x; })();   // tanh x = 1/x
  const HR_MAX = 2 * XSTAR / Math.cosh(XSTAR);                     // ≈ 1.3255
  function solve(h, R = 1) {                                        // → { stable: a, unstable: a } or null
    const k = 2 * R / h, f = x => Math.cosh(x) - k * x; if (f(XSTAR) > 0) return null;
    const bis = (lo, hi) => { for (let i = 0; i < 80; i++) { const m = (lo + hi) / 2; (f(lo) * f(m) <= 0) ? hi = m : lo = m; } return (lo + hi) / 2; };
    const x1 = bis(1e-9, XSTAR), x2 = bis(XSTAR, 50); return { stable: h / (2 * x1), unstable: h / (2 * x2), x1, x2 };
  }
  const area = (a, h) => { const x = h / (2 * a); return Math.PI * a * a * (2 * x + Math.sinh(2 * x)); };
  const HR_EQUAL = (() => { let lo = 0.5, hi = HR_MAX - 1e-9; for (let i = 0; i < 80; i++) { const m = (lo + hi) / 2, s = solve(m); (area(s.stable, m) < 2 * Math.PI) ? lo = m : hi = m; } return (lo + hi) / 2; })();
  // the film as a profile r(z) that moves by mean curvature (overdamped): r_t = r_zz/(1+r_z²) − 1/r, ends pinned at R
  function Profile(h, R = 1, M = 161, a0 = null) {
    const p = { h, R, M, z: new Float64Array(M), r: new Float64Array(M), pinched: false, t: 0 };
    const s = solve(h, R), a = a0 ?? (s ? s.stable : R * 0.7);
    for (let i = 0; i < M; i++) { p.z[i] = -h / 2 + h * i / (M - 1); p.r[i] = s || a0 ? a * Math.cosh(p.z[i] / a) : R * (1 - 0.3 * Math.cos(Math.PI * p.z[i] / h) ** 2); }
    p.setH = hNew => { const sc = hNew / p.h; p.h = hNew; for (let i = 0; i < M; i++) p.z[i] *= sc; };      // pulling the rings apart stretches the film
    p.step = (steps = 50) => {
      if (p.pinched) return; const dz = p.h / (M - 1), dt = 0.2 * dz * dz; const r = p.r, rn = new Float64Array(M); rn[0] = rn[M - 1] = p.R;
      for (let s = 0; s < steps; s++) {
        for (let i = 1; i < M - 1; i++) { const rz = (r[i + 1] - r[i - 1]) / (2 * dz), rzz = (r[i + 1] - 2 * r[i] + r[i - 1]) / (dz * dz); rn[i] = r[i] + dt * (rzz / (1 + rz * rz) - 1 / Math.max(r[i], 1e-4)); }
        for (let i = 1; i < M - 1; i++) r[i] = rn[i]; p.t += dt;
        if (Math.min(...r) < 0.02 * p.R) { p.pinched = true; break; }
      }
    };
    p.neck = () => Math.min(...p.r);
    p.area = () => { let A = 0; for (let i = 0; i < M - 1; i++) { const dzz = p.z[i + 1] - p.z[i], dr = p.r[i + 1] - p.r[i]; A += Math.PI * (p.r[i] + p.r[i + 1]) * Math.hypot(dzz, dr); } return A; };
    return p;
  }
  // a surface-of-revolution mesh (axis along y) for the renderer, with a film-thickness field
  function revolve(zs, rs, S = 72, t = 0, thick = {}) {
    const M = zs.length, n = M * (S + 1), P = new Float32Array(n * 3), N = new Float32Array(n * 3), D = new Float32Array(n), I = new Uint32Array((M - 1) * S * 6);
    const top = thick.top ?? 300, bottom = thick.bottom ?? 900, ymin = Math.min(...zs), ymax = Math.max(...zs);
    for (let i = 0; i < M; i++) {
      const dz = (zs[Math.min(M - 1, i + 1)] - zs[Math.max(0, i - 1)]), dr = (rs[Math.min(M - 1, i + 1)] - rs[Math.max(0, i - 1)]), l = Math.hypot(dz, dr) || 1;
      for (let j = 0; j <= S; j++) { const th = 2 * Math.PI * j / S, c = Math.cos(th), s = Math.sin(th), k = i * (S + 1) + j;
        P[3 * k] = rs[i] * c; P[3 * k + 1] = zs[i]; P[3 * k + 2] = rs[i] * s; N[3 * k] = dz / l * c; N[3 * k + 1] = -dr / l; N[3 * k + 2] = dz / l * s;
        const x = rs[i] * c, zz = rs[i] * s, u = (ymax - zs[i]) / (ymax - ymin + 1e-9);            // drains toward the lower ring (y is up)
        D[k] = thick.fn ? thick.fn(j / S * 1.7, 1 - u) : top + (bottom - top) * u * u + 70 * Math.sin(2.4 * x + 1.1 * t + 1.6 * Math.sin(2.1 * zz - 0.6 * t)) * Math.sin(2.2 * zz + 0.8 * t); }
    }
    let q = 0; for (let i = 0; i < M - 1; i++) for (let j = 0; j < S; j++) { const a = i * (S + 1) + j, b = a + 1, c = a + S + 1, d = c + 1; I[q++] = a; I[q++] = c; I[q++] = b; I[q++] = b; I[q++] = c; I[q++] = d; }
    return [P, N, D, I];
  }
  function disk(y, R, S = 72, rings = 18, t = 0) {                  // a flat film across a ring
    const zs = [], rs = []; for (let i = 0; i <= rings; i++) { zs.push(y); rs.push(R * i / rings); }
    const out = revolve(zs, rs, S, t, { top: 350, bottom: 350 }); const N = out[1]; for (let k = 0; k < N.length; k += 3) { N[k] = 0; N[k + 1] = 1; N[k + 2] = 0; }
    const D = out[2], P = out[0]; for (let k = 0; k < D.length; k++) { const x = P[3 * k], z = P[3 * k + 2]; D[k] = 420 + 260 * (x * 0.4 + 0.5) + 60 * Math.sin(3 * z + t); }
    return out;
  }
  root.Catenoid = { solve, area, Profile, revolve, disk, HR_MAX, HR_EQUAL, XSTAR };
})(typeof window !== "undefined" ? window : globalThis);
