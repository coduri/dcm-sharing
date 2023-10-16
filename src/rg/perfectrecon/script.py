from PIL import Image
from src.rg.perfectrecon.functions import *

# Carico l'immagine in scala di grigi e costruisco array np
image = Image.open("../../../resources/secret.jpg").convert('L')
image_array = np.array(image).astype(int)

# Creo e salvo la prima random grid
grid1 = create_random_grid(image_array.shape)
grid1_image = Image.fromarray(grid1.astype(np.uint8))
grid1_image.save("../../../resources/output/rg/perfectrecon/grid1.png")

# Creo e salvo la seconda random grid
grid2 = create_difference_grid(image_array, grid1)
grid2_image = Image.fromarray(grid2.astype(np.uint8))
grid2_image.save("../../../resources/output/rg/perfectrecon/grid2.png")

# Effettuo una "sovrapposizione" delle due grid
over = overlay_grids(grid1, grid2)
over_image = Image.fromarray(over.astype(np.uint8))
over_image.save("../../../resources/output/rg/perfectrecon/over.png")
