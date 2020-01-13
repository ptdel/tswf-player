import ffmpeg


class Stream:
    """ A Class which threads instances of ffmpeg to play songs.
    The Stream outputs the song to an rtmp endpoint.
    """

    def __init__(self):
        self.process = None

    def stream_song(self, song):
        """ Replace the existing process with an async call to
        play a song with ffmpeg.

        :param str song: a url provided by the tswf-api
        :return: side-effect of playing song
        :rtype: None
        """
        self.process = (
            ffmpeg.input(song, re=None, vn=None)
            .output(
                "rtmp://127.0.0.1:1935/tswf",
                preset="fast",
                acodec="aac",
                audio_bitrate="192k",
                ar=44100,
                threads=0,
                format="flv",
            )
            .run_async(pipe_stdout=True)
        )


#: instance of Stream for use in other modules
stream = Stream()
