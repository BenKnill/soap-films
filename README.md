# The Soap Computer

Episode 4 simulations live in `docs/`: film interference, Steiner networks,
area minimization, catenoids, WebGL films and GPU flow. Open `docs/index.html`
through a local static server to use the existing interactive demonstrations.
`PLAN.md` and `RESEARCH.md` hold the earlier episode plan and source notes.

## Measure the simulated soap computer

Node 24 and a project Python environment are required. The oracle uses an
independent convex solver; the film itself remains the browser's
`docs/steiner.js`, imported unchanged by Node.

```sh
uv venv .venv --python 3.13.2
uv pip install --python .venv/bin/python -r requirements.txt
node tools/success.test.mjs
node tools/success.mjs --smoke
node tools/success.mjs --grid
```

The last command writes `results/success-grid.md` and its underlying JSON,
with a verdict, Wilson 95% intervals and an explicitly defined knee. For a
durable full run on this shared machine:

```sh
systemd-run --user --unit=soap-steiner-grid --collect \
  --working-directory="$PWD" "$(command -v node)" tools/success.mjs --grid
systemctl --user is-active soap-steiner-grid
journalctl --user -u soap-steiner-grid -n 20 --no-pager
```

Four workers share the cores with other lanes. Each cell has 1,000 independently
seeded dips into the **same** unit-circumradius regular polygon. Initial dips
are paired across shake amplitudes 0, 0.15 and 0.5; confidence intervals describe
the dip distribution within each cell, not independent differences between
paired cells. The table also reports gained and lost successes on these paired
dips, with conservative approximate 95% difference intervals formed from two
97.5% Wilson intervals using Bonferroni. The simulator's initial random topology distribution is retained,
including its existing random-sort pin ordering; it is not uniform over trees.
Each dip relaxes for at most 4,000 iterations, takes one shake (uniform x/y
junction displacements in ±amplitude/2), then relaxes for at most another 4,000.
The zero-shake control gets the same two relaxation budgets. There is no
best-of selection or repeated annealing schedule. Convergence requires a
maximum move below 1e-7 and no topology event in that step. Nonconvergence counts
as failure and is reported separately. Connectivity and tree structure are
checked before scoring; invalid results fail the command.

### Independent optimum reference

`tools/optimum.py` enumerates **all** labelled full topologies by inserting each
new terminal into each existing edge. Counts are `(2n−5)!!`: 1, 3, 15, 105, 945
for n=3…7. Every fixed topology is minimized as a convex second-order cone
program. Zero-length edges are allowed, covering non-full trees as degeneracies,
including the regular hexagon's optimum: five polygon sides, length 5.
This exhaustive strategy follows the full-topology framework described in
[Smith's exact algorithm](https://epubs.siam.org/doi/abs/10.1137/0150015) and
[the conic formulation literature](https://optimization-online.org/wp-content/uploads/2018/12/6976.pdf).

The solver's primal points give an upper bound from actual edge lengths. Its
dual edge vectors are projected onto zero junction divergence and scaled into
unit disks to give a lower bound by weak duality. A residual allowance uses
the fact that an optimum lies in the terminal convex hull. The global bracket
is the minimum of each bound across all topologies; the command refuses gaps
over 1e-7. Scoring accepts a converged network within 0.01% of the optimum and
refuses ambiguous classifications across that bracket. This is exhaustive
numerical optimization in double precision, not a symbolic radical formula or
an HOL-certified Steiner optimum. Only the catenoid constant below is formally
certified. Tests cover exact triangle, square, obtuse-triangle and hexagon
values, degeneration and topology counts.

The measured knee is the largest adjacent percentage-point drop, rather than
a fitted phase transition. These are **simulated networks, not real soap-film
experiments**. Pin count changes polygon geometry; this curve cannot establish
a universal failure threshold, and a single shake need not improve success.

## Certify the catenoid snap

Use the shared Hearth installation and heavy profile without rebuilding it:

```sh
export PATH=/home/bluestar/src/hol-hearth:$PATH
export HOL_WORKBENCH_RUNTIME_CONFIG=/home/bluestar/hearth/runtime.toml
hearth prove proofs/catenoid_snap.ml --profile heavy --timeout 900 \
  --run-root /home/bluestar/lanes/soap-steiner/runs/catenoid
hearth inspect /home/bluestar/lanes/soap-steiner/runs/catenoid \
  --binding CATENOID_SNAP_ENCLOSURE
```

The proof uses the modern multivariate exponential's kernel-checked Taylor
remainder at rational endpoints, continuity and the intermediate value theorem.
It encloses the unique positive root of `t*tanh(t)=1` in
**(1.1996786402, 1.1996786403)**. `soap_tanh` explicitly defines tanh using
`(exp(2t)−1)/(exp(2t)+1)`; no numerical result is asserted as an axiom.
The theorem also excludes other positive roots outside this interval.
`2t/cosh(t)` is the dimensionless ring separation h/R; its existing browser
value of about 1.325487 is numerical, and is not part of the proved enclosure.

`EPISODE-4.md` is the one-page measured script outline and three shot descriptions.
All validation is local. No GitHub Actions check is required or authorized.
Small tables, sources and proof receipts stay on this K-backed Linux filesystem.
No bulk media or archives are produced by these commands.
