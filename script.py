import numpy as np
import pydicom
import os
from PIL import Image, ImageDraw, ImageFont

def get_dicom_image(dicom_file):
    # Read the DICOM file
    ds = pydicom.dcmread(dicom_file)
    ds.PatientName = ''
    ds.PatientID = ''

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

    print(dicom_dict)

    dicom_dict_arr = []
    # Extract the pixel data
    image_data = ds.pixel_array
    for d in image_data:
        w, h = d.shape
        dicom_dict['width'] = w
        dicom_dict['height'] = h
        # dicom_dict['data'].append(d[0])

        if 'RescaleIntercept' in ds and 'RescaleSlope' in ds:
            d = d * ds.RescaleSlope + ds.RescaleIntercept
        d = np.uint8(d)
        pil_image = Image.fromarray(d)
        draw = ImageDraw.Draw(pil_image)
        font = ImageFont.load_default()
        text = f'''
StudyDate: {ds.StudyDate}
PatientName: {ds.PatientName}
PatientID: {ds.PatientID}
PatientBirthDate: {ds.PatientBirthDate}
PatientSex: {ds.PatientSex}
        '''
        draw.text((10, 10), text, fill=255, font=font)
        dicom_dict['data'].append(np.array(pil_image))

    return dicom_dict

def get_dicom_images_in_dir(dirname):
    ds_arr = []
    for filename in os.listdir(dirname):
        filename = os.path.join(dirname, filename)
        ds_arr.append(get_dicom_image(filename))
    return ds_arr