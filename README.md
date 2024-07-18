# dcm4chee to Orthanc Study Transfer

## Overview
This repository contains Python code to transfer anonymized medical studies from dcm4chee to Orthanc PACS. The process involves downloading studies from dcm4chee, pushing them to Orthanc PACS, anonymizing them, and then transferring the anonymized studies to another destination Orthanc PACS.
`main.py` will check if any new studies have been uploaded on dcm4chee, if yes then anonymize it and send to destination PACS
Create a cron job that runs `python main.py` at regular intervals (hopefully when dcm4chee has minimal activity so that no errors are encountered during uploading process)

## Requirements
To run this code, ensure the following prerequisites are met:
1. Python is installed on your system.
2. An Orthanc PACS is set up and accessible.
3. The `requests` library is installed in your Python environment.
4. A Cron job is set up to execute `python main.py` at specified intervals.

(cron job has not been created yet)

## Usage
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd <repository-name>
   ```
   
2. **Modify Configuration:**
   Update the initial parameters in the `main` function of `main.py` according to your setup and requirements.

3. **Run the Script:**
   Execute the script either manually or through the Cron job:
   ```
   python main.py
   ```

## Workflow
1. **Download Studies from dcm4chee:** Initially, non-anonymized studies are downloaded from dcm4chee.
   
2. **Push to Orthanc PACS:** The downloaded studies are then pushed to the Orthanc PACS set up at the hospital.

3. **Anonymize Studies:** The studies are anonymized within the Orthanc PACS.

4. **Delete Downloaded Studies:** The original studies downloaded from dcm4chee are deleted from the server.

5. **Transfer to Destination Orthanc:** Finally, the anonymized studies are transferred from the hospital's Orthanc PACS to the destination Orthanc PACS.

## Notes
- This project aims to keep the use of external libraries to a minimum, with `requests` being the only dependency.
- Ensure proper configuration and access permissions are set up on both dcm4chee and Orthanc PACS for smooth operation.

---
