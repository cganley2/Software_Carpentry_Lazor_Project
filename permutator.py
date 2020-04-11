import read_and_interpret_board as rib
from Lazor_solver import Lazor_solver
import itertools
import copy
from win_condition_check import win_condition_check


def permutator(lazor):
    # flatten playGrid and remove block spaces that can't be used
    # then add all movable blocks (A, B, C) to list 
    lazor.flat = list(filter(lambda a: a != 'x', lazor.flat))
    index = 0
    for blockType in lazor.blocks:
        for i in range(int(blockType[1])):
            lazor.flat[index] = blockType[0]
            index += 1

    # this is the bottleneck, especially when larger than 3x3 level
    totalPermutations = list(itertools.permutations(lazor.flat))
    reducedPermutations = list(set(totalPermutations))

    print('total permutations possible: {0}'.format(len(totalPermutations)))
    print('reduced permutations: {0}'.format(len(reducedPermutations)))
    # i am so efficient, wow

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
        rib.read_bff_file("../showstopper_4"), verbose=True)
    lazor = Lazor_solver(board, blocks, lasers, points, playGrid)
    permutator(lazor)
