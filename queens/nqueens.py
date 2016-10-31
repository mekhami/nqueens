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
import itertools


def backtrack_start(number):
    """
    Params: number, the N in N-Queens
    Returns: The solution position.
    Starts the actual backtracking.
    """
    grid = [list(range(number)) for y in range(number)]
    return ac3_backtrack(grid)


def ac3_backtrack(grid):
    """
    Params: grid, the current state of the grid.
    Returns: the solution, or a recursive call to a child node.
    Does backtrack search with added arc_consistency
    """
    if complete(grid):
        return grid
    row_index = grid.index(most_constrained_row(grid))
    for column in grid[row_index]:
        grid_copy = [row[:] for row in grid]
        grid_copy[row_index] = [column]
        if arc_consistency(grid_copy):
            new_grid = ac3_backtrack(grid_copy)
            if new_grid is not None:
                return ac3_backtrack(new_grid)


def arc_consistency(grid):
    ""
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
            neighbors = set((y, tail) for y in n if y != tail)
            queue |= neighbors
    return True


def revise(grid, head, tail):
    """
    Params: grid, and two row indexes.
    Returns: True if the tail has had elements removed from its domain, false if not
    Removes any elements from the tail that do not work based on the head domain
    """
    revised = False
    for value in grid[tail]:
        if fails_constraints(grid, head, tail, value):
            grid[tail].remove(value)
            revised = True
    return revised


def most_constrained_row(grid):
    """
    Params: grid
    Returns: The row which has the fewest possible places to put the queen
    """
    return min([row for row in grid if len(row) > 1], key=len)


def least_constraining_value(grid, row):
    pass


def fails_constraints(grid, head, tail, value):
    """
    Params: grid, head row index, tail row index, value to check.
    Returns: True if the value from the tail is invalid to the head, False if not
    """
    # If the value for the tail row CANNOT be placed in the HEAD row, return True.
    for item in grid[head]:
        if value != item and value-(abs(tail-head)) != item and value+(abs(tail-head)) != item:
            return False
    return True


def fails(grid):
    """
    Params: grid, a grid state
    Returns: True if any row has no possible values, else False
    """
    return any(len(row) == 0 for row in grid)


def complete(grid):
    """
    Params: grid, a grid state
    Returns: True if all of the rows in the grid are length 1, else False
    """
    return all(len(row) == 1 for row in grid)


if __name__ == '__main__':
    print(backtrack_start(10))
