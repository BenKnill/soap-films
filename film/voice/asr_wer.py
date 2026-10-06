"""Episode 2/3 asr_check.py with a word error rate: local Whisper (large-v3-turbo q4, offline, hash-bound)
on every selected clip, Whisper's English normalizer on both sides, WER against the spoken (`say`) and the
written (`show`) form of each line; the lower one counts. Verdict: every clip at or under --max-wer.
Usage: asr_wer.py [--timing timing.json] [--max-wer 0.10]
"""
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, '/Users/boxer/Documents/Codex/2026-09-09/turn-x20/work/ch6')
import local_asr
from transformers.models.whisper.english_normalizer import EnglishTextNormalizer

HERE = Path.cwd()
p = argparse.ArgumentParser(); p.add_argument('--timing', default='timing.json'); p.add_argument('--max-wer', type=float, default=0.10)
p.add_argument('--report', default='asr-report.json')
args = p.parse_args()
norm = EnglishTextNormalizer(json.loads((local_asr.DEFAULT_MODEL / 'normalizer.json').read_text()))
import re
words = lambda s: norm(re.sub(r'\b([A-Z])-([A-Z])(?:-([A-Z]))?\b', lambda m: ''.join(g for g in m.groups() if g), s)).split()


def wer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r != h))
    return d[-1], len(ref)


T = json.loads((HERE / args.timing).read_text())
rep, errs, total, worst = [], 0, 0, 0.0
for l in T['lines']:
    wav = HERE / f"clips/{l['clip']}-seed{l.get('seed', 42)}.wav"
    heard = local_asr.transcribe(wav, destination=wav.with_suffix('.asr.json'))['text']
    hyp = words(heard)
    (e, n), ref = min((wer(words(l[k]), hyp), k) for k in ('say', 'show'))
    errs += e; total += n; worst = max(worst, e / n)
    rep.append(dict(i=l['index'], wer=round(e / n, 3), errors=e, ref_words=n, ref=ref, say=l['say'], heard=heard.strip()))
    if e:
        print(f"{l['index']:02d} WER {e}/{n}={e / n:.3f} vs {ref}\n  say:   {l['say']}\n  heard: {heard.strip()}", flush=True)
(HERE / args.report).write_text(json.dumps(rep, indent=1))
ok = worst <= args.max_wer
print(f"{'PASS' if ok else 'FAIL'} asr: {len(rep)} clips, overall WER {errs}/{total}={errs / total:.4f}, "
      f"worst clip {worst:.3f} (limit {args.max_wer:.2f}), {sum(r['errors'] == 0 for r in rep)} clips exact")
sys.exit(0 if ok else 1)
