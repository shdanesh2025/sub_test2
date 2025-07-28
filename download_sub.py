import yt_dlp
import time
import json
import sys
import os
from mega import Mega

# Function to upload a file to Mega
def upload_to_mega(file_path):
    mega = Mega()
    m = mega.login(email='shdanesh2025@gmail.com', password='1234qweR@!#$GH')  # Use your Mega login credentials
    print(f"Uploading {file_path} to Mega...")
    try:
        file = m.upload(file_path)
        link = m.get_upload_link(file)  # Generate the public link
        print(f"Uploaded {file_path} to Mega. Link: {link}")
    except Exception as e:
        print(f"Failed to upload {file_path} to Mega. Error: {str(e)}")

# Function to download subtitles with retries for rate limiting
def download_subtitles(url, retries=3):
    options = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'skip_download': True,
        'outtmpl': '%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',
    }

    for attempt in range(retries):
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
            print(f"Successfully downloaded subtitles for {url}")
            return True
        except yt_dlp.utils.DownloadError as e:
            print(f"Download error for {url}: {str(e)}")
            time.sleep(5)  # wait before retrying
        except yt_dlp.utils.ExtractorError as e:
            print(f"Extractor error for {url}: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error occurred for {url}: {str(e)}")
            return False

    # Even after retries, we don't fail, just log and continue
    print(f"Failed to download subtitles for {url} after {retries} attempts, skipping upload.")
    return False

# Read job data from jobs.json
with open('jobs.json') as f:
    jobs_data = json.load(f)

# Extract job range (example: from job 1 to job 10)
job_index = int(sys.argv[1])  # Get job index from command-line argument
start_index = (job_index - 1) * 10
end_index = start_index + 10

# List to keep track of all downloaded subtitles (.vtt files)
all_vtt_files = []

# Iterate over the jobs in the specified range
for job in jobs_data[start_index:end_index]:
    url = job["url"]
    job_id = job["job_id"]

    # Download subtitles
    if download_subtitles(url):
        # Collect the .vtt files in the current directory
        vtt_files = [f for f in os.listdir() if f.endswith('.vtt')]
        all_vtt_files.extend(vtt_files)  # Add to the list of all downloaded subtitles
    else:
        print(f"Skipping {url} due to download error.")

# If there are any .vtt files, zip them into one file
if all_vtt_files:
    zip_filename = f"subtitles{job_index}.zip"
    os.system(f"zip {zip_filename} {' '.join(all_vtt_files)} || echo 'No subtitles to zip'")

    # Upload to Mega
    upload_to_mega(zip_filename)
else:
    print(f"No subtitles to zip or upload for job range {start_index+1} to {end_index}.")
