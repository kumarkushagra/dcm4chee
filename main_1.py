# Problem:-
# PatientID, StudyInstanceUID, SeriesInstanceUID, SOPInstanceUID

import pydicom
import requests
import os

from download import * 
from Push_Studies.archive import *
from Push_Studies.main import anonymize_zip
from Push_Studies.Upload import *

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

    # All files anonymized and ziped, Pushing to PACS
    upload_all_zip_files_in_directory(download_path)
if __name__=="__main__":
    main()