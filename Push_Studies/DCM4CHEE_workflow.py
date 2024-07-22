import os

def find_dicom_files(directory):
    dicom_files = []
    
    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            # Check if the file is a DICOM file based on extension or content (if needed)
            if filename.endswith('.dcm'):  # Adjust the condition if DICOM files have different extensions
                file_path = os.path.join(dirpath, filename)
                file_path = file_path.replace('\\', '/')  # Replace backslashes with forward slashes
                dicom_files.append(file_path)
                # If you need to check DICOM file content, you can add additional checks here

    return dicom_files


# Pass the list through anonymize function



if __name__=="__main__":
    directory_path = r"C:/Users/Admin/Desktop/DICOM/"
    dicom_files_list = find_dicom_files(directory_path)

    for file_path in dicom_files_list:
        print(file_path)