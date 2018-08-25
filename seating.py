import re
import sys
from collections import namedtuple

EXP = re.compile("\d+")

"""
A location object which has the row number, column number of the starting seat, column number of the ending seat, exclusive. Used in checking for empty seats."""
Seats = namedtuple("Seats", "row start end")


class Seating:
    """An instance of this class represents a seating layout."""

    def __init__(self, rows: int, columns: int):
        if rows == 0 or columns == 0:
            raise ValueError("The number of rows or columns cannot be zero.")

        self.rows = rows
        self.columns = columns

        self._board = []  # main layout
        for i in range(rows):
            row = [0] * columns
            self._board.append(row)

    def reserve(self, s: str):
        """Reserve one or more seats, given the special format, e.g. R1C4."""
        if not s:
            return

        seats = s.split(" ")
        for seat in seats:
            r, c = self._parse(seat)
            cell = self._board[r][c]
            if self._board[r][c] == 0:
                self._board[r][c] = 1

    def _parse(self, token: str) -> tuple:
        """Get the row and column indexes of the special input format, e.g. R1C4."""
        coordinates = EXP.findall(token)
        if len(coordinates) != 2:
            raise ValueError("Input improperly formatted.")  # not two coordinates

        # subtracting 1 to convert to normal zero-based list access
        return tuple(int(c) - 1 for c in coordinates)

    def _distance(self, x: int, y: int) -> int:
        """Returns the distance for a given point from the central seat.
        The central seat is always the median seat in the first row.
        """
        cx, cy = 0, self.columns // 2
        return x + abs(cy - y)

    def _reduce_distance(self, location: tuple) -> int:
        """Returns the combined distance of a group of consecutive seats from the central seat."""
        row, first, last = location
        total = 0
        for n in range(first, last):
            total += self._distance(row, n)

        return total

    def _find_possible_seats(self, n: int) -> list:
        """Returns a list of coordinates for n consecutive empty seats for every row.
        The format is the following: row, starting seat, ending seat (exclusive).
        """
        coordinates = []

        # avoid indexing outside the bounds
        columns_to_check = self.columns - (n - 1)

        for row in range(self.rows):
            for column in range(columns_to_check):
                # check if not a single seat in n consecutive seats is taken
                if not any(self._board[row][column : column + n]):
                    coordinates.append(Seats(row, column, column + n))

        return coordinates

    def reserve_best_available_seats(self, n: int) -> bool:
        """Returns True if an attempt to find any n consecutive seats succeeds.
        Otherwise, returns False.
        """
        if n >= self.columns:  # can't reserve an entire row at once
            return False

        coordinates = self._find_possible_seats(n)
        if not coordinates:
            return False

        distances = [(coord, self._reduce_distance(coord)) for coord in coordinates]
        # sort the coordinates by distance and get the shortest
        closest = sorted(distances, key=lambda t: t[1])[0]
        seat = closest[0]  # get the namedtuple with the coordinates
        row, first, last = seat
        for i in range(first, last):
            self._board[row][i] = 1
        return True

    def print_seating(self):
        """Visualize the seating layout. Better than use a str of the layout in a __repr__,
        since it would not make sense to print the layout upon printing a method reference, for example.
        """
        print("".join(str(row) + "\n" for row in self._board))


if __name__ == "__main__":
    s = Seating(3, 11)
    print("Please type in initially reserved seats.")
    print(
        "For example, R1C4 R1C6 R2C3 R2C7 R3C9 R3C10. Or hit 'Return' to not set initial seats."
    )
    init = input()
    try:
        s.reserve(init)
    except (ValueError, IndexError) as e:
        print(e)
        sys.exit(1)

    print("Now type the number of consecutive seats you wish to reserve.")
    print("Type 'q' to quit:\n")

    command = ""
    while True:
        command = input()
        if command == "q":
            break
        else:
            try:
                command = int(command)
                success = s.reserve_best_available_seats(command)
                if success:
                    s.print_seating()
                else:
                    print("Not available\n")
            except ValueError:
                print("Invalid number\n")

    print("Done!\n")
    s.print_seating()
