import json
import pydicom
from dicom.functions import from_PNG_to_DataPixel


# Funzione che ricostruisce il file DICOM recuperando i metadati dal segreto decifrato ed i valori dei pixel dell'immagine convertita
def reconstruction(folder_path):
    pathSecretJson = folder_path + "tmp/secret.json"
    pathReconstructedDicom = folder_path + "reconstructed.dcm"
    pathConvertedDicom = folder_path + "tmp/converted_DICOM.png"

    # Apro file JSON
    try:
        with open(pathSecretJson, 'r') as file:
            data_json = json.load(file)

    except FileNotFoundError:
        print(f"Error: The file '{pathSecretJson}' required for reconstructioning does not exist.")
        return None

    except Exception as e:
        print(f"An error occurred: {str(e)}. \n"
              f"Please check if you are trying to decrypt a file encrypted with '-ef txt' using '-ef json'.")
        return None

    # Estraggo i due oggetti
    dataset_json = json.dumps(data_json["dataset_json"])
    metafile_json = json.dumps(data_json["metafile_json"])

    # Creo dataset
    ds = pydicom.Dataset.from_json(json.loads(dataset_json))
    ds.file_meta = pydicom.Dataset.from_json(json.loads(metafile_json))
    #ds.BitsAllocated = 8

    # Recupero valori dei pixel dall'immagine PNG e li inserisco nel Dataset
    ds.PixelData = from_PNG_to_DataPixel(pathConvertedDicom)
    ds.save_as(pathReconstructedDicom)

    return True
