# Problem:-
# PatientID, StudyInstanceUID, SeriesInstanceUID, SOPInstanceUID

import pydicom
import requests
import os

from download import * 
from Push_Studies.archive import *
from Push_Studies.anonymize_zip import anonymize_zip
from Push_Studies.Upload import *
from delete_temp_zip import delete_temp_files
from download import list_zip_files,update_csv
def main():
    dcm4chee_url = "http://13.235.102.234:8080"
    csv_file_path = "Logs/Uploaded_dcm4chee.csv"
    download_path = "./Temp_Downloads"
    source_url = "http://localhost:8042"
    destination_url = "http://localhost:1111"


    # ensure that nessecary directory exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    # Downloading
    all_studies = fetch_study_ids(dcm4chee_url)
    uploaded_studies = get_uploaded_study_ids(csv_file_path)
    new_studies = list(set(all_studies) - set(uploaded_studies))
    if not new_studies:
        print("No new studies to download.")
        return
    # Downloading studies
    print("Downloading...")
    download_study_zips(new_studies, dcm4chee_url, download_path)
    print("Downaloded")
    
    
    # Listing all zip files in temp_downloads    
    zip_files = [f for f in os.listdir(download_path) if f.endswith('.zip')]

    # Iterating through each file
    for zip_file in zip_files:
        # Passing zip file into the function 
        anonymize_zip(f"Temp_Downloads/{zip_file}")

    # All files anonymized and UN-ziped, Pushing to PACS
    print(download_path)
    dicom_paths=list_zip_files()
    Upload_list(dicom_paths)

    # deleting temporary files
    delete_temp_files()
    
    # Update the CSV
    update_csv(list(set(uploaded_studies).union(new_studies)), csv_file_path)

if __name__=="__main__":
    main()


# # Delete all studies on ORTHANC PACS:-
# import requests

# # Orthanc server URL
# ORTHANC_URL = "http://localhost:8042"

# def get_studies():
#     """Fetches the list of all studies from Orthanc."""
#     response = requests.get(f"{ORTHANC_URL}/studies")
#     response.raise_for_status()
#     return response.json()

# def delete_study(study_id):
#     """Deletes a study from Orthanc given its ID."""
#     response = requests.delete(f"{ORTHANC_URL}/studies/{study_id}")
#     response.raise_for_status()

# def main():
#     studies = get_studies()
#     for study_id in studies:
#         try:
#             delete_study(study_id)
#             print(f"Deleted study: {study_id}")
#         except requests.HTTPError as e:
#             print(f"Failed to delete study {study_id}: {e}")

# if __name__ == "__main__":
#     main()
