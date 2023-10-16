from PIL import Image
from src.rg.bitplane.functions import *

# Decompongo l'immagine in bitplane
img = Image.open('../../../resources/secret.jpg').convert('L')
bit_planes = slice_bit_plane(img, 8)

# Salvo tutti i bitplane
for i, bit_plane in enumerate(bit_planes):
    bit_plane_image = Image.fromarray((bit_plane * 255).astype(np.uint8))

    path = f'../../../resources/output/rg/bitplane/bitplane{i}.png'
    bit_plane_image.save(path)
