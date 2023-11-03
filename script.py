import pydicom
import os


def tile_dicom_image(dicom_file):
    # Read the DICOM file
    ds = pydicom.dcmread(dicom_file)

    dicom_dict = {}
    dicom_dict['data'] = []

    key_prop = ['StudyDate',
     'PatientName',
     'PatientID',
     'PatientBirthDate',
     'PatientSex']

    dicom_dict['filename'] = dicom_file

    for dd in ds:
        if dd.keyword in key_prop:
            dicom_dict[dd.keyword] = dd.repval[1:-1]

    dicom_dict_arr = []
    # Extract the pixel data
    image_data = ds.pixel_array
    for tile in image_data:
        w, h = tile.shape
        dicom_dict['width'] = w
        dicom_dict['height'] = h
        dicom_dict['data'].append(tile[0])

    return dicom_dict

def get_tiled_dicom_images_in_directory(dirname):
    ts_arr = []
    for filename in os.listdir(dirname):
        filename = os.path.join(dirname, filename)
        ts_arr.append(tile_dicom_image(filename))
    return ts_arr