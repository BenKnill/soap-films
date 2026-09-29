# Episode 4: The Soap Computer (working title)

**One idea:** a soap film pulls itself as small as it can. That single habit makes it solve geometry problems instantly and beautifully, but like a lazy genius it finds *a* good answer, not always *the* best one.

**Why this episode follows the Rhine one:** there, a surface showed us a hidden flow. Here, a surface is itself the computation. The last line of Episode 3 promised soap films.

## Story beats (draft)

1. **Cold open: the stripes.**
   - Picture: a film seen under a sodium lamp shows dark and bright stripes; switch to daylight and it becomes a rainbow.
   - Beat: the colours are a ruler measuring the film's thickness in nanometres, one stripe per ~221 nm (the thin-film passage the user remembers from Feynman; to be verified).
   - Hook: "this film is about a thousandth of a millimetre thick, and it is about to solve a problem computers find hard."
2. **The soap computer.**
   - Picture: pins between two plates; the film builds a shortest-road network with its own 120° junctions.
   - Beat: the Steiner tree problem, which is NP-hard.
   - Twist: dip again and you get a different, longer network. Films find local minima. (Story candidate: Scott Aaronson tried this; being verified.)
3. **Why 120°.** Three equal tensions balance only at 120°. Show the pull arrows at a junction.
4. **Only two ways to meet.**
   - Plateau's rules from the frames: three films along a line at 120°, four lines at a point at ~109.47°.
   - Jean Taylor (1976) proved there are no other stable ways for films to meet.
   - Picture: tetrahedron and cube frames; the cube's little square in the middle, which can sit in any of three orientations (symmetry breaking).
5. **The chain and the catenoid.**
   - A hanging chain (catenary, the 1691 solutions) spun around its axis is the film between two rings (Euler 1744).
   - Pull the rings apart: between h/R ≈ 1.055 and 1.3255 the film keeps a shape with *more* area than two disks, a local minimum. Past 1.3255 it snaps.
   - That's the same local-minimum story as the soap computer, in one smooth dial.
6. **Computing by settling down.**
   - Annealing: shake the system so it can escape poor minima. The "shake" button in the soap computer is exactly this.
   - Modern physical optimizers, stated modestly.
7. **Ending.** Back to the stripes. The film drains, turns black, and pops.

## Visual toolkit (built, in `docs/`)

- `filmcolor.js`: thin-film interference colour from the CIE matching functions, with daylight and sodium-lamp lookup tables.
- `steiner.js`: 2D film network with gradient descent and topology changes (T1 flips, absorption into pins, peeling off pins). Tested exact on the square (1+√3), the equilateral triangle (√3) and obtuse triangles.
- `surface.js`: 3D area minimiser on shared-edge patch meshes.
  - Tetrahedron frame: area exactly 6√2; 120.0° between films; 109.5° at the junction.
  - Cube frame: central square side ≈ 0.19 of the cube edge.
- `catenoid.js`: exact two-branch catenoid, h/R max = 1.325487, equal area at 1.055395; axisymmetric curvature flow for the collapse.
- `film3d.js`: WebGL film renderer (interference shading, wire tubes, triple lines, junction markers).

## Open questions

- Whether to reproduce a real soap-computer experiment. We could put pins between plates and film it. The user has footage skills and a phone; worth asking.
- The balance between the "lazy optimizer" framing and the singularities (Taylor) material.
- Length target: probably 7–8 minutes, like Episode 3.
