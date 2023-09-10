import os
import requests
from bs4 import BeautifulSoup

# Starting a session for requests
session = requests.Session()

# Specify the URL of the page containing transcript links
transcript_page_url = 'https://maximumfun.org/podcasts/my-brother-my-brother-and-me/?_post-type=transcript&_paged=1&_sort=date_desc'

# Get the current working directory
current_directory = os.getcwd()

# Specify the subfolder name where you want to save the downloads
subfolder_name = "MBMBAM Transcripts"

# Combine the current directory with the subfolder to create the full path
download_folder = os.path.join(current_directory, subfolder_name)

# Create the download folder
os.makedirs(download_folder, exist_ok=True)

# Defining an empty list of transcript pages
transcript_list = []

# Looping through all 31 pages and extracting all transcript page links
for page_number in range(1, 32):
    link = f'https://maximumfun.org/podcasts/my-brother-my-brother-and-me/?_post-type=transcript&_paged={page_number}&_sort=date_desc'
    page = session.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    transcripts = soup.select(".latest-panel-loop-item-title a")
    transcript_list.extend([transcript["href"] for transcript in transcripts])

# Defining an empty list of transcripts download links
download_links = []

# Looping through transcript page links
for transcript_url in transcript_list:
    transcript_page = session.get(transcript_url)
    download = BeautifulSoup(transcript_page.content, 'html.parser')
    download_link = download.select(".btn-transcript-download")

    # Check if download link(s) were found
    if download_link:
        download_links.extend([link["href"] for link in download_link])

# Loop through download links and download files
for download_url in enumerate(download_links):
    response = session.get(download_url, stream=True)
    filename = download_url.split("/")[-1]
    save_path = os.path.join(download_folder, filename)

    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
