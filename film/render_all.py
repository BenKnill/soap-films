"""Render the film's shots listed in film/timeline.json into MEDIA/frames/<shot>/fNNNNN.png (resumable).

  python film/render_all.py MEDIA [--only ID ...] [--samples 32] [--blender PATH] [--python PATH]
  python film/render_all.py MEDIA --check          verdict only: every shot has all its frames

Blender shots run film/blender/<script> headless (Cycles picks CUDA on bluestar26, Metal on the Mac) with the
timeline's arguments; 2D shots run film/graphics/shots2d.py. Frames already present are skipped. Per-frame overlay
data from Blender shots lands in MEDIA/frames/<shot>/meta.json for the compositor.
"""
import argparse, json, os, subprocess, sys, time

here = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("media"); ap.add_argument("--only", nargs="*"); ap.add_argument("--samples", default="32")
ap.add_argument("--blender", default=os.path.expanduser("~/.local/bin/blender")); ap.add_argument("--python", default=sys.executable)
ap.add_argument("--check", action="store_true")
a = ap.parse_args()
TL = json.load(open(os.path.join(here, "timeline.json")))


def missing(s):
    d = os.path.join(a.media, "frames", s["id"]); f0 = s.get("first", 0)
    return [f for f in range(f0, f0 + s["frames"]) if not (os.path.exists(p := os.path.join(d, f"f{f:05d}.png")) and os.path.getsize(p) > 0)]


shots = [s for s in TL["shots"] if not a.only or s["id"] in a.only]
if not a.check:
    for s in shots:
        d = os.path.join(a.media, "frames", s["id"]); os.makedirs(d, exist_ok=True)
        todo = missing(s)
        if not todo:
            print(f"SHOT {s['id']}: complete ({s['frames']} frames)", flush=True); continue
        t0 = time.time(); f0 = s.get("first", 0)
        if s["kind"].startswith("blender:"):
            script = s["kind"].split(":", 1)[1]
            args = [f"{k}={v}" for k, v in s["args"].items()]
            cmd = [a.blender, "-b", "--python-exit-code", "1", "-P", script, "--", f"out={d}/f%05d.png", f"first={f0}", f"last={f0 + s['frames'] - 1}",
                   f"meta={d}/meta.json", f"samples={a.samples}"] + args
            subprocess.run(cmd, cwd=os.path.join(here, "blender"), check=True)
        else:
            shot = s["kind"].split(":", 1)[1]
            subprocess.run([a.python, os.path.join(here, "graphics", "shots2d.py"), shot, f"{d}/f%05d.png", str(s["frames"]),
                            json.dumps(s["cues"])], check=True)
        print(f"SHOT {s['id']}: {len(todo)} frames in {time.time() - t0:.0f} s ({(time.time() - t0) / len(todo):.2f} s/frame)", flush=True)
bad = {s["id"]: len(m) for s in shots if (m := missing(s))}
n = sum(s["frames"] for s in shots)
print(f"{'PASS' if not bad else 'FAIL'} render-all: {len(shots)} shots, {n - sum(bad.values())}/{n} frames present"
      + (f"; missing {bad}" if bad else ""))
sys.exit(1 if bad else 0)
