import unittest
from queens.nqueens import complete, fails


class ConstraintTests(unittest.TestCase):
    def setUp(self):
        self.grid = [list(range(5)) for x in range(5)]

    def test_incomplete(self):
        self.assertFalse(complete(self.grid))

    def test_complete(self):
        self.assertTrue(complete([[0], [1], [2], [3], [4]]))

    def test_fails(self):
        self.assertTrue(fails([[], [1], [1, 2]]))
        self.assertFalse(fails([[1], [2], [3]]))
