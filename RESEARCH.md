# Episode 4 research: soap films as lazy optimizers

Compiled 2026-09-29 for the "soap computer" episode (see `PLAN.md`).

**How each item was checked**

| Tag | Meaning |
|---|---|
| [CR] | Metadata (authors, venue, volume, pages, DOI) confirmed through the Crossref API |
| [FT] | I read the full text or the relevant passage myself (PDF, scan or publisher page) |
| [AX] | arXiv record or PDF read |
| [WC] | Licence confirmed through the Wikimedia Commons API |
| [WP] | Wikipedia or another secondary source only; not checked further |
| [COMP] | Computed by me (Python, or Surface Evolver 2.70 built from source) |

**Status labels:** "flag" means wrong, misleading, contested or unverified. "Verdict" is my overall conclusion.

---

## 1. Joseph Plateau: book, laws, blindness

**Life.** Joseph Antoine Ferdinand Plateau was born in Brussels on 14 Oct 1801 and died in Ghent on 15 Sep 1883 [WP]. Nature published an obituary: "Joseph-Antoine-Ferdinand Plateau", *Nature* 28:529–530 (27 Sep 1883), doi:10.1038/028529a0 [CR].

**Book.** Plateau, J. (1873). *Statique expérimentale et théorique des liquides soumis aux seules forces moléculaires*. 2 vols. Paris: Gauthier-Villars; London: Trübner & Co.; Gand & Leipzig: F. Clemm. Publisher line taken from Maxwell's review [FT].
- Public-domain scans:
  - vol. 1: https://archive.org/details/statiqueexprime01platgoog
  - vol. 2: https://archive.org/details/statiqueexprime00platgoog
  - The Internet Archive marks both "NOT_IN_COPYRIGHT".
- The book gathers his long series of memoirs from the 1840s to the 1860s on "figures d'équilibre". I did not check the exact span (1842/43 to 1868).

**The laws in Plateau's own words.** Vol. 1, Ch. V ("Systèmes laminaires, leur développement, leurs lois"), §184, pp. 320–321 [FT, archive.org OCR]:
> « …toujours à une même arête liquide aboutissent trois lames, et … les arêtes liquides aboutissant à un même point liquide sont toujours au nombre de quatre ; … leur invariabilité constitue deux lois. En outre, … il résulte de l'égalité des tensions que les trois lames unies par une arête liquide font nécessairement entre elles, à cette arête, des angles égaux, et que, par suite, les quatre arêtes concourant en un même point liquide font aussi entre elles, à ce point, des angles égaux, ce qui constitue deux autres lois générales. »

My translation: "Three films always meet at one liquid edge, and four liquid edges always meet at one liquid point. Because the tensions are equal, the three films meet at equal angles (120°) and the four edges meet at equal angles (the tetrahedral angle, arccos(−1/3) ≈ 109.47°)." So Plateau stated four laws: two about counts and two about angles. He derived the angles from equal tension, and he checked them by measurement on the tetrahedron, prism and octahedron frames (§185).

**Blindness.**
- **The 1829 sun-gazing is real.** MacTutor says: "his ardour for experimentation pushed him to carry out a very dangerous experiment consisting in looking directly at the bright sun during approximately twenty-five seconds." Source: https://mathshistory.st-andrews.ac.uk/Biographies/Plateau/ [FT]
- **Timeline (sources differ).**
  - MacTutor: eye inflammation from 1841, totally blind by 1843. He was made full professor at Ghent on 29 June 1844.
  - Summaries of De Laey (see below): problems began "when he was 42" and total blindness came in 1844.
  - Recommended wording: **"blind by 1843–44, at about 42."**
- **Cause.** The sun-gazing cause is contested and probably wrong.
  - Plateau himself blamed the 1829 experiment.
  - An ophthalmologist, J. J. De Laey, argues the sun-gazing gave only a temporary scotoma that healed within days, and that the real cause was **chronic uveitis**, which had no effective treatment then. Linking the two events is a *post hoc* fallacy.
  - Citation: De Laey, J. J. (2002). "De blindheid van Joseph Plateau. Mythe en realiteit." *Tijdschrift voor Geneeskunde* 58(13):915–920. doi:10.2143/TVG.58.13.1001372 [CR]. I could not read the abstract myself. The content above comes from summaries at https://aty.sdsu.edu/vision/others.html and from the ResearchGate record "The blind Joseph Plateau. Myth and reality".
  - Wikipedia agrees: "this may not have been the case, and he may have instead had chronic uveitis".
- **Recommended script wording:** "He went blind in his early forties. He blamed a youthful experiment staring at the sun, but modern doctors think it was an eye inflammation."

