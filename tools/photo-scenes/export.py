"""Save rendered scenes (out/*.png) as web-ready WebP into assets/img."""
import os
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'img')
D = os.environ.get('SITE_IMG', D)

def exp(src, name, box=None, maxside=2000, q=80):
    im = Image.open(f'out/{src}.png').convert('RGB')
    if box: im = im.crop(box)
    im.thumbnail((maxside, maxside), Image.LANCZOS)
    im.save(f'{D}/{name}.webp', quality=q, method=6)
    print(name, im.size, os.path.getsize(f'{D}/{name}.webp') // 1024, 'KB')

# hero (wide, empty table on the left for the headline)
exp('coq-hero', 'hero-qyzgaldaq', maxside=2600, q=78)
exp('tul-hero', 'hero-nauryz', maxside=2600, q=78)
exp('jus-hero', 'hero-jusan', maxside=2600, q=78)
# scenes
exp('tul-linen', 'nauryz-linen', maxside=1400)
exp('tul-marble', 'nauryz-marble')
exp('tul-dark', 'nauryz-dark', maxside=2400)
exp('tul-detail', 'nauryz-detail', maxside=1000)
exp('coq-marble', 'qyzgaldaq-marble')
exp('coq-linen', 'qyzgaldaq-linen', maxside=1800)
exp('jus-linen', 'jusan-linen', maxside=1400)
exp('jus-marble', 'jusan-marble', maxside=1800)
# catalog (4:5)
exp('tul-linen', 'p-nauryz-service', maxside=1000)
exp('tul-marble', 'p-nauryz-plates', box=(419, 0, 1379, 1200), maxside=1000)
exp('tul-detail', 'p-nauryz-piala', box=(90, 0, 806, 896), maxside=1000)
exp('coq-linen', 'p-qyzgaldaq-dinner', box=(533, 800, 1125, 1540), maxside=1000)
exp('coq-linen', 'p-qyzgaldaq-tea', box=(0, 470, 576, 1190), maxside=1000)
exp('coq-linen', 'p-qyzgaldaq-dessert', box=(0, 1170, 576, 1890), maxside=1000)
exp('jus-linen', 'p-jusan-set', maxside=1000)
exp('jus-marble', 'p-jusan-teapot', box=(690, 520, 1705, 1789), maxside=1000)
exp('jus-marble', 'p-jusan-cup', box=(0, 1010, 620, 1785), maxside=1000)
# social preview 1200x630
im = Image.open('out/coq-marble.png').convert('RGB').resize((1200, 675), Image.LANCZOS).crop((0, 22, 1200, 652))
im.save(f'{D}/og-image.jpg', quality=85)
