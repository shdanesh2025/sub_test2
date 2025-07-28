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
        'subtitlesformat': 'srt',  # Set subtitle format to .srt
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

# List to keep track of all downloaded subtitles (.srt files)
all_srt_files = []
subtitles_mapping = []  # List to hold the mapping of subtitles to job_id

# User-defined suffix for the zip file name
suffix = "_batch1"  # Change this to whatever suffix you prefer

# Iterate over the jobs in the specified range
for job in jobs_data[start_index:end_index]:
    url = job["url"]
    job_id = job["job_id"]

    # Download subtitles
    if download_subtitles(url):
        # Collect the .srt files in the current directory
        srt_files = [f for f in os.listdir() if f.endswith('.srt')]
        all_srt_files.extend(srt_files)  # Add to the list of all downloaded subtitles
        
        # Add to subtitles mapping
        for srt_file in srt_files:
            subtitles_mapping.append({
                'job_id': job_id,
                'subtitle_file': srt_file
            })
    else:
        print(f"Skipping {url} due to download error.")

# If there are any .srt files, zip them into one file along with the JSON mapping
if all_srt_files:
    # Save the mapping to a JSON file
    mapping_filename = f"subtitles_mapping_{job_index}.json"
    with open(mapping_filename, 'w') as mapping_file:
        json.dump(subtitles_mapping, mapping_file, indent=4)
        print(f"Saved mapping to {mapping_filename}")
    
    # Add suffix to zip file name
    zip_filename = f"subtitles_{job_index}{suffix}.zip"
    zip_command = f"zip -r \"{zip_filename}\" " + " ".join([f"\"{file}\"" for file in all_srt_files] + [mapping_filename])
    os.system(zip_command + " || echo 'No subtitles to zip'")

    # Check if the zip was successful and upload it
    if os.path.exists(zip_filename):
        upload_to_mega(zip_filename)
    else:
        print(f"Zip file {zip_filename} does not exist. Skipping upload.")
else:
    print(f"No subtitles to zip or upload for job range {start_index+1} to {end_index}.")
