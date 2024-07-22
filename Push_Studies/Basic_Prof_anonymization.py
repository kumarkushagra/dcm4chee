import pydicom
from pydicom.dataset import Dataset, FileDataset
from tags import get_tags

def anonymize_dicom(dicom_file_path):
    tags_dict = get_tags()
    ds = pydicom.dcmread(dicom_file_path)
    
    for tag, attributes in tags_dict.items():
        if tag in ds:
            if 'Z' in attributes[0]:
                ds[tag].value = ''  # Clear the value
            elif 'D' in attributes[0]:
                del ds[tag]  # Delete the tag
            elif 'X' in attributes[0]:
                ds[tag].value = ''  # Replace with a dummy date
            # elif 'U' in attributes:
            #     ds[tag].value = 'dummy'  # Replace with a dummy UID
    dicom_file_path=f"{dicom_file_path}_new_anon.dcm"
    ds.save_as(dicom_file_path)
    print(f"Anonymized DICOM file saved as {dicom_file_path}")

# Example usage
input_file = r'C:\Users\Admin\Desktop\testing\CT000000.dcm'
anonymize_dicom(input_file)
