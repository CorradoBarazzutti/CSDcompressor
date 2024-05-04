import unittest

from src.utilities.neighbours import d_infinity_neighbours


class NeighboursTest(unittest.TestCase):

    def test_1_infinity_neighbours(self): # test d_infinity_neighbours
        self.assertEqual(
            d_infinity_neighbours((1, 1), [3, 3]),
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)])
        self.assertEqual(
            d_infinity_neighbours((0, 0), [3, 3]),
            [(0, 1), (1, 0), (1, 1)])


if __name__ == '__main__':
    unittest.main()
