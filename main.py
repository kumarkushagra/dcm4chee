import os
import requests

def list_dicom_files(directory):
    dicom_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.dcm'):
                file_path = os.path.join(root, file)
                # Convert backslashes to forward slashes
                file_path = file_path.replace('\\', '/')
                dicom_files.append(file_path)
    
    return dicom_paths_arr

def upload_dicom_file(dicom_paths_arr):
    orthanc_url = "http://localhost:8042"

    for dicom_file_path in dicom_file_paths:
        # Read the DICOM file in binary mode
        with open(dicom_file_path, 'rb') as f:
            dicom_data = f.read()

        # Upload the DICOM file
        orthanc_url_with_instances = orthanc_url.rstrip('/') + '/instances'
        response = requests.post(orthanc_url_with_instances, data=dicom_data, headers={'Content-Type': 'application/dicom'})

