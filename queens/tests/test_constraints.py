import unittest
from queens.nqueens import remove_vertical, remove_diagonal, complete, fails


class ConstraintTests(unittest.TestCase):
    def setUp(self):
        self.grid = [list(range(5)) for x in range(5)]

    def test_remove_vertical(self):
        remove_vertical(self.grid, 0)
        self.assertEqual(
            self.grid,
            [
                [1, 2, 3, 4],
                [1, 2, 3, 4],
                [1, 2, 3, 4],
                [1, 2, 3, 4],
                [1, 2, 3, 4],
            ]
        )

    def test_remove_vertical_non_zero(self):
        remove_vertical(self.grid, 3)
        self.assertEqual(
            self.grid,
            [
                [0, 1, 2, 4],
                [0, 1, 2, 4],
                [0, 1, 2, 4],
                [0, 1, 2, 4],
                [0, 1, 2, 4],
            ]
        )

    def test_remove_vertical_after_elements_set(self):
        grid = [
            [0],
            [2],
            [1, 3, 4],
            [1, 3, 4],
            [1, 3, 4],
        ]
        remove_vertical(grid, 1)
        self.assertEqual(
            grid,
            [
                [0],
                [2],
                [3, 4],
                [3, 4],
                [3, 4]
            ]
        )

    def test_remove_diagonal_edgecase(self):
        grid = [[0], [2], [4], [1], [1, 3], [3]]
        remove_vertical(grid, 1)
        self.assertEqual(
            grid,
            [[0], [2], [4], [], [3], [3]]
        )

    def test_remove_diagonal(self):
        remove_diagonal(self.grid, 0, 0)
        self.assertEqual(
            self.grid,
            [
                [1, 2, 3, 4],
                [0, 2, 3, 4],
                [0, 1, 3, 4],
                [0, 1, 2, 4],
                [0, 1, 2, 3]
            ]
        )

    def test_remove_diagonal_non_zero(self):
        remove_diagonal(self.grid, 0, 2)
        self.assertEqual(
            self.grid,
            [
                [0, 1,    3, 4],
                [0,    2,    4],
                [   1, 2, 3   ],
                [0, 1, 2, 3, 4],
                [0, 1, 2, 3, 4]
            ]
        )

    def test_remove_diagonal_with_previous_elements_set(self):
        grid = [
            [0            ],
            [         3   ],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
        ]
        remove_diagonal(grid, 2, 2)
        self.assertEqual(
            grid,
            [
                [             ],
                [             ],
                [0, 1,    3, 4],
                [0,    2,    4],
                [   1, 2, 3,  ],
            ]
        )

    def test_incomplete(self):
        self.assertFalse(complete(self.grid))

    def test_complete(self):
        self.assertTrue(complete([[0], [1], [2], [3], [4]]))

    def test_fails(self):
        self.assertTrue(fails([[], [1], [1, 2]]))
        self.assertFalse(fails([[1], [2], [3]]))
