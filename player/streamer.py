import ffmpeg
from settings import settings


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
                settings.server.rtmp_host,
                preset=settings.music.preset,
                acodec=settings.music.audio_codec,
                audio_bitrate=settings.music.audio_bitrate,
                ar=settings.music.sample_frequency,
                threads=settings.music.threads,
                format=settings.music.format,
            )
            .run_async(pipe_stdout=True)
        )


#: instance of Stream for use in other modules
stream = Stream()
