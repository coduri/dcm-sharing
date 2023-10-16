import os
from PIL import Image

from steganography.lsb.functions import *
from rg.perfectrecon.functions import *


# Funzione che decifra le random grid ottenute da un file DICOM con le varie opzioni settate
def decrypt(folder_path, metadata_choice, encoding_format):
    pathRandomGrid1 = folder_path + "grid1.png"
    pathRandomGrid2 = folder_path + "grid2.png"

    pathReconBits = folder_path + "reconstruction_bits.txt"
    pathStegoImage = folder_path + "tmp/stego_object.png"
    pathConvertedDicom = folder_path + "tmp/converted_DICOM.png"

    pathSecretTxt = folder_path + "secret.txt"
    pathSecretJson = folder_path + "tmp/secret.json"

    # Apro le due immagini contenenti le random grid
    try:
        grid1_img = Image.open(pathRandomGrid1)
        grid2_img = Image.open(pathRandomGrid2)

    except FileNotFoundError:
        print(f"Error: At least one of the files, '{pathRandomGrid1}' or '{pathRandomGrid2}' does not exist.")
        return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    # Verifico se esiste cartella tmp, altrimenti la creo
    if not os.path.exists(folder_path + "/tmp"):
        os.makedirs(folder_path + "/tmp")

    # RG Perfect Reconstruction: ricostruisco e salvo lo stego-object
    grid1_array = np.array(grid1_img).astype(int)
    grid2_array = np.array(grid2_img).astype(int)
    stego_array = overlay_grids(grid1_array, grid2_array)

    stego_image = Image.fromarray(stego_array.astype(np.uint8))
    stego_image.save(pathStegoImage)

    # LSB: recupero segreto come stringa
    bit_array = None

    if metadata_choice == 'all':
        try:
            with open(pathReconBits, 'r') as file:
                bit_string = file.read()
                bit_array = [int(bit) for bit in bit_string]

        except FileNotFoundError:
            print(f"Error: The file '{pathReconBits}' required for decryption in 'all metadata' mode does not exist.")
            return None

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    secret, cover_array = decode(stego_array, bit_array)

    if secret is None:
        print("Error: Unable to reconstruct the secret.")
        return None

    # LSB: se è avvenuta ricostruzione del cover object la salvo
    if cover_array is not None:
        cover_image = Image.fromarray(cover_array.astype(np.uint8))
        cover_image.save(pathConvertedDicom)

    # LSB: salvo segreto in formato txt o json
    if encoding_format == 'txt':
        with open(pathSecretTxt, 'w') as file:
            file.write(secret)

    else:  # encoding_format == 'json':
        with open(pathSecretJson, 'w') as file:
            file.write(secret)

    return True
