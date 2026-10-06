"""The film's 2D shots, drawn frame by frame from the measured and proved results.

  python shots2d.py SHOT OUT_PATTERN NFRAMES CUES_JSON [--fps 24] [--only F ...]

SHOT is dips (film/data/dips-n6.json: the first 60 measured six-pin dips, scored), chart (results/success-grid.json: success rate against pin count, Wilson intervals, the shake series),
proof (t tanh t = 1 and the HOL-certified enclosure of its root) or endcard. CUES_JSON maps cue names to seconds
from the start of the shot (from the narration's timing.json); missing cues never fire.
"""
import argparse, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gfx import *

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FAR = 1e9


def chart(t, cue, grid):
    im, d = canvas()
    res = {(r["n"], r["shake"]): r for r in grid["results"]}
    x0, x1, y0, y1 = 300, 1390, 250, 870            # plot box: y0 = 100 %, y1 = 0 %
    X = lambda n: x0 + (n - 3) / 4 * (x1 - x0)
    Y = lambda p: y1 - p * (y1 - y0)
    a = ramp(t, 0.0, 0.8)
    face("M", 46).draw(d, (120, 110), "How often does the film find the shortest network?", mix(INK, BG, a))
    face("R", 26).draw(d, (120, 160), "Simulated films on regular polygons · 1,000 random dips per point · bars: 95% intervals",
                      mix(INK2, BG, a))
    # axes and grid (recessive)
    for p in (0, 0.25, 0.5, 0.75, 1.0):
        line(d, [(x0 - 20, Y(p)), (x1 + 30, Y(p))], mix(GRID, BG, a), 1.5)
        face("R", 24).draw(d, (x0 - 34, Y(p) + 8), f"{int(p * 100)}%", mix(MUTED, BG, a), "r")
    for n in range(3, 8):
        face("R", 26).draw(d, (X(n), y1 + 46), f"{n} pins", mix(INK2, BG, a), "c")
        # the polygon itself under each tick: pin count also changes the shape
        hl = ramp(t, cue.get("shape", FAR), 0.5) * (1 - ramp(t, cue.get("shake", FAR), 0.5))
        col = mix(mix(GOLD, MUTED, hl), BG, a); r = 22 + 6 * hl; cy = y1 + 100
        pts = [(X(n) + r * math.cos(2 * math.pi * k / n + math.pi / 2), cy - r * math.sin(2 * math.pi * k / n + math.pi / 2)) for k in range(n)]
        line(d, pts + [pts[0]], col, 1.5)
        for px, py in pts: dot(d, px, py, 3.2, col)
    if "shape" in cue:
        hl = ramp(t, cue["shape"], 0.5) * (1 - ramp(t, cue.get("shake", FAR), 0.5))
        face("R", 24).draw(d, (X(5), y1 + 170), "the shape changes with the pin count", mix(GOLD, BG, hl), "c")

    def series(shake, color, dx, reveal):
        """reveal(n) in [0,1] per point; returns the drawn points"""
        pts = []
        for n in range(3, 8):
            k = reveal(n)
            if k <= 0: continue
            r = res[(n, shake)]; x = X(n) + dx
            lo, hi = r["ci"]
            line(d, [(x, Y(lo)), (x, Y(hi))], mix(color, BG, k), 3)
            for yy in (lo, hi): line(d, [(x - 7, Y(yy)), (x + 7, Y(yy))], mix(color, BG, k), 2.5)
            pts.append((n, x, Y(r["rate"]), k))
        for (n0, xa, ya, ka), (n1, xb, yb, kb) in zip(pts, pts[1:]):
            s = kb; line(d, [(xa, ya), (xa + (xb - xa) * s, ya + (yb - ya) * s)], mix(color, BG, min(ka, 1)), 3)
        for n, x, y, k in pts:
            dot(d, x, y, 7.5, mix(color, BG, k), ring=BG)
        return pts

    base_rev = lambda n: ramp(t, cue.get("c345", FAR), 0.7) if n <= 5 else ramp(t, cue.get("c6", FAR), 0.9) if n == 6 else ramp(t, cue.get("c7", FAR), 0.9)
    sh = ramp(t, cue.get("shake", FAR), 0.9)
    if sh > 0:
        series(0.5, AQUA, 14, lambda n: sh)
        series(0.15, ORANGE, -14, lambda n: sh)
    series(0, BLUE, 0, base_rev)
    # direct labels (text ink, never series colour)
    k = ramp(t, cue.get("c345", FAR), 0.7)
    face("M", 26).draw(d, (X(4), Y(1.0) - 26), "1,000 / 1,000", mix(INK, BG, k), "c")
    k = ramp(t, cue.get("c6", FAR), 0.7)
    r6 = res[(6, 0)]
    face("M", 28).draw(d, (X(6) + 24, Y(r6["rate"]) + 52), "506 / 1,000", mix(INK, BG, k))
    face("R", 22).draw(d, (X(6) + 24, Y(r6["rate"]) + 82), f"{r6['ci'][0] * 100:.1f}–{r6['ci'][1] * 100:.1f}%", mix(INK2, BG, k))
    k = ramp(t, cue.get("knee", FAR), 0.6) * (1 - ramp(t, cue.get("shake", FAR), 0.6))
    if k > 0:
        xm = (X(5) + X(6)) / 2; ym = (Y(1.0) + Y(r6["rate"])) / 2
        face("B", 30).draw(d, (xm - 30, ym), "−49.4 points", mix(GOLD, BG, k), "r")
        face("R", 22).draw(d, (xm - 30, ym + 30), "the biggest drop", mix(INK2, BG, k), "r")
    k = ramp(t, cue.get("c7", FAR), 0.7)
    r7 = res[(7, 0)]
    face("M", 28).draw(d, (X(7) - 4, Y(r7["rate"]) - 50), "577 / 1,000", mix(INK, BG, k), "c")
    k = ramp(t, cue.get("c6", FAR) + 2.0, 0.8) * (1 - ramp(t, cue.get("shake", FAR), 0.5))
    face("R", 21).draw(d, (x0, y1 + 230), f"Six pins: {r6['unresolved']} of the 1,000 dips had not settled within the step budget; they count as failures.",
                       mix(MUTED, BG, k))
    # legend (always, >= 2 series) and the shake note
    lx, ly = 1450, 300
    items = [(BLUE, "no shake", 1.0), (ORANGE, "one shake, amplitude 0.15", sh), (AQUA, "one shake, amplitude 0.5", sh)]
    for i, (c, txt, kk) in enumerate(items):
        if kk <= 0: continue
        kk = kk * a
        line(d, [(lx, ly + 40 * i - 8), (lx + 34, ly + 40 * i - 8)], mix(c, BG, kk), 3)
        dot(d, lx + 17, ly + 40 * i - 8, 6, mix(c, BG, kk), ring=BG)
        face("R", 24).draw(d, (lx + 48, ly + 40 * i), txt, mix(INK2, BG, kk))
    if sh > 0:
        r615, r65 = res[(6, 0.15)], res[(6, 0.5)]
        face("M", 26).draw(d, (lx, 540), f"Six pins: {r6['rate'] * 100:.1f}% → {r615['rate'] * 100:.1f}% and {r65['rate'] * 100:.1f}%", mix(INK, BG, sh))
        kn = ramp(t, cue.get("noise", FAR), 0.6)
        if kn > 0:
            x = X(6); lo, hi = r6["ci"]
            rrect(d, (x - 40, Y(hi) - 6, x + 40, Y(lo) + 6), 8, outline=mix(GOLD, BG, kn), width=2)
            face("M", 26).draw(d, (lx, 590), "inside the noise", mix(GOLD, BG, kn))
            pr = {(p["n"], p["shake"]): p for p in grid["paired"]}
            p = pr[(6, 0.15)]
            face("R", 21).draw(d, (lx, 628), f"paired change +{p['difference'] * 100:.1f} points,", mix(INK2, BG, kn))
            face("R", 21).draw(d, (lx, 656), f"95% interval {p['ci'][0] * 100:.1f} to +{p['ci'][1] * 100:.1f}".replace("-", "−"), mix(INK2, BG, kn))
    return finish(im)


