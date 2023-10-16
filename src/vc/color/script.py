from src.vc.color.functions import *


image = Image.open("../../../resources/cinquecento_color.png")

# Decomposizione di colori
cyan_channel = 0
magenta_channel = 1
yellow_channel = 2

image = image.convert("CMYK")

# Azzero altri canali => ottengo immagini monocromatiche e le salvo
cyan_monochrome = zero_other_channels(image, cyan_channel)
magenta_monochrome = zero_other_channels(image, magenta_channel)
yellow_monochrome = zero_other_channels(image, yellow_channel)

cyan_monochrome.save("../../../resources/output/vc/color/monochrome_cyan.tiff")
magenta_monochrome.save("../../../resources/output/vc/color/monochrome_magenta.tiff")
yellow_monochrome.save("../../../resources/output/vc/color/monochrome_yellow.tiff")

# Effettuo dithering su ciascuna immagine monocromatica e le salvo
dthrd_cyan = floyd_steinberg_dithering(cyan_monochrome, cyan_channel)
dthrd_magenta = floyd_steinberg_dithering(magenta_monochrome, magenta_channel)
dthrd_yellow = floyd_steinberg_dithering(yellow_monochrome, yellow_channel)

cyan_monochrome.save("../../../resources/output/vc/color/dithered_cyan.tiff")
magenta_monochrome.save("../../../resources/output/vc/color/dithered_magenta.tiff")
yellow_monochrome.save("../../../resources/output/vc/color/dithered_yellow.tiff")

# Combino le immagini tra loro e salvo il risultato
combined_image = merge_dithered_images(dthrd_cyan, dthrd_magenta, dthrd_yellow)
combined_image.save("../../../resources/output/vc/color/combined_image.tiff")
