import json
import os
import pydicom
from pydicom import dcmread

from dicom.functions import *
from steganography.lsb.functions import *
from rg.perfectrecon.functions import *


# Funzione che cifra un file DICOM con le varie opzioni settate
def encrypt(path_dicom, metadata_choice, encoding_format, path_output):
    pathConvertedDicom = path_output + "tmp/converted_DICOM.png"
    pathStegoImage = path_output + "tmp/stego_object.png"
    pathReconBits = path_output + "reconstruction_bits.txt"

    pathRandomGrid1 = path_output + "grid1.png"
    pathRandomGrid2 = path_output + "grid2.png"

    # Apro DICOM file e lo verifico
    try:
        DICOM_file = dcmread(path_dicom, force=True)

    except pydicom.errors.InvalidDicomError:
        print("Error: The file is not a valid DICOM file.")
        return None

    except FileNotFoundError:
        print(f"Error: The file {path_dicom} does not exist.")
        return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    # Verifico se esiste cartella tmp, altrimenti la creo
    if not os.path.exists(path_output + "/tmp"):
        os.makedirs(path_output + "/tmp")

    # LSB: Ottengo cover-image dal file DICOM
    cover_array = from_DataPixel_to_PNG(DICOM_file.pixel_array, pathConvertedDicom)

    # LSB: Preparo il segreto con i metadati da nascondere
    secret_metadata = ""

    if metadata_choice == 'partial':
        sensitive_dataset = get_sensitive_metadata(DICOM_file)

        if encoding_format == 'txt':
            for md in sensitive_dataset:
                secret_metadata += (f"Tag: {md.tag} | "
                                    f"Descrizione: {md.name} | "
                                    f"Valore: {md.value}; \n")

        else:  # encoding_format == 'json'
            secret_metadata = sensitive_dataset.to_json()

    else:  # metadata_choice == 'all':
        if encoding_format == 'txt':
            # Cancello i PixelData, li ricostruirò dall'immagine PNG
            del DICOM_file.PixelData

            for md in DICOM_file:
                secret_metadata += (f"Tag: {md.tag} | "
                                    f"Descrizione: {md.name} | "
                                    f"Valore: {md.value}; \n")

        else:  # encoding_format == 'json'
            json_metadata = get_all_metadata_json(DICOM_file)
            secret_metadata = json.dumps(json_metadata)

    # LSB: Costruisco e salvo stego-object
    stego_array, lsb_array = encode(cover_array, secret_metadata)

    if stego_array is None:
        print("Error: Message too long")
        return None

    stego_image = Image.fromarray(stego_array.astype('uint8'))
    stego_image.save(pathStegoImage)

    # LSB: Se richiesto salvo i bit che consentiranno la ricostruzione
    if metadata_choice == 'all' and (lsb_array is not None):
        with open(pathReconBits, 'w') as file:
            for bit in lsb_array:
                file.write(str(bit))

    # RG Perfect Reconstruction: Creo e salvo la prima random grid
    grid1 = create_random_grid(stego_array.shape)
    grid1_image = Image.fromarray(grid1.astype(np.uint8))
    grid1_image.save(pathRandomGrid1)

    # RG Perfect Reconstruction: Creo e salvo la seconda random grid
    grid2 = create_difference_grid(stego_array, grid1)
    grid2_image = Image.fromarray(grid2.astype(np.uint8))
    grid2_image.save(pathRandomGrid2)

    return True