def proof(t, cue):
    im, d = canvas()
    a = ramp(t, 0.0, 0.8)
    face("M", 46).draw(d, (120, 110), "Where does the catenoid run out?", mix(INK, BG, a))
    # left: the curve t tanh t with the line y = 1
    px0, px1, py0, py1 = 140, 900, 260, 820                 # t in [0, 2], y in [0, 2]
    TX = lambda v: px0 + v / 2.0 * (px1 - px0); TY = lambda v: py1 - v / 2.0 * (py1 - py0)
    for v in (0, 0.5, 1.0, 1.5, 2.0):
        line(d, [(px0, TY(v)), (px1, TY(v))], mix(GRID, BG, a), 1.5)
        face("R", 22).draw(d, (px0 - 14, TY(v) + 8), f"{v:g}", mix(MUTED, BG, a), "r")
        face("R", 22).draw(d, (TX(v), py1 + 34), f"{v:g}", mix(MUTED, BG, a), "c")
    face("R", 24).draw(d, (px1, py1 + 72), "t", mix(INK2, BG, a), "r")
    kc = ramp(t, 0.3, 1.6)
    n = 200; pts = []
    for i in range(int(n * kc) + 1):
        v = 2.0 * i / n; pts.append((TX(v), TY(v * math.tanh(v))))
    if len(pts) > 1: line(d, pts, BLUE, 3)
    line(d, [(px0, TY(1)), (px1, TY(1))], mix(INK2, BG, a), 1.5)
    face("M", 30).draw(d, (TX(0.25), TY(1.62)), "t · tanh t", mix(INK, BG, kc))
    face("R", 24).draw(d, (TX(1.62), TY(1) - 16), "= 1", mix(INK2, BG, a))
    kr = ramp(t, cue.get("root", 1.8), 0.6)
    tr = 1.1996786402
    if kr > 0:
        line(d, [(TX(tr), TY(1)), (TX(tr), py1)], mix(GOLD, BG, kr), 2)
        dot(d, TX(tr), TY(1), 9, mix(GOLD, BG, kr), ring=BG)
    # right: the proved enclosure, digits locking in
    rx = 1010
    kp = ramp(t, cue.get("prover", FAR), 0.6)
    if kp > 0:
        badge(d, rx, 300, "PROVED in HOL Light", mix(GOLD, BG, kp), 24)
        face("R", 26).draw(d, (rx, 360), "exactly one positive root, and it lies in", mix(INK2, BG, kp))
    kd = ramp(t, cue.get("pin", FAR), 0.4)
    if kd > 0:
        lo, hi = "1.1996786402", "1.1996786403"
        nd = 3 + int(round(kd * (len(lo) - 3)))     # digits revealed
        fm = face("MONO", 54)
        sl = lo[:nd] + "·" * (len(lo) - nd); sh = hi[:nd] + "·" * (len(hi) - nd)
        fm.draw(d, (rx, 450), sl, mix(INK, BG, kp)); face("R", 34).draw(d, (rx + fm.length(lo) + 18, 450), "< t <", mix(INK2, BG, kp))
        fm.draw(d, (rx, 520), sh, mix(INK, BG, kp))
        kw = ramp(t, cue.get("pin", FAR) + 1.2, 0.5)
        face("R", 24).draw(d, (rx, 572), "an interval one ten-billionth wide", mix(INK2, BG, kw))
        face("R", 20).draw(d, (rx, 610), "proofs/catenoid_snap.ml · 0 new axioms", mix(MUTED, BG, kw))
    kh = ramp(t, cue.get("computed", FAR), 0.6)
    if kh > 0:
        badge(d, rx, 712, "COMPUTED, not proved", mix(INK2, BG, kh), 22)
        face("R", 26).draw(d, (rx, 770), "ring spacing at the snap  h/R = 2t / cosh t ≈ 1.3255", mix(INK, BG, kh))
    kf = ramp(t, cue.get("fluid", FAR), 0.6)
    if kf > 0:
        face("R", 24).draw(d, (rx, 850), "The proof covers this equation,", mix(INK2, BG, kf))
        face("R", 24).draw(d, (rx, 884), "not the fluid, and not the film's stability.", mix(INK2, BG, kf))
    return finish(im)


