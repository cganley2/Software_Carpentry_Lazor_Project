import read_and_interpret_board as rib
from Lazor_solver import Lazor_solver
import itertools
import copy
from win_condition_check import win_condition_check
import math

def comb(n,r): #didn't use but useful during debugging
    return math.factorial(n)/((math.factorial(r)*math.factorial(n-r)))

def free_space_calc(playGrid):
    free_block_spaces = [[y,x] for y in range(len(playGrid)) for x in range(len(playGrid[y])) if playGrid[y][x] not in ["x","A","B","C","-","L", "P"]] # Returns index of possible spaces in grid
    
    return free_block_spaces


def quick_permu(playGrid, block_type=[]): # format block_type = ["A","A"] #Initialized as empty
    if len(block_type) > 0: #Check if there is any of the particular blocktype in the grid.
        original_grid = copy.deepcopy(playGrid)
        all_grid_permutations = []
        number_of_blocks = len(block_type) #  E.g: number of As
        # Returns index of possible spaces in grid
        free_block_spaces = [[y,x] for y in range(len(playGrid)) for x in range(len(playGrid[i])) if playGrid[y][x] not in ["x","A","B","C","-","L","P"]]
        # Hope I didn't mess up the order of x,y. It should work.
        scenarios = list(itertools.combinations(free_block_spaces,number_of_blocks)) #Generate posible scenarios with this block type
        for each_scenario in scenarios:
            for each_free_space in each_scenario:
                original_grid[each_free_space[0]][each_free_space[1]] = f"{block_type[0]}"  #Assign str(A) "A" to the free space coordinate.
            all_grid_permutations.append(original_grid) #This output should be the input for the next round of permutation calculaiton, the new "original grid"
            #Next step is to reset original_grid so that next permutation can be calculated:
            original_grid = copy.deepcopy(playGrid) # It is supposed to be a deep copy to run through permutations without changing the original copy of playgrid.
        return all_grid_permutations
    else:
        return playGrid  #  If no A's then just return untouched grid
def generator(playGrid, all_block_type): # format all_block_type = [["B","B"],["A","A","A","A"]]
    # Order of handling blocks actually doesn't matter
    B_populated_grid = quick_permu(playGrid, all_block_type[1]) #returns B_populated grid lists if any, else original playGrid
    A_populated_grid = [quick_permu(B_grid, all_block_type[0]) for B_grid in B_populated_grid] #List of of lists of B and A populated grids

    return A_populated_grid
    #[[A_populated grids from B_populated template 1],[A_populated grids from B_populated template 2],[A_populated grids from B_populated template 3]]
    #TODO: #Not sure how to handle a 3rd block type unless we can change A_populated_grid to a list of grids.




    

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
    reducedPermutations = generator(playGrid, block_types) #Have to make a list of permu, not list of lists of grids (Sorry if that's confusing)
    
    for perm in reducedPermutations:
        permIndex = 0
        board_test = copy.deepcopy(lazor)
        # place the blocks according to the permutation tuple order
        for rowIndex in range(1, len(board_test.playGrid), 2):
            for colIndex in range(1, len(board_test.playGrid[rowIndex]), 2):
                if board_test.playGrid[rowIndex][colIndex] is 'o':
                    board_test.playGrid[rowIndex][colIndex] = perm[permIndex]
                    permIndex += 1
        print('before')
        for i in board_test.playGrid:
            print(i)
        print('\n')
        board_test.extend_lazor()

        print('after')
        for i in board_test.playGrid:
            print(i)
        win = win_condition_check(board_test)

        if win is True:
            break


if __name__ == "__main__":
    board, blocks, lasers, points, playGrid = rib.board_interpretor(
        rib.read_bff_file("unit_test_3x3"), verbose=True)
    lazor = Lazor_solver(board, blocks, lasers, points, playGrid)
    permutator(lazor)
