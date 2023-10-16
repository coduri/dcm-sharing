import numpy as np
from PIL import Image
from pydicom import Dataset

# Lista di tag considerati sensibili
sensitive_tags = [
    '(0010, 0010)', '(0010, 0030)', '(0010, 0040)', '(0010, 0020)',
    '(0008, 0050)', '(0008, 0090)', '(0010, 1040)', '(0010, 1010)',
    '(0008, 0080)', '(0008, 1030)', '(0008, 103E)', '(0020, 0010)',
    '(0008, 0020)', '(0008, 0030)', '(0020, 000D)', '(0008, 0018)'
]


# Funzione che dato un tag dice se è considerato sensibile o no
def is_sensitive_metadata(tag):
    return str(tag) in sensitive_tags


# Funzione che restituisce un Dataset contenente i metadati considerati sensibili
def get_sensitive_metadata(ds):
    sensitive_metadata = Dataset()

    for elem in ds:
        if is_sensitive_metadata(elem.tag):
            sensitive_metadata.add(elem)

    return sensitive_metadata


# Funzione che restituisce tutti i metadati del Dataset e i Metafile
def get_all_metadata_json(ds):
    del ds.PixelData

    json_data = {
        "dataset_json": ds.to_json(),
        "metafile_json": ds.file_meta.to_json()
    }

    return json_data


# Funzione che prende i pixel data, salva immagine convertita nel path indicato e restituisce l'immagine in forma array
def from_DataPixel_to_PNG(pixel_data_array, destination_path):
    image_data = pixel_data_array.astype(float)
    rescaled_image = (np.maximum(image_data, 0) / image_data.max()) * 255
    final_image = np.uint8(rescaled_image)

    imagePIL = Image.fromarray(final_image)
    imagePIL.save(destination_path)

    return final_image


# Funzione che prende il percorso dell'immagine PNG, e ne ricava i pixel data per ricostruire il file DICOM
def from_PNG_to_DataPixel(png_image_path):
    img = Image.open(png_image_path)
    img_array = np.array(img.getdata(), dtype=np.uint8)

    return img_array.tobytes()
