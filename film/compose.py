"""Compose the film: the rendered shots of film/timeline.json, crossfades, on-screen labels, narration -> mp4.

  python film/compose.py MEDIA AUDIO.wav OUT.mp4 [--crf 18] [--only-frames F ... --png DIR]

Each output frame takes its shot's frame at the same film time; overlapping shots crossfade over the timeline's
xf seconds; the opening's sodium-light frames crossfade over its daylight frames at the cues. Labels are drawn from
the per-frame metadata the Blender shots wrote (screen positions, lengths, h/R, areas). The narration is padded
with silence to the picture's length and muxed as AAC. Prints DURATIONS with the probed audio and video lengths.
"""
import argparse, json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphics"))
from gfx import face, INK, INK2, MUTED, GOLD, ease

here = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("media"); ap.add_argument("audio"); ap.add_argument("out")
ap.add_argument("--crf", default="18"); ap.add_argument("--only-frames", type=int, nargs="*"); ap.add_argument("--png")
a = ap.parse_args()
TL = json.load(open(os.path.join(here, "timeline.json")))
FPS, XF, DUR = TL["fps"], TL["xf"], TL["duration"]
NF = int(round(DUR * FPS))
SH = {s["id"]: s for s in TL["shots"]}
main = [s for s in TL["shots"] if s["id"] != "open-sodium"]
meta = {}
for s in TL["shots"]:
    p = os.path.join(a.media, "frames", s["id"], "meta.json")
    if os.path.exists(p): meta[s["id"]] = json.load(open(p))
F = lambda w, z: face(w, z, 1)
ramp = lambda t, t0, d=0.6: ease((t - t0) / d)


def load(s, j):
    j = max(0, min(s["frames"] - 1, j)); f = s.get("first", 0) + j
    return Image.open(os.path.join(a.media, "frames", s["id"], f"f{f:05d}.png")).convert("RGB"), f


def fade(c, k): return tuple(int(round(v * max(0.0, min(1.0, k)))) for v in c)


def text(d, xy, s, col, k, w="R", z=28, anchor="l", shadow=True):
    if k <= 0: return
    if shadow:
        F(w, z).draw(d, (xy[0] + 2, xy[1] + 2), s, fade((0, 0, 0), k), anchor)
    F(w, z).draw(d, xy, s, fade(col, k), anchor)


def overlay(s, im, t, f):
    """labels for shot s at shot time t (its frame number f)"""
    d = ImageDraw.Draw(im); c = s["cues"]; m = meta.get(s["id"], {}).get(str(f))
    out = s["end"] - s["start"]
    if s["id"] == "open":
        k_na = ramp(t, c["na_in"], 0.8) * (1 - ramp(t, c["na_out"], 0.8))
        text(d, (80, 1010), "daylight", INK2, (1 - k_na) * ramp(t, 1.0, 1.0) * (1 - ramp(t, c["title"] - 1.0, 0.6)), z=26)
        text(d, (80, 1010), "sodium light: one wavelength, 589 nm", INK2, k_na, z=26)
        text(d, (80, 966), "one stripe per 221 nm of thickness", INK, k_na * ramp(t, c["stripe"], 0.6), "M", 30)
        kt = ramp(t, c["title"], 1.2)
        text(d, (960, 560), "The Soap Computer", INK, kt, "L", 104, "c")
    elif s["id"] == "computer" and m:
        r = m["rigs"][0]
        text(d, (80, 70), "simulated film (four-pin dip #3 of 1,000) · rendered in Blender", MUTED, ramp(t, c["tag"], 0.8), z=24, shadow=False)
        if r and r["arcs"] > 0:
            for x, y in r["jx"]:
                text(d, (x + 58, y - 34), "120°", GOLD, r["arcs"], "M", 34, "l")
        if r:
            ka = ramp(t, c["answer"], 0.8)
            text(d, (960, 990), f"length {r['L'] / math.sqrt(2):.3f} × side  =  (1 + √3) × side, the shortest possible", INK, ka, "M", 34, "c")
    elif s["id"] == "twice" and m:
        text(d, (80, 70), "simulated films: six-pin dips #1 and #3 of the 1,000 measured · hexagon side 1", MUTED, ramp(t, c["tag"], 0.8), z=24, shadow=False)
        for i, (r, cue, col, note) in enumerate(zip(m["rigs"], ("longer", "shortest"), (INK, GOLD), ("", "the shortest"))):
            if not r: continue
            x = r["centre"][0]; y = max(p[1] for p in r["pins"]) + 70
            k = ramp(t, c[cue], 0.7)
            lab = f"length {r['L']:.3f}" + (f"  ·  {100 * (r['L'] / 5 - 1):.1f}% longer" if i == 0 else "  ·  the shortest")
            text(d, (x, y), lab, col, k, "M", 32, "c")
        r0 = m["rigs"][0]
        if r0:
            k = ramp(t, c["local"], 0.7)
            x = r0["centre"][0]; y = min(p[1] for p in r0["pins"]) - 40
            text(d, (x, y), "a local minimum", GOLD, k, "M", 34, "c")
    elif s["id"] == "rings" and m:
        k = ramp(t, c["readout"], 0.8)
        hr = m["hr"]
        text(d, (90, 110), f"ring spacing  h/R = {min(hr, 1.3255):.3f}" if m["phase"] == "catenoid" else "ring spacing  h/R = 1.335", INK, k, "M", 34)
        if m["phase"] == "catenoid":
            text(d, (90, 160), f"film area ÷ two flat discs = {m['area_ratio']:.3f}", INK2, k, "R", 30)
        ke = ramp(t, c["equal"], 0.6) * (1.0 if hr >= 1.0554 else 0.0)
        if m["phase"] == "catenoid":
            text(d, (90, 214), "two flat discs now have less area: the film keeps a local minimum", GOLD, ke, "M", 30)
        if m["phase"] != "catenoid":
            ks = ramp(t, c["snap"], 0.5)
            text(d, (90, 160), "past h/R ≈ 1.3255 there is no catenoid (computed)", GOLD, ks, "M", 30)
        text(d, (90, 1010), "exact catenoids, then a simulated collapse (curvature flow) · rendered in Blender", MUTED, k, z=24, shadow=False)


