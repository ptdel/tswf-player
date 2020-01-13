from bottle import Bottle, request, HTTPResponse
from streamer import stream  # type: ignore
from settings import settings

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
    if client_ip != settings.restart.allowed_host:
        return HTTPResponse(status=403)
    if stream.process is not None:
        stream.process.terminate()
        return HTTPResponse(status=200)
