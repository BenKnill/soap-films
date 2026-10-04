# Film success grid

Regular polygons of unit circumradius; 1,000 independent initial dips per cell (unless marked smoke).
One shake after settling, then settle again. Success = converged connected tree within 0.01% of the exhaustive optimum.
Unresolved and invalid outcomes count as failures. Intervals are marginal 95% Wilson intervals for simulation dip randomness.

| n | shake amplitude | successes/dips | success % (95% CI) | unresolved | invalid | mean length/optimum |
|---|---|---|---|---|---|---|
| 3 | 0 | 1000/1000 | 100.0 (99.6–100.0) | 0 | 0 | 1.000000 |
| 3 | 0.15 | 1000/1000 | 100.0 (99.6–100.0) | 0 | 0 | 1.000000 |
| 3 | 0.5 | 1000/1000 | 100.0 (99.6–100.0) | 0 | 0 | 1.000000 |
| 4 | 0 | 1000/1000 | 100.0 (99.6–100.0) | 0 | 0 | 1.000000 |
| 4 | 0.15 | 1000/1000 | 100.0 (99.6–100.0) | 0 | 0 | 1.000000 |
| 4 | 0.5 | 1000/1000 | 100.0 (99.6–100.0) | 0 | 0 | 1.000000 |
| 5 | 0 | 1000/1000 | 100.0 (99.6–100.0) | 0 | 0 | 1.000000 |
| 5 | 0.15 | 1000/1000 | 100.0 (99.6–100.0) | 0 | 0 | 1.000000 |
| 5 | 0.5 | 1000/1000 | 100.0 (99.6–100.0) | 0 | 0 | 1.000000 |
| 6 | 0 | 506/1000 | 50.6 (47.5–53.7) | 66 | 0 | 1.031650 |
| 6 | 0.15 | 510/1000 | 51.0 (47.9–54.1) | 46 | 0 | 1.028277 |
| 6 | 0.5 | 509/1000 | 50.9 (47.8–54.0) | 51 | 0 | 1.029121 |
| 7 | 0 | 577/1000 | 57.7 (54.6–60.7) | 0 | 0 | 1.039760 |
| 7 | 0.15 | 561/1000 | 56.1 (53.0–59.1) | 16 | 0 | 1.043355 |
| 7 | 0.5 | 562/1000 | 56.2 (53.1–59.2) | 19 | 0 | 1.044270 |

Knee = largest adjacent decrease in success rate over the sampled pin counts.
- Shake 0: n=5→6, drop 49.4 percentage points; non-overlapping marginal intervals.
- Shake 0.15: n=5→6, drop 49.0 percentage points; non-overlapping marginal intervals.
- Shake 0.5: n=5→6, drop 49.1 percentage points; non-overlapping marginal intervals.

| n | exhaustive topologies | optimum lower | optimum upper |
|---|---|---|---|
| 3 | 1 | 2.9999999989 | 3.0000000000 |
| 4 | 3 | 3.8637033041 | 3.8637033052 |
| 5 | 15 | 4.5743291892 | 4.5743291902 |
| 6 | 105 | 4.9999999985 | 5.0000000000 |
| 7 | 945 | 5.2066048674 | 5.2066048699 |

These are simulated networks, not measurements of real soap films. Pin count is confounded with polygon geometry; the knee is specific to this layout family, solver and protocol.
