import shutil
from .archive import unzip_zip_file, zip_dir
from .create_dcm_list import list_dcm_files
from .Basic_Prof_anonymization import anonymize_dicom

def anonymize_zip(zip_file_path):
    # Extracting the zip file 
    unzip_dir_path = unzip_zip_file(zip_file_path)

    # Listing dcm files
    dcm_list = list_dcm_files(unzip_dir_path)
    counter = 0
    # Anonymizing dicom files
    for dicom_file in dcm_list:
        anonymize_dicom(dicom_file,counter)
        counter+=1
    
    # Zipping files
    zip_dir(unzip_dir_path)

if __name__=="__main__":
    anonymize_zip(r"D:\PROJECT\dcm4chee\Temp_Downloads\1.3.6.1.4.1.5962.1.1.0.0.0.1194732126.13032.0.1.zip")
