import yt_dlp
import time
import json
import sys
from mega import Mega
import os

# Function to upload a file to Mega
def upload_to_mega(file_path):
    mega = Mega()
    m = mega.login(email='your_mega_email@example.com', password='your_mega_password')  # Use your Mega login credentials
    print(f"Uploading {file_path} to Mega...")
    file = m.upload(file_path)
    m.get_upload_link(file)  # Generate the public link
    print(f"Uploaded {file_path} to Mega. Link: {m.get_upload_link(file)}")

# Read job data from jobs.json
with open('jobs.json') as f:
    jobs_data = json.load(f)

# Extract job range (example: from job 1 to job 10)
job_index = int(sys.argv[1])  # Get job index from command-line argument
start_index = (job_index - 1) * 10
end_index = start_index + 10

for job in jobs_data[start_index:end_index]:
    url = job["url"]
    job_id = job["job_id"]
    
    # Define download options for yt-dlp
    options = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'skip_download': True,
        'outtmpl': '%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',
    }

    # Download subtitles
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        print(f"Successfully downloaded subtitles for {url}")
    except yt_dlp.utils.DownloadError as e:
        print(f"Download error for {url}: {str(e)}")  # Video unavailable or other download errors
    except yt_dlp.utils.ExtractorError as e:
        print(f"Extractor error for {url}: {str(e)}")  # Issues with extracting video info
    except Exception as e:
        print(f"An unexpected error occurred for {url}: {str(e)}")  # Other unexpected errors
    finally:
        # Pause before next download (optional)
        time.sleep(2)

    # Zip subtitles into a file
    zip_filename = f"subtitles{job_index}.zip"
    os.system(f"zip {zip_filename} *.vtt || echo 'No subtitles to zip'")

    # Upload to Mega
    upload_to_mega(zip_filename)
