from __future__ import unicode_literals
from config import ydl_opts
import youtube_dl

#: instance of youtube_dl python client.
ydl = youtube_dl.YoutubeDL(ydl_opts)
