import sys
import pytest
from pathlib import Path
from boddle import boddle
from bottle import HTTPResponse, request
from unittest import mock

base_directory = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(base_directory / "player"))

from route import restart


def test_restart_route_forbidden():
    with boddle():
        f = restart()
        assert type(f) == HTTPResponse
        assert f.status_code == 403


def test_restart_route_allowed():
    with mock.patch("streamer.stream.process", return_value=True):
        with boddle():
            request.environ["REMOTE_ADDR"] = "127.0.0.1"
            f = restart()
            assert request.environ.get("REMOTE_ADDR") == "127.0.0.1"
            assert type(f) == HTTPResponse
            assert f.status_code == 200
