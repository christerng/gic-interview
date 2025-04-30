import curses
from typing import NewType, Optional, Self
from src._constants import (
    MOVIE_MIN_ROWS,
    MOVIE_MAX_ROWS,
    MOVIE_MIN_COLS,
    MOVIE_MAX_COLS,
    BOOKING_ID_PAD,
    BOOKING_MAP_MIN_WIDTH,
    BOOKING_MAP_COL_WIDTH,
    SCREEN_DEFAULT_SPACING,
)


BookingID = NewType("BookingID", str)
BookingMap = NewType("BookingMap", str)


class Seat:
    def __init__(self) -> Self:
        self._is_booked = False
        self._booking_id: Optional[BookingID] = None

    @property
    def is_booked(self) -> bool:
        return self._is_booked

    @property
    def booking_id(self) -> BookingID:
        return self._booking_id

    def book(self, booking_id: BookingID) -> None:
        self._is_booked = True
        self._booking_id = booking_id

    def unbook(self) -> None:
        self._is_booked = False
        self._booking_id = None

    def get_chr(self, booking_id: BookingID) -> str:
        """
        Returns a char based on whether the seat is booked and with which ID

        Parameters
            booking_id: BookingID
                The Booking ID to match with the seat's Booking ID
        Returns
            str
        """
        if self._is_booked and self._booking_id == booking_id:
            return "o"
        if self._is_booked:
            return "#"
        return "."


