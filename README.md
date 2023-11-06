# pyqt-dicom-viewer
DICOM file viewer powered by PyQt

Just a simple version of DICOM file viewer.

Not as good as mydicom viewer or anything like that :)

I got sample DICOM files for this small project in this <a href="https://www.rubomedical.com/dicom_files/">site</a>

## What is DICOM file
DICOM (Digital Imaging and Communications in Medicine) file is a standard format for storing and transmitting medical images. 
 
DICOM files are used extensively in various medical imaging equipment and software.

Such as CT, MRI. That monochrome frames in the computer of the doctor's office you know :)

## Requirements
* PyQt5 >= 5.14
* pydicom

## How to Install
1. git clone ~
2. pip install -r requirements.txt
3. python main.py

## Preview
![image](https://github.com/yjg30737/pyqt-dicom-viewer/assets/55078043/65ef86d0-9f28-4169-ab16-7793e1cabd1d)

## TODO
* extract the metadata (e.g. patient information)
* support WSI(Whole Slide Images)

