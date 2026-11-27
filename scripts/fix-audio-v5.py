"""Generate complete isolated syllables; never crop voiced syllable tails.
Use actual target characters with the Meijia Mandarin voice; audition required.
"""
from pathlib import Path
import subprocess, tempfile, wave, array
ROOT=Path(__file__).resolve().parents[1]
ITEMS={44:('钻','进'),48:('粗','细')}
with tempfile.TemporaryDirectory() as tmp:
    cache={}
    for char in {c for pair in ITEMS.values() for c in pair}:
        a=Path(tmp)/(char+'.aiff'); p=Path(tmp)/(char+'.wav')
        subprocess.run(['say','-v','Meijia','-r','175','-o',str(a),char+'。'],check=True)
        subprocess.run(['afconvert','-f','WAVE','-d','LEI16',str(a),str(p)],check=True)
        with wave.open(str(p)) as w:
            params=w.getparams(); samples=array.array('h',w.readframes(w.getnframes()))
        # Remove only digital silence outside the full utterance, preserving
        # 50 ms padding and every non-silent sample (including final tone).
        audible=[i for i,x in enumerate(samples) if abs(x)>16]
        assert audible and params.nchannels==1 and params.sampwidth==2
        pad=int(params.framerate*.05)
        samples=samples[max(0,audible[0]-pad):min(len(samples),audible[-1]+pad+1)]
        cache[char]=(params,samples)
    for i,(first,second) in ITEMS.items():
        params,a=cache[first]; other,b=cache[second]
        assert params.framerate==other.framerate
        silence=lambda sec: array.array('h',[0]*int(params.framerate*sec))
        output=a+silence(.08)+b+silence(.55)+a+silence(.2)
        path=ROOT/'audio'/f'{i}-v5.wav'
        with wave.open(str(path),'wb') as w:
            w.setparams(params);w.writeframes(output.tobytes())
        print(path.name,round(len(output)/params.framerate,2),'seconds')