**He did the soap-film work blind.** He kept working with the help of his son Félix Plateau, his son-in-law Gustave Van der Mensbrugghe and colleagues at Ghent (Catholic Encyclopedia 1913, https://en.wikisource.org/wiki/Catholic_Encyclopedia_(1913)/Joseph-Antoine_Plateau [WP]). The memoir series only began in the 1840s, and the wire-frame ("laminar system") work falls after he lost his sight, so the observations were made by others under his direction. This is my inference from the dates; I did not check the date of each memoir.

**Other sources**
- Wautier, K., Jonckheere, A. & Segers, D. (2012). "The Life and Work of Joseph Plateau: Father of Film and Discoverer of Surface Tension." *Physics in Perspective* 14(3):258–278. doi:10.1007/s00016-012-0087-8 [CR]. Paywalled; not read.
- **Maxwell reviewed the book.** Maxwell, J. C. (1874). "Statique expérimentale et théorique des Liquides…" *Nature* 10:119–121 (18 June 1874). doi:10.1038/010119a0 [CR, first paragraph FT]. His opening:
  > "ON an Etruscan vase in the Louvre figures of children are seen blowing bubbles. … whatever our nominal age may be—we are of the same family as those Etruscan children."
  - A public-domain scan of that Nature issue is on Commons [WC]: https://commons.wikimedia.org/wiki/File:Nature_-_a_Weekly_Illustrated_Journal_of_Science._Volume_10,_1874_June_18,_(No._242)_(IA_dbc.wroc_pl.15783).pdf

---

## 2. Jean E. Taylor (1976)

**Citation.** Taylor, J. E. (1976). "The structure of singularities in soap-bubble-like and soap-film-like minimal surfaces." *Annals of Mathematics* (2) 103(3):489–539. doi:10.2307/1970949. MR0428181; Zbl 0335.49032. [CR; Annals page https://annals.math.princeton.edu/1976/103-3/p08]. Taylor is the **sole author**.

**What she proved.**
- **The class of surfaces.** She works with Almgren's "(M, ε, δ)-minimal sets": closed 2-dimensional sets that cannot lower their area by deformations inside small balls, up to an error ε(r)·r².
  - ε ≡ 0 models soap films.
  - ε(r) ≤ C r^α allows for volume constraints, which is what soap-bubble clusters need.
- **The main result.** Near every point, such a set in R³ is C^{1,α}-diffeomorphic to one of exactly three minimal cones:
  1. a plane;
  2. **Y**: three half-planes meeting along a line at 120°;
  3. **T**: the cone over the edges of a regular tetrahedron. This is six sheets and four Y-lines meeting at arccos(−1/3) ≈ 109.47°.
- **What this means for the singular set.** It consists of C^{1,α} curves of Y-type plus isolated T-points. This is Plateau's laws as a theorem.
- **The cone classification behind it.** There are exactly 10 cones built over nets of great-circle arcs on the sphere that meet at 120°: the plane, the Y, and 8 polyhedral cones (tetrahedron, cube, triangular prism, pentagonal prism, dodecahedron and three more). Taylor showed that only the plane, Y and T minimize area. Ken Brakke puts it this way: "There are only eight polyhedra that satisfy this condition. But only one gives a true minimal cone, since the other seven cones can be deformed to soap films of less area." (https://kenbrakke.com/cones/cones.htm [FT])
- **Densities.** The area in the unit ball divided by π is 1 for the plane, 3/2 for Y and 6·arccos(−1/3)/(2π) ≈ 1.8245 for T [COMP].

**What it built on**
- Almgren, F. J. (1976). "Existence and regularity almost everywhere of solutions to elliptic variational problems with constraints." *Mem. Amer. Math. Soc.* 4(165). doi:10.1090/memo/0165 [CR].
- Her thesis did the triple-curve case: Taylor, J. E. (1973). "Regularity of the singular sets of two-dimensional area-minimizing flat chains modulo 3 in R³." *Inventiones Math.* 22:119–159. doi:10.1007/BF01392299 [CR]. Princeton PhD 1973, advisor Almgren.

**Popular companion article.** Almgren, F. J. & Taylor, J. E. (1976). "The geometry of soap films and soap bubbles." *Scientific American* 235(1):82–93 (July 1976). doi:10.1038/scientificamerican0776-82 [CR].

**Modern re-proof.** G. David (2008), arXiv:0806.2080, abstract [AX]: "Jean Taylor's result … says that Almgren almost-minimal sets of dimension 2 in R³ are locally C^{1+α}-equivalent to minimal cones."

**Quotes you can use**
- Martin Li (CUHK), Hong Kong Laureate Forum talk, 2021: "Jean TAYLOR published the first mathematical proof of Plateau's laws, hence confirming Plateau's observations in his soap film experiments more than a century ago." https://www.hklaureateforum.org/en/soap-films-minimal-surfaces-and-beyond [FT]
- Biographies of Women Mathematicians (Agnes Scott): Taylor "has been described as an 'experimental mathematician' who does experiments as a motivation for ideas, but then tries to prove that what she sees is what you have to get." https://www.agnesscott.edu/lriddle/women/jtaylor.htm [FT]. This is the biographer's paraphrase, not Taylor's own words. Her own voice is probably in D. J. Albers, "Still Questioning Authority: An Interview with Jean Taylor", *College Math. J.* 27(4), 1996 (not read).

**Flags**
- Wikipedia's Jean Taylor page says "she, along with Almgren, published the first proof". That runs together the sole-authored Annals paper and the joint Scientific American article.
- The theorem covers idealized, area-minimizing sets **away from the wire boundary**. Real films have finite thickness and Plateau borders; that is fine for a story, but say "ideal films".
- On notation: Taylor's hypotheses allow a small ε, not only ε = 0. "(M,0,δ)" is the soap-film special case.

---

## 3. The Steiner tree problem

**Three points (the Fermat–Torricelli point).**
- Fermat posed the problem to Torricelli (1640s). Torricelli solved it, and Viviani published the solution in 1659 [WP, "Fermat point"].
- Scholarly source: Krarup, J. & Vajda, S. (1997). "On Torricelli's geometrical solution to a problem of Fermat." *IMA J. Management Math.* 8(3):215–224. doi:10.1093/imaman/8.3.215 [CR].

**Networks.** The name is a historical misnomer.
- Source: Brazil, M., Graham, R. L., Thomas, D. A. & Zachariasen, M. (2014). "On the history of the Euclidean Steiner tree problem." *Arch. Hist. Exact Sci.* 68(3):327–354. doi:10.1007/s00407-013-0127-z [CR; abstract FT]. The abstract: "goes back to Gergonne in the early nineteenth century."
- Gergonne (1810/11, *Annales de Mathématiques pures et appliquées* 1:375–384) posed it as linking cities by canals of least total length.
- Gauss described a version in an 1836 letter to Schumacher [WP; attributed via Brazil et al., not read].
- The first serious treatment is Jarník & Kössler (1934, in Czech, *Časopis pro pěstování matematiky a fysiky* 63:223–235).
- **Flag:** Steiner did not pose the network problem. The name was popularized by Courant & Robbins.

**Courant and Robbins, with soap films**
- Courant, R. & Robbins, H. (1941). *What Is Mathematics?* Oxford University Press. Ch. VII "Maxima and Minima" contains "Steiner's Problem" and a later section on soap-film experiments. 2nd ed. revised by I. Stewart, OUP 1996. I did not check the section numbers or pages; the 1941 scans on archive.org are lending-only. Dutta et al. cite pp. 354–356, 359–361 and 385–397 of the 1996 edition.
- Courant, R. (1940). "Soap film experiments with minimal surfaces." *Amer. Math. Monthly* 47(3):167–174. doi:10.1080/00029890.1940.11990957 [CR].

**Structure of optimal networks**
- Every added (Steiner) point has degree 3 with 120° angles.
- There are at most n−2 Steiner points; a "full" tree has exactly n−2.
- Source: Gilbert, E. N. & Pollak, H. O. (1968). "Steiner minimal trees." *SIAM J. Appl. Math.* 16(1):1–29. doi:10.1137/0116001 [CR]. The properties themselves are older (Gergonne, and Jarník–Kössler) [WP].

**Hardness**
- Garey, M. R., Graham, R. L. & Johnson, D. S. (1977). "The complexity of computing Steiner minimal trees." *SIAM J. Appl. Math.* 32(4):835–859. doi:10.1137/0132072 [CR]. This paper covers the **Euclidean** problem and shows it is NP-hard.
- Earlier conference version: "Some NP-complete geometric problems", *STOC '76*, pp. 10–22. doi:10.1145/800113.803626 [CR].
- Rectilinear version: Garey & Johnson, "The rectilinear Steiner tree problem is NP-complete", same SIAM issue, pp. 826–834 [search result only].
- **Precision caveat.** The exact Euclidean decision problem is not known to be in NP, because lengths are sums of square roots. With finite precision it is NP-complete. Aaronson (2005) makes the same point in his footnote 1.

**Steiner ratio (optional).** The Gilbert–Pollak conjecture says the ratio is 2/√3. It is still open: the 1990 Du–Hwang proof is considered incomplete (Ivanov & Tuzhilin 2012, *Algorithmica* 62:630–632, doi:10.1007/s00453-011-9508-3) [WP].

**Why plates and pins give shortest networks.** Between two parallel plates the film area equals gap × total length. The pins, though, must be thin; see Dutta et al. below.

---

## 4. Scott Aaronson's soap experiment, and others

**Citation.** Aaronson, S. (2005). "Guest Column: NP-complete problems and physical reality." *ACM SIGACT News* 36(1):30–52. doi:10.1145/1052796.1052804 [CR]; arXiv:quant-ph/0502072 [AX, FT §3].

**Background.** The soap-bubble argument for P = NP came from Bringsjord, S. & Taylor, J. (2004), "P=NP", arXiv:cs/0406056 [AX]. Craig Feinstein then bet on comp.theory that no paper shows soap films missing the global minimum.

**What Aaronson did** (quote):
> "I bought two 8″ × 9″ glass plates, paint to mark grid points on the plates, thin copper rods which I cut into 1″ pieces, suction cups to attach the rods to the plates, liquid oil soap, a plastic tub to hold the soapy water, and work gloves. I obtained instances of the Euclidean Steiner Tree problem from the OR-Library website. I concentrated on instances with 3 to 7 vertices…"

**What he found:**
> "with 3 or 4 pegs, the optimum tree usually is found. However, by no means is it always found, especially with more pegs. … I also sometimes found triangular 'bubbles' of three Steiner vertices—which is much harder to explain, since such a structure could never occur in a Steiner tree. In general, the results were highly nondeterministic; I could obtain entirely different trees by dunking the same configuration more than once. Sometimes I even obtained a tree that did not connect all the pegs."

> "sometimes the bubbles would start in a suboptimal configuration, then slowly 'relax' toward a better one. Even with 4 or 5 pegs, this process could take around ten seconds…"

**His conclusion:** "I found no reason to doubt the 'party line,' that soap bubbles do not solve NP-complete problems in polynomial time by magic."

**His footnote 3** cites his own column as the paper Feinstein asked for, adding: "**I win.**"

**Other soap-film Steiner experiments (verified)**
- **Dutta, Khastgir & Roy (2010).** Dutta, P., Khastgir, S. P. & Roy, A. (2010). "Steiner trees and spanning trees in six-pin soap films." *Am. J. Phys.* 78(2):215–221. doi:10.1119/1.3247982 [CR]; arXiv:0806.1340 [AX, FT] (IIT Kharagpur).
  - Six pins at the corners of a regular hexagon with unit side. The films usually reported have lengths **5, √27 ≈ 5.196 and √28 ≈ 5.292**.
  - The shortest one (length 5) is a *spanning tree*, i.e. five sides of the hexagon with no Steiner points. Their footnote 2: "There are cases (like the present six-pin problem), where the minimal tree is a spanning tree."
  - Thicker pins (0.32, 0.80, 2.60 and 4.48 mm) create new, non-minimal stable films. Quote: "each configuration indicates a local minimum in the energy structure of the system. Many a times these local minima are not deep enough and are also not well separated so the slightest perturbation would slide a particular configuration to a different nearby lower local minimum state."
- **Isenberg's papers**
  - Isenberg, C. (1975). "Problem solving with soap films, Parts I & II." *Physics Education* 10:452–456 and 500–503. doi:10.1088/0031-9120/10/6/314 and 10.1088/0031-9120/10/7/004 [CR].
  - Isenberg, C. (1976). "The soap film: an analogue computer." *American Scientist* 64:514–518, reprinted as a centennial classic in 2012, doi:10.1511/2012.96.243 [CR for the 2012 reprint].
  - Isenberg, C. (1977). "Problem solving with soap films." *Phys. Teacher* 15(1):9–18. doi:10.1119/1.2339522 [CR].
- **Video.** Mihai Oltean, "Solving Steiner tree problem with water and soap", YouTube https://www.youtube.com/watch?v=PI6rAOWu-Og (confirmed through oEmbed).

---

## 5. The catenoid: history and the two-ring numbers

**Euler (1744).** *Methodus inveniendi lineas curvas maximi minimive proprietate gaudentes*. Lausanne & Geneva: Bousquet. Caput V, §47, Exemplum VII, about pp. 196–197 (page read from OCR headers) [FT, Smithsonian scan https://archive.org/details/methodusinvenie00eule].
> "Invenire curvam, quae inter omnes alias ejusdem longitudinis, circa axem AZ rotata, producat solidum cujus superficies sit vel maxima vel minima."

Euler finds the answer "est aequatio generalis pro Catenaria, & satisfacit, dummodo axis respectu catenae suspensae situm teneat horizontalem … priori casu superficies solidi fiet minima."

Nuances:
- Euler poses the problem among curves *of equal length*. The general answer is a catenary whose directrix is parallel to the axis; the catenoid is the case where the directrix is the axis.
- I found **no figure** for §47 in the 1744 plates, so don't promise "Euler's catenoid drawing".
- Wikipedia says "found and proved to be minimal by Leonhard Euler in 1744" [WP].
- Matthias Weber's note on this example: https://minimalsurfaces.blog/2018/10/14/exemplum-vii/

**Meusnier.** Memoir presented in 1776 and published in 1785: "Mémoire sur la courbure des surfaces," *Mém. Math. Phys. (Savants étrangers)* 10:477–510 [WP].
- He showed the catenoid and helicoid satisfy Lagrange's minimal-surface equation (1760/62).
- He read that equation geometrically as principal curvatures that are equal and opposite, which we now call zero mean curvature.
- The term "mean curvature" came later, so the phrase "Meusnier showed zero mean curvature" is an anachronism.

**Two coaxial rings of radius R, separation h.** Profile r(z) = a·cosh(z/a). Write t = h/(2a), so R = a·cosh t [COMP]:

| Quantity | Value |
|---|---|
| Existence limit | h/R ≤ 2t/cosh t, maximal where t·tanh t = 1 (t* = 1.1996786) |
| Critical ratio | **h/R = 2/sinh t* = 1.3254868**, i.e. h/(2R) = **0.6627434** |
| Neck radius at the limit | 0.5524 R |
| Area at the limit | t* × (2πR²) ≈ **1.1997 × the two disks** |
| Equal area with two disks (Goldschmidt solution) | 2t + sinh 2t = 1 + cosh 2t gives t = 0.6392323, so **h/R = 1.0553948**; neck 0.8255 R |
| 1.0554 < h/R < 1.3255 | The fat catenoid is a local but not global minimum. The thin catenoid is always unstable. |

Independent check:
- Goldstein, R. E., Pesci, A. I., Raufaste, C. & Shemilt, J. D. (2021). "Geometry of catenoidal soap film collapse induced by boundary deformation." *Phys. Rev. E* 104:035105. doi:10.1103/PhysRevE.104.035105 [CR, FT]. **Open access under CC BY 4.0.**
- They use D = (half-separation)/R and report D_c = 0.6627, α_c = 0.5524, A_c = 1.199, and D* = 0.528 for the Goldschmidt crossover. All of these agree with my table.
- Your `docs/catenoid.js` also gives 1.325487 and 1.055395.

**Flag:** 0.6627 is often quoted as "h/R". It is h/(2R), i.e. separation divided by diameter.

**What happens at collapse** (Goldstein et al. 2021, Fig. 1 caption, quoted):
> "(ii) narrowing of the neck, (iii) formation of the 'Martini glass' configuration consisting of two cones connected by a cylinder, (iv) development of a double pinch at the ends of the central cylindrical region, and (v) formation of a double-cone configuration and breakup of the central thread leading to satellite bubbles."

- The area relaxes towards the two-disk value "in less than 30 ms".
- The film starts at 57° to the axis, close to arctan(R/d_c) = 56.5°.

Classic references:
- Cryer, S. A. & Steen, P. H. (1992). "Collapse of the soap-film bridge: quasistatic description." *J. Colloid Interface Sci.* 154(1):276–288. doi:10.1016/0021-9797(92)90101-Q [CR].
- Robinson, N. D. & Steen, P. H. (2001). "Observations of singularity formation during the capillary collapse and bubble pinch-off of a soap film bridge." *J. Colloid Interface Sci.* 241(2):448–458. doi:10.1006/jcis.2001.7717 [CR].
- Salkin, L., Schmit, A., Panizza, P. & Courbin, L. (2014). "Influence of boundary conditions on the existence and stability of minimal surfaces of revolution made of soap films." *Am. J. Phys.* 82(9):839–847. doi:10.1119/1.4879541 [CR].
- Isenberg's book also treats it. I did not check the page.

---

## 6. The catenary

**History** [WP "Catenary", which cites Lockwood and Truesdell 1960; primary sources not read]:
- **Galileo.** *Two New Sciences* (1638) is often said to claim the chain is a parabola. In fact he called it an approximate parabola that is good for shallow sag. **Flag:** "Galileo thought it was a parabola" oversimplifies.
- **Jungius.** Joachim Jungius (1587–1657) showed it is not a parabola; this was published posthumously in 1669.
- **Hooke.** His 1675 anagram "ut pendet continuum flexile, sic stabit contiguum rigidum inversum" means "as hangs the flexible line, so but inverted will stand the rigid arch". It was decoded in 1705.
- **1691.** Jakob Bernoulli posed the challenge in 1690. Leibniz, Huygens and Johann Bernoulli published solutions in *Acta Eruditorum*, June 1691. A public-domain scan of the 1691 volume is on Commons [WC]: https://commons.wikimedia.org/wiki/File:Acta_eruditorum._1691_(IA_s1id13206570).pdf (find the June pages and plates).

**The link: one integral.**
- A hanging chain of fixed length minimizes its potential energy, which is proportional to ∫ y ds.
- A surface of revolution has area 2π ∫ y ds.
- Euler's §47 minimizes exactly this integral among curves of fixed length, and **Euler himself says the answer is the hanging-chain curve** with the axis horizontal.
- If the length is free, the directrix drops onto the axis and you get the catenoid. So "the catenoid is the catenary spun around its axis" is more than a coincidence: both are minimizers of the same integral.

---

## 7. Soap-film physics numbers

**Surface tension.** Pure water is about 72 mN/m.
- Dish-soap bubble mix (2 parts Dreft, 2 water, 1 glycerol): "γ_b = 26 ± 1 mN/m". Source: Cohen, C., Darbois Texier, B., Reyssat, E., Snoeijer, J. H., Quéré, D. & Clanet, C. (2017). "On the shape of giant soap bubbles." *PNAS* 114(10):2515–2519. doi:10.1073/pnas.1616904114 [FT via PMC5347548].
- TTAB lab solutions: 35–38 mN/m (Goldstein et al. 2021).
- **Use 25–35 mN/m.** The film has two surfaces, so its tension is 2γ ≈ 0.05–0.07 N/m.
- Measurement-method paper: Román, F. L., Faro, J. & Velasco, S. (2001). "A simple experiment for measuring the surface tension of soap solutions." *Am. J. Phys.* 69(8):920–921. doi:10.1119/1.1365402 [CR].

**Thickness**
- Colourful films are about 0.1 to a few µm. Cohen et al. measured 0.81 µm and 6.6 µm on giant bubbles from bursting speeds of 8 and 2.8 m/s. That fits Culick's law V = √(2γ/(ρh)): with h = 1 µm, V ≈ 7 m/s [COMP].
- Black films come in two kinds [WP "Soap film", citing Pugh 2016, *Bubble and Foam Chemistry*, CUP; other sources vary]:
  - common black film: about 10–100 nm, often quoted ≈ 30–50 nm, depending on salt;
  - Newton black film: ≈ 4–5 nm, basically two surfactant layers.
- **Flag:** "5–30 nm" is acceptable shorthand, but common black films can be thicker. Say "a few to a few tens of nanometres".

**Colours.** Thin-film interference, explained in the Harvard demo page quoted in §11.

**Drainage.** Gravity, plus suction into the Plateau borders, thins the top of a vertical film. The colour bands are lines of equal thickness. The top turns silver-grey, then black, before the film pops.

**Young–Laplace**
- Each surface gives Δp = γ(1/R₁ + 1/R₂). A bubble has two surfaces, so Δp = **4γ/R**.
- Example: R = 2 cm and γ = 25 mN/m give **Δp = 5 Pa**, about 1/20,000 atm [COMP].
- A film spanning a wire frame has the same air pressure on both sides, so its mean curvature is 0 and it must be saddle-shaped.
- Source: de Gennes, P.-G., Brochard-Wyart, F. & Quéré, D. (2004). *Capillarity and Wetting Phenomena*. Springer. doi:10.1007/978-0-387-21656-0 [CR].

---

## 8. Cube and tetrahedron frames

**Plateau on the cube** (1873, vol. 1, §182, pp. 318–319, Fig. 71; his frame was 7 cm on a side) [FT]:
> « la charpente cubique donne invariablement le système que je représente ici : il se compose … de douze lames partant respectivement des douze arêtes solides et aboutissant toutes à une lamelle unique quadrangulaire placée au milieu de l'ensemble. Les côtés de cette lamelle sont légèrement courbes ainsi que toutes les autres arêtes liquides, et conséquemment toutes les lames, à l'exception de la lamelle centrale, ont de faibles courbures. »

So the cube film has 13 films. The central one is flat because it lies in a mirror plane of the cube. The films meet in 4 T-points at the corners of the little square.

**My Surface Evolver computation** [COMP]. I used Brakke's `cubefilm.fe` and refined to 40,960 facets. The mesh converged between the last two refinement levels. For a unit cube:

| Quantity | Value |
|---|---|
| Corners of the central face | (0.5, 0.4070, 0.4070) and symmetric points |
| Corner-to-corner side | **≈ 0.186 × edge**, about 1.3 cm on Plateau's 7 cm frame. Your `surface.js` gives ≈ 0.19. |
| Area of the central face | ≈ 0.0378. That is more than the straight-sided square (0.0346), so its edges bow slightly outward. |
| Total film area | **4.23957** |
| Cone over the 12 edges | 3√2 = 4.24264 |

- The film beats the cone by only **0.07%**. Yet the cone is never seen, because it is not stable: it is one of Taylor's seven non-minimizing cones.
- By symmetry the square can sit in any of 3 orientations.

**Tetrahedron.** Plateau §185, p. 321:
> « formé de six lames qui se joignent suivant quatre arêtes liquides aboutissant toutes au centre de la figure. »

These are six flat triangles meeting at the centre, with 120° between films and 109.47° between the four lines. The area is (3√2/4)·a² ≈ 1.0607 a². Evolver confirms the flat cone is stable: the centre vertex stays at the centroid, and the area is 6√2 for edge 2√2 [COMP].

**References**
- Isenberg, C. (1978). *The Science of Soap Films and Soap Bubbles*. Clevedon: Tieto. Dover reprint 1992, ISBN 0-486-26960-4 (Open Library OL4117530W). I checked the bibliographic data only, not the pages.
- Brakke, K. A. (1992). "The Surface Evolver." *Experimental Math.* 1(2):141–165. doi:10.1080/10586458.1992.10504253 [CR].
- Brakke's cone gallery and data files: https://kenbrakke.com/cones/cones.htm. The files are `cubefilm.fe`, `cubecone.fe` and `tetraflm.fe`.

To reproduce: Evolver 2.70 (built with `-DGENERIC` and `nulgraph.o`, plus a one-line stub for `set_graphics_title`). Run `r; g …; u; V; … hessian` for 5 refinements, then print `total_area` and `vertex[9..12]`. The build lives in the session scratchpad.

---

## 9. Computing by minimization: keep it modest

**Simulated annealing.** Kirkpatrick, S., Gelatt, C. D. & Vecchi, M. P. (1983). "Optimization by simulated annealing." *Science* 220(4598):671–680. doi:10.1126/science.220.4598.671 [CR; abstract FT via PubMed 17813860]:
> "There is a deep and useful connection between statistical mechanics … and multivariate or combinatorial optimization … A detailed analogy with annealing in solids provides a framework for optimization of the properties of very large and complex systems."

Černý discovered it independently: Černý, V. (1985). *J. Optim. Theory Appl.* 45(1):41–51. doi:10.1007/BF00940812 [CR].

**Ising machines** (physical optimizers)
- NP problems as Ising problems: Lucas, A. (2014). "Ising formulations of many NP problems." *Front. Phys.* 2:5. doi:10.3389/fphy.2014.00005 [CR].
- Coherent Ising machines (laser pulses in a fibre loop):
  - Inagaki, T. et al. (2016). "A coherent Ising machine for 2000-node optimization problems." *Science* 354:603–606. doi:10.1126/science.aah4243 [CR].
  - McMahon, P. L. et al. (2016). "A fully programmable 100-spin coherent Ising machine with all-to-all connections." *Science* 354:614–617. doi:10.1126/science.aah5178 [CR].
- Superconducting quantum annealer (D-Wave): Johnson, M. W. et al. (2011). "Quantum annealing with manufactured spins." *Nature* 473:194–198. doi:10.1038/nature10012 [CR].
- Comparison of the two: Hamerly, R. et al. (2019). *Sci. Adv.* 5:eaau0823. doi:10.1126/sciadv.aau0823 [CR].
- **Review for the modest line.** Mohseni, N., McMahon, P. L. & Byrnes, T. (2022). "Ising machines as hardware solvers of combinatorial optimization problems." *Nat. Rev. Phys.* 4:363–379. doi:10.1038/s42254-022-00440-8 [CR; abstract FT]:
  > "Today, Ising hardware based on classical digital technologies is the best performing for common benchmark problems. However, the performance is problem-dependent…"

**Framing:** these machines are heuristics. Like soap, they can get stuck in local minima, and none is known to solve NP-hard problems efficiently.

---

## 10. Images: licences checked through the Commons API

| What | URL | Licence |
|---|---|---|
| Plateau daguerreotype, 1843, by Joseph Pelizzaro. Taken in the year he went blind. | https://commons.wikimedia.org/wiki/File:Joseph_Plateau.jpg | Public domain |
| Same portrait, retouched (Albert Callisto) | https://commons.wikimedia.org/wiki/File:Joseph_Plateau_-_clean.jpg | CC BY-SA 4.0 |
| Plateau engraving, *Popular Science Monthly* vol. 36 | https://commons.wikimedia.org/wiki/File:PSM_V36_D594_Joseph_Antoine_Ferdinand_Plateau.jpg | Public domain |
| Plateau lithographs by J. Desmannez (KU Leuven), including a 3665×5167 scan | https://commons.wikimedia.org/wiki/File:Jh._Plateau,_PA08758.jpg and https://commons.wikimedia.org/wiki/File:J._Plateau,_PA02905.jpg | Public domain |
| 1873 title page (BEIC) | https://commons.wikimedia.org/wiki/File:Plateau,_Joseph_Antoine_Ferdinand_%E2%80%93_Statique_exp%C3%A9rimentale_et_th%C3%A9orique_des_liquides_soumis_aux_seules_forces_mol%C3%A9culaires,_1873_%E2%80%93_BEIC_3905896.jpg | Public domain |
| 1873 book figures: Fig. 71 cube (p. 318); Figs. 73–75 tetrahedron, prism, octahedron (pp. 320–321) | archive.org `statiqueexprime01platgoog` | Public domain (Google scan; Google asks for non-commercial use, which is a request, not a US legal restriction) |
| Same book at MDZ | MDZ | "No Copyright – Non-Commercial Use Only". Avoid for a monetized video. |
| Same book at Gallica | Gallica | Free for non-commercial use; commercial use needs a licence. Avoid for a monetized video. |
| Euler 1744, full scan | https://commons.wikimedia.org/wiki/File:Methodus_inveniendi_lineas_curvas_maximi_minimive_proprietate_gaudentes,_sive,_Solutio_problematis_isoperimetrici_latissimo_sensu_accepti_(IA_methodusinvenie00eule).pdf | Public domain |
| Euler 1744 title page | https://commons.wikimedia.org/wiki/File:Methodus_inveniendi_-_Leonhard_Euler_-_1744.jpg | Public domain |
| Euler 1744, two redrawn variation figures, "Fig. 3" and "Fig. 4". Not a catenoid. | Commons | CC BY-SA 4.0 |
| *Acta Eruditorum* 1691 (the catenary papers) | https://commons.wikimedia.org/wiki/File:Acta_eruditorum._1691_(IA_s1id13206570).pdf | Public domain |
| C. V. Boys, *Soap-Bubbles, their colours and the forces which mould them*: many classic figures | https://commons.wikimedia.org/wiki/File:Soap-bubbles,_their_colours_and_the_forces_which_mould_them_(IA_cu31924031226974).pdf | Public domain |
| Maxwell's 1874 review, in *Nature* no. 242 | link in §1 | Public domain |
| Modern photo: soap-film catenoid | https://commons.wikimedia.org/wiki/File:Bulle_cat%C3%A9no%C3%AFde.png | CC0 |
| Modern photos: cube and tetrahedron frame films (Universum Bremen, "Bin im Garten") | https://commons.wikimedia.org/wiki/File:Minimalfl%C3%A4che_mit_Seifenhaut_W%C3%BCrfel_0328.JPG and https://commons.wikimedia.org/wiki/File:Minimalfl%C3%A4che_mit_Seifenhaut_Tetraeder_0326.JPG | CC BY-SA 3.0 |
| Modern photos: Plateau-problem exhibits, Matemateca IME-USP | "Problema de Plateau 01–08" | CC BY-SA 4.0 |
| Collapse-sequence photos, Goldstein et al. 2021 | *PRE* article | CC BY 4.0: reusable with attribution |

**Not openly licensed**
- Courant & Robbins (1941; 1996 edition): OUP copyright. The archive.org copies are lending-only. Do not reuse the figures.
- Courant (1940) *Monthly*: treat as copyrighted.
- Aaronson (2005) and Dutta et al. (2010): arXiv non-exclusive licence only. Ask the authors, or redraw.

---

## 11. Feynman's sodium-lamp passage (added request)

**Feynman Lectures on Physics.** Vol. I, Ch. 30 "Diffraction", §30-5 "Colored films; crystals" (https://www.feynmanlectures.caltech.edu/I_30.html) [FT via a reader proxy]:
> "if we look at the reflection of a light source in a thin film, we see the sum of two waves; if the thicknesses are small enough, these two waves will produce an interference, either constructive or destructive, depending on the signs of the phases. It might be, for instance, that for red light, we get an enhanced reflection, but for blue light … a destructively interfering reflection, so that we see a bright red reflection. If we change the thickness … it may be reversed … So we see colors when we look at thin films … Thus we suddenly appreciate another hundred thousand situations involving the colors that we see on oil films, soap bubbles, etc. at different angles."

This passage does **not** mention sodium light or monochromatic stripes.
- I also searched these chapters: I-27, 29, 31, 33, 34, 35, 36 and 38, II-33, and III-1 and III-3. None pairs sodium light with films. II-33 only mentions "the colors of oil films" and coated lenses.
- The site blocked me before I could check I-26, 28, 32 and 37. According to a search snippet, I-32 mentions sodium's wavelength in the context of light scattering.

**Where the sodium passage actually is: Feynman's 1983 Esalen workshop**, "Quantum Mechanical View of Reality" (Esalen Institute, Big Sur, Nov 1983), talk 2, part 1, at about 15:30. Video: https://www.youtube.com/watch?v=Ec03o-7rHLw (title confirmed through oEmbed). Wikiquote's transcription (unofficial, with ellipses):
> "[T]o make it easy... we'll suppose that all the light... is exactly one color... At night... they have these yellow street lights... that's a sodium light... and that emits light all of one color... Then take the soap bubble and blow it at night.. and then you'll see the bands... [You] can take... very thin glass... you can see very thin bands… suppose then that we do have light like from sodium-vapor so that all the light... is always photons of exactly the same energy. We call it monochromatic, one color light."

**Check the audio before putting this on screen.**

**The same idea in print.** Feynman, R. P. (1985). *QED: The Strange Theory of Light and Matter*. Princeton UP. doi:10.1515/9781400847464 [CR]. Caption of Fig. 18, text via Goodreads; page not checked:
> "As the thickness of a layer increases, the two surfaces produce a partial reflection of monochromatic light whose probability fluctuates in a cycle from 0% to 16%. … when two colors such as pure red and pure blue are aimed at the layer, a given thickness will reflect only red, only blue, both … or neither color (black). If the layer is of varying thicknesses, such as a drop of oil spreading out on a mud puddle, all of the combinations will occur. In sunlight, which consists of all colors, all sorts of combinations occur, which produce lots of colors."

**The classic demonstration.**
- PSSC *Physics* (D. C. Heath, 1960), Ch. 19 §9 "Interference in Thin Films" has the famous colour photographs, as cited by Harvard.
- Harvard Natural Sciences Lecture Demonstrations, https://sciencedemonstrations.fas.harvard.edu/presentations/thin-film-interference [FT]:
  > "The interference produces a pattern of beautiful colors in white light, or dark and light bands in monochromatic light. … The reflection from the front surface is a so-called 'hard reflection' and results in a 180° phase shift … at the top of the soap film, where the thickness of the film is much less than the wavelength of light … one observes no reflection…"

**The physics (checked)**
- The sodium D lines are 589.0 and 589.6 nm (standard values).
- At normal incidence there is one dark–bright–dark cycle per thickness change of **λ/(2n) = 589/(2 × 1.33) ≈ 221 nm**. At oblique incidence the step is λ/(2n cos θ_t).
- **Dark where very thin.** Reflection at the front (air to water) flips the phase by π; the back reflection (water to air) does not. So as t → 0 the two reflections cancel.
- The first bright band is at t = λ/(4n) ≈ 111 nm.
- The bands are horizontal because drainage makes the film thicker lower down. Each band is a contour of equal thickness.
- The small gap between the two D lines does not matter: it would only wash out the fringes after about 1000 of them, i.e. roughly 0.2 mm of film.

---

## Story hooks (surprising and true)

1. **A blind man codified the laws of soap films.** Plateau was blind by 1843–44, and others made the frame observations for him. He blamed staring at the sun in 1829; an ophthalmologist blames uveitis. His best-known photo is a daguerreotype from 1843.
2. **Maxwell reviewed the book in 1874** and opened with Etruscan children blowing bubbles on a vase in the Louvre.
3. **The cube's little square saves 0.07%.** The film with the small central square has only 0.07% less area than the obvious cone over the cube's edges. The soap never makes the cone, because the cone is not even a local minimum.
4. **Only 3 of 10 junctions survive.** There are 10 geometrically balanced ways for films to meet at a point; only 3 are stable. It took until 1976 (Taylor) to prove Plateau's rules.
5. **Aaronson's "I win."** He bought glass plates, copper rods and suction cups, and saw soap make impossible triangular "bubbles" and even networks that failed to connect all the pegs. He cited his own column in a footnote: "I win."
6. **The hexagon needs no Steiner points.** The best network for six pins on a hexagon is just five of its sides, yet soap happily settles into the 3.9% and 5.8% longer Steiner networks (√27 and √28).
7. **The catenoid is "wrong" before it breaks.** From h/R = 1.055 it is already a worse answer than two flat disks. Just before it snaps at 1.3255 it has 20% more area than the disks, and it collapses in under 30 ms, often leaving a tiny satellite bubble.
8. **Euler's catenoid problem is the hanging-chain problem in disguise.** Both minimize the same integral ∫ y ds, and Euler says so in 1744.
9. **Steiner didn't pose the Steiner problem.** Gergonne did, around 1810/11, with canals between cities.
10. **The pressure inside a 2 cm bubble** is about 5 Pa more than outside, one twenty-thousandth of an atmosphere.
11. **Feynman's sodium-lamp soap bubble** is from a 1983 Esalen talk, not from the Feynman Lectures.

---

## 12. Why bubbles show moving swirls (added request)

**Summary.** A soap film is a nearly two-dimensional fluid, a few hundred nanometres to a few micrometres thick. Its thickness is carried along with the flow and diffuses very little, so the interference colours act like a dye painted onto the flow.

The flow itself behaves like 2D turbulence. In two dimensions, energy moves to larger scales (Kraichnan's inverse cascade), so small eddies merge into a few long-lived, rounded vortices. That is also why Jupiter's atmosphere is dominated by big storms.

Three things keep stirring the film:
- **Heat:** warm film at the base rises in plumes. Heated half-bubbles grow isolated, hurricane-like vortices that wander over the dome.
- **Drainage:** thinner film is lighter, so on a vertical film it rises in plumes from the side borders. This is marginal regeneration.
- **Air currents and evaporation.**

Each swirl winds the thickness field into spiral filaments, and we see them as bands of colour.

**Caveat:** the film is not exactly incompressible. Fast flows and large thickness changes couple back into the motion. For the slow swirls on a bubble, "passive dye" is a good approximation.

### Evidence and citations

**(a) Soap films as 2D fluids, and 2D turbulence**
- Couder, Y., Chomaz, J. M. & Rabaud, M. (1989). "On the hydrodynamics of soap films." *Physica D* 37(1–3):384–405. doi:10.1016/0167-2789(89)90144-9 [CR; abstract FT]:
  > "on short time scales each element of the film moves as a whole so that the film can be considered as a two-dimensional fluid with a local density proportional to its thickness. … The film behaves as an incompressible fluid whenever the motions occur at velocities small compared to the velocity of its elastic waves."
- Couder, Y. (1981). "The observation of a shear flow instability in a rotating system with a soap membrane." *J. Physique Lettres* 42(19):429–431. doi:10.1051/jphyslet:019810042019042900 [CR].
- Gharib, M. & Derango, P. (1989). "A liquid film (soap film) tunnel to study two-dimensional laminar and turbulent shear flows." *Physica D* 37(1–3):406–416. doi:10.1016/0167-2789(89)90145-0 [CR; abstract not read].
- Kellay, H., Wu, X.-l. & Goldburg, W. I. (1995). "Experiments with turbulent soap films." *Phys. Rev. Lett.* 74(20):3975–3978. doi:10.1103/PhysRevLett.74.3975 [CR].
- Kellay, H. & Goldburg, W. I. (2002). "Two-dimensional turbulence: a review of some recent experiments." *Rep. Prog. Phys.* 65(5):845–894. doi:10.1088/0034-4885/65/5/204 [CR; abstract not read].
- Rivera, M., Vorobieff, P. & Ecke, R. E. (1998). "Turbulence in flowing soap films: velocity, vorticity, and thickness fields." *Phys. Rev. Lett.* 81(7):1417–1420. doi:10.1103/PhysRevLett.81.1417 [CR; abstract FT via OSTI 641548]. The abstract reports "the effects of compressibility arising from variations in film thickness", but also that the correlations are "consistent with theoretical predictions for two-dimensional turbulence."
- Vorobieff, P., Rivera, M. & Ecke, R. E. (1999). "Soap film flows: Statistics of two-dimensional turbulence." *Phys. Fluids* 11(8):2167–2177. doi:10.1063/1.870078 [CR].
- Inverse cascade theory: Kraichnan, R. H. (1967). "Inertial ranges in two-dimensional turbulence." *Phys. Fluids* 10(7):1417–1423. doi:10.1063/1.1762301 [CR].

**(b) Heated half-bubbles and hurricane-like vortices**
- Seychelles, F., Amarouchene, Y., Bessafi, M. & Kellay, H. (2008). "Thermal convection and emergence of isolated vortices in soap bubbles." *Phys. Rev. Lett.* 100(14):144501. doi:10.1103/PhysRevLett.100.144501 [CR; abstract FT via PubMed 18518038]:
  > "half a soap bubble heated at the equator … develops thermal convection at its equator. A particular feature of this cell is the emergence of isolated vortices. These vortices resemble hurricanes or cyclones … a study of the mean square displacement of these objects showing signs of superdiffusion."
- Meuel, T., Xiong, Y. L., Fischer, P., Bruneau, C. H., Bessafi, M. & Kellay, H. (2013). "Intensity of vortices: from soap bubbles to hurricanes." *Sci. Rep.* 3:3455. doi:10.1038/srep03455 [CR; FT].
  - Set-up: half-bubbles 12 cm across on a heated, optionally rotating brass disk. The bath can be set from 30 to 90 °C; most results use 55 °C.
  - Vortices have "a well defined center or 'eye'" and spirals 1–2 cm across. The colours are white-light interference.
  - Measurements: vortex tracks, lifetimes, and velocity and vorticity profiles, which are Gaussian vortices.
  - Findings: rotation pushes vortices toward the pole and shortens long-lived ones. The vortices go through spells of intensification with trochoidal (looping) motion of the centre. A simple intensification relation fits both these vortices and tropical cyclones.
  - **Licence: CC BY-NC-ND 3.0.** Figures cannot be modified or used commercially.
- Follow-up: Seychelles, F., Ingremeau, F., Pradere, C. & Kellay, H. (2010). "From intermittent to nonintermittent behavior in two dimensional thermal convection in a soap bubble." *Phys. Rev. Lett.* 105:264502. doi:10.1103/PhysRevLett.105.264502 [PubMed 21231671].

**(c) Marginal regeneration**
- Mysels, K. J., Shinoda, K. & Frankel, S. (1959). *Soap Films: Studies of Their Thinning and a Bibliography*. London & New York: Pergamon, 116 pp. [Open Library OL7333581W; contents not read]. This is the classic source for the term.
- Nierstrasz, V. A. & Frens, G. (1998). "Marginal regeneration in thin vertical liquid films." *J. Colloid Interface Sci.* 207(2):209–217. doi:10.1006/jcis.1998.5646 [CR].
- Seiwert, J., Kervil, R., Nou, S. & Cantat, I. (2017). "Velocity field in a vertical foam film." *Phys. Rev. Lett.* 118:048001. doi:10.1103/PhysRevLett.118.048001 [abstract FT via PubMed 28186817]:
  > "Upward velocities up to 10 cm/s are measured close to the lateral menisci, whereas a slower velocity field is obtained in the center of the film…"
- Gros, A., Bussonnière, A., Nath, S. & Cantat, I. (2021). "Marginal regeneration in a horizontal film: instability growth law in the nonlinear regime." *Phys. Rev. Fluids* 6:024004. doi:10.1103/PhysRevFluids.6.024004 [CR].

**(d) Thickness as a passive dye**
- Film mass is conserved: ∂h/∂t + ∇·(h**u**) = 0. When **u** is nearly divergence-free (Couder et al. 1989), this reduces to Dh/Dt ≈ 0. Each patch keeps its thickness, and therefore its colour, while the flow stretches and folds it. Diffusion of thickness is negligible on these scales, so the filaments sharpen instead of blurring.
- Greffier, O., Amarouchene, Y. & Kellay, H. (2002). "Thickness fluctuations in turbulent soap films." *Phys. Rev. Lett.* 88(19):194101. doi:10.1103/PhysRevLett.88.194101 [abstract FT via PubMed 12005634]:
  > "the statistics of these fluctuations closely resemble those of a passive scalar field in a turbulent flow … just like dye or temperature fluctuations in 3D turbulent flows."

**Images.** Commons has CC BY-SA 4.0 bubble macro photos. I checked the licences but have not viewed the images, so check that they actually show swirls:
- https://commons.wikimedia.org/wiki/File:Macro_Photography_of_a_soap_bubble.jpg
- https://commons.wikimedia.org/wiki/File:Thin_Film_Interference_Soap_Bubble.jpg

The APS papers are copyrighted. For the Jupiter comparison, NASA imagery (e.g. Juno or Cassini) is generally public domain; check each item's credit line.
