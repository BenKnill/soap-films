# soap-steiner — complete, 2026-10-04

- PASS — `node tools/success.mjs --grid` — `PASS: 15 cells × 1000 dips; table results/success-grid.md; knees 0:5→6, 0.15:5→6, 0.5:5→6` (soap-steiner-grid journal, 22:50:00 UTC). Table contains marginal confidence intervals, paired shake-effect intervals and exhaustive optimum brackets.
- PASS — `hearth prove proofs/catenoid_snap.ml --profile heavy --timeout 180 --run-root runs/acceptance` — `PASSED catenoid_snap.ml: 2/2 bindings proved, 0 new axioms, eval 38.4s (heavy)` (23:14:19 UTC). Decimal output: `CATENOID SNAP: 1.1996786402 < t < 1.1996786403 (unique positive root of t*tanh(t)=1)`.
- PASS — `test -s EPISODE-4.md && wc -w EPISODE-4.md` — `515 EPISODE-4.md`; one-page outline contains the measured beats and exactly three shot descriptions, now including the certified root. Manually checked its numbers and limitations against the generated table and theorem.

Results: the largest sampled drop is 5→6 pins. Unshaken hexagon success is
50.6% (95% Wilson interval 47.5–53.7%); the two shake amplitudes give 51.0% and
50.9%. Paired gains of 4 and 3 successes per 1,000 have effect intervals including
zero. Seven pins recover to 57.7% without shaking. These are simulated networks
on regular polygons, not real-film measurements or a universal pin-count law.
Unresolved runs count as failures and are separately reported.

Implemented: headless use of the unchanged browser simulation, four workers,
seeded paired dips, exhaustive full-topology SOCP enumeration including collapsed
edges, primal/dual reference brackets, local tests, generated grid, catenoid HOL
proof, documented local commands, and a measured episode outline. The Steiner
reference is exhaustive numerical optimization with gaps below 1e-7; only the
catenoid constant is HOL-certified. Ben can edit the episode framing; no Ben-only
step is required for these completion checks.

Local evidence: `node tools/success.test.mjs` passed the independent triangle,
square, obtuse-triangle and hexagon optima, topology counts, tree validity,
reproducibility, marginal/paired intervals and iteration cap. `snap_algebra.ml`
passed 5/5 bindings on light; `snap_bounds.ml` passed 6/6 on heavy; both added zero
axioms. The final acceptance used no project basis, checked the complete source
and imports, and matched both quoted theorem conclusions with empty hypotheses.
Receipt: runs/acceptance/20261004T231338Z-146738-catenoid_snap-5196b2/transcript.log.json.
Its source/dependency identities match the final proof files. No unchanged proof
was rerun for status, and no CI or cold replay was used.

Operational decisions: long jobs use ~/lanes/bin/lane-run. Repo tools/hearth sets
this machine's runtime environment inside the executable and delegates to the
shared installation, preserving KillMode=process. The modern library's open_in
name collision in Hearth basis capture is worked around locally by restoring
Stdlib.open_in after the bounds proof; no shared tool was changed. Both launcher
and capture friction are recorded in ~/lanes/FINDINGS.md. The temporary authoring
basis f87ce4a36b5d was retired; this lane has no retained basis or running job.
Small sources, tables, environment and proof receipts use the K-backed Linux
filesystem; storage was checked before basis capture.

Previous goal turn: verified wait on the live heavy-profile build. Final turn:
progress—heavy became healthy, the explicit IVT witness and local basis workaround
were checked, full warm acceptance passed, and the completion audit matched each
Done-when requirement. All work is on codex/steiner-rate; no required work remains.