class Movie:
    def __init__(self, title: str, rows: int, cols: int):
        self._title = title
        self._seats = [[Seat() for _ in range(cols)] for _ in range(rows)]
        self._booking_id = 0

    @classmethod
    def from_user_input(cls, user_input: str) -> Self:
        """
        Returns a Movie object from user input

        Parameters
            user_input: str
                The user input to validate then initalize the Movie with
        Returns
            Movie
        """
        if len(split_input := user_input.split()) != 3:
            raise ValueError(
                "Invalid input format. Expected: [Title] [Row] [SeatsPerRow]."
            )
        title, rows, cols = split_input
        if not title:
            raise ValueError("Movie title cannot be empty.")
        if not rows.isdecimal() or not MOVIE_MIN_ROWS <= int(rows) <= MOVIE_MAX_ROWS:
            raise ValueError("Row number must be between 1 and 26.")
        if not cols.isdecimal() or not MOVIE_MIN_COLS <= int(cols) <= MOVIE_MAX_COLS:
            raise ValueError("Seats per row must be between 1 and 50.")
        return cls(title, int(rows), int(cols))

    @property
    def title(self) -> str:
        return self._title

    def seats_unbooked(self) -> int:
        return sum(1 for row in self._seats for seat in row if not seat.is_booked)

    def book(
        self,
        seats_to_book: int,
        row_index: Optional[int] = None,
        col_index: Optional[int] = None,
    ) -> BookingID:
        """
        Make a booking and return its Booking ID, following the following logic:

        If `row_index` and `col_index`,
            Fill from right of `(row_index, col_index)`.
            Then from middle of next row in row order.

        Else,
            Fill from middle of each row in row order.

        Parameters
            seats_to_book: int
                Number of seats to book
            row_index: Optional[int]
                Starting row index, if any
            col_index: Optional[int]
                Starting col index, if any
        Returns
            BookingID
        """
        if row_index is not None and col_index is not None:
            booking_id = f"GIC{str(self._booking_id).zfill(BOOKING_ID_PAD)}"

            # Fill from right
            for seat in self._seats[row_index][col_index:]:
                if seats_to_book <= 0:
                    return BookingID(booking_id)

                if seat.is_booked:
                    continue

                seat.book(booking_id)
                seats_to_book -= 1

            # Fill from middle from next row
            for row in self._seats[row_index + 1 :]:
                left_ptr = right_ptr = len(row) // 2
                left_ptr -= (
                    len(row) % 2 == 0
                )  # So left and right pointers are symmetric
                while left_ptr >= 0 and right_ptr < len(row):
                    if seats_to_book <= 0:
                        return BookingID(booking_id)
                    if not row[left_ptr].is_booked:
                        row[left_ptr].book(booking_id)
                        seats_to_book -= 1

                    if seats_to_book <= 0:
                        return BookingID(booking_id)
                    if not row[right_ptr].is_booked:
                        row[right_ptr].book(booking_id)
                        seats_to_book -= 1

                    left_ptr -= 1
                    right_ptr += 1

        else:
            self._booking_id += 1
            booking_id = f"GIC{str(self._booking_id).zfill(BOOKING_ID_PAD)}"

            # Fill from middle
            for row in self._seats:
                left_ptr = right_ptr = len(row) // 2
                left_ptr -= (
                    len(row) % 2 == 0
                )  # So left and right pointers are symmetric
                while left_ptr >= 0 and right_ptr < len(row):
                    if seats_to_book <= 0:
                        return BookingID(booking_id)
                    if not row[left_ptr].is_booked:
                        row[left_ptr].book(booking_id)
                        seats_to_book -= 1

                    if seats_to_book <= 0:
                        return BookingID(booking_id)
                    if not row[right_ptr].is_booked:
                        row[right_ptr].book(booking_id)
                        seats_to_book -= 1

                    left_ptr -= 1
                    right_ptr += 1

        return BookingID(booking_id)

    def unbook(self, booking_id: BookingID) -> None:
        """
        Unbooks seats with given Booking ID

        Parameters
            booking_id: BookingID
                The Booking ID to match against seat Booking ID
        Returns
            None
        """
        for row in self._seats:
            for seat in row:
                if seat.booking_id == booking_id:
                    seat.unbook()

    def get_map(self, booking_id: BookingID) -> BookingMap:
        """
        Constructs and returns a string representing a matrix of seats

        Parameters
            booking_id: BookingID
                The Booking ID to match against seat Booking ID
        Returns
            BookingMap
        """
        width = max(BOOKING_MAP_MIN_WIDTH, BOOKING_MAP_COL_WIDTH * len(self._seats[0]))

        booking_map = []
        booking_map.append(f"Booking id: {booking_id}")
        booking_map.append("Selected seats:\n")
        booking_map.append("S   C   R   E   E   N".center(width))
        booking_map.append("-" * width)
        for index, row in enumerate(reversed(self._seats)):
            booking_row = []
            booking_row.append(chr(ord("A") + len(self._seats) - 1 - index))
            for seat in row:
                booking_row.append(seat.get_chr(booking_id))
            booking_map.append("   ".join(booking_row))
        footer_row = []
        footer_row.append(" ")
        for i in range(len(self._seats[0])):
            footer_row.append(str(i + 1))
        booking_map.append("   ".join(footer_row))

        return "\n".join(booking_map)


class ScrollingScreen:
    def __init__(self, screen: curses.window) -> Self:
        self._screen = screen

        self._screen.clear()
        self._screen.scrollok(True)
        self._screen.idlok(True)

    def getstr(self) -> str:
        return self._screen.getstr().decode().strip()

    def getch(self) -> int:
        return self._screen.getch()

    def deleteln(self) -> None:
        self._screen.deleteln()

    def clear(self) -> None:
        self._screen.clear()

    def addstr(self, str: str, spacing: int = SCREEN_DEFAULT_SPACING) -> None:
        """
        Uses line-by-line scrolling instead of moving cursor out of bounds

        Parameters
            str: str
                The string to be printed
            spacing: int = SCREEN_DEFAULT_SPACING
                The number of lines of spacing above the string to be printed
        Returns
            None
        """
        y, _ = self._screen.getyx()
        while True:
            try:
                self._screen.addstr(y + spacing, 0, str)
            except curses.error:
                self._screen.scroll()
                y -= 1
            else:
                break
