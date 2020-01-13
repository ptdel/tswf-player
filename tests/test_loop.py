from player.loop import interrupted
import sys
import pytest
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock


base_directory = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(base_directory / "player"))

from loop import playloop


def test_playloop_calls_youtube_dl():
    fake_response = MagicMock(return_value=True, json=lambda: {"Next": "yes"})
    with (
        mock.patch("streamer.stream.process", return_value=None)
        and mock.patch("requests.get", return_value=fake_response)
    ):
        with mock.patch("ydl.ydl.download", return_value=None) as mocked_ydl:
            global interrupted
            playloop(interrupted=True)
            mocked_ydl.assert_called_once_with(["yes"])
