import os
import requests

def upload_zip_file(zip_paths_arr):
    if type(zip_paths_arr) != list:
        zip_paths_arr = [zip_paths_arr]
    orthanc_url = "http://localhost:8042"

    for zip_file_path in zip_paths_arr:
        # Read the ZIP file in binary mode
        with open(zip_file_path, 'rb') as f:
            zip_data = f.read()

        # Upload the ZIP file
        orthanc_url_with_instances = orthanc_url.rstrip('/') + '/instances'
        response = requests.post(orthanc_url_with_instances, data=zip_data, headers={'Content-Type': 'application/zip'})
        response.raise_for_status()

def upload_all_zip_files_in_directory(directory_path):
    # Get a list of all zip files in the directory
    zip_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.zip')]
    
    # Upload each zip file
    if zip_files:
        upload_zip_file(zip_files)
        print(f"Uploaded {len(zip_files)} zip files.")
    else:
        print("No zip files found in the directory.")

# Example usage
if __name__=="__main__":
    upload_all_zip_files_in_directory()