def dips(t, cue, data):
    """the first 60 measured six-pin dips (no shake), drawn as settled networks, then scored against the optimum"""
    im, d = canvas()
    a = ramp(t, 0.0, 0.8)
    face("M", 46).draw(d, (120, 110), "Six pins, dipped again and again", mix(INK, BG, a))
    face("R", 26).draw(d, (120, 160), "Simulated films · the first 60 of 1,000 random dips · each settled network as the film left it",
                      mix(INK2, BG, a))
    pins = data["pins"]; ref = data["reference"]; n = len(pins)
    cols, rows, cw, chh, gx, gy = 10, 6, 118, 118, 120, 230
    t_grid, t_check = cue.get("grid", 0.5), cue.get("check", FAR)
    shown = scored = found = 0
    for i, dp in enumerate(data["dips"][:cols * rows]):
        k = ramp(t, t_grid + 0.09 * i, 0.4)
        if k <= 0: continue
        shown += 1
        s = ramp(t, t_check + 0.05 * i, 0.3)
        if s >= 0.5: scored += 1; found += dp["success"]
        cx = gx + (i % cols) * cw + cw / 2; cy = gy + (i // cols) * chh + chh / 2
        P = lambda v: pins[v] if v < n else dp["jx"][v - n]
        col = mix(mix(GOLD, INK2, s) if dp["success"] else mix(mix(MUTED, BG, 0.55), INK2, s), BG, k)
        R = 40
        for e0, e1 in dp["edges"]:
            p0, p1 = P(e0), P(e1)
            line(d, [(cx + R * p0["x"], cy - R * p0["y"]), (cx + R * p1["x"], cy - R * p1["y"])], col, 2.2)
        for q in pins: dot(d, cx + R * q["x"], cy - R * q["y"], 3.0, mix(INK2, BG, k))
    # the reference: the shortest network, found by trying every layout
    kr = ramp(t, t_check - 0.6, 0.6)
    if kr > 0:
        cx, cy, R = 1560, 470, 150
        jx = ref.get("junctions", [])
        P = lambda v: (pins[v]["x"], pins[v]["y"]) if v < n else tuple(jx[v - n])
        for e0, e1 in ref["edges"]:
            (x0_, y0_), (x1_, y1_) = P(e0), P(e1)
            line(d, [(cx + R * x0_, cy - R * y0_), (cx + R * x1_, cy - R * y1_)], mix(GOLD, BG, kr), 4)
        for q in pins: dot(d, cx + R * q["x"], cy - R * q["y"], 7, mix(INK, BG, kr))
        face("M", 28).draw(d, (cx, cy + R + 66), f"the shortest: length {ref['upper']:.3f}", mix(INK, BG, kr), "c")
        face("R", 22).draw(d, (cx, cy + R + 100), f"found by trying all {ref['topologies']} layouts", mix(INK2, BG, kr), "c")
    if scored:
        kc = ramp(t, t_check, 0.4)
        face("M", 34).draw(d, (1560, 840), f"found it: {found} of {scored}", mix(INK, BG, kc), "c")
        face("R", 22).draw(d, (1560, 876), "(within 0.01% of the shortest, and settled)", mix(INK2, BG, kc), "c")
    return finish(im)


def endcard(t, cue):
    im, d = canvas((0, 0, 0))
    a = ramp(t, 0.2, 1.0)
    face("L", 84).draw(d, (W / 2, 330), "The Soap Computer", mix(INK, (0, 0, 0), a), "c")
    rows = [("Simulated", "Steiner film networks, 1,000 dips per point (docs/steiner.js, results/success-grid.md)"),
            ("Searched", "shortest networks by trying every layout (tools/optimum.py, numerical)"),
            ("Proved", "t · tanh t = 1 has one positive root, in (1.1996786402, 1.1996786403) (HOL Light)"),
            ("Rendered", "Blender Cycles with thin-film interference; the films' flow is procedural")]
    for i, (k, v) in enumerate(rows):
        kk = ramp(t, 0.8 + 0.35 * i, 0.8)
        face("M", 26).draw(d, (430, 480 + 56 * i), k, mix(GOLD if k == "Proved" else INK, (0, 0, 0), kk), "r")
        face("R", 26).draw(d, (460, 480 + 56 * i), v, mix(INK2, (0, 0, 0), kk))
    return finish(im)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("shot"); ap.add_argument("out"); ap.add_argument("nframes", type=int); ap.add_argument("cues")
    ap.add_argument("--fps", type=float, default=24); ap.add_argument("--only", type=int, nargs="*")
    a = ap.parse_args()
    cue = json.loads(a.cues)
    grid = json.load(open(os.path.join(ROOT, "results", "success-grid.json")))
    dd = json.load(open(os.path.join(ROOT, "film", "data", "dips-n6.json"))) if a.shot == "dips" else None
    fn = {"chart": lambda t: chart(t, cue, grid), "proof": lambda t: proof(t, cue), "endcard": lambda t: endcard(t, cue),
          "dips": lambda t: dips(t, cue, dd)}[a.shot]
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    for f in (a.only if a.only else range(a.nframes)):
        p = a.out % f
        if os.path.exists(p) and os.path.getsize(p) > 0 and not a.only: continue
        fn(f / a.fps).save(p, compress_level=1)
    print(f"DONE {a.shot}: {a.nframes} frames -> {a.out}")
