# import requests

# # Define the Orthanc URL and the studies to anonymize
# orthanc_url = "http://localhost:8042"
# new_studies = ["1971163a-26b23f46-66a62f33-229e6a17-9fddfee0"]

# # Create the payload for the POST request
# payload = {
#     "Resources": new_studies,
#     # "Keep": ["SOPInstanceUID", "SOPClassUID"],
#     # "Force": True
# }

# # Perform the POST request to the bulk-anonymize tool
# try:
#     anonymize_response = requests.post(
#         f"{orthanc_url}/tools/bulk-anonymize",
#         json=payload
#     )
#     anonymize_response.raise_for_status()  # Raise an error for bad responses
#     print("Anonymization successful!")
# except requests.exceptions.RequestException as e:
#     print(f"An error occurred: {e}")
#     if e.response is not None:
#         print("Response content:", e.response.content)


import requests

# Define the Orthanc URL and the studies to anonymize
orthanc_url = "http://localhost:8042"
new_studies = ["1971163a-26b23f46-66a62f33-229e6a17-9fddfee0"]

# Create the payload for the POST request
payload = {
    "Resources": new_studies,
    "Keep": [
        "PatientID"
    ],
    "Force": True
}

# Perform the POST request to the bulk-anonymize tool
try:
    anonymize_response = requests.post(
        f"{orthanc_url}/tools/bulk-anonymize",
        json=payload
    )
    anonymize_response.raise_for_status()  # Raise an error for bad responses
    print("Anonymization successful!")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    if e.response is not None:
        print("Response content:", e.response.content)










