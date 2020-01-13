import requests
import threading
from signal import signal, SIGINT
from time import sleep
from streamer import stream  # type: ignore
from ydl import ydl


def exit_signal(signal, frame):
    """ Handler function used to exit the playloop. """
    global interrupted
    interrupted = True


#: Registered exit_handler
signal(SIGINT, exit_signal)


#: Default loop state
interrupted = False


def playloop(interrupted=interrupted):
    """ A loop that runs forever.  This will attempt to grab a song from the
    tswf-api and download it.  Once it's downloaded the loop will call ffmpeg
    to play the song, waiting for it to finish before moving on.
    ``ydl.download`` will call the ``download_hook`` when it has completed,
    this hook is what actually calls the stream to play the song.
    """
    while True:
        if stream.process is None or stream.process.poll() is not None:
            next_song = requests.get("http://127.0.0.1:8080/api/next", verify=False)
            ydl.download(
                [next_song.json()["Next"]]
            ) if "Next" in next_song.json() else sleep(5)
            if interrupted:
                break  # check for interruption at the end for testing purposes.


player = threading.Thread(name="player", target=playloop)
