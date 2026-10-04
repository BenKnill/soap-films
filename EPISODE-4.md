# Episode 4 — The Soap Computer

**Spine:** “A film can settle into a beautiful answer. How often is it the best
answer?” Working outline, about seven minutes; framing ready for Ben's edit.

**0:00–0:50 — A computer made of soap.** Open on the two-plate pin apparatus
and a film pulling straight walls together. Three equal tensions balance at
120°. Establish the target: connect every pin with the least total wall length.
Begin with known checks: the equilateral triangle and square; a unit-side
square's best network has length 1+√3. Junctions beat roads restricted to pins.

**0:50–2:00 — Beautiful does not mean best.** Add pins and dip again. A settled
network can keep a longer topology. Overlay an independently enumerated optimum,
not “the shortest network we happened to see.” On the unit-radius hexagon the
winner is five sides, length 5: an answer with no free junctions at all.

**2:00–3:40 — Put a number on the disappointment.** Reveal the measured curve:
1,000 simulated dips per point, regular polygons with 3–7 pins. With no shake,
3, 4 and 5 pins all score 1,000/1,000; six pins score **506/1,000 = 50.6%**
(95% Wilson interval **47.5–53.7%**). The largest drop is **5→6 pins**, 49.4
percentage points. Seven pins recover to **57.7%** (54.6–60.7%): complexity does
not produce a smooth one-way decline in this geometry family. Keep the label
“simulation” on screen. Explain the score: connected, converged, within 0.01%
of the global length; 66 unshaken hexagon runs did not converge within the budget
and count as failures, rather than evidence of a stable local minimum.

**3:40–4:40 — Does shaking rescue it?** Add the two shake curves. One shake of
amplitude 0.15 gives **51.0%** at six pins; amplitude 0.5 gives **50.9%**.
Their marginal intervals overlap the control's. Say: “This shake protocol
didn't give us a clear rescue.” Do not claim an improvement, an optimal annealing
schedule, or that all physical shaking fails. All three knees are 5→6 for these
layouts. These intervals measure dip randomness, not model accuracy.

**4:40–6:20 — The same trap, with one smooth dial.** Move to the catenoid between
two rings. A hanging-chain profile becomes a surface; pull the rings apart.
The stationary branch reaches its fold where **t·tanh(t)=1**, with t=h/(2a).
The proof encloses its unique positive root between **1.1996786402** and
**1.1996786403**. Show the numerical mapping h/R≈1.325487 separately. This
certifies the root, not the fluid dynamics or a complete stability theorem.
The existing catenoid model supplies the snap animation. A locally retained
shape and a global optimum are different questions.

**6:20–7:00 — What the soap computer taught us.** Return to the film. “Settling
down is a way to compute. It isn't a promise to find the best answer.” Let the
colour drain to black and the film disappear. Real-film footage can illustrate
the idea; do not present it as validation of these simulated percentages.

## Three shots

1. **One frame, two answers:** overhead hexagon, fixed pins, a longer settled
   dip beside the enumerated five-edge winner. Highlight length difference and
   120° junctions; keep both networks at the same scale. Hold long enough to see
   that adding junctions can still lose.
2. **The knee appears:** animate the unshaken curve from n=3 to 7 with Wilson
   bars, then add the 0.15 and 0.5 shake curves. Freeze on 5→6, display the
   1,000-dip denominator and unresolved count, and leave the seven-pin recovery
   visible. Caption: “regular polygons · simulated films · one shake.”
3. **A certified dial:** side view of two rings separating, the catenoid neck
   shrinking; inset `t·tanh(t)−1` crossing zero inside the certified interval.
   Switch from the exact root enclosure to the approximate h/R readout, then
   show the existing collapse animation. Caption the proof's scope explicitly.

Numbers: [measured grid](results/success-grid.md). Protocol and limitations:
[README](README.md). Root theorem: [catenoid_snap.ml](proofs/catenoid_snap.ml).
