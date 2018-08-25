# Theater seating puzzle

## Running
The driver program is part of the main script:
> python3 seating.py

To launch tests, run:
> python3 -m unittest seating_test.py

## Notes
1. For the sake of simplicity, user's selection of the initial dimensions of the seating layout is omitted from the driver program to keep it shorter. Pass desired dimensions to the constructor in code.
1. The total Manhattan distance of a group of seats from the central seat is the sum of all distances of each seat. Perhaps, a different metric can be used.
1. The program does not actually parse the user-specified input to reserve one or more seats, e.g., R1C4. It just gets two numbers for the row and column, in that order. Any vowel(s) could precede or follow a number. In this case, I think, it would suffice, but, generally, it's not robust and extensible.
1. Perhaps, using regular expressions for the above parsing is overkill, but for the scope of the problem, it might be OK.
1. Perhaps, the introduction of a separate 'protocol' for finding the location of a group of best seats is a bit odd:
(0, 3, 6), where 0 is the row number, 3 is the column number of the starting seat, and 6 is the column number of the ending seat, exclusive. But it is easy to use it in checking for empty seats. As the program's functionality expands, this little abstraction can become convenient.
1. The program is fast even with a grid of 1000 by 1000 seats, but, perhaps, could be made faster by using some clever, more efficient iteration over all cells.
1. For learning something new, I decided to try and use Python's built-in type annotations just on method signatures.
1. For the sake of simplicity, I decided not to handle an IndexError in any special way, or alert the user with more detailed text in this case. Just print the error and exit.
