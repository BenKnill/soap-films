"""Build film/timeline.json from the narration timing: every shot's window, frame count, render arguments and cues.

  python film/timeline.py [--timing film/voice/timing.json] [--out film/timeline.json]

The picture follows the voice. Shot windows overlap by XF seconds for crossfades; cue times are seconds from the
start of their shot, taken from line start times in timing.json.
"""
import argparse, json, os

FPS, XF, ENDCARD = 24, 0.5, 7.0
ap = argparse.ArgumentParser()
here = os.path.dirname(os.path.abspath(__file__))
ap.add_argument("--timing", default=os.path.join(here, "voice", "timing.json"))
ap.add_argument("--out", default=os.path.join(here, "timeline.json"))
a = ap.parse_args()
T = json.load(open(a.timing))
L = [l["start"] for l in T["lines"]]
E = [l["end"] for l in T["lines"]]
beat = {k: v["start"] for k, v in T["beats"].items()}
fr = lambda s: int(round(s * FPS))

# cut points: each shot ends XF after the next one starts
cuts = {"open": 0.0, "computer": beat["computer"] - 1.0, "twice": beat["twice"] - 0.7, "dips": beat["measure"] - 0.7,
        "chart": L[21] - 1.2, "rings": beat["rings"] - 0.7, "proof": beat["proof"] - 0.9, "end": beat["end"] - 0.8,
        "endcard": E[-1] + 2.2}
order = ["open", "computer", "twice", "dips", "chart", "rings", "proof", "end", "endcard"]
total = cuts["endcard"] + ENDCARD
win = {}
for i, k in enumerate(order):
    s = cuts[k]; e = cuts[order[i + 1]] + XF if i + 1 < len(order) else total
    win[k] = (s, e)
loc = lambda k, t: round(t - win[k][0], 3)          # film time -> shot time
lf = lambda k, t: fr(t - win[k][0])                   # film time -> shot frame

shots = []


def add(id, kind, k, args=None, cues=None, extra=None):
    s, e = win[k]
    d = dict(id=id, kind=kind, start=round(s, 3), end=round(e, 3), frames=fr(e - s), args=args or {}, cues=cues or {})
    if extra: d.update(extra)
    shots.append(d)


# 1 open: flat film, daylight; a sodium version of the same frames is crossfaded in under lines 2-3
o_end = fr(win["open"][1])
add("open", "blender:flatfilm.py", "open", dict(dist=f"0:2.05,{fr(L[3])}:2.2,{fr(L[4]) + 30}:3.25,{o_end}:3.35",
                                                yaw=f"0:-7,{o_end}:5", pitch="3", lens="50", flow="0.035", soft="2.6"),
    cues=dict(na_in=loc("open", L[2] - 0.2), na_out=loc("open", L[4] - 0.6), stripe=loc("open", L[3]),
              title=loc("open", L[5] - 0.2)))
na0, na1 = fr(L[2] - 0.2) - 6, fr(L[4] - 0.6) + 24
shots.append(dict(id="open-sodium", kind="blender:flatfilm.py", start=round(na0 / FPS, 3), end=round(na1 / FPS, 3),
                  frames=na1 - na0, first=na0, args=dict(shots[0]["args"], light="sodium"), cues={}))
# 2 the soap computer: four pins on a square (measured four-pin dip #3)
k = "computer"
add("computer", "blender:computer.py", k, dict(traj="../data/traj-n4-d2.json", starts=str(lf(k, L[6] + 4.2)), dur="132", lift="30",
                                               arcs=f"{lf(k, L[8])}:{lf(k, E[8] + 1.2)}", dist=f"0:6.1,{fr(win[k][1] - win[k][0])}:5.4",
                                               pitch="56", yaw="-30", yawrate="0.03", soft="2.4"),
    cues=dict(arcs=loc(k, L[8]), arcs_end=loc(k, E[8] + 1.2), answer=loc(k, L[11] + 2.0), tag=loc(k, L[6] + 4.2)))
# 3 two dips of six pins (measured six-pin dips #1 and #3)
k = "twice"
add("twice", "blender:computer.py", k, dict(traj="../data/traj-n6-d0.json,../data/traj-n6-d2.json", offs="-1.4,1.4",
                                            starts=f"{lf(k, E[12] - 0.6)},{lf(k, E[12] + 1.6)}", dur="150,170", lift="30",
                                            dist=f"0:8.6,{fr(win[k][1] - win[k][0])}:8.0", pitch="58", yaw="-6", yawrate="0.008", soft="2.4"),
    cues=dict(tag=loc(k, E[12]), shortest=loc(k, L[15]), longer=loc(k, L[16]), local=loc(k, L[17])))
# 4 the first 60 measured six-pin dips, then 5 the success-rate chart
k = "dips"
add("dips", "2d:dips", k, cues=dict(grid=loc(k, L[18] + 0.4), check=loc(k, L[20] + 0.3)))
k = "chart"
add("chart", "2d:chart", k, cues=dict(c345=loc(k, L[21]), c6=loc(k, L[22]), knee=loc(k, L[23]), c7=loc(k, L[24]),
                                      shape=loc(k, L[25] + 1.5), shake=loc(k, L[27]), noise=loc(k, L[28])))
# 6 the catenoid: pull the rings apart, the waist narrows, the film snaps
k = "rings"
snap = lf(k, L[33] + 3.4)
add("rings", "blender:catenoid.py", k, dict(hr=f"0:0.55,{lf(k, L[31])}:0.56,{lf(k, E[31])}:0.97,{lf(k, L[32] + 0.6)}:1.0,{lf(k, E[32])}:1.24,{lf(k, L[33] + 2.6)}:1.3254",
                                            snap=str(snap), flow="40", split="10", hr_final="1.335", dist="6.3", pitch="13",
                                            yaw="-10", yawrate="0.03", soft="2.2"),
    cues=dict(readout=loc(k, L[31] - 0.5), equal=loc(k, L[32]), snap=round(snap / FPS, 3)))
# 7 the proved constant
k = "proof"
add("proof", "2d:proof", k, cues=dict(root=loc(k, L[34] + 1.0), prover=loc(k, L[35]), pin=loc(k, L[36]),
                                      computed=loc(k, L[37]), fluid=loc(k, L[38])))
# 8 the film drains and pops
k = "end"
pop = lf(k, E[41] + 0.15)
add("end", "blender:flatfilm.py", k, dict(dist="3.3", yaw="-4", pitch="2", lens="50", flow="0.035", soft="2.6",
                                          thin=f"0:1.0,{lf(k, L[40])}:0.9,{lf(k, E[40])}:0.62",
                                          black=f"0:-0.3,{lf(k, L[40]) - 6}:-0.3,{lf(k, E[40]) + 6}:0.62",
                                          hole=f"0:-1,{pop}:-1,{pop + 1}:0.0,{pop + 7}:2.4"),
    cues=dict(pop=round(pop / FPS, 3)))
add("endcard", "2d:endcard", "endcard")
json.dump(dict(fps=FPS, xf=XF, duration=round(total, 3), audio_end=T["duration"], shots=shots), open(a.out, "w"), indent=1)
print(f"timeline: {len(shots)} shots, {round(total, 2)} s, {sum(s['frames'] for s in shots)} rendered frames "
      f"({sum(s['frames'] for s in shots if s['kind'].startswith('blender'))} in Blender)")
for s in shots: print(f"  {s['id']:12s} {s['start']:7.2f}-{s['end']:7.2f}  {s['frames']:5d} frames  {s['kind']}")
