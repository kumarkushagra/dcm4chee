import pydicom

# Load the original and anonymized DICOM files
original_file_path = 'C:/Users/Admin/Desktop/testing/CT000000.dcm'
anonymized_file_path = 'C:/Users/Admin/Desktop/testing/CT000000.dcm_new_anon.dcm'

original_dicom = pydicom.dcmread(original_file_path)
anonymized_dicom = pydicom.dcmread(anonymized_file_path)

# Extract patient-related information from both files
original_patient_info = {
    'PatientName': original_dicom.get('PatientName', 'N/A'),
    'PatientID': original_dicom.get('PatientID', 'N/A'),
    'PatientBirthDate': original_dicom.get('PatientBirthDate', 'N/A'),
    'PatientSex': original_dicom.get('PatientSex', 'N/A')
}

anonymized_patient_info = {
    'PatientName': anonymized_dicom.get('PatientName', 'N/A'),
    'PatientID': anonymized_dicom.get('PatientID', 'N/A'),
    'PatientBirthDate': anonymized_dicom.get('PatientBirthDate', 'N/A'),
    'PatientSex': anonymized_dicom.get('PatientSex', 'N/A')
}

print("Original Patient Info:", original_patient_info)
print("Anonymized Patient Info:", anonymized_patient_info)
