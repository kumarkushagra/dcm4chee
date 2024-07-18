# dcm4chee to Orthanc Study Transfer

### Overview
This repository features Python code for transferring anonymized medical studies from dcm4chee to Orthanc PACS. The process involves:
- Downloading studies from dcm4chee
- Pushing them to Orthanc PACS
- Anonymizing the data
- Transferring anonymized studies to another Orthanc PACS instance.

### Functionality
The `main.py` script:
- Monitors dcm4chee for new study uploads
- Anonymizes and sends new studies to the destination PACS.

### Deployment

Modify `cronjob file` such that the path for `python {ACTUAL PATH OF}/main.py` is correct and modify timings if reqquired (timings have been set to -3AM -everyday).
(Cron job has not been tested)

---
## Requirements
To run this code, ensure the following prerequisites are met:
1. Python is installed on your system.
2. An Orthanc PACS is set up and accessible.
3. The `requests` library is installed in your Python environment.
4. A Cron job is set up to execute `python main.py` at 3AM everyday.

## Usage
1. **Clone the repository:**
   ```
   git clone https://github.com/kumarkushagra/dcm4chee.git
   cd <path where you want to clone this repo>
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
