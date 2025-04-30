from src._types import Seat, Movie, ScrollingScreen
from src._constants import SCREEN_DEFAULT_SPACING
from unittest.mock import Mock


class TestSeat:
    def test_get_chr(self):
        seat = Seat()
        assert seat.get_chr("") == "."

        seat = Seat()
        seat.book("some_booking_id")
        assert seat.get_chr("some_booking_id") == "o"

        seat = Seat()
        seat.book("some_booking_id")
        assert seat.get_chr("other_booking_id") == "#"


class TestMovie:
    def test_book(self):
        movie = Movie("", 1, 1)
        movie.book(1)
        assert movie.seats_unbooked() == 0

    def test_unbook(self):
        movie = Movie("", 1, 1)
        booking_id = movie.book(1)
        movie.unbook(booking_id)
        assert movie.seats_unbooked() == 1

    def test_get_map(self):
        movie = Movie("", 1, 1)
        assert (
            movie.get_map("")
            == """Booking id: 
Selected seats:

   S   C   R   E   E   N   
---------------------------
A   .
    1"""
        )


class TestScrollingScreen:
    def test_addstr(self):
        stdscn = Mock()
        stdscn.getyx = Mock(return_value=(0, 0))

        screen = ScrollingScreen(stdscn)
        screen.addstr("str")

        stdscn.getyx.assert_called_once()
        stdscn.addstr.assert_called_once_with(0 + SCREEN_DEFAULT_SPACING, 0, "str")
