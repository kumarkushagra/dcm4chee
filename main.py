import os
import requests
import csv

from download import *
from Upload_n_anonymize import upload_zip_file
from SCP import pacs_to_pacs_transfer
from delete_temp_zip import delete_temp_files



def main():
    # Hard code the initial parameters
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
    download_study_zips(new_studies, dcm4chee_url, download_path)
    update_csv(list(set(uploaded_studies).union(new_studies)), csv_file_path)
    dicom_paths = list_zip_files()

    # Uploading and anonymizing data
    upload_zip_file(dicom_paths,csv_file_path)

    # deleting temporary files
    delete_temp_files()

    # Transfering data
    pacs_to_pacs_transfer(source_url, destination_url)


if __name__ == "__main__":
    main()
