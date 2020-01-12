from log import Logger
from hooks import download_hook

#: YoutubeDL options.
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "/songs/%(title)s.%(ext)s",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        },
        {"key": "FFmpegMetadata"},
        {"key": "XAttrMetadata"},
    ],
    "logger": Logger(),
    "progress_hooks": [download_hook],
}
