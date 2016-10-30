"""
N-queens backtracking search with constraint propagation.
By Lawrence Vanderpool (lawrence.vanderpool@gmail.com)

The board structure is:
    [[0, 1, 2, 3, 4]
     [0, 1, 2, 3, 4]
     [0, 1, 2, 3, 4]
     [0, 1, 2, 3, 4]
     [0, 1, 2, 3, 4]]

Rows in this grid are the domain of each row. IE in the row [0, 1, 2] the queen can be placed on the
1st, 2nd, or 3rd column.
"""
import copy
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
    """
    Params: grid
    Returns: True if the grid can be made fully arc consistent, false if not
    Applies arc consistency to every arc in the grid.
    """
    n = range(len(grid))
    queue = set(itertools.permutations(n, r=2))
    while queue:
        head, tail = queue.pop()
        if revise(grid, head, tail):
            if len(grid[tail]) == 0:
                return False
            queue |= set([(head, y) for y in n if (y != tail) and (y != head)])
    return True


def revise(grid, head, tail):
    """
    Params: grid, and two row indexes.
    Returns: True if the tail has had elements removed from its domain, false if not
    Removes any elements from the tail that do not work based on the head domain
    """
    revised = False
    for value in grid[tail]:
        if fails_constraints(head, tail):
            grid[tail].remove(value)
        revised = True
    return revised


def fails_constraints(head, tail):
    """
    Params: grid and two row indexes
    Returns: True if the value from the tail is invalid to the head, False if not
    """
    pass


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


if __name__ == '__main__':
    print(backtrack_start(6))
