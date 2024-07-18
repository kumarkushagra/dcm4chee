import os
import requests
import csv
from zipfile import ZipFile
from io import BytesIO

# Downloading begins here
def fetch_study_ids(dcm4chee_url):
    response = requests.get(f"{dcm4chee_url}/dcm4chee-arc/aets/DCM4CHEE/rs/studies/")
    response.raise_for_status()
    return [study['0020000D']['Value'][0] for study in response.json()]

def get_uploaded_study_ids(csv_file_path):
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            return [row[0] for row in reader if row]
    return []

def download_and_extract_studies(study_ids, dcm4chee_url, download_path):
    os.makedirs(download_path, exist_ok=True)
    for study_id in study_ids:
        print(f"Downloading study {study_id}...")
        response = requests.get(f"{dcm4chee_url}/dcm4chee-arc/aets/DCM4CHEE/rs/studies/{study_id}?accept=application%2Fzip&dicomdir=true")
        response.raise_for_status()
        with ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(download_path)
        print(f"Downloaded and extracted study {study_id}")

def update_csv(new_study_ids, csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([[study_id] for study_id in new_study_ids])
    print("CSV file updated with new study IDs.")

def list_dicom_files(directory):
    dicom_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.dcm'):
                file_path = os.path.join(root, file)
                # Convert backslashes to forward slashes
                file_path = file_path.replace('\\', '/')
                dicom_files.append(file_path)
    
    return dicom_files

# Uploading begins here

def upload_dicom_file(dicom_paths_arr):
    orthanc_url = "http://localhost:8042"

    for dicom_file_path in dicom_paths_arr:
        # Read the DICOM file in binary mode
        with open(dicom_file_path, 'rb') as f:
            dicom_data = f.read()

        # Upload the DICOM file
        orthanc_url_with_instances = orthanc_url.rstrip('/') + '/instances'
        response = requests.post(orthanc_url_with_instances, data=dicom_data, headers={'Content-Type': 'application/dicom'})
        response.raise_for_status()

    # Anonymization begins here

    # Creating a list containing New Uploaded Studies
    csv_file_path = 'Orthanc_uploaded_StudyID.csv'
    uploaded_list = []
    # Check if the file exists before attempting to read it
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                uploaded_list.append(row['Uploaded'])
    
    new_studies_list = requests.get(f"{orthanc_url}/studies").json()
    new_studies = list(set(new_studies_list) - set(uploaded_list))
    
    anonymize_response = requests.post(
        f"{orthanc_url}/tools/bulk-anonymize",
        json={"Resources": new_studies}
    )
    anonymize_response.raise_for_status()

    # Delete original studies from Orthanc PACS
    for study_id in new_studies:
        study_delete_url = f'{orthanc_url}/studies/{study_id}'
        delete_response = requests.delete(study_delete_url)
        delete_response.raise_for_status()

    all_studies = requests.get(f"{orthanc_url}/studies").json()
    new_studies = list(set(all_studies) - set(uploaded_list))

    # Updating the CSV file
    fieldnames = ['Uploaded']
    data = []
    concatenated_string = ''.join(new_studies)
    
    if os.path.isfile(csv_file_path):
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames if 'Uploaded' in reader.fieldnames else fieldnames + reader.fieldnames
            data = [{**row, 'Uploaded': row.get('Uploaded', '') + concatenated_string} for row in reader]
    else:
        data = [{'Uploaded': concatenated_string}]
    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def pacs_to_pacs_transfer(source_url, destination_url):
    # Get the list of studies from the source Orthanc
    response = requests.get(f"{source_url}/studies")
    if response.status_code != 200:
        print(f"Failed to get studies from source Orthanc: {response.status_code}")
        return

    studies = response.json()

    for study in studies:
        print(f"Sending study: {study}")

        # Download the study as a ZIP file and stream it directly to the destination
        archive_url = f"{source_url}/studies/{study}/archive"
        with requests.get(archive_url, stream=True) as r:
            if r.status_code != 200:
                print(f"Failed to download study {study}: {r.status_code}")
                continue

            # Stream the downloaded ZIP file directly to the destination Orthanc
            upload_response = requests.post(
                f"{destination_url}/instances",
                headers={"Content-Type": "application/zip"},
                data=r.iter_content(chunk_size=8192)  # 8192 bytes (8 kb)
                # if memory is the constraint, reduce this number 
            )
            if upload_response.status_code != 200:
                print(f"Failed to upload study {study} to destination Orthanc: {upload_response.status_code}")
            else:
                print(f"Study {study} transferred successfully.")

def delete_temp_files():
    directory_path = "./Temp_Downloads"

    for root, dirs, files in os.walk(directory_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                os.rmdir(dir_path)
            except OSError as e:
                print(f"Failed to delete {dir_path}. Reason: {e}")

def main():
    dcm4chee_url = "http://13.235.102.234:8080"
    csv_file_path = "Uploaded_dcm4chee.csv"
    download_path = "./Temp_Downloads"
    source_url = "http://localhost:8042"
    destination_url="http://localhost:1111"
    
    all_studies = fetch_study_ids(dcm4chee_url)
    uploaded_studies = get_uploaded_study_ids(csv_file_path)
    new_studies = list(set(all_studies) - set(uploaded_studies))
    if not new_studies:
        print("No new studies to download.")
        return

    download_and_extract_studies(new_studies, dcm4chee_url, download_path)
    update_csv(list(set(uploaded_studies).union(new_studies)), csv_file_path)

    dicom_paths = list_dicom_files(download_path)
    upload_dicom_file(dicom_paths)
    delete_temp_files()
    pacs_to_pacs_transfer(source_url, destination_url)


if __name__ == "__main__":
    main()
 