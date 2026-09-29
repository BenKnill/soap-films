// Soap-film flow on the GPU: why bubbles swirl.
// A soap film is a two-dimensional fluid: it can flow within its sheet but hardly across it, and its in-plane flow
// is close to incompressible. Its thickness barely diffuses, so thickness is carried like dye and gets stretched into
// fine filaments; the interference colours show it. Two things stir it:
//   - "bubble": a half bubble on a warm plate. Warm film at the foot is lighter and rises toward the top in plumes;
//     2D turbulence gathers the motion into big, long-lived vortices (the hurricane-like storms of Kellay's group).
//   - "frame": a vertical film in a wire frame. Gravity drains it (thick at the bottom, thin at the top), and thin,
//     light film is pulled out at the borders and rises in plumes (marginal regeneration).
// Model: incompressible 2D flow on a grid (stable fluids: semi-Lagrangian advection, pressure projection), a buoyancy
// force, a little vorticity confinement, and two scalars carried by the flow: temperature T and thickness h (nm),
// advected with MacCormack so the striations stay sharp. The half bubble is simulated on its azimuthal-equidistant
// map (the pole at the centre, the foot on the rim), which keeps distortion under about 36 % and has no pole problem.
(function (root) {
  const VS = `#version 300 es
  in vec2 aQ; out vec2 vQ; void main() { vQ = aQ * 0.5 + 0.5; gl_Position = vec4(aQ, 0.0, 1.0); }`;
  const HEAD = `#version 300 es
  precision highp float; precision highp sampler2D;
  uniform sampler2D uA; uniform vec2 uN; uniform int uMode; uniform float uDt, uTime;
  in vec2 vQ; out vec4 o;
  ivec2 cell() { return ivec2(gl_FragCoord.xy); }
  bool inside(vec2 c) {                                   // c: cell centre coordinates
    if (uMode == 0) return length(c - 0.5 * uN) < 0.5 * uN.x - 1.5;
    return c.x > 1.0 && c.y > 1.0 && c.x < uN.x - 1.0 && c.y < uN.y - 1.0; }
  vec4 at(sampler2D t, ivec2 i) { i = clamp(i, ivec2(0), ivec2(uN) - 1); return texelFetch(t, i, 0); }
  vec4 bil(sampler2D t, vec2 p) {                          // p in cell units, cell centres at i + 0.5
    p -= 0.5; vec2 f = fract(p); ivec2 i = ivec2(floor(p));
    return mix(mix(at(t, i), at(t, i + ivec2(1, 0)), f.x), mix(at(t, i + ivec2(0, 1)), at(t, i + ivec2(1, 1)), f.x), f.y); }
  float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
  float vnoise(vec2 p) { vec2 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i), hash(i + vec2(1, 0)), f.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), f.x), f.y); }
  `;
  // advection, MacCormack: forward, backward, then corrected and clamped (velocity stays plain semi-Lagrangian)
  const FS_FWD = HEAD + `void main() { vec2 c = gl_FragCoord.xy; vec4 A = at(uA, cell()); if (!inside(c)) { o = vec4(0, 0, A.zw); return; } o = bil(uA, c - uDt * A.xy); }`;
  const FS_BWD = HEAD + `uniform sampler2D uF; void main() { vec2 c = gl_FragCoord.xy; vec4 A = at(uA, cell()); if (!inside(c)) { o = at(uF, cell()); return; } o = bil(uF, c + uDt * A.xy); }`;
  const FS_COR = HEAD + `uniform sampler2D uF, uB; void main() {
    vec2 c = gl_FragCoord.xy; ivec2 i = cell(); vec4 A = at(uA, i), F = at(uF, i), B = at(uB, i); if (!inside(c)) { o = vec4(0, 0, A.zw); return; }
    vec2 p = c - uDt * A.xy - 0.5; ivec2 j = ivec2(floor(p)); vec4 s0 = at(uA, j), s1 = at(uA, j + ivec2(1, 0)), s2 = at(uA, j + ivec2(0, 1)), s3 = at(uA, j + ivec2(1, 1));
    vec4 lo = min(min(s0, s1), min(s2, s3)), hi = max(max(s0, s1), max(s2, s3)), r = clamp(F + 0.5 * (A - B), lo, hi);
    o = vec4(F.xy, r.zw); }`;
  const FS_CURL = HEAD + `void main() { ivec2 i = cell(); float w = 0.5 * ((at(uA, i + ivec2(1, 0)).y - at(uA, i - ivec2(1, 0)).y) - (at(uA, i + ivec2(0, 1)).x - at(uA, i - ivec2(0, 1)).x)); o = vec4(w, 0, 0, 1); }`;
  const FS_FORCE = HEAD + `uniform sampler2D uW; uniform float uBuoy, uHeat, uConf, uThin, uFeed, uHRim, uHTop, uHBot, uTopThin, uVisc, uDiffH, uHeatK, uSpin;
    void main() {
      vec2 c = gl_FragCoord.xy; ivec2 i = cell(); vec4 A = at(uA, i); if (!inside(c)) { o = vec4(0, 0, A.zw); return; }
      vec2 u = A.xy; float T = A.z, h = A.w;
      vec4 nL = inside(c - vec2(1, 0)) ? at(uA, i - ivec2(1, 0)) : A, nR = inside(c + vec2(1, 0)) ? at(uA, i + ivec2(1, 0)) : A, nB = inside(c - vec2(0, 1)) ? at(uA, i - ivec2(0, 1)) : A, nT = inside(c + vec2(0, 1)) ? at(uA, i + ivec2(0, 1)) : A;
      vec4 lap = nL + nR + nB + nT - 4.0 * A; u += uDt * uVisc * lap.xy; T += uDt * uDiffH * lap.z; h += uDt * uDiffH * lap.w;
      // vorticity confinement: puts back the swirl that the grid smears away
      float wl = abs(at(uW, i - ivec2(1, 0)).x), wr = abs(at(uW, i + ivec2(1, 0)).x), wb = abs(at(uW, i - ivec2(0, 1)).x), wt = abs(at(uW, i + ivec2(0, 1)).x), w = at(uW, i).x;
      vec2 g = vec2(wr - wl, wt - wb); float gl = length(g); if (gl > 1e-6) { vec2 n = g / gl; u += uDt * uConf * vec2(n.y * w, -n.x * w); }
      if (uMode == 0) {
        vec2 ctr = 0.5 * uN, d = c - ctr; float R = 0.5 * uN.x - 1.5, r = length(d) / R; vec2 up = -d / max(length(d), 1e-3);   // "up" the bubble is toward the pole, the centre
        u += uDt * uBuoy * T * up;                                                          // warm film is lighter: it rises
        float lat = 1.5707963 * (1.0 - r);                                                   // a spinning plate: Coriolis force 2Ω sin(latitude), as on a planet
        u += uDt * uSpin * sin(lat) * vec2(u.y, -u.x);
        float ang = atan(d.y, d.x), band = smoothstep(0.86, 0.99, r);
        float patchy = smoothstep(0.35, 0.8, vnoise(vec2(ang * uHeatK / 6.2832 * 6.2832 + 11.0, uTime * 0.15)));
        T += uDt * (uHeat * band * (0.25 + patchy) * (1.0 - T) - 0.003 * T);               // heated at the foot (warmer in a few patches), cooled everywhere
        h += uDt * (band * uFeed * (uHRim - h) - uThin * h * (1.0 - r * r));                // fresh thick film at the foot; the top drains thinner
      } else {
        float y = c.y / uN.y, x = c.x / uN.x, ref = mix(uHBot, uHTop, pow(y, 0.8));        // drained background: thick at the bottom, thin at the top
        u.y += uDt * uBuoy * (ref - h) / 1000.0;                                            // thin film is lighter: it rises
        float edge = max(smoothstep(0.06, 0.0, x), smoothstep(0.94, 1.0, x)) + 0.6 * smoothstep(0.05, 0.0, y);
        float puff = step(0.62, vnoise(vec2(x * 3.0 + 9.0 * floor(uTime * 0.7), y * 22.0 - uTime * 0.9)));
        h += uDt * uFeed * edge * puff * (0.45 * ref - h);                                  // marginal regeneration: thin film pulled out at the borders
        h += uDt * uThin * (ref - h) * 0.2 - uDt * uTopThin * smoothstep(0.75, 1.0, y) * h; // slow drainage toward the background; the top thins
      }
      h = max(h, 8.0); o = vec4(u, T, h); }`;
  const FS_DIV = HEAD + `void main() { vec2 c = gl_FragCoord.xy; ivec2 i = cell();
    vec2 L = inside(c - vec2(1, 0)) ? at(uA, i - ivec2(1, 0)).xy : vec2(0), R = inside(c + vec2(1, 0)) ? at(uA, i + ivec2(1, 0)).xy : vec2(0);
    vec2 B = inside(c - vec2(0, 1)) ? at(uA, i - ivec2(0, 1)).xy : vec2(0), T = inside(c + vec2(0, 1)) ? at(uA, i + ivec2(0, 1)).xy : vec2(0);
    o = vec4(inside(c) ? 0.5 * (R.x - L.x + T.y - B.y) : 0.0, 0, 0, 1); }`;
  const FS_JAC = HEAD + `uniform sampler2D uP, uD; void main() { vec2 c = gl_FragCoord.xy; ivec2 i = cell(); float pc = at(uP, i).x; if (!inside(c)) { o = vec4(0); return; }
    float l = inside(c - vec2(1, 0)) ? at(uP, i - ivec2(1, 0)).x : pc, r = inside(c + vec2(1, 0)) ? at(uP, i + ivec2(1, 0)).x : pc, b = inside(c - vec2(0, 1)) ? at(uP, i - ivec2(0, 1)).x : pc, t = inside(c + vec2(0, 1)) ? at(uP, i + ivec2(0, 1)).x : pc;
    o = vec4((l + r + b + t - at(uD, i).x) * 0.25, 0, 0, 1); }`;
  const FS_GRAD = HEAD + `uniform sampler2D uP; void main() { vec2 c = gl_FragCoord.xy; ivec2 i = cell(); vec4 A = at(uA, i); if (!inside(c)) { o = vec4(0, 0, A.zw); return; } float pc = at(uP, i).x;
    float l = inside(c - vec2(1, 0)) ? at(uP, i - ivec2(1, 0)).x : pc, r = inside(c + vec2(1, 0)) ? at(uP, i + ivec2(1, 0)).x : pc, b = inside(c - vec2(0, 1)) ? at(uP, i - ivec2(0, 1)).x : pc, t = inside(c + vec2(0, 1)) ? at(uP, i + ivec2(0, 1)).x : pc;
    o = vec4(A.xy - 0.5 * vec2(r - l, t - b), A.zw); }`;
  const FS_INIT = HEAD + `uniform float uHTop, uHBot, uHRim; void main() { vec2 c = gl_FragCoord.xy; float n = vnoise(c * 0.05) - 0.5;
    if (uMode == 0) { float r = length(c - 0.5 * uN) / (0.5 * uN.x); o = vec4(0, 0, 0, mix(uHTop, uHRim, r * r) + 80.0 * n); }
    else { float y = c.y / uN.y; o = vec4(0, 0, 0, mix(uHBot, uHTop, pow(y, 0.8)) + 60.0 * n); } }`;
  // display: the flat frame, and the half bubble in 3D
  const FS_FLAT = HEAD + `uniform sampler2D uLUT; uniform float uDMax; void main() { vec2 c = vQ * uN; float h = bil(uA, c).w; vec3 col = texture(uLUT, vec2(clamp(h / uDMax, 0.0, 1.0), 0.5)).rgb; o = vec4(col, 1.0); }`;
  const VS_DOME = `#version 300 es
  in vec3 aP; uniform mat4 uM; out vec3 vP; void main() { vP = aP; gl_Position = uM * vec4(aP, 1.0); }`;
  const FS_DOME = `#version 300 es
  precision highp float; precision highp sampler2D; in vec3 vP; uniform sampler2D uA, uLUT; uniform vec2 uN; uniform vec3 uEye; uniform float uDMax, uR; out vec4 o;
  vec4 at(ivec2 i) { i = clamp(i, ivec2(0), ivec2(uN) - 1); return texelFetch(uA, i, 0); }
  vec4 bil(vec2 p) { p -= 0.5; vec2 f = fract(p); ivec2 i = ivec2(floor(p)); return mix(mix(at(i), at(i + ivec2(1, 0)), f.x), mix(at(i + ivec2(0, 1)), at(i + ivec2(1, 1)), f.x), f.y); }
  void main() {
    vec3 n = normalize(vP), v = normalize(uEye - vP); float c = abs(dot(n, v)), ct = sqrt(max(0.0, 1.0 - (1.0 - c * c) / 1.7689));
    float th = acos(clamp(n.y, -1.0, 1.0)), lam = atan(n.z, n.x);                                    // colatitude from the pole (y up), longitude
    vec2 uv = 0.5 + 0.5 * (th / 1.5707963) * vec2(cos(lam), sin(lam)); float h = bil(uv * uN).w;
    vec3 col = texture(uLUT, vec2(clamp(h * ct / uDMax, 0.0, 1.0), 0.5)).rgb; float fres = 0.35 + 0.65 * pow(1.0 - c, 3.0);
    o = vec4(col * (0.55 + 0.45 * fres), 0.8 * (0.45 + 0.55 * fres)); }`;
  const FS_PLATE = `#version 300 es
  precision highp float; in vec3 vP; uniform vec3 uEye; out vec4 o; void main() { float r = length(vP.xz); vec3 v = normalize(uEye - vP); float s = pow(1.0 - abs(v.y), 4.0);
    o = vec4(vec3(0.05, 0.055, 0.07) * (1.0 - 0.4 * smoothstep(1.0, 2.2, r)) + 0.08 * s, 1.0); }`;
  const m4 = {
    persp: (fov, asp, n, f) => { const t = 1 / Math.tan(fov / 2); return [t / asp, 0, 0, 0, 0, t, 0, 0, 0, 0, (f + n) / (n - f), -1, 0, 0, 2 * f * n / (n - f), 0]; },
    look: (e, c, u) => { const s3 = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]], cr = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]], nr = a => { const l = Math.hypot(...a) || 1; return a.map(x => x / l); }, dt = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
      const z = nr(s3(e, c)), x = nr(cr(u, z)), y = cr(z, x); return [x[0], y[0], z[0], 0, x[1], y[1], z[1], 0, x[2], y[2], z[2], 0, -dt(x, e), -dt(y, e), -dt(z, e), 1]; },
    mul: (a, b) => { const o = new Array(16).fill(0); for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) for (let k = 0; k < 4; k++) o[j * 4 + i] += a[k * 4 + i] * b[j * 4 + k]; return o; }
  };
  function create(canvas, opts = {}) {
    const mode = opts.mode === "frame" ? 1 : 0, NX = opts.NX || (mode ? 256 : 384), NY = opts.NY || (mode ? 340 : 384);
    const gl = canvas.getContext("webgl2", { antialias: true, premultipliedAlpha: false, preserveDrawingBuffer: !!opts.preserve }); if (!gl) throw new Error("WebGL2 unavailable");
    if (!gl.getExtension("EXT_color_buffer_float")) throw new Error("float render targets unavailable");
    const sh = (t, s) => { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o) + "\n" + s.slice(0, 200)); return o; };
    const prog = (vs, fs, attr = "aQ") => { const p = gl.createProgram(); gl.attachShader(p, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs)); gl.bindAttribLocation(p, 0, attr); gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p)); const cache = {}; p.u = n => cache[n] ?? (cache[n] = gl.getUniformLocation(p, n)); return p; };
    const P = { fwd: prog(VS, FS_FWD), bwd: prog(VS, FS_BWD), cor: prog(VS, FS_COR), curl: prog(VS, FS_CURL), force: prog(VS, FS_FORCE), div: prog(VS, FS_DIV), jac: prog(VS, FS_JAC), grad: prog(VS, FS_GRAD), init: prog(VS, FS_INIT), flat: prog(VS, FS_FLAT), dome: prog(VS_DOME, FS_DOME, "aP"), plate: prog(VS_DOME, FS_PLATE, "aP") };
    const tex = () => { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA32F, NX, NY, 0, gl.RGBA, gl.FLOAT, null);
      for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.NEAREST], [gl.TEXTURE_MAG_FILTER, gl.NEAREST], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D, k, v);
      const f = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, f); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0); return { t, f }; };
    let A = tex(), A2 = tex(); const F = tex(), B = tex(), W = tex(), D = tex(); let Pp = tex(), Pq = tex();
    const quad = gl.createVertexArray(); gl.bindVertexArray(quad); gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer()); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    const lut = gl.createTexture(); let lutInfo = null;
    const setLight = l => { lutInfo = FilmColor.filmLUT(512, 1600, l); gl.bindTexture(gl.TEXTURE_2D, lut); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 512, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, lutInfo.data); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); };
    setLight(opts.light || "day");
    const S = { gl, canvas, mode, NX, NY, time: 0, setLight,
      params: mode === 0 ? { buoy: 0.04, heat: 0.06, conf: 0.015, thin: 0.0015, feed: 0.04, hRim: 620, hTop: 230, hBot: 620, topThin: 0, jacobi: 50, visc: 0.02, diffH: 0.008, heatK: 7, spin: 0.04 }
                         : { buoy: 0.012, heat: 0, conf: 0.05, thin: 0.004, feed: 0.1, hRim: 0, hTop: 120, hBot: 1400, topThin: 0.004, jacobi: 50, visc: 0.04, diffH: 0.01, heatK: 0 } };
    Object.assign(S.params, opts.params || {});
    const run = (p, target, bind) => { gl.useProgram(p); gl.bindFramebuffer(gl.FRAMEBUFFER, target.f); gl.viewport(0, 0, NX, NY); gl.bindVertexArray(quad);
      gl.uniform2f(p.u("uN"), NX, NY); gl.uniform1i(p.u("uMode"), mode); gl.uniform1f(p.u("uTime"), S.time);
      let unit = 0; for (const [name, tx] of Object.entries(bind)) { if (typeof tx === "number") { gl.uniform1f(p.u(name), tx); continue; } gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, tx.t); gl.uniform1i(p.u(name), unit++); }
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); };
    S.reset = () => { const q = S.params; run(P.init, A, { uHTop: q.hTop, uHBot: q.hBot, uHRim: q.hRim }); S.time = 0; };
    S.step = (dt = 1) => {
      const q = S.params;
      run(P.fwd, F, { uA: A, uDt: dt }); run(P.bwd, B, { uA: A, uF: F, uDt: dt }); run(P.cor, A2, { uA: A, uF: F, uB: B, uDt: dt }); [A, A2] = [A2, A];
      run(P.curl, W, { uA: A });
      run(P.force, A2, { uA: A, uW: W, uDt: dt, uBuoy: q.buoy, uHeat: q.heat, uConf: q.conf, uThin: q.thin, uFeed: q.feed, uHRim: q.hRim, uHTop: q.hTop, uHBot: q.hBot, uTopThin: q.topThin, uVisc: q.visc, uDiffH: q.diffH, uHeatK: q.heatK, uSpin: q.spin || 0 }); [A, A2] = [A2, A];
      run(P.div, D, { uA: A });
      for (let k = 0; k < q.jacobi; k++) { run(P.jac, Pq, { uP: Pp, uD: D }); [Pp, Pq] = [Pq, Pp]; }
      run(P.grad, A2, { uA: A, uP: Pp }); [A, A2] = [A2, A];
      S.time += dt / 60;
    };
    // the half bubble mesh (unit hemisphere, y up) and the plate
    const dome = (() => { const P3 = [], I = [], NT = 64, NL = 128; for (let i = 0; i <= NT; i++) for (let j = 0; j <= NL; j++) { const th = (Math.PI / 2) * i / NT, la = 2 * Math.PI * j / NL; P3.push(Math.sin(th) * Math.cos(la), Math.cos(th), Math.sin(th) * Math.sin(la)); }
      for (let i = 0; i < NT; i++) for (let j = 0; j < NL; j++) { const a = i * (NL + 1) + j, b = a + 1, c = a + NL + 1, d = c + 1; I.push(a, c, b, b, c, d); }
      const vao = gl.createVertexArray(); gl.bindVertexArray(vao); gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer()); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(P3), gl.STATIC_DRAW); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, gl.createBuffer()); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint32Array(I), gl.STATIC_DRAW); return { vao, n: I.length }; })();
    const plate = (() => { const P3 = [0, 0, 0], I = []; const S2 = 96; for (let j = 0; j <= S2; j++) { const a = 2 * Math.PI * j / S2; P3.push(3 * Math.cos(a), 0, 3 * Math.sin(a)); } for (let j = 1; j <= S2; j++) I.push(0, j, j + 1);
      const vao = gl.createVertexArray(); gl.bindVertexArray(vao); gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer()); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(P3), gl.STATIC_DRAW); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, gl.createBuffer()); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint32Array(I), gl.STATIC_DRAW); return { vao, n: I.length }; })();
    S.cam = { yaw: 0.5, pitch: 0.38, dist: 3.4, auto: 0.06 }; let drag = null;
    if (mode === 0) { canvas.addEventListener("pointerdown", e => { drag = [e.clientX, e.clientY]; canvas.setPointerCapture(e.pointerId); });
      canvas.addEventListener("pointermove", e => { if (!drag) return; S.cam.yaw -= (e.clientX - drag[0]) * 0.008; S.cam.pitch = Math.max(0.05, Math.min(1.45, S.cam.pitch + (e.clientY - drag[1]) * 0.008)); drag = [e.clientX, e.clientY]; });
      canvas.addEventListener("pointerup", () => { drag = null; }); }
    S.draw = (dt = 0, o = {}) => {
      const dpr = Math.min(2, window.devicePixelRatio || 1), w = Math.round(canvas.clientWidth * dpr), h = Math.round(canvas.clientHeight * dpr); if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
      gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, w, h); gl.clearColor(0.03, 0.035, 0.05, 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      if (mode === 1 || o.flat) {                              // the frame (or the bubble's map): film letterboxed in the canvas
        const asp = NX / NY, ch = h * 0.94, cw = ch * asp; gl.viewport(Math.round((w - cw) / 2), Math.round((h - ch) / 2), Math.round(cw), Math.round(ch));
        gl.useProgram(P.flat); gl.bindVertexArray(quad); gl.uniform2f(P.flat.u("uN"), NX, NY); gl.uniform1i(P.flat.u("uMode"), mode); gl.uniform1f(P.flat.u("uDMax"), lutInfo.dMax);
        gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, A.t); gl.uniform1i(P.flat.u("uA"), 0); gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, lut); gl.uniform1i(P.flat.u("uLUT"), 1); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); return;
      }
      if (!drag) S.cam.yaw += S.cam.auto * dt;
      const c = S.cam, eye = [c.dist * Math.cos(c.pitch) * Math.sin(c.yaw), 0.35 + c.dist * Math.sin(c.pitch), c.dist * Math.cos(c.pitch) * Math.cos(c.yaw)], M = m4.mul(m4.persp(0.75, w / h, 0.05, 50), m4.look(eye, [0, 0.35, 0], [0, 1, 0]));
      gl.enable(gl.DEPTH_TEST); gl.useProgram(P.plate); gl.uniformMatrix4fv(P.plate.u("uM"), false, M); gl.uniform3fv(P.plate.u("uEye"), eye); gl.bindVertexArray(plate.vao); gl.drawElements(gl.TRIANGLES, plate.n, gl.UNSIGNED_INT, 0);
      gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE); gl.depthMask(false);
      gl.useProgram(P.dome); gl.uniformMatrix4fv(P.dome.u("uM"), false, M); gl.uniform3fv(P.dome.u("uEye"), eye); gl.uniform2f(P.dome.u("uN"), NX, NY); gl.uniform1f(P.dome.u("uDMax"), lutInfo.dMax);
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, A.t); gl.uniform1i(P.dome.u("uA"), 0); gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, lut); gl.uniform1i(P.dome.u("uLUT"), 1);
      gl.bindVertexArray(dome.vao); gl.drawElements(gl.TRIANGLES, dome.n, gl.UNSIGNED_INT, 0); gl.depthMask(true); gl.disable(gl.BLEND); gl.disable(gl.DEPTH_TEST);
    };
    S.sampler = () => { const st = S.readState(); return (u, v) => { u = ((u % 1) + 1) % 1; v = Math.max(0, Math.min(1, v)); const x = u * (NX - 1), y = v * (NY - 1), i = Math.floor(x), j = Math.floor(y), fx = x - i, fy = y - j, i1 = Math.min(NX - 1, i + 1), j1 = Math.min(NY - 1, j + 1);
      const h = (ii, jj) => st[4 * (jj * NX + ii) + 3]; return (h(i, j) * (1 - fx) + h(i1, j) * fx) * (1 - fy) + (h(i, j1) * (1 - fx) + h(i1, j1) * fx) * fy; }; };
    S.readState = () => { const out = new Float32Array(NX * NY * 4); gl.bindFramebuffer(gl.FRAMEBUFFER, A.f); gl.readPixels(0, 0, NX, NY, gl.RGBA, gl.FLOAT, out); return out; };
    S.reset(); return S;
  }
  root.SoapFlow = { create };
})(typeof window !== "undefined" ? window : globalThis);
