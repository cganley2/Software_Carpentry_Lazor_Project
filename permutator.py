import read_and_interpret_board as rib
from Lazor_solver import Lazor_solver
import itertools
import copy
from win_condition_check import win_condition_check
import math


def quick_permu(playGrid, block_type=[]):
    # Check if there is any of the particular blocktype in the grid.
    if len(block_type) > 0:
        original_grid = copy.deepcopy(playGrid)
        all_grid_permutations = []
        number_of_blocks = len(block_type)  # E.g: number of As
        # Returns index of possible spaces in grid
        free_block_spaces = [[y, x] for y in range(len(playGrid))
                             for x in range(len(playGrid[y]))
                             if (playGrid[y][x] not in
                                 ["x", "A", "B", "C", "-", "L", "P"]
                                 )]
        # Hope I didn't mess up the order of x,y. It should work.
        # Generate posible scenarios with this block type
        scenarios = list(itertools.combinations(
            free_block_spaces, number_of_blocks))
        for each_scenario in scenarios:
            for each_free_space in each_scenario:
                # Assign str(A) "A" to the free space coordinate.
                original_grid[each_free_space[0]
                              ][
                    each_free_space[1]] = f"{block_type[0]}"
            all_grid_permutations.append(original_grid)

            original_grid = copy.deepcopy(playGrid)
        return all_grid_permutations
    else:
        return playGrid  # If no A's then just return untouched grid


# format all_block_type = [["B","B"],["A","A","A","A"]]
def generator(playGrid, all_block_type):
    # Order of handling blocks actually doesn't matter
    # returns B_populated grid lists if any, else original playGrid
    perm_list = []

    if len(all_block_type) > 1:
        B_populated_grid = quick_permu(playGrid, all_block_type[1])
        # List of of lists of B and A populated grids
        A_populated_grid = [quick_permu(B_grid, all_block_type[0])
                            for B_grid in B_populated_grid]
        for i in A_populated_grid:
            for j in i:
                perm_list.append(j)

    else:
        A_populated_grid = quick_permu(playGrid, all_block_type[0])

    return perm_list


def permutator(lazor):
    # flatten playGrid and remove block spaces that can't be used
    # then add all movable blocks (A, B, C) to list
    # lazor.flat = list(filter(lambda a: a != 'x', lazor.flat))
    # index = 0
    # for blockType in lazor.blocks:
    #     for i in range(int(blockType[1])):
    #         lazor.flat[index] = blockType[0]
    #         index += 1

    # # this is the bottleneck, especially when larger than 3x3 level
    # totalPermutations = list(itertools.permutations(lazor.flat))
    # reducedPermutations = list(set(totalPermutations))

    win = False
    for playGridPerm in reducedPermutations:

        permIndex = 0
        board_test = copy.deepcopy(lazor)
        board_test.playGrid = playGridPerm

        board_test.solver()

        win = win_condition_check(board_test)

        if win is True:
            return board_test.board
            break

    if win is not True:
        print('could not find solution\n')
