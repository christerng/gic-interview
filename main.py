import curses
from src._types import Movie, ScrollingScreen
from src._enums import MainMenuOptions


def handle_admin(screen: ScrollingScreen) -> Movie:
    while True:
        screen.addstr(
            "Please define movie title and seating map in "
            "[Title] [Row] [SeatsPerRow] format:\n> "
        )
        try:
            return Movie.from_user_input(screen.getstr())
        except ValueError as e:
            screen.addstr(str(e), spacing=1)


def handle_user(screen: ScrollingScreen, movie: Movie) -> None:
    while True:
        screen.addstr(
            f"""Welcome to GIC Cinemas
[1] Book tickets for {movie.title} ({movie.seats_unbooked()} seats available)
[2] Check bookings
[3] Exit
Please enter your selection:
> """,
        )
        match screen.getch():
            case MainMenuOptions.MAKE_BOOKING:
                _make_booking(screen, movie)
            case MainMenuOptions.CHECK_BOOKING:
                _check_booking(screen, movie)
            case MainMenuOptions.EXIT:
                _exit(screen)
            case _:
                screen.deleteln()
                screen.addstr("> ", spacing=1)


def _make_booking(screen: ScrollingScreen, movie: Movie) -> None:
    while True:
        screen.addstr(
            "Enter number of tickets to book, "
            "or enter blank to go back to main menu:\n> "
        )
        if not (user_input := screen.getstr()):
            return

        if (seats_to_book := int(user_input)) > movie.seats_unbooked():
            screen.addstr(
                f"Sorry, there are only {movie.seats_unbooked()} seats available.",
                spacing=1,
            )
            continue

        booking_id = movie.book(seats_to_book)
        screen.addstr(
            f"Successfully reserved {seats_to_book} {movie.title} tickets.", spacing=1
        )
        screen.addstr(movie.get_map(booking_id), spacing=1)

        while True:
            screen.addstr(
                "Enter blank to accept seat selection, "
                "or enter new seating position:\n> "
            )

            if not (user_input := screen.getstr()):
                screen.addstr(f"Booking id: {booking_id} confirmed.")
                return

            movie.unbook(booking_id)

            row_index = ord(user_input[:1]) - ord("A")
            col_index = int(user_input[1:]) - 1

            booking_id = movie.book(seats_to_book, row_index, col_index)
            screen.addstr(movie.get_map(booking_id), spacing=1)


def _check_booking(screen: ScrollingScreen, movie: Movie) -> None:
    while True:
        screen.addstr("Enter booking id, or enter blank to go back to main menu:\n> ")
        if booking_id := screen.getstr():
            screen.addstr(movie.get_map(booking_id))
        return


def _exit(screen: ScrollingScreen) -> None:
    screen.addstr("Thank you for using GIC Cinemas system. Bye!")
    screen.getch()
    exit()


def main(stdscr: curses.window) -> None:
    curses.echo()

    screen = ScrollingScreen(stdscr)

    movie = handle_admin(screen)
    handle_user(screen, movie)


if __name__ == "__main__":
    curses.wrapper(main)
