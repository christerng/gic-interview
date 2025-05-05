from src._types import Seat, Movie, ScrollingScreen
from src._constants import (
    SCREEN_DEFAULT_SPACING,
    MOVIE_MAX_COLS,
    MOVIE_MIN_ROWS,
    MOVIE_MIN_COLS,
    MOVIE_MAX_ROWS,
)
from unittest.mock import Mock
import pytest


@pytest.fixture
def seat():
    return Seat()


class TestSeat:
    def test_init(self, seat):
        assert seat.is_booked is False
        assert seat.get_chr("some_booking_id") == "."

    def test_book(self, seat):
        seat.book("some_booking_id")
        assert seat.is_booked is True
        assert seat.get_chr("some_booking_id") == "o"
        assert seat.get_chr("other_booking_id") == "#"

    def test_unbook(self, seat):
        seat.book("some_booking_id")
        assert seat.is_booked is True
        assert seat.get_chr("some_booking_id") == "o"

        seat.unbook()
        assert seat.is_booked is False
        assert seat.get_chr("some_booking_id") == "."


@pytest.fixture
def min_movie():
    return Movie("min_title", MOVIE_MIN_ROWS, MOVIE_MIN_COLS)


@pytest.fixture
def max_movie():
    return Movie("max_title", MOVIE_MAX_ROWS, MOVIE_MAX_COLS)


class TestMovie:
    def test_init(self, min_movie, max_movie):
        assert min_movie.title == "min_title"
        assert min_movie.seats_unbooked() == MOVIE_MIN_ROWS * MOVIE_MIN_COLS

        assert max_movie.title == "max_title"
        assert max_movie.seats_unbooked() == MOVIE_MAX_ROWS * MOVIE_MAX_COLS

    def test_from_user_input_valid(self):
        min_movie = Movie.from_user_input(
            f"some_title {MOVIE_MIN_ROWS} {MOVIE_MIN_COLS}"
        )
        assert min_movie.title == "some_title"
        assert min_movie.seats_unbooked() == MOVIE_MIN_ROWS * MOVIE_MIN_COLS

        max_movie = Movie.from_user_input(
            f"some_title {MOVIE_MAX_ROWS} {MOVIE_MAX_COLS}"
        )
        assert max_movie.title == "some_title"
        assert max_movie.seats_unbooked() == MOVIE_MAX_ROWS * MOVIE_MAX_COLS

    def test_from_user_input_invalid(self):
        with pytest.raises(ValueError):
            Movie.from_user_input("")
        with pytest.raises(ValueError):
            Movie.from_user_input(f"some_title some_non_decimal {MOVIE_MIN_COLS}")
        with pytest.raises(ValueError):
            Movie.from_user_input(f"some_title {MOVIE_MIN_ROWS} some_non_decimal")
        with pytest.raises(ValueError):
            Movie.from_user_input(f"some_title {MOVIE_MIN_ROWS - 1} {MOVIE_MIN_COLS}")
        with pytest.raises(ValueError):
            Movie.from_user_input(f"some_title {MOVIE_MAX_ROWS + 1} {MOVIE_MIN_COLS}")
        with pytest.raises(ValueError):
            Movie.from_user_input(f"some_title {MOVIE_MIN_ROWS} {MOVIE_MIN_COLS - 1}")
        with pytest.raises(ValueError):
            Movie.from_user_input(f"some_title {MOVIE_MIN_ROWS} {MOVIE_MAX_COLS + 1}")

    def test_book_one(self, min_movie, max_movie):
        min_booking_id = min_movie.book(1)
        assert min_movie.seats_unbooked() == MOVIE_MIN_ROWS * MOVIE_MIN_COLS - 1
        assert min_booking_id == "GIC0001"

        max_booking_id = max_movie.book(1)
        assert max_movie.seats_unbooked() == MOVIE_MAX_ROWS * MOVIE_MAX_COLS - 1
        assert max_booking_id == "GIC0001"

    def test_book_multiple(self, max_movie):
        max_booking_id = max_movie.book(50)
        assert max_movie.seats_unbooked() == MOVIE_MAX_ROWS * MOVIE_MAX_COLS - 50
        assert max_booking_id == "GIC0001"

    def test_get_map_min(
        self,
        min_movie,
    ):
        assert (
            min_movie.get_map("")
            == """Booking id: 
Selected seats:

   S   C   R   E   E   N   
---------------------------
A   .
    1  """
        )
        booking_id = min_movie.book(1)
        assert (
            min_movie.get_map(booking_id)
            == f"""Booking id: {booking_id}
Selected seats:

   S   C   R   E   E   N   
---------------------------
A   o
    1  """
        )
        assert (
            min_movie.get_map("some_booking_id")
            == """Booking id: some_booking_id
Selected seats:

   S   C   R   E   E   N   
---------------------------
A   #
    1  """
        )

    def test_get_map_max(self, max_movie):
        assert (
            max_movie.get_map("")
            == """Booking id: 
Selected seats:

                                                                                         S   C   R   E   E   N                                                                                          
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Z   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
Y   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
W   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
V   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
U   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
T   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
S   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
R   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
Q   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
P   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
O   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
N   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
M   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
L   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
K   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
J   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
I   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
H   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
G   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
F   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
E   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
D   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
C   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
B   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
A   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .
    1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50"""
        )

    def test_unbook_existent(self, min_movie, max_movie):
        booking_id = min_movie.book(1)
        assert min_movie.seats_unbooked() == MOVIE_MIN_ROWS * MOVIE_MIN_COLS - 1
        min_movie.unbook(booking_id)
        assert min_movie.seats_unbooked() == MOVIE_MIN_ROWS * MOVIE_MIN_COLS

        booking_id = max_movie.book(1)
        assert max_movie.seats_unbooked() == MOVIE_MAX_ROWS * MOVIE_MAX_COLS - 1
        max_movie.unbook(booking_id)
        assert max_movie.seats_unbooked() == MOVIE_MAX_ROWS * MOVIE_MAX_COLS

    def test_unbook_nonexistent(self, min_movie, max_movie):
        min_movie.book(1)
        assert min_movie.seats_unbooked() == MOVIE_MIN_ROWS * MOVIE_MIN_COLS - 1
        min_movie.unbook("some_booking_id")
        assert min_movie.seats_unbooked() == MOVIE_MIN_ROWS * MOVIE_MIN_COLS - 1

        max_movie.book(1)
        assert max_movie.seats_unbooked() == MOVIE_MAX_ROWS * MOVIE_MAX_COLS - 1
        max_movie.unbook("some_booking_id")
        assert max_movie.seats_unbooked() == MOVIE_MAX_ROWS * MOVIE_MAX_COLS - 1


class TestScrollingScreen:
    def test_addstr(self):
        stdscn = Mock()
        stdscn.getyx = Mock(return_value=(0, 0))

        screen = ScrollingScreen(stdscn)
        screen.addstr("str")

        stdscn.getyx.assert_called_once()
        stdscn.addstr.assert_called_once_with(0 + SCREEN_DEFAULT_SPACING, 0, "str")
