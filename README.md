# GIC-Interview

Christopher's implementation of a movie-booking TUI for GIC's take-home assignment.

## Installation

On MacOS or Linux, use curl to install [uv](https://docs.astral.sh/uv/).

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Use uv to run tests.

```bash
uv run pytest
```

Use uv to run app.

```bash
uv run main.py
```

## Description

- The project is composed of an entrypoint and helper modules.
  - `main.py` is the project's entrypoint. It instantiates the `ScrollingScreen` and `Movie` instance.
  - `_types.py` contains implementations of the `ScrollingScreen` and `Movie` classes.
  - `_enums.py` contains an `IntEnum` for handling user input in the main menu.
  - `_constants.py` contains constants used throughout the project.
- The TUI uses Python's [curses](https://docs.python.org/3/library/curses.html) to write to and read from the terminal.
  - [curses](https://docs.python.org/3/library/curses.html) is wrapped by a custom `ScrollingScreen` class to scroll the terminal, which gives a better user experience and prevents the cursor from going off-screen and raising an error.
- The `Movie` class is constructed by a movie title, the number of rows, and the number of columns of seats.
  - The public `.get_map` method returns a seating map of the `Movie` as a string, with different characters for whether a seat is booked or not, and whether it is currently reserved by someone making or checking a booking or not.
  - The public `.book` method returns a Booking ID as a string, while prompting the user to either accept its default seat selection or to enter a new starting seat to book.
