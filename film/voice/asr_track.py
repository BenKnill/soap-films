"""ASR check on a finished film's audio track: local Whisper (asr_wer.py's model and normalizer) on each line's stretch of
the track, cut at the line's times in timing.json (the voice starts at t = 0 in the film), WER against the line's
'say' or 'show' form, whichever is lower, as in asr_wer.py. Whole-track transcription is not used: Whisper invents
words in the silent tail. Usage: asr_track.py FILM_OR_AUDIO [--timing timing.json]
"""
import argparse, json, re, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, '/Users/boxer/Documents/Codex/2026-09-09/turn-x20/work/ch6')
import local_asr
from transformers.models.whisper.english_normalizer import EnglishTextNormalizer

p = argparse.ArgumentParser(); p.add_argument('audio'); p.add_argument('--timing', default='timing.json')
args = p.parse_args()
norm = EnglishTextNormalizer(json.loads((local_asr.DEFAULT_MODEL / 'normalizer.json').read_text()))
words = lambda s: norm(re.sub(r'\b([A-Z])-([A-Z])(?:-([A-Z]))?\b', lambda m: ''.join(g for g in m.groups() if g), s)).split()


def wer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r != h))
    return d[-1], len(ref)


T = json.loads(Path(args.timing).read_text())
tmp = Path(tempfile.mkdtemp())
errs = total = 0
for l in T['lines']:
    seg = tmp / f"line{l['index']:02d}.wav"
    t0 = max(0.0, l['start'] - 0.25)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-t', f"{l['end'] + 0.35 - t0:.3f}", '-i', args.audio,
                    '-vn', '-ac', '1', '-ar', '16000', str(seg)], check=True)
    heard = local_asr.transcribe(seg, destination=seg.with_suffix('.asr.json'))['text']
    (e, n), ref = min((wer(words(l[k]), words(heard)), k) for k in ('say', 'show'))
    errs += e; total += n
    if e:
        print(f"{l['index']:02d} WER {e}/{n} vs {ref}\n  say:   {l['say']}\n  heard: {heard.strip()}", flush=True)
print(f"{'PASS' if errs == 0 else 'FAIL'} asr-track: {args.audio}: {len(T['lines'])} lines cut from the track, "
      f"WER {errs}/{total} = {errs / total:.4f}")
sys.exit(0 if errs == 0 else 1)
