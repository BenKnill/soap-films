# Episode 4 — The Soap Computer

**Spine:** “A film can settle into a beautiful answer. How often is it the best
answer?” Working outline, about seven minutes; framing ready for Ben's edit.

**0:00–0:50 — A computer made of soap.** Open on pins between plates. Surface
tension pulls straight walls together; three equal tensions balance at 120°.
The target: connect every pin with the least total wall length. Start with known
triangle and square checks: a unit-side square's optimum is 1+√3.

**0:50–2:00 — Beautiful does not mean best.** Dip again and get a longer
topology. Overlay the independently enumerated optimum. On the unit-radius
hexagon the winner is five sides, length 5, with no free junctions.

**2:00–3:40 — Put a number on the disappointment.** Reveal the measured curve:
1,000 simulated dips per point, regular polygons with 3–7 pins. With no shake,
3, 4 and 5 pins all score 1,000/1,000; six pins score **506/1,000 = 50.6%**
(95% Wilson interval **47.5–53.7%**). The largest drop is **5→6 pins**, 49.4
percentage points. Seven pins recover to **57.7%** (54.6–60.7%): complexity does
not produce a smooth one-way decline in this geometry family. Keep the label
“simulation” on screen. Explain the score: connected, converged, within 0.01%
of the global length; 66 unshaken hexagon runs did not converge within the budget
and count as failures, rather than evidence of a stable local minimum.

**3:40–4:40 — Does shaking rescue it?** One shake of amplitude 0.15 gives
**51.0%** at six pins; amplitude 0.5 gives **50.9%**. Marginal intervals overlap
the control's; paired gains are just 3–4 successes per 1,000, with effect intervals
including zero. “This protocol didn't give us a clear rescue.” All three knees
are 5→6. This is not a test of every annealing schedule; the intervals describe
dip randomness, not model accuracy. Pin count also changes polygon geometry.

**4:40–6:20 — One smooth dial.** Separate two rings holding a catenoid.
Its stationary branch folds where **t·tanh(t)=1**, t=h/(2a). The HOL proof targets
the unique positive root in **(1.1996786402, 1.1996786403)**; replay is pending.
Show the separate numerical mapping h/R≈1.325487, then the existing collapse
animation. Certifying this root does not certify fluid dynamics or the complete
stability theorem. A retained shape and a global optimum are different questions.

**6:20–7:00 — What the soap computer taught us.** Return to the film. “Settling
down is a way to compute. It isn't a promise to find the best answer.” Let the
colour drain to black and the film disappear. Real-film footage can illustrate
the idea; do not present it as validation of these simulated percentages.

## Three shots

1. **Two answers:** overhead hexagon, longer settled dip beside the enumerated
   five-edge winner. Same scale; highlight length difference and 120° junctions.
2. **The knee:** draw the unshaken curve with Wilson bars, then both shake
   curves. Freeze on 5→6; retain the seven-pin recovery, denominator and unresolved
   count. Caption: “regular polygons · simulated films · one shake.”
3. **Certified dial:** rings separate, neck shrinks; inset `t·tanh(t)−1`
   crosses zero inside the target enclosure. Distinguish the proved interval from
   the approximate h/R readout before the simulated collapse.

Numbers: [measured grid](results/success-grid.md). Protocol and limitations:
[README](README.md). Root theorem: [catenoid_snap.ml](proofs/catenoid_snap.ml).
