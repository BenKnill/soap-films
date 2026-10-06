# The Soap Computer: script

Episode 4 narration, 517 spoken words, 262.0 s of voice at 118 wpm (VoxCPM2 series narrator, seed 42). The spoken forms (numbers in words) are in `film/voice/script.json`; this is the written form, which is also the caption text.

What each beat rests on is noted in italics: *measured*, *simulated*, *computed* or *proved*.

## Cold open: the film as a ruler (0.6–29.7 s)

*rendered (Blender Cycles thin-film interference; procedural drainage and swirl)*

This soap film is thinner than a wavelength of light. Its colours are a ruler: each band is a different thickness. Under the pure yellow of a sodium lamp, the rainbow turns into stripes, one stripe for every 221 nanometers of thickness.

A film like this pulls itself as small as it can. That one habit makes it a computer.

## A computer made of soap (32.5–71.7 s)

*simulated (docs/steiner.js, measured four-pin dip #3), rendered*

Put pins between two glass plates, dip them in soapy water, and lift. Film walls join the pins, and tension pulls every wall as short as it can. Where walls meet, three equal pulls balance only at 120 degrees.

So the film hunts for the shortest network joining every pin. That's the Steiner tree problem, and with many pins it's hard even for computers.

Four pins on a square: the film finds the best, 1 + √3 times the side.

## Dip twice (73.7–106.3 s)

*simulated (measured six-pin dips #1 and #3), rendered*

Now put six pins on a hexagon, and dip twice.

Both films settle, with every junction at 120 degrees. But they are different networks.

The shortest has no junctions at all: five sides of the hexagon. The other is about four percent longer, and the film keeps it anyway.

The film found a local minimum: nothing nearby is shorter, but it isn't the shortest.

## Put a number on it (107.9–156.7 s)

*measured in simulation (results/success-grid.md: 1,000 dips per point, Wilson 95% intervals); optimum by exhaustive numerical search (tools/optimum.py)*

How often does it find the shortest? We counted, in a simulation, not a tub of soap. For three to seven pins on a regular polygon, we ran a thousand random dips each, and checked each against the shortest network, found by trying every layout.

Three, four and five pins: a thousand out of a thousand. Six pins: 506 out of one thousand. A coin toss. The biggest drop is from five pins to six.

Seven pins recover a little, to 58 percent. But the polygon changes shape with the pin count, so this curve belongs to this setup.

## Does shaking help? (157.9–178.6 s)

*measured in simulation (same grid, paired shake effects)*

Can shaking help? Jiggling lets a system escape a poor valley; that's the idea of annealing. One shake after settling moved six pins from 50.6 to 51 percent. That is inside the noise. This shake did not rescue the film.

## One smooth dial (180.4–211.0 s)

*exact catenoid shapes (docs/catenoid.js equations); the collapse is a simulated curvature flow*

Here is the same story as one smooth dial. Between two rings, a film makes a catenoid: a hanging chain's curve, spun around the axis.

Pull the rings apart, and its waist narrows. Soon two flat discs would have less area, but the film holds on: a local minimum again.

Then there is no catenoid left to keep. The film snaps.

## What is proved (214.4–244.2 s)

*proved in HOL Light (proofs/catenoid_snap.ml): one positive root of t·tanh t = 1, in (1.1996786402, 1.1996786403); h/R ≈ 1.3255 is computed, not proved*

The snap comes where t · tanh t = 1. In the HOL Light theorem prover, we proved that this has exactly one positive root, and pinned it down to within one ten-billionth.

The ring spacing at the snap, about 1.33 radii, is computed, not proved. The proof covers this equation. It does not cover the fluid.

## Ending (246.0–261.4 s)

*rendered (drainage to a black film, then the pop)*

Settling down is a way to compute. It is not a promise of the best answer.

As this film drains, its top turns black, just a few tens of nanometers thick. And then it's gone.
