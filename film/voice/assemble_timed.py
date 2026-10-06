"""Scene-locked variant of the episode 2/3 assemble.py.

Same edge trims, fades, clause/sentence/paragraph gaps and loudness mastering, but each beat
starts at its scene time `at` (plus LEAD), or later if the previous beat runs long.
Writes narration.wav (48 kHz, mastered), timing.json and a per-beat fit report.
Usage: assemble_timed.py [--limit SECONDS]
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf

HERE = Path(__file__).resolve().parent
GAP = {'clause': 0.2, 'sentence': 0.55, 'paragraph': 0.8}
LEAD, MIN_GAP, TAIL = 0.5, 0.6, 0.6

p = argparse.ArgumentParser(); p.add_argument('--limit', type=float); p.add_argument('--script', default='script.json')
args = p.parse_args()
script = json.loads((HERE / args.script).read_text())
limit = args.limit or script['duration']
sel_path = HERE / 'selection.json'
selection = json.loads(sel_path.read_text()) if sel_path.exists() else {}


def load_trimmed(say):
    h = hashlib.sha1(say.encode()).hexdigest()[:12]; seed = selection.get(h, 42)
    a, sr = sf.read(HERE / f'clips/{h}-seed{seed}.wav', dtype='float32')
    hop = round(.01 * sr); n = len(a) // hop
    rms = np.sqrt(np.mean(a[:n * hop].reshape(n, hop) ** 2, axis=1))
    act = np.flatnonzero(rms > max(1e-5, float(rms.max()) * 10 ** (-55 / 20)))
    head = max(0, int(act[0] * hop) - round(.08 * sr)); end = min(len(a), int((act[-1] + 1) * hop) + round(.12 * sr))
    clip = a[head:end].copy(); f = round(.004 * sr); clip[:f] *= np.linspace(0, 1, f); clip[-f:] *= np.linspace(1, 0, f)
    return h, seed, clip, sr


placed, lines, beats, t, sr = [], [], {}, 0.0, None
bl = script['beats']
for bi, b in enumerate(bl):
    # a beat with "follow": true has no scene anchor; it starts a paragraph gap after the previous one
    # "pause" adds a visual hold (seconds) before a following beat
    t = t + GAP['paragraph'] + b.get('pause', 0) if b.get('follow') else max(b['at'] + LEAD, t + MIN_GAP)
    bstart, blines = t, []
    for k, l in enumerate(b['lines']):
        h, seed, clip, rate = load_trimmed(l['say'])
        sr = sr or rate; assert rate == sr
        placed.append((round(t * sr), clip))
        rec = dict(index=len(lines), clip=h, seed=seed, beat=b['id'], show=l['show'], say=l['say'],
                   start=round(t + 0.06, 3), end=round(t + len(clip) / sr - 0.1, 3))
        t += len(clip) / sr; blines.append(rec); lines.append(rec)
        if k < len(b['lines']) - 1:
            t += GAP[l['b']]
    nxt = next((c['at'] for c in bl[bi + 1:] if not c.get('follow')), limit)
    at = None if b.get('follow') else b['at']
    beats[b['id']] = dict(at=at, start=round(bstart, 3), speech_end=round(t, 3), window_end=nxt,
                          drift=0.0 if at is None else round(bstart - at - LEAD, 3), slack=round(nxt - t, 3), lines=blines)

end = t + TAIL
raw = np.zeros(round(end * sr), dtype=np.float32)
for i0, clip in placed:
    raw[i0:i0 + len(clip)] += clip
sf.write(HERE / 'narration-raw.wav', raw, sr, subtype='FLOAT')
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(HERE / 'narration-raw.wav'), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
                    '-f', 'null', '-'], capture_output=True, text=True, check=True)
loud = json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0]
gain = min(-16 - float(loud['input_i']), -1.5 - float(loud['input_tp']))
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(HERE / 'narration-raw.wav'), '-af', f'volume={gain}dB',
                '-ar', '48000', '-c:a', 'pcm_s16le', str(HERE / 'narration.wav')], check=True)
(HERE / 'timing.json').write_text(json.dumps(dict(duration=round(end, 3), limit=limit, beats=beats, lines=lines), indent=1,
                                             ensure_ascii=False))
words = sum(len(l['say'].split()) for l in lines)
for k, v in beats.items():
    flag = 'OK ' if v['slack'] >= 0.3 and v['drift'] <= 0.3 else 'FIT'
    at = 'follow' if v['at'] is None else f"{v['at']:6.1f}"
    print(f"{flag} {k:10s} at {at:>6s}  start {v['start']:7.2f}  speech_end {v['speech_end']:7.2f}  "
          f"window_end {v['window_end']:6.1f}  slack {v['slack']:+5.2f}  drift {v['drift']:+5.2f}")
ok = end <= limit and all(v['slack'] >= 0.3 and v['drift'] <= 0.3 for v in beats.values())
print(f"{'PASS' if ok else 'FAIL'} assemble: {end:.2f}s of {limit:.0f}s, {len(lines)} lines, {words} words "
      f"({words / end * 60:.0f} wpm), gain {gain:+.1f} dB")
