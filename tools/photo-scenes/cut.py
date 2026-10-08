"""Remove photobox background: python3 cut.py birefnet-general s1 s2 ... (src/<name>.png -> cut/<name>_birefn.png)"""
import sys, time, os
from rembg import new_session, remove
from PIL import Image
os.makedirs('cut', exist_ok=True)
s = new_session(sys.argv[1])
for n in sys.argv[2:]:
    t=time.time()
    im = Image.open(f'src/{n}.png').convert('RGB')
    out = remove(im, session=s)
    out.save(f'cut/{n}_{sys.argv[1][:6]}.png'); print(n, time.time()-t, flush=True)
