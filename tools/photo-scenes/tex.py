"""Procedural surfaces, light & compositing helpers for Maison Aelyra scenes."""
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageFilter, ImageDraw

def _resize(a, w, h, rs=Image.BICUBIC):
    return np.asarray(Image.fromarray(a.astype(np.float32), 'F').resize((w, h), rs))

def fbm(h, w, base=4, octaves=6, seed=0, aspect=(1, 1), persistence=0.5):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for i in range(octaves):
        gw = max(2, int(base * aspect[0] * 2 ** i)); gh = max(2, int(base * aspect[1] * 2 ** i))
        g = rng.random((gh + 3, gw + 3)).astype(np.float32)
        up = _resize(g, w + int(3 * w / gw), h + int(3 * h / gh))
        out += amp * up[:h, :w]; tot += amp; amp *= persistence
    out /= tot
    return (out - out.min()) / (out.max() - out.min() + 1e-6)

def blur(a, r):
    if r <= 0: return a
    return gaussian_filter(a.astype(np.float32), r)

def grain(h, w, amt=3.0, seed=7):
    return np.random.default_rng(seed).normal(0, amt, (h, w, 1)).astype(np.float32)

def marble(h, w, seed=1, base=(242, 238, 231), vein=(128, 124, 120), gold=(190, 160, 112)):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    s = max(h, w)
    n = fbm(h, w, base=2, octaves=4, seed=seed, persistence=0.45)
    nf = fbm(h, w, base=24, octaves=3, seed=seed + 5, persistence=0.5) - 0.5
    fade = np.clip((fbm(h, w, base=2, octaves=3, seed=seed + 7) - 0.35) * 2.2, 0, 1)
    t = (x * 0.75 + y * 0.65) / s * 1.6 + n * 1.1 + nf * 0.05
    v = 1 - np.abs(np.sin(t * np.pi))
    soft = blur(v ** 10, s * 0.006) * 0.5
    sharp = v ** 140 * 0.9
    veins = (soft + sharp) * fade
    n2 = fbm(h, w, base=3, octaves=4, seed=seed + 11, persistence=0.5)
    t2 = (x * -0.45 + y * 0.9) / s * 2.6 + n2 * 1.4 + nf * 0.08
    v2 = 1 - np.abs(np.sin(t2 * np.pi))
    fade2 = np.clip((fbm(h, w, base=3, octaves=3, seed=seed + 9) - 0.5) * 3, 0, 1)
    hair = (v2 ** 220 * 0.7 + blur(v2 ** 20, s * 0.003) * 0.18) * fade2
    cloud = fbm(h, w, base=2, octaves=6, seed=seed + 3) - 0.5
    img = np.empty((h, w, 3), np.float32)
    for c in range(3):
        img[..., c] = base[c] + cloud * 9
    veins = np.clip(blur(veins, 0.8), 0, 1)[..., None]
    hair = np.clip(blur(hair, 0.6), 0, 1)[..., None]
    img = img * (1 - veins * 0.55) + np.array(vein, np.float32) * veins * 0.55
    img = img * (1 - hair * 0.5) + np.array(gold, np.float32) * hair * 0.5
    img += grain(h, w, 1.4, seed)
    return np.clip(img, 0, 255)

def plaster(h, w, seed=6, base=(236, 229, 218)):
    cloud = fbm(h, w, base=2, octaves=7, seed=seed, persistence=0.55) - 0.5
    mid = fbm(h, w, base=10, octaves=4, seed=seed + 1) - 0.5
    pores = (np.random.default_rng(seed).random((h, w)) > 0.99965).astype(np.float32)
    pores = blur(pores, 0.9) * 6
    img = np.empty((h, w, 3), np.float32)
    for c in range(3):
        img[..., c] = base[c] + cloud * 16 + mid * 5 - pores * 22
    img += grain(h, w, 2.0, seed)
    return np.clip(img, 0, 255)

def linen(h, w, seed=2, base=(232, 224, 211)):
    rng = np.random.default_rng(seed)
    rowv = rng.normal(0, 1, h).astype(np.float32); colv = rng.normal(0, 1, w).astype(np.float32)
    rowv = np.convolve(rowv, [0.25, 0.5, 0.25], 'same'); colv = np.convolve(colv, [0.25, 0.5, 0.25], 'same')
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    weave = np.sin(x * np.pi / 1.6) * np.sin(y * np.pi / 1.6)
    slub = fbm(h, w, base=6, octaves=4, seed=seed + 5, aspect=(1, 18)) - 0.5
    slubv = fbm(h, w, base=6, octaves=4, seed=seed + 6, aspect=(18, 1)) - 0.5
    fold = fbm(h, w, base=2, octaves=4, seed=seed + 9) - 0.5
    lum = rowv[:, None] * 2.2 + colv[None, :] * 2.2 + weave * 2.5 + slub * 9 + slubv * 7 + fold * 18
    img = np.empty((h, w, 3), np.float32)
    for c in range(3):
        img[..., c] = base[c] + lum
    img += grain(h, w, 2.2, seed)
    return np.clip(img, 0, 255)

