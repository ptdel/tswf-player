from loop import player
from route import app
from bottle import run
from settings import settings


if __name__ == "__main__":
    """ the application entry-point. """
    player.start()
    run(app, host=settings.server.host, port=settings.server.port)
    player.join()
