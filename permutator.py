import read_and_interpret_board as rib
from Lazor_solver import Lazor_solver
import itertools
import copy
from win_condition_check import win_condition_check
import math


def quick_permu(playGrid, block_type=[]):
    '''
    This functions generates all possible permutations of a grid
    given the blocks.

        ** Parameters **
        playGrid: *list* *list* *str*
            Expansion of board_layout that explicitly denotes the LINES in the
            board, allowing for easier calculation of laser movement. 'o' is
            a space where a block can be, 'x' is a space where a black cannot
            be, 'P' is a point that must be intersected, 'L' is a point where a
            laser starts
        block_type: *list* *str*
            List containing the type of block
            appearing the number of times that it is present in the
            playGrid.

    ** Returns **
        all_grid_permutations or playGrid: *list* *list* *str*
            Contains all the possible permutations of the playGrid with boxes
            placed.
    '''
    if len(block_type) > 0:
        original_grid = copy.deepcopy(playGrid)
        all_grid_permutations = []
        number_of_blocks = len(block_type)
        free_block_spaces = [[y, x] for y in range(len(playGrid))
                             for x in range(len(playGrid[y]))
                             if (playGrid[y][x] not in
                                 ["x", "A", "B", "C", "-", "L", "P"]
                                 )]
        scenarios = list(itertools.combinations(
            free_block_spaces, number_of_blocks))
        for each_scenario in scenarios:
            for each_free_space in each_scenario:
                original_grid[each_free_space[0]
                              ][
                    each_free_space[1]] = f"{block_type[0]}"
            all_grid_permutations.append(original_grid)

            original_grid = copy.deepcopy(playGrid)
        return all_grid_permutations
    else:
        return [playGrid]



def generator(playGrid, all_block_type):
    '''
    This functions generates all possible permutations of a grid
    given the blocks.

        ** Parameters **
        playGrid: *list* *list* *str*
            Expansion of board_layout that explicitly denotes the LINES in the
            board, allowing for easier calculation of laser movement. 'o' is
            a space where a block can be, 'x' is a space where a black cannot
            be, 'P' is a point that must be intersected, 'L' is a point where a
            laser starts
        all_block_type: *list* *list* *str*
            List containing the types of blocks
            appearing the number of times that it is present in the
            playGrid.

    ** Returns **
        perm_list: *list* *list* *list* *str*
            Contains all the possible permutations of the playGrid with boxes
            placed.
    '''

    perm_list = []
    A_blocks = []
    B_blocks = [] 
    C_blocks = []
    for i in all_block_type:
        if i[0] == "A":
            for j in range(len(i)):
                A_blocks.append(i[0])
        if i[0] == "B":
            for j in range(len(i)):
                B_blocks.append(i[0])
        if i[0] == "C":
            for j in range(len(i)):
                C_blocks.append(i[0])
        all_block = [A_blocks, B_blocks,C_blocks]

    B_populated_grid = quick_permu(playGrid, all_block[0])

    A_populated_grid = [quick_permu(B_grid, all_block[1]) for B_grid in B_populated_grid]


    C_populated_grid = [quick_permu(each_grid, all_block[2]) for A_grid in A_populated_grid for each_grid in A_grid]

    for i in C_populated_grid:
        for j in i:
            perm_list.append(j)

    return perm_list


def permutator(lazor):
    '''
    This functions generates all possible permutations of a grid
    given the blocks.

        ** Parameters **
        lazor: *Lazor_Solver Object*
            Expansion of board_layout that explicitly denotes the LINES in the
            board, allowing for easier calculation of laser movement. 'o' is
            a space where a block can be, 'x' is a space where a black cannot
            be, 'P' is a point that must be intersected, 'L' is a point where a
            laser starts

    ** Returns **
        board_test.board: *list* *list* *str*
            Contains the winning gird with the position
            of the blocks needed.
    '''


    reducedPermutations = generator(lazor.barePlayGrid, lazor.block_types)

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
        print("could not find solution\n")
