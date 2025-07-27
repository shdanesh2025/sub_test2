from yt_dlp import YoutubeDL

url = 'https://www.youtube.com/watch?v=blEIcn8mRGg'

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
