import os
from yt_dlp import YoutubeDL

url = 'https://www.youtube.com/watch?v=blEIcn8mRGg'

with open("cookies.txt", "w", encoding="utf-8") as f:
    f.write(os.environ["YOUTUBE_COOKIES"])

options = {
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'skip_download': True,
    'outtmpl': '%(title)s.%(ext)s',
    'cookiefile': 'cookies.txt',
}

with YoutubeDL(options) as ydl:
    ydl.download([url])
