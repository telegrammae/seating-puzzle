import unittest
from seating import Seating, Seats


class TestSeating(unittest.TestCase):
    def test_invalid_state(self):
        self.assertRaises(ValueError, Seating, 0, 0)
        self.assertRaises(ValueError, Seating, 3, 0)
        self.assertRaises(ValueError, Seating, 0, 3)

    def test_distance(self):
        s = Seating(3, 11)
        self.assertAlmostEqual(4, s._distance(2, 3))

    def test_reduce_distance(self):
        s = Seating(3, 11)
        coordinates = Seats(1, 2, 5)
        self.assertAlmostEqual(9, s._reduce_distance(coordinates))

    def test_parse(self):
        s = Seating(3, 11)
        indexes = s._parse("R2C9")
        self.assertAlmostEqual((1, 8), indexes)

    def test_reserve(self):
        s = Seating(3, 11)
        s.reserve("R1C4 R1C6 R2C3 R2C7 R3C9 R3C10")
        occupied = 0
        for row in range(s.rows):
            for column in range(s.columns):
                if s._board[row][column] == 1:
                    occupied += 1
        self.assertAlmostEqual(6, occupied)
