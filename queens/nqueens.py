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
    print("Not implemented yet.")
