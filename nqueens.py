"""
N-queens backtracking search with constraint propagation.
By Lawrence Vanderpool (lawrence.vanderpool@gmail.com)

The board structure is:
    [[0, 1, 2, 3, 4]
     [0, 1, 2, 3, 4]
     [0, 1, 2, 3, 4]
     [0, 1, 2, 3, 4]
     [0, 1, 2, 3, 4]]

Rows in this grid are the domain of each row. IE in the row [0, 1, 2] the queen can be placed on the 1st,
2nd, or 3rd column.
"""
import copy
import unittest
import itertools


def backtrack_start(number):
    """
    The wrapper around the recursive function to start the stack
    param number: number of queens to solve for (also size of grid!)
    """
    grid = [list(range(number)) for x in range(number)]
    return backtrack(grid)


def backtrack(grid):
    """
    The recursive function to solve n-queens with forward checking
    and arc consistency.
    """
    if complete(grid):
        return grid
    row_index = grid.index(next((row for row in grid if len(row) != 1), None))
    for column in grid[row_index]:
        grid_copy = propagate_constraints(copy.deepcopy(grid), row_index, column)
        print(grid_copy)
        new_grid = backtrack(grid_copy)
        if new_grid is not None:
            if not fails(new_grid):
                return new_grid


def arc_consistency(grid):
    queue = list(itertools.permutations(range(len(grid)), r=2))
    while queue:
        row1_index, row2_index = queue.pop()
        if revise(grid, row1_index, row2_index):
            if len(grid[row1_index]) == 0:
                return False
            # TODO: Add neighboring arcs to queue
    return True


def revise(grid, r1, r2):
    revised = False
    for value in grid[r1]:
        if fails_constraints(grid[r2], grid[r1]):
            grid[r1].remove(value)
        revised = True
    return revised


def fails_constraints(row2, row1):
    pass


# UNUSED
def propagate_constraints(grid, row_index, value):
    """
    Take a grid, return the grid that will be the result of enforcing
    all the constraints on that grid. (Diagonal, vertical, horizontal)
    The horizontal constraint is implicit when you select a column for
    the row, so only horizontal and diagonal is needed.
    """
    remove_vertical(grid, value)
    remove_diagonal(grid, row_index, value)

    # Assign the correct row value since we removed it as part of
    # the above operations.
    grid[row_index] = [value]
    return grid


def remove_diagonal(grid, row_index, value):
    """
    Remove the values diagonally in the grid
    """
    for row, _ in enumerate(grid):
        try:
            grid[row].remove(value+(row-row_index))
        except ValueError:
            pass

        try:
            grid[row].remove(value-(row-row_index))
        except ValueError:
            pass


def remove_vertical(grid, value):
    """
    Remove the value vertically in the grid
    """
    for row in grid:
        try:
            row.remove(value)
        except ValueError:
            pass


def fails(grid):
    """
    Fails a grid if any of the rows have no possible solutions
    """
    return any(len(row) == 0 for row in grid)


def complete(grid):
    """
    Returns True if all of the rows in the grid are length 1, thus there's a queen in every row.
    All other constraints will pass by the nature of checking them and propagating the constraints
    in the actual backtracking recursion.
    """
    return all(len(row) == 1 for row in grid)


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


if __name__ == '__main__':
    print("running asserts first")
    unittest.main()
    # print(backtrack_start(6))