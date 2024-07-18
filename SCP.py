import requests

# Modify code to compare what all studies have been sent (store this data in a csv)
def pacs_to_pacs_transfer(source_url, destination_url):

    # Get the list of studies from the source Orthanc
    response = requests.get(f"{source_url}/studies")
    studies = response.json()
    for study in studies:
        # Download the study as a ZIP file and stream it directly to the destination
        archive_url = f"{source_url}/studies/{study}/archive"
        with requests.get(archive_url, stream=True) as r:
            # Stream the downloaded ZIP file directly to the destination Orthanc
            upload_response = requests.post(
                f"{destination_url}/instances",
                headers={"Content-Type": "application/zip"},
                data=r.iter_content(chunk_size=8192)  # 8192 bytes (8 kb)
                # if memory is the constraint, reduce this number 
            )


if __name__ == "__main__":
    source_url = "http://localhost:8042"
    destination_url = "http://localhost:1111"
    pacs_to_pacs_transfer(source_url, destination_url)
    