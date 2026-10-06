"""timing.json -> SRT (show text), same cue rule as the episode 2/3 assemble.py. Usage: srt.py DIR OUT.srt"""
import json, sys
from pathlib import Path
lines = json.loads((Path(sys.argv[1]) / 'timing.json').read_text())['lines']
ts = lambda x: (lambda ms: f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}')(round(x * 1000))
out = []
for i, l in enumerate(lines):
    nxt = lines[i + 1]['start'] if i + 1 < len(lines) else l['end'] + 1
    until = nxt - 0.08 if nxt - l['end'] < 0.9 else l['end'] + 0.35
    out.append(f'{i+1}\n{ts(l["start"] - 0.08)} --> {ts(until - 0.02)}\n{l["show"]}\n')
Path(sys.argv[2]).write_text('\n'.join(out))
