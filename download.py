import os
import requests
import csv

# Downloading begins here
def fetch_study_ids(dcm4chee_url):
    response = requests.get(f"{dcm4chee_url}/dcm4chee-arc/aets/DCM4CHEE/rs/studies/")
    response.raise_for_status()
    study_ids = [study['0020000D']['Value'][0] for study in response.json()]
    return study_ids

def get_uploaded_study_ids(csv_file_path):
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            uploaded_study_ids = [row[0] for row in reader if row]
            print(f"Found {len(uploaded_study_ids)} uploaded study IDs.")
            return uploaded_study_ids
    return []

def download_study_zips(study_ids, dcm4chee_url, download_path):
    os.makedirs(download_path, exist_ok=True)
    for study_id in study_ids:
        response = requests.get(f"{dcm4chee_url}/dcm4chee-arc/aets/DCM4CHEE/rs/studies/{study_id}?accept=application%2Fzip&dicomdir=true")
        response.raise_for_status()
        zip_file_path = os.path.join(download_path, f"{study_id}.zip")
        with open(zip_file_path, 'wb') as zip_file:
            zip_file.write(response.content)

def update_csv(new_study_ids, csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([[study_id] for study_id in new_study_ids])

def list_zip_files():
    directory="Temp_Downloads"
    zip_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.zip'):
                file_path = os.path.join(root, file)
                # Convert backslashes to forward slashes
                file_path = file_path.replace('\\', '/')
                zip_files.append(file_path)
    
    return zip_files



if __name__ == '__main__':
    dcm4chee_url = "http://13.235.102.234:8080"
    csv_file_path = "Logs/Uploaded_dcm4chee.csv"
    download_path = "./Temp_Downloads"
    
    all_studies = fetch_study_ids(dcm4chee_url)
    uploaded_studies = get_uploaded_study_ids(csv_file_path)
    new_studies = list(set(all_studies) - set(uploaded_studies))
    print(f"{new_studies}")
    if not new_studies:
        print("No new studies to download.")
        #return

    download_study_zips(new_studies, dcm4chee_url, download_path)
    update_csv(list(set(uploaded_studies).union(new_studies)), csv_file_path)
    print(type(list_zip_files()))
    print(list_zip_files())