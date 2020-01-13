from time import sleep
import threading
from bottle import Bottle, run, request, HTTPResponse
from ydl import ydl
from requests import get
from player import stream  # type: ignore

#: bottle application
app = Bottle()


@app.route("/restart")
def restart():
    """ terminates the existing stream process, thereby skipping the currently
    playing song.  The request must be made by an authorized host.

    :param str client_ip: the remote address requesting a restart.
    :return: HTTP status indicating success/fail of restart request
    :rtype: HTTPResponse
    """
    client_ip = request.environ.get("REMOTE_ADDR")
    if client_ip != "127.0.0.1":
        return HTTPResponse(status=403)
    if stream.process is not None:
        stream.process.terminate()
        return HTTPResponse(status=200)


def playloop():
    """ A loop that runs forever.  This will attempt to grab a song from the
    tswf-api and download it.  Once it's downloaded the loop will call ffmpeg
    to play the song, waiting for it to finish before moving on.
    ``ydl.download`` will call the ``download_hook`` when it has completed,
    this hook is what actually calls the stream to play the song.
    """
    while True:
        if stream.process is None or stream.process.poll() is not None:
            next_song = get("http://127.0.0.1:8080/api/next", verify=False)
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


if __name__ == "__main__":
    """ the application entry-point. """
    player.start()
    run(app, host="localhost", port=8081)
    player.join()
