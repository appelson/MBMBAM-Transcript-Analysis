import os
import requests
from bs4 import BeautifulSoup

def transcript_links(podcast, page_start, page_end):
    session = requests.Session()
    
    # Determine the base URL based on the podcast name
    if podcast == "My Brother, My Brother, and Me":
        base_url = 'https://maximumfun.org/podcasts/my-brother-my-brother-and-me/?_post-type=transcript&_paged={}&_sort=date_desc'
    elif podcast == "The Adventure Zone":
        base_url = "https://maximumfun.org/podcasts/adventure-zone/?_post-type=transcript&_paged={}&_sort=date_desc"
    elif podcast == "Wonderful!":
        base_url = "https://maximumfun.org/podcasts/wonderful/?_post-type=transcript&_paged={}&_sort=date_desc"
    else:
        raise ValueError("Unknown podcast name")

    # List to store all transcript links
    transcript_list = []

    # Loop through pages to get transcript links
    for page_number in range(page_start, page_end + 1):
        link = base_url.format(page_number)
        page = session.get(link)

        if page.status_code != 200:
            print(f"Failed to retrieve page {page_number}. Skipping...")
            continue

        soup = BeautifulSoup(page.content, 'html.parser')
        transcripts = soup.select(".latest-panel-loop-item-title a")

        # Extract href attribute for each transcript link
        transcript_list.extend([transcript["href"] for transcript in transcripts if "href" in transcript.attrs])

    # List to store download links
    download_links = []

    # Loop through transcript links to get download links
    for transcript_url in transcript_list:
        transcript_page = session.get(transcript_url)

        if transcript_page.status_code != 200:
            print(f"Failed to retrieve transcript page {transcript_url}. Skipping...")
            continue

        download = BeautifulSoup(transcript_page.content, 'html.parser')
        download_link = download.select(".btn-transcript-download")

        if download_link:
            download_links.extend([link["href"] for link in download_link if "href" in link.attrs])

    return download_links


def download_transcripts(podcast, page_start, page_end):
    # Get the list of download links
    download_links = transcript_links(podcast, page_start, page_end)
    
    # Set up folder for downloading transcripts
    current_directory = os.getcwd()
    subfolder_name = podcast + " Transcripts"
    download_folder = os.path.join(current_directory, subfolder_name)
    os.makedirs(download_folder, exist_ok=True)

    # Loop through download links and download the transcripts
    for download_url in download_links:
        try:
            response = requests.get(download_url, stream=True)
            filename = download_url.split("/")[-1]
            save_path = os.path.join(download_folder, filename)

            # Only download if the file doesn't already exist
            if not os.path.exists(save_path):
                with open(save_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)

                print(f"Downloaded: {filename}")
            else:
                print(f"File {filename} already exists, skipping download.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {download_url}: {e}")
            
            
download_transcripts("Wonderful!",1,28)