def walnut(h, w, seed=3, dark=(46, 30, 21), light=(104, 70, 46)):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    n = fbm(h, w, base=3, octaves=6, seed=seed, aspect=(1, 6))
    fine = fbm(h, w, base=8, octaves=4, seed=seed + 4, aspect=(1, 30))
    rings = 0.5 + 0.5 * np.sin((y / h * 38 + n * 9) * np.pi)
    rings = rings ** 2.2
    m = np.clip(rings * 0.65 + fine * 0.35, 0, 1)[..., None]
    img = np.array(dark, np.float32) * (1 - m) + np.array(light, np.float32) * m
    plank = h // 3
    seam = np.zeros((h, w), np.float32)
    for k in range(1, 4):
        yy = k * plank + int(rng_off(seed, k))
        if 0 < yy < h: seam[max(0, yy - 1):yy + 2] = 1
    seam = blur(seam, 1.2)[..., None]
    img *= 1 - seam * 0.55
    sheen = blur(fbm(h, w, base=2, octaves=3, seed=seed + 8), 30)[..., None]
    img *= 0.88 + sheen * 0.24
    img += grain(h, w, 1.8, seed)
    return np.clip(img, 0, 255)

def rng_off(seed, k):
    return np.random.default_rng(seed * 10 + k).integers(-40, 40)

