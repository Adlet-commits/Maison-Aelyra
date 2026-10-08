import sys, os
import numpy as np
from PIL import Image
from tex import *

OUT = 'out'; os.makedirs(OUT, exist_ok=True)
cut = lambda n: Image.open(f'cut/{n}_birefn.png').convert('RGBA')

def table(kind, w, h, seed, persp=None, light=None, leaves=None, leaf_op=0.22):
    """Lit surface. persp=top_scale -> surface seen at an angle (texture made taller, then squashed)."""
    th = int(h * 1.7) if persp else h
    tex = {'marble': lambda: marble(th, w, seed=seed), 'linen': lambda: linen(th, w, seed=seed),
           'plaster': lambda: plaster(th, w, seed=seed),
           'dark': lambda: plaster(th, w, seed=seed, base=(64, 58, 52))}[kind]()
    if light is not None:
        tex = apply_light(tex, window_light(th, w, seed=seed, **light))
    if leaves:
        ls = leaf_shadow(th, w, seed=seed + 1, **leaves)
        tex = tex * (1 - ls[..., None] * leaf_op)
    if persp:
        tex = perspective(tex, top_scale=persp, out_h=h)
        tex = depth_blur(tex, r_top=7, start=0.0, end=0.6)
    return tex

def finish(img, vig=0.22, cx=0.5, cy=0.5, warmth=(1.01, 1.0, 0.98), contrast=1.04):
    img = vignette(img, vig, cx, cy)
    img = (img - 128) * contrast + 128
    return np.clip(img * np.array(warmth, np.float32), 0, 255)

def leaf_on_dish(img, mask, seed, op=0.12, **kw):
    """Light leaf shadow over the porcelain too, so it sits in the same light."""
    h, w = mask.shape
    ls = leaf_shadow(h, w, seed=seed, **kw)
    return img * (1 - (ls * mask)[..., None] * op)

def flatlay(name, src, kind, seed, w=None, h=None, scale=1.0, x=0, y=0, light=None, leaves=None, dish_leaf=0.1, vig=0.2):
    c = cut(src)
    if scale != 1: c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    w = w or c.width; h = h or c.height
    bg = table(kind, w, h, seed, light=light, leaves=leaves)
    img, m = place(bg, c, x, y, 1.0, shadow=(int(w * 0.012), int(w * 0.010), 0.38), contact=(3, 3, 0.45), shadow_dir=(0.7, 1.0))
    if leaves: img = leaf_on_dish(img, m, seed + 1, op=dish_leaf, **leaves)
    if light is not None:
        wl = window_light(h, w, seed=seed, **light)
        img = img * (1 - m[..., None]) + apply_light(img, wl, ambient=0.93) * m[..., None]
    img = finish(img, vig)
    save(img, f'{OUT}/{name}.png', q=100)
    print(name, img.shape)

def spot(img, cx, cy, rx, ry, gain=0.9, warm=(1.06, 1.0, 0.9)):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.clip(1 - (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2), 0, 1) ** 1.6
    return img * (1 + d[..., None] * gain * np.array(warm, np.float32))

def angled(name, src, kind, seed, w, h, scale, x, y, persp=0.62, light=None, leaves=None, vig=0.2, shadow_op=0.4, dark=False):
    c = cut(src)
    if scale != 1: c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    bg = table(kind, w, h, seed, persp=persp, light=light, leaves=leaves)
    if dark:
        bg = spot(bg, x + c.width * 0.5, y + c.height * 0.45, c.width * 0.85, c.height * 0.75, gain=1.1)
    img, m = place(bg, c, x, y, 1.0, shadow=(int(w * 0.018), int(w * 0.012), shadow_op), contact=(4, 5, 0.55), shadow_dir=(0.45, 1.0),
                   gains=(1.0, 0.97, 0.9) if dark else (1.025, 1.0, 0.955))
    img, _ = place(img, c, x, y, 1.0, shadow=(int(w * 0.035), int(w * 0.02), 0.22), contact=(2, 3, 0.5), shadow_dir=(0.4, 1.0),
                   gains=(1.0, 0.97, 0.9) if dark else (1.025, 1.0, 0.955))
    if dark:
        yy = np.linspace(0, 1, h)[:, None]
        img = img * (1 - m[..., None] * (0.06 + 0.1 * yy[..., None]))
    if leaves: img = leaf_on_dish(img, m, seed + 1, op=0.08, **leaves)
    img = finish(img, vig, cy=0.55)
    save(img, f'{OUT}/{name}.png', q=100)
    print(name, img.shape)

def detail():
    a = np.asarray(Image.open('src/s3.png').convert('RGB')).astype(np.float32)
    a = warm_fix(a, (1.03, 1.0, 0.95), 2)
    # warm up the cool photobox backdrop at the top
    h, w = a.shape[:2]
    cool = np.clip((a[..., 2] - a[..., 0]) / 25, 0, 1) * np.clip((a.mean(-1) - 170) / 40, 0, 1)
    cool = blur(cool, 3)[..., None]
    a = a * (1 - cool) + np.array([236, 229, 218], np.float32) * cool
    img = finish(a, 0.25)
    save(img, f'{OUT}/tul-detail.png', q=100); print('tul-detail')

if __name__ == '__main__':
    which = sys.argv[1:] or ['all']
    jobs = {
        # Coquelicot — pink poppy flat-lays
        'coq-marble': lambda: flatlay('coq-marble', 's5', 'marble', 21, leaves=dict(count=6), light=dict(scale=1.2, softness=60)),
        'coq-linen': lambda: flatlay('coq-linen', 's4', 'linen', 31, leaves=dict(count=5), dish_leaf=0.12),
        # Tulipe — angled table shots
        'tul-marble': lambda: angled('tul-marble', 's2', 'marble', 41, 1800, 1200, 1.2, 362, 80, leaves=dict(count=5), light=dict(scale=1.3, softness=70)),
        'tul-linen': lambda: angled('tul-linen', 's1', 'linen', 51, 1100, 1375, 1.15, 0, 300, leaves=dict(count=4)),
        'tul-dark': lambda: angled('tul-dark', 's2', 'dark', 61, 2400, 1100, 1.05, 1640 - 440, 560 - 486, vig=0.45, shadow_op=0.7, dark=True),
        # Wide hero versions: empty table on the left for the headline
        'coq-hero': lambda: flatlay('coq-hero', 's5', 'marble', 22, w=2600, h=1125, x=650, leaves=dict(count=6), light=dict(scale=1.0, softness=70)),
        'tul-hero': lambda: angled('tul-hero', 's2', 'marble', 42, 2600, 1200, 0.95, 1141, 177, leaves=dict(count=6), light=dict(scale=1.0, softness=80)),
        # Jusan — tea set
        'jus-linen': lambda: angled('jus-linen', 's6', 'linen', 71, 1125, 1406, 1.0, 0, -285, persp=0.55, leaves=dict(count=4)),
        'jus-marble': lambda: flatlay('jus-marble', 's7', 'marble', 81, leaves=dict(count=6), light=dict(scale=1.1, softness=60)),
        # s6h = s6 with the left cup (the piece touching the left edge) removed, so the set can sit on the right
        'jus-hero': lambda: angled('jus-hero', 's6h', 'marble', 91, 2600, 1200, 1.0, 1475, -348, persp=0.55, leaves=dict(count=6), light=dict(scale=1.0, softness=80)),
    }
    jobs['tul-detail'] = detail
    for k, f in jobs.items():
        if 'all' in which or k in which: f()
