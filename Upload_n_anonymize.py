import os
import requests
import csv


# Uploading begins here
def upload_zip_file(zip_paths_arr):
    if type(zip_paths_arr) != list:
        zip_paths_arr = [zip_paths_arr]
    orthanc_url = "http://localhost:8042"

    for zip_file_path in zip_paths_arr:
        print(f"Uploading ZIP file: {zip_file_path}")
        # Read the ZIP file in binary mode
        with open(zip_file_path, 'rb') as f:
            zip_data = f.read()

        # Upload the ZIP file
        orthanc_url_with_instances = orthanc_url.rstrip('/') + '/instances'
        response = requests.post(orthanc_url_with_instances, data=zip_data, headers={'Content-Type': 'application/zip'})
        response.raise_for_status()
        print(f"Uploaded ZIP file: {zip_file_path}")

    # Anonymization begins here

    print("Fetching list of new uploaded studies for anonymization...")
    csv_file_path = 'Orthanc_uploaded_StudyID.csv'
    uploaded_list = []
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                uploaded_list.append(row['Uploaded'])
    
    new_studies_list = requests.get(f"{orthanc_url}/studies").json()
    new_studies = list(set(new_studies_list) - set(uploaded_list))
    
    print(f"Anonymizing {len(new_studies)} new studies...")
    anonymize_response = requests.post(
        f"{orthanc_url}/tools/bulk-anonymize",
        json={"Resources": new_studies}
    )
    anonymize_response.raise_for_status()
    print("Anonymization complete.")

    # Delete original studies from Orthanc PACS
    print("Deleting original studies from Orthanc PACS...")
    for study_id in new_studies:
        study_delete_url = f'{orthanc_url}/studies/{study_id}'
        delete_response = requests.delete(study_delete_url)
        delete_response.raise_for_status()
    print("Original studies deleted.")

    all_studies = requests.get(f"{orthanc_url}/studies").json()
    new_studies = list(set(all_studies) - set(uploaded_list))

    print("Updating the CSV file with uploaded studies...")
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
    print("CSV file updated with uploaded studies.")


if __name__ == "__main__":
    zip_paths_arr = r"Temp_Downloads/1.3.6.1.4.1.5962.1.1.0.0.0.1194732126.13032.0.1.zip"
    upload_zip_file(zip_paths_arr)
