import unittest
from path_finder import Board, Cell


class TestPathFinder(unittest.TestCase):
    def test_grid_length(self):
        board = Board()

        self.assertEqual(len(board.grid), 16)
        self.assertEqual(len(board.grid[0]), 20)

    def test_grid_instances(self):
        board = Board()

        for row in board.grid:
            for cell in row:
                self.assertIsInstance(cell, Cell)

    def test_adj_attributes(self):
        board = Board()

        for x, row in enumerate(board.grid):
            for y, cell in enumerate(row):
                if x-1 >= 0:
                    self.assertTrue(cell.above)
                if y+1 < len(board.grid[0]):
                    self.assertTrue(cell.right)
                if x+1 < len(board.grid):
                    self.assertTrue(cell.below)
                if y-1 >= 0:
                    self.assertTrue(cell.left)


if __name__ == '__main__':
    unittest.main()