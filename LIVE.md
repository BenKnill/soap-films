# The Soap Computer — live presentation

Open `docs/live.html` directly in a modern browser with WebGL2. The live page loads only adjacent files and system fonts. The original long-form page and all numerical/renderer engines are unchanged. No Blender assets or new physical model were added.

## Local validation

From this repository, run:

```sh
taskset -c 11 node tests/live-models.mjs
node --check docs/live.js
node --check docs/live-model.js
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 taskset -c 11 python3 tests/validate-local.py
```

These check connected trees, geometry, reproducible examples and finite area-relaxation output. They do not certify solver convergence, global optimality, or browser pixels. The offline presentation kit separately exercises the actual browsers, scene controls, camera reset, touch, screen sizes and one-page guide printing. No GitHub Actions or deployment is involved. Captured model/syntax evidence is in `validation/local-checks.txt`. With the neighbouring kit’s pinned Playwright dependencies installed, run `unshare -rn taskset -c 11 node tests/live-browser-smoke.mjs` for a source-only four-scene functional smoke; its captured result is `validation/browser-smoke.json`. This smoke checks interventions, keyboard/touch navigation, 3D camera changes and exact scene reset snapshots. `validation/browser-smoke-after.json` records the later rehearsal-driven fix: changing a dip clears the overlay, and equal-length comparisons are stated explicitly, with hashes of the tested controller and guide. It does not replace the kit’s viewport and rehearsal review.

## Integration and automation

Copy `docs/live.html` as `soap/index.html`, plus adjacent `live.css`, `live.js`, `live-model.js`, `live-guide.html`, `steiner.js`, `surface.js`, `film3d.js`, `filmcolor.js`. Rewrite the guide's `live.html` back link to `index.html` and the previous-presentation link to `../rhine/index.html` in the kit. Source references in the guide are optional outbound reading; they are not runtime dependencies.

Four scenes expose `body[data-scene-index]` (zero based) and `data-scene-count="4"`. Buttons `#scene-next`, `#scene-prev`, `#scene-reset` also expose `data-action="next"`, `back`, `reset`. Arrows navigate. R resets the **current scene**, camera and interventions. Space/Enter retain native button behavior. Each scene entry starts in its canonical state. No simulation or automatic camera animation runs with time.

`window.SoapLive.getState()` / `window.presentationState()` returns deterministic scene, ready/error, playing=false, intervention flags, model geometry digest/measurements and camera state. `SoapLive.go(index)` and `reset()` support diagnostics; prefer user controls in acceptance tests. `getDiagnostics()` exposes draw count, whether WebGL exists, and buffer size; its counters intentionally do not enter reset snapshots.

- Scene 0: `#soap-reveal` reveals seed 1, six-pin network, length sqrt(27), four free junctions. Initially only pins are drawn.
- Scene 1: starts with the first network. `#soap-dip` alternates seeds 1 and 4, the latter length 5 with no free junctions. `#soap-compare` overlays the five-side connected competitor and toggles `comparison`. Changing the dip clears that overlay, keeping each five-edge network visually distinct; an explicit equal-length comparison uses a numerical tolerance rather than saying “0% longer.”
- Scene 2: existing `Surface.tetrahedron(8)` after 600 finite relaxation steps. `#soap-highlight` toggles the renderer's lines/dots and `highlighted`.
- Scene 3: starts with existing `Surface.cube(8)` after 600 steps, highlights on. `#soap-frame` toggles tetrahedron/cube. This changes geometry digest, mesh counts and frame identity. Drag/wheel control the existing Film3D camera on both 3D scenes.

`#network` uses Canvas2D. `#film` uses the existing WebGL2 Film3D renderer. Hidden panels use the HTML `hidden` attribute. The only canvases are these two visible-size scene views. Numeric readings come from model edges and meshes; no screenshot is treated as a theorem proof.

## Content boundaries

The theorem statement is restricted to ideal area-minimizing films in three dimensions and away from wire boundaries. Taylor's theorem supports smooth sheet/Y/T local types; the numerical surface topology is supplied, not discovered. The five-side competitor directly shows the first numerical network is not globally shortest, without claiming that this code proves the exact Steiner optimum. Both dips are selected examples, not an empirical frequency estimate. The colour/thickness field is illustrative.

Sources: repository `RESEARCH.md` sections 2–4 and the primary publications linked from `docs/live-guide.html`. Taylor's authorship/publication and David's reproof statement were checked against the Annals and arXiv pages on 2026-10-03.