def frame(k):
    t = k / FPS
    act = [s for s in main if s["start"] - 1e-9 <= t < s["end"] - 1e-9] or [main[-1]]
    layers = []
    for s in act:
        ts = t - s["start"]; j = int(round(ts * FPS))
        im, f = load(s, j)
        if s["id"] == "open":
            na = SH["open-sodium"]; c = s["cues"]
            kn = ease((ts - c["na_in"]) / 0.8) * (1 - ease((ts - c["na_out"]) / 0.8))
            if kn > 0:
                jn = f - na["first"]
                if 0 <= jn < na["frames"]:
                    imn, _ = load(na, jn); im = Image.blend(im, imn, kn)
        overlay(s, im, ts, f)
        layers.append((s, im))
    im = layers[0][1]
    for s, nxt in layers[1:]:
        im = Image.blend(im, nxt, ease((t - s["start"]) / XF))
    if t > DUR - 1.0: im = Image.blend(im, Image.new("RGB", im.size), ease((t - (DUR - 1.0)) / 1.0))
    return im


if a.only_frames:
    os.makedirs(a.png, exist_ok=True)
    for k in a.only_frames: frame(k).save(os.path.join(a.png, f"c{k:05d}.jpg"), quality=90)
    print("wrote", len(a.only_frames), "frames to", a.png); sys.exit(0)

cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(FPS),
       "-i", "-", "-i", a.audio, "-filter:a", f"apad=whole_dur={NF / FPS}", "-t", f"{NF / FPS}",
       "-c:v", "libx264", "-preset", "slow", "-crf", a.crf, "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-colorspace", "bt709", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", a.out]
ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for k in range(NF):
    ff.stdin.write(np.asarray(frame(k), dtype=np.uint8).tobytes())
    if k % 480 == 0: print(f"frame {k}/{NF}", flush=True)
ff.stdin.close(); assert ff.wait() == 0
probe = lambda st: float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", st, "-show_entries", "stream=duration",
                                         "-of", "csv=p=0", a.out], capture_output=True, text=True).stdout.strip())
v, au = probe("v:0"), probe("a:0")
ok = abs(v - au) <= 0.5
print(f"{'DURATIONS OK' if ok else 'DURATIONS FAIL'}: video {v:.3f} s, audio {au:.3f} s, |difference| {abs(v - au):.3f} s (limit 0.5); {a.out}")
sys.exit(0 if ok else 1)
