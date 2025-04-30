import main
from unittest.mock import Mock
import pytest


def test_handle_admin():
    screen = Mock()
    screen.getstr = Mock(return_value="title 1 1")
    movie = main.handle_admin(screen)
    assert movie.title == "title"
    assert movie.seats_unbooked() == 1


def test_exit():
    with pytest.raises(SystemExit) as e:
        main._exit(Mock())
    assert e.type is SystemExit
    assert e.value.code is None
