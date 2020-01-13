from streamer import stream  # type: ignore


def download_hook(data, stream=stream):
    """ The action to take when youtube_dl finishes downloading a song.

    :param dict data: Dowload information emitted by YoutubeDL
    :param object stream: player instance
    :return: side-effect of playing the downloaded song.
    :rtype: None
    """
    if data["status"] == "finished":
        stream.stream_song(data["filename"])
