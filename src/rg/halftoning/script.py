from PIL import Image
from src.rg.halftoning.functions import *

# Carico l'immagine in scala di grigi e faccio halftoning
image = Image.open("../../../resources/secret.jpg").convert('1')
image.save("../../../resources/output/rg/halftoning/dithered.png")

# Trasformo immagine in un array di 0 (bianco) e 1 (nero)
image_array = 1 - np.array(image).astype(int)

# Creo le random grid
rg1 = create_first_random_grid(image_array.shape)
rg2 = create_second_random_grid(image_array, rg1)

# Sovrappongo le immagini
overlap_OR = overlay_images_OR(rg1, rg2)
overlap_XOR = overlay_images_XOR(rg1, rg2)

# Salvo le random grid e il risultato delle sovrapposizioni
image_rg1 = Image.fromarray(rg1.astype(np.uint8) * 255)
image_rg1.save("../../../resources/output/rg/halftoning/RG1.png")
image_rg2 = Image.fromarray(rg2.astype(np.uint8) * 255)
image_rg2.save("../../../resources/output/rg/halftoning/RG2.png")

XOR_image = Image.fromarray(overlap_XOR.astype(np.uint8) * 255)
XOR_image.save("../../../resources/output/rg/halftoning/overlap_XOR.png")
OR_image = Image.fromarray(overlap_OR.astype(np.uint8) * 255)
OR_image.save("../../../resources/output/rg/halftoning/overlapOR.png")
