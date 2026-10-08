import os
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'img')
def exp(src, name, box=None, maxside=2000, q=80):
    im = Image.open(f'out/{src}.png').convert('RGB')
    if box: im = im.crop(box)
    im.thumbnail((maxside, maxside), Image.LANCZOS)
    im.save(f'{D}/{name}.webp', quality=q, method=6)
    print(name, im.size, os.path.getsize(f'{D}/{name}.webp') // 1024, 'KB')
    return im
# scenes
exp('coq-marble', 'coquelicot-marble')
exp('coq-linen', 'coquelicot-linen', maxside=1800)
exp('tul-marble', 'tulipe-marble')
exp('tul-linen', 'tulipe-linen', maxside=1400)
exp('tul-dark', 'tulipe-dark', maxside=2400)
exp('tul-detail', 'tulipe-detail', maxside=1000)
exp('coq-hero', 'hero-coquelicot', maxside=2600, q=78)
exp('tul-hero', 'hero-tulipe', maxside=2600, q=78)
# catalog (4:5)
exp('tul-linen', 'p-tulipe-service', maxside=1000)
exp('tul-marble', 'p-tulipe-plates', box=(419, 0, 1379, 1200), maxside=1000)
exp('tul-detail', 'p-tulipe-piala', box=(90, 0, 806, 896), maxside=1000)
exp('coq-linen', 'p-coquelicot-dinner', box=(533, 800, 1125, 1540), maxside=1000)
exp('coq-linen', 'p-coquelicot-tea', box=(0, 470, 576, 1190), maxside=1000)
exp('coq-linen', 'p-coquelicot-dessert', box=(0, 1170, 576, 1890), maxside=1000)
# social preview 1200x630
im = Image.open('out/coq-marble.png').convert('RGB').resize((1200, 675), Image.LANCZOS).crop((0, 22, 1200, 652))
im.save(f'{D}/og-image.jpg', quality=85); print('og', im.size)
