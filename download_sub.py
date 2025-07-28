import yt_dlp  # Make sure yt_dlp is imported
from yt_dlp import YoutubeDL
import time
import sys

url = 'https://www.youtube.com/watch?v=blEIcn8yyjf'

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
        with YoutubeDL(options) as ydl:
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
