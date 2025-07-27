# download_sub.py
from yt_dlp import YoutubeDL

url = 'https://www.youtube.com/watch?app=desktop&v=blEIcn8mRGg'

options = {
    'writesubtitles': True,
    'writeautomaticsub': True,  # fallback to auto subs if no manual ones
    'subtitleslangs': ['en'],   # change to ['all'] or other language codes if needed
    'skip_download': True,      # we only want subtitles
    'outtmpl': '%(title)s.%(ext)s',
}

with YoutubeDL(options) as ydl:
    ydl.download([url])
