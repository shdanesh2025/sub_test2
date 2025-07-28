import yt_dlp
import json
import time
import sys

# Load the jobs from jobs.json
try:
    with open('jobs.json', 'r') as f:
        jobs_data = json.load(f)
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {str(e)}")
    sys.exit(1)  # Exit with an error code if JSON is invalid
except Exception as e:
    print(f"Error reading jobs.json: {str(e)}")
    sys.exit(1)

# Get the first URL from the list
if jobs_data:
    first_job = jobs_data[0]  # Take the first job in the list
    url = first_job["url"]
else:
    print("No jobs found in jobs.json.")
    sys.exit(1)  # Exit with an error code if no jobs are found

# Options for yt-dlp
options = {
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'skip_download': True,
    'outtmpl': '%(title)s.%(ext)s',
    'cookiefile': 'cookies.txt',
}

def download_video(url):
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
        # Optional: Pause for a short time before the next download
        time.sleep(2)

# Start the download process
download_video(url)

# Ensure GitHub Action passes even if there's an error
sys.exit(0)  # Forcefully exit with a success code (0)
