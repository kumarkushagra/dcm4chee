import os
from pydicom import dcmread
from pynetdicom import AE, StoragePresentationContexts

def upload_dicom_files(directory_path, ae_title, server_ip, server_port):
    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"Directory not found: {directory_path}")
        return

    # Initialize the Application Entity
    ae = AE()

    # Add the supported presentation contexts (for storage services)
    ae.requested_contexts = StoragePresentationContexts

    # Create association with the remote AE
    assoc = ae.associate(server_ip, server_port, ae_title=ae_title)

    if assoc.is_established:
        print("Association established with the server.")

        # Iterate over each file in the directory
        for file_name in os.listdir(directory_path):
            if file_name.endswith('.dcm'):
                file_path = os.path.join(directory_path, file_name)
                try:
                    # Read the DICOM file
                    ds = dcmread(file_path)

                    # Send the DICOM file
                    status = assoc.send_c_store(ds)

                    # Check the status of the C-STORE operation
                    if status:
                        print(f"Successfully uploaded: {file_name}")
                    else:
                        print(f"Failed to upload {file_name}. Status: {status}")
                except Exception as e:
                    print(f"Error uploading {file_name}: {e}")
        
        # Release the association
        assoc.release()
        print("Association released.")
    else:
        print("Failed to establish association with the server.")

# Example usage
directory = r"C:\Users\Admin\Desktop\delete asap"
ae_title = "DCM4CHEE"
server_ip = "13.235.102.234"
server_port = 11112

upload_dicom_files(directory, ae_title, server_ip, server_port)