def perspective(img, top_scale=0.55, out_h=None):
    """Tilt a flat texture so it recedes towards the top (table seen at an angle)."""
    h, w = img.shape[:2]
    out_h = out_h or h
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    inset = w * (1 - top_scale) / 2
    # source quad corners for output (0,0),(w,0),(w,h),(0,h)
    src = [(inset, 0), (w - inset, 0), (w, h), (0, h)]
    dst = [(0, 0), (w, 0), (w, out_h), (0, out_h)]
    coeffs = _persp_coeffs(dst, src)
    out = im.transform((w, out_h), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    return np.asarray(out).astype(np.float32)

def _persp_coeffs(pa, pb):
    m = []
    for p1, p2 in zip(pa, pb):
        m.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        m.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
    A = np.array(m, np.float64); B = np.array(pb, np.float64).reshape(8)
    return np.linalg.solve(A, B).tolist()

def depth_blur(img, r_top=10, start=0.0, end=0.55):
    """Blur the far (top) part of a scene progressively — shallow depth of field."""
    h = img.shape[0]
    b = np.stack([blur(img[..., c], r_top) for c in range(3)], -1)
    b2 = np.stack([blur(img[..., c], r_top / 3) for c in range(3)], -1)
    yy = np.linspace(0, 1, h)[:, None, None]
    t = np.clip((yy - start) / (end - start), 0, 1)
    far = np.clip(1 - t * 2, 0, 1); mid = np.clip(np.minimum(t * 2, 2 - t * 2), 0, 1)
    near = np.clip(t * 2 - 1, 0, 1)
    return b * far + b2 * mid + img * near

def window_light(h, w, seed=4, angle=-0.35, panes=(3, 2), softness=38, scale=1.0):
    """Light map: 1 = sunlit, 0 = shade. Soft window with mullions, skewed."""
    S = 2
    big = Image.new('L', (w * S, h * S), 0)
    d = ImageDraw.Draw(big)
    pw, ph = int(w * 0.36 * scale), int(h * 0.62 * scale)
    x0, y0 = int(w * S * 0.04), int(-h * S * 0.05)
    bar = int(min(w, h) * 0.022 * S)
    for i in range(panes[0]):
        for j in range(panes[1]):
            cx = x0 + i * (pw * S // panes[0]); cy = y0 + j * (ph * S // panes[1])
            d.rectangle([cx + bar, cy + bar, cx + pw * S // panes[0] - bar, cy + ph * S // panes[1] - bar], fill=255)
    big = big.transform(big.size, Image.AFFINE, (1, angle, 0, 0, 1, 0), Image.BICUBIC)
    big = big.resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(softness))
    return np.asarray(big).astype(np.float32) / 255

def leaf_shadow(h, w, seed=5, count=6, softness=(5, 26), leaf=(0.045, 0.085)):
    """Shadow map of leafy (olive-like) branches, 1 = shadow."""
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    M = max(w, h)
    for layer, sf in enumerate(np.linspace(softness[1], softness[0], 3)):
        im = Image.new('L', (w, h), 0); d = ImageDraw.Draw(im)
        for b in range(count):
            if rng.random() < 0.5:
                x, y = rng.uniform(-0.1, 0.7) * w, -0.08 * h; ang = rng.uniform(0.9, 1.6)
            else:
                x, y = -0.08 * w, rng.uniform(-0.1, 0.7) * h; ang = rng.uniform(-0.1, 0.7)
            L = rng.uniform(0.3, 0.7) * M; steps = 60; side = 1
            for s_ in range(steps):
                ang += rng.normal(0, 0.035)
                nx, ny = x + np.cos(ang) * L / steps, y + np.sin(ang) * L / steps
                d.line([x, y, nx, ny], fill=255, width=max(2, int(M * 0.0025)))
                if rng.random() < 0.33:
                    side = -side
                    la = ang + side * rng.uniform(0.35, 0.9)
                    ll = rng.uniform(*leaf) * M; lw = ll * rng.uniform(0.2, 0.32)
                    cx, cy = nx + np.cos(la) * ll * 0.5, ny + np.sin(la) * ll * 0.5
                    lf = Image.new('L', (int(ll * 2) + 2, int(ll * 2) + 2), 0)
                    ImageDraw.Draw(lf).ellipse([ll - ll * 0.5, ll - lw / 2, ll + ll * 0.5, ll + lw / 2], fill=255)
                    lf = lf.rotate(-np.degrees(la), resample=Image.BICUBIC)
                    im.paste(255, (int(cx - ll), int(cy - ll)), lf)
                x, y = nx, ny
        a = np.asarray(im.filter(ImageFilter.GaussianBlur(float(sf)))).astype(np.float32) / 255
        acc = np.maximum(acc, a * (0.5 + 0.2 * layer))
    return np.clip(acc, 0, 1)

def apply_light(img, light, ambient=0.86, warm=(1.035, 1.0, 0.95), cool=(0.985, 0.99, 1.01)):
    L = light[..., None]
    gain = ambient + (1 - ambient) * L * 1.15 + 0.06
    tint = np.array(cool, np.float32) * (1 - L) + np.array(warm, np.float32) * L
    return img * gain * tint

def vignette(img, strength=0.25, cx=0.5, cy=0.5):
    h, w = img.shape[:2]
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((x / w - cx) * 1.0) ** 2 + ((y / h - cy) * (h / w)) ** 2)
    d = d / d.max()
    return img * (1 - strength * d[..., None] ** 2)

def warm_fix(rgb, gains=(1.025, 1.0, 0.955), lift=0.0):
    return np.clip(rgb * np.array(gains, np.float32) + lift, 0, 255)

def place(scene, cut, x, y, scale=1.0, shadow=(22, 18, 0.42), contact=(5, 4, 0.5), gains=(1.025, 1.0, 0.955), shadow_dir=(0.6, 1.0)):
    """Composite an RGBA cut-out onto scene (float HxWx3) with soft drop + contact shadows."""
    if scale != 1.0:
        cut = cut.resize((int(cut.width * scale), int(cut.height * scale)), Image.LANCZOS)
    a = np.asarray(cut).astype(np.float32)
    rgb, al = warm_fix(a[..., :3], gains), a[..., 3] / 255
    H, W = scene.shape[:2]; h, w = al.shape
    pad = max(h, w) + 10
    big = np.zeros((H + 2 * pad, W + 2 * pad), np.float32)
    big[y + pad:y + pad + h, x + pad:x + pad + w] = al
    bigc = np.zeros((H + 2 * pad, W + 2 * pad, 3), np.float32)
    bigc[y + pad:y + pad + h, x + pad:x + pad + w] = rgb
    # occluding mask in scene coords
    m = big[pad:pad + H, pad:pad + W]
    sh = np.zeros_like(m)
    for (r, d, op) in (shadow, contact):
        dx, dy = int(d * shadow_dir[0]), int(d * shadow_dir[1])
        s = blur(np.roll(np.roll(big, dy, 0), dx, 1), r)[pad:pad + H, pad:pad + W]
        sh = 1 - (1 - sh) * (1 - s * op)
    scene = scene * (1 - sh[..., None] * np.array([0.92, 0.95, 1.0], np.float32))
    layer = bigc[pad:pad + H, pad:pad + W]
    return scene * (1 - m[..., None]) + layer * m[..., None], m

def save(img, path, q=84, size=None):
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    if size: im = im.resize(size, Image.LANCZOS)
    im.save(path, quality=q, method=6)
    return im
