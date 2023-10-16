from PIL import Image
from src.vc.basic.functions import *

# Immagine selezionata e convertita in bianco e nero
image = Image.open("../../../resources/secret.jpg")
image = image.convert('1')
image.save("../../../resources/output/vc/basic/halftoned.png")

# Matrici per determinare subpixel
w = [[1, 1, 0, 0], [1, 1, 0, 0]]
b = [[1, 1, 0, 0], [0, 0, 1, 1]]

# Pixel expansion
share1 = Image.new("1", (image.size[0] * 2, image.size[1] * 2))
share2 = Image.new("1", (image.size[0] * 2, image.size[1] * 2))
out = Image.new("1", (image.size[0] * 2, image.size[1] * 2))


# Generazione degli share
for i in range(0, image.size[0]):
    for j in range(0, image.size[1]):
        # Ottengo valore pixel secondo standard VC
        source_pixel_rgb = image.getpixel((i, j))
        source_pixel_vc = map_rgb_to_bit(source_pixel_rgb)

        # Bianco
        if source_pixel_vc == 0:
            random_white_matrix = random_col_permutation(w)
            populate_subpixels(share1, share2, i, j, random_white_matrix)

        # Nero
        else:
            random_black_matrix = random_col_permutation(b)
            populate_subpixels(share1, share2, i, j, random_black_matrix)


# Simulo sovrapposizione degli share e rimappo ad RGB
for i in range(0, image.size[0] * 2):
    for j in range(0, image.size[1] * 2):
        # Sovrapposizione degli share (OR)
        share1_vc_value = share1.getpixel((i, j))
        share2_vc_value = share2.getpixel((i, j))
        out_vc_value = share1_vc_value | share2_vc_value

        # Re-mapping dei pixel da standard VC a codifica RGB
        share1.putpixel((i, j), map_bit_to_rgb(share1_vc_value))
        share2.putpixel((i, j), map_bit_to_rgb(share2_vc_value))
        out.putpixel((i, j), map_bit_to_rgb(out_vc_value))

# Salvo immagini
share1.save("../../../resources/output/vc/basic/share1.png")
share2.save("../../../resources/output/vc/basic/share2.png")
out.save("../../../resources/output/vc/basic/overlap.png")
