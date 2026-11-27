"""Preserve complete recordings and add 450 ms startup silence for mobile output."""
from pathlib import Path
import wave
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'audio'/'mobile-v1';out.mkdir(exist_ok=True)
for i in range(50):
    suffix='-v5' if i in [44,48] else '-v4' if i in [31,44,45,47,48] else '-v3' if i in [8,25,35,49,23,46,20,14] else ''
    with wave.open(str(ROOT/'audio'/f'{i}{suffix}.wav'),'rb') as w:
        params=w.getparams();frames=w.readframes(w.getnframes())
    assert params.sampwidth==2 and frames
    silence=bytes(round(params.framerate*.45)*params.nchannels*params.sampwidth)
    dest=(ROOT/'audio'/'mobile-v2' if i in [44,48] else out)/f'{i}.wav'
    dest.parent.mkdir(exist_ok=True)
    with wave.open(str(dest),'wb') as w:
        w.setparams(params);w.writeframes(silence+frames)
    with wave.open(str(dest),'rb') as w:
        result=w.readframes(w.getnframes())
    assert result==silence+frames
print('PASS: all 50 recordings retain original samples, preceded by 450 ms silence')
