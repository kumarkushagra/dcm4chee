import os
import zipfile
import tempfile
import shutil

def anonymize_zip(zip_path, anonymize_func, output_zip_path):
    """
    Anonymizes the contents of a zip file.

    Parameters:
    zip_path (str): Path to the input zip file.
    anonymize_func (function): Function that takes a file path and anonymizes its contents.
    output_zip_path (str): Path to the output anonymized zip file.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Step 1: Extract the contents of the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Step 2: Traverse through the directories and files
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Step 3: Anonymize the file contents
                anonymize_func(file_path)

        # Step 4: Create a new zip file with the anonymized data
        with zipfile.ZipFile(output_zip_path, 'w') as zip_out:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zip_out.write(file_path, arcname)

def example_anonymize_func(file_path):
    """
    An example anonymization function that overwrites the file with anonymized content.

    Parameters:
    file_path (str): Path to the file to be anonymized.
    """
    with open(file_path, 'r+') as file:
        content = file.read()
        # Perform anonymization (e.g., replace patient names or IDs)
        anonymized_content = content.replace('patient_name', 'anonymous')
        file.seek(0)
        file.write(anonymized_content)
        file.truncate()

# Usage
input_zip_path = 'path/to/your/input.zip'
output_zip_path = 'path/to/your/output_anonymized.zip'
anonymize_zip(input_zip_path, example_anonymize_func, output_zip_path)
