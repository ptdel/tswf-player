import requests
import threading
from pathlib import Path
from random import choice
from signal import signal, SIGINT
from streamer import stream  # type: ignore
from ydl import ydl
from settings import settings


def exit_signal(signal, frame):
    """ Handler function used to exit the playloop. """
    global interrupted
    interrupted = True


#: Registered exit_handler
signal(SIGINT, exit_signal)


#: Default loop state
interrupted = False


#: Path to the music file directory
music_directory = Path(settings.music.directory).glob("**/*")
music_files = [file_ for file_ in music_directory if file_.is_file()]  # heh


def playloop(interrupted=interrupted):
    """ A loop that runs forever.  This will attempt to grab a song from the
    tswf-api and download it.  Once it's downloaded the loop will call ffmpeg
    to play the song, waiting for it to finish before moving on.
    ``ydl.download`` will call the ``download_hook`` when it has completed,
    this hook is what actually calls the stream to play the song.
    """
    while True:
        if stream.process is None or stream.process.poll() is not None:
            next_song = requests.get(settings.server.call_next, verify=False).json()
            if "Next" in next_song:
                try:
                    ydl.download([next_song["Next"]])
                except Exception as e:
                    print(e)
            else:
                stream.stream_song(choice(music_files))

        if interrupted:
            break  # check for interruption at the end for testing purposes.


player = threading.Thread(name="player", target=playloop)
