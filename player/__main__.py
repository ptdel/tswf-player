from time import sleep
import threading
from bottle import Bottle, run, request, HTTPResponse
from ydl import ydl
from requests import get
from player import stream  # type: ignore


app = Bottle()


@app.route("/restart")
def restart():
    client_ip = request.environ.get("REMOTE_ADDR")
    if client_ip != "127.0.0.1":
        return HTTPResponse(status=403)
    if stream.process is not None:
        stream.process.terminate()
        return HTTPResponse(status=200)


def playloop():
    while True:
        if stream.process is None or stream.process.poll() is not None:
            next_song = get("https://127.0.0.1/api/next", verify=False)
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
    player.start()
    run(app, host="localhost", port=8081)
    player.join()
