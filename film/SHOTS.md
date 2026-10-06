# The Soap Computer: shots

10 shots, 270.5 s at 24 fps, 1920×1080. Windows come from the narration timing (`film/timeline.py` → `film/timeline.json`); neighbouring shots overlap 0.5 s for crossfades. Blender shots render on bluestar26 (Cycles, CUDA, 32 samples, GPU denoiser); `film/render_all.py` renders them all, `film/compose.py` adds the labels and the narration.

| # | shot | picture | source | window (s) | duration (s) | frames |
|---|---|---|---|---|---|---|
| 1 | `open` | A vertical film in a rectangular wire frame, daylight thin-film colours; slow pull-back; title. | Blender `film/blender/flatfilm.py` | 0.00–32.00 | 32.00 | 768 |
| 2 | `open-sodium` | The same frames under one wavelength (589.3 nm Airy reflectance): stripes; crossfaded in under the sodium lines. | Blender `flatfilm.py light=sodium` | 9.67–22.50 | 12.83 | 308 |
| 3 | `computer` | Pins between glass plates; the walls lift out of the soap and relax to the Steiner tree (two 120° junctions, glowing arcs). | Blender `film/blender/computer.py` + `film/data/traj-n4-d2.json` | 31.50–73.46 | 41.96 | 1007 |
| 4 | `twice` | Two six-pin rigs dipped one after the other: a four-junction network (length 5.196) and five hexagon sides (length 5). | Blender `computer.py` + `traj-n6-d0.json`, `traj-n6-d2.json` | 72.96–107.74 | 34.78 | 835 |
| 5 | `dips` | The first 60 measured six-pin dips as settled networks, then scored against the shortest network (27 of 60). | 2D `film/graphics/shots2d.py dips` + `film/data/dips-n6.json` | 107.24–128.14 | 20.90 | 502 |
| 6 | `chart` | Success rate against pin count with Wilson bars, the 5→6 knee, seven-pin recovery, the shape caveat, both shake series. | 2D `shots2d.py chart` + `results/success-grid.json` | 127.64–180.18 | 52.54 | 1261 |
| 7 | `rings` | Rings pulled apart (h/R 0.55 → 1.3254), live h/R and area readout; at the snap a curvature-flow collapse into two discs. | Blender `film/blender/catenoid.py` | 179.68–214.03 | 34.35 | 824 |
| 8 | `proof` | t·tanh t against 1, the root, the HOL-proved enclosure digit by digit; the computed h/R ≈ 1.3255 marked as computed. | 2D `shots2d.py proof` | 213.53–245.73 | 32.20 | 773 |
| 9 | `end` | The film again: bands slide down, a black film spreads from the top, then a hole opens and the film is gone. | Blender `flatfilm.py` | 245.23–263.97 | 18.74 | 450 |
| 10 | `endcard` | Title and the four lines: simulated, searched, proved, rendered. | 2D `shots2d.py endcard` | 263.47–270.47 | 7.00 | 168 |

Every Steiner network on screen is a measured dip: the same seeded dip `tools/success.mjs` scores, re-run with `film/sims/steiner_traj.mjs` on bluestar26 (Node 24), where the first 1,000 unshaken six-pin dips reproduce the grid's 506/1,000. On the Mac's Node 26 some seeds settle differently (the relaxation is chaotic), so trajectories are made on bluestar26.
