import requests
import threading
from time import sleep
from streamer import stream  # type: ignore
from ydl import ydl


def playloop():
    """ A loop that runs forever.  This will attempt to grab a song from the
    tswf-api and download it.  Once it's downloaded the loop will call ffmpeg
    to play the song, waiting for it to finish before moving on.
    ``ydl.download`` will call the ``download_hook`` when it has completed,
    this hook is what actually calls the stream to play the song.
    """
    while True:
        if stream.process is None or stream.process.poll() is not None:
            next_song = requests.get("https://127.0.0.1/api/next", verify=False)
            if "Next" in next_song.json():
                try:
                    ydl.download([next_song.json()["Next"]])
                except Exception as e:
                    print("Error downloading : ", next_song.json())
                    raise e
            else:
                print("no songs")

        sleep(5)


player = threading.Thread(name="player", target=playloop)
