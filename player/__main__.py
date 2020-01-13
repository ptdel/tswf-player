from loop import player
from route import app
from bottle import run


if __name__ == "__main__":
    """ the application entry-point. """
    player.start()
    run(app, host="localhost", port=8081)
    player.join()
