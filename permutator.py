import read_and_interpret_board as rib
from Lazor_solver import Lazor_solver
import itertools
import copy
from win_condition_check import win_condition_check
import math


def comb(n, r):  # didn't use but useful during debugging
    return math.factorial(n) / ((math.factorial(r) * math.factorial(n - r)))


def free_space_calc(playGrid):
    free_block_spaces = [[y, x] for y in range(len(playGrid)) for x in range(len(playGrid[y])) if playGrid[y][x] not in [
        "x", "A", "B", "C", "-", "L", "P"]]  # Returns index of possible spaces in grid

    return free_block_spaces


# format block_type = ["A","A"] #Initialized as empty
def quick_permu(playGrid, block_type=[]):
    # Check if there is any of the particular blocktype in the grid.
    if len(block_type) > 0:
        original_grid = copy.deepcopy(playGrid)
        all_grid_permutations = []
        number_of_blocks = len(block_type)  # E.g: number of As
        # Returns index of possible spaces in grid
        free_block_spaces = [[y, x] for y in range(len(playGrid)) for x in range(
            len(playGrid[y])) if playGrid[y][x] not in ["x", "A", "B", "C", "-", "L", "P"]]
        # Hope I didn't mess up the order of x,y. It should work.
        # Generate posible scenarios with this block type
        scenarios = list(itertools.combinations(
            free_block_spaces, number_of_blocks))
        for each_scenario in scenarios:
            for each_free_space in each_scenario:
                # Assign str(A) "A" to the free space coordinate.
                original_grid[each_free_space[0]][each_free_space[1]] = f"{block_type[0]}"
            # This output should be the input for the next round of permutation calculaiton, the new "original grid"
            all_grid_permutations.append(original_grid)
            # Next step is to reset original_grid so that next permutation can be calculated:
            # It is supposed to be a deep copy to run through permutations without changing the original copy of playgrid.
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

        # for i in range(len(perm_list)):
        #     for j in perm_list[i]:
        #         print(j)
        #     print('\n')

    else:
        A_populated_grid = quick_permu(playGrid, all_block_type[0])

        # print(A_populated_grid)

        # for i in A_populated_grid:
        #     for j in i:
        #         perm_list.append(j)

        # for i in perm_list:
        #     for j in i:
        #         print(i)
        #     print('\n')
        # print(perm_list)
    

    return perm_list
    #[[A_populated grids from B_populated template 1],[A_populated grids from B_populated template 2],[A_populated grids from B_populated template 3]]
    # TODO: #Not sure how to handle a 3rd block type unless we can change A_populated_grid to a list of grids.


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
    # #Instead, create all positible positions (o's, or blocks) and assign A or B to hem.
    # #   # How? Eg: 4A, 1B: Create grids with B occupying a space and then assign A to the free spaces "o", aka: not "x" or "B"
    #     # format would be, for i in blocks. Assign and generate new grids with possible positions, then go to next block i.

    # print('total permutations possible: {0}'.format(len(totalPermutations)))
    # print('reduced permutations: {0}'.format(len(reducedPermutations)))
    # # i am so efficient, wow
    # block_types =
    # Have to make a list of permu, not list of lists of grids (Sorry if that's confusing)
    reducedPermutations = generator(lazor.barePlayGrid, lazor.block_types)

    for playGridPerm in reducedPermutations:
        permIndex = 0
        board_test = copy.deepcopy(lazor)
        board_test.playGrid = playGridPerm

        # print('before')
        # for i in board_test.playGrid:
        #     print(i)
        # print('\n')
        board_test.solver()

        # print('after')
        # for i in board_test.playGrid:
        #     print(i)
        win = win_condition_check(board_test)

        if win is True:
            break

    if win is not True:
        print('could not find solution')
