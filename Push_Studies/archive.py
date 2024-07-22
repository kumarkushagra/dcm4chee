import shutil
import zipfile
import os

def zip_dir(dir_path):
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory not found: {dir_path}")
    zip_path = dir_path
    shutil.make_archive(zip_path, 'zip', dir_path)
    shutil.rmtree(dir_path)
    os.rename(f'{zip_path}.zip', f'{zip_path}.zip')

def unzip_zip_file(zip_path):
    """Extracts a zip file into a directory named after the zip file, deletes the original zip file, and returns the extraction path."""
    base_name = os.path.splitext(os.path.basename(zip_path))[0]  # Get the zip file name without extension
    extraction_path = os.path.join(os.path.dirname(zip_path), base_name)  # Create a directory path
    os.makedirs(extraction_path, exist_ok=True)  # Create the directory if it doesn't exist

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)
    
    os.remove(zip_path)
    return extraction_path


def unzip_directory(directory_path):
    """Extracts all zip files in the specified directory and deletes the original zip files."""
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.zip'):
            zip_path = os.path.join(directory_path, file_name)
            unzip_zip_file(zip_path)

if __name__=="__main__":
    print(unzip_zip_file(r"D:\PROJECT\dcm4chee\Temp_Downloads\1.2.276.0.7230010.3.1.2.1381411976.1178.1721028319.745316.zip"))