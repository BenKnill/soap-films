# soap-steiner — 2026-10-04

- PASS — `node tools/success.mjs --grid` — `PASS: 15 cells × 1000 dips; table results/success-grid.md; knees 0:5→6, 0.15:5→6, 0.5:5→6` (systemd journal, soap-steiner-grid, 22:50:00 UTC). Includes paired shake effects and their intervals.
- FAIL — `hearth prove proofs/catenoid_snap.ml --profile heavy` — NOT RUN: heavy is still being built; `HOL_WORKBENCH_RUNTIME_CONFIG=/home/bluestar/hearth/runtime.toml /home/bluestar/src/hol-hearth/hearth doctor --profile heavy` reports `DOCTOR: blocked`, `PROFILES: blocked (heavy)`. Confirmed live `hearth-profile-heavy.service`, PID 83807; build reached 2060s at 22:55:20 UTC. This is a verified wait, not a Ben-only blocker. The independent algebraic component has now passed on light.
- PASS — `test -s EPISODE-4.md && wc -w EPISODE-4.md` — one-page working outline exists, 514 words, with measured beats and exactly three shot descriptions. Manually checked against results/success-grid.md; the catenoid proof line is explicitly a draft pending replay.

Changed: cloned the empty lane checkout (remote default is master, not main), created
codex/steiner-rate, imported the existing browser simulation unchanged, added the
headless command, exhaustive SOCP reference, local tests, measured table, protocol
README and episode outline. `node tools/success.test.mjs` reports `PASS: independent
optimum fixtures, degeneracy, topology counts, tree validity, seeded reproducibility,
marginal and paired Wilson intervals, and iteration cap`. Smoke also passes. No CI used.
Continuation: made the continuity composition explicit in the proof draft;
shortened the outline; moved progress to stderr; added and tested paired shake
effects so inference does not depend on overlapping marginal intervals alone.
The full grid reran after this statistical output change and reproduced every rate.
Proof progress: factored three algebraic lemmas into proofs/snap_algebra.ml.
The first light-profile replay exposed a division-normalization error; repaired it
with a conditional field theorem. `hearth prove proofs/snap_algebra.ml --profile
light --timeout 180 --run-root runs/algebra` then returned `PASSED snap_algebra.ml:
3/3 bindings proved, 0 new axioms, eval 0.6s (light)`. Inspection confirms exact
source conclusions and empty hypotheses for all three lemmas. Receipt:
runs/algebra/20261004T225450Z-125158-snap_algebra-b5707b/transcript.log.json.
The main catenoid source now imports this checked algebra; its heavy replay is pending.

Decisions: regular unit-radius polygons n=3…7; one shake at amplitudes 0, 0.15,
0.5; four workers; paired initial dips; success within 0.01% with convergence
and connectivity required. Exact topology enumeration includes collapsed edges;
numerical primal/dual gaps are under 1e-7, not HOL-certified. No claim about
real-film success rates or a universal pin-count threshold. A single shake
does not clearly help this measured protocol. Native K-backed Linux storage
used for the small environment, generated tables and proof run directory.

Checkpoint: ebf2796 pushed to origin/codex/steiner-rate; catenoid source is explicitly
an unvalidated draft. Shared missing-playbook and heavy-provisioning findings
were deduplicated with `+1 soap-steiner` in ~/lanes/FINDINGS.md.

Next: wait for the confirmed live shared heavy-profile build, run the small
catenoid proof leaf, fix any proof errors, then perform one full warm acceptance
with zero new axioms. Replace the draft catenoid status with that command's
verdict and decimal enclosure; push tested checkpoints to this lane's branch.
Previous goal turn: verified wait on a confirmed live heavy build. This turn:
progress (fixed and proved the algebraic component) and a verified wait on heavy.
The complete enclosure has not yet been replayed.
