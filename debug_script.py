import read_and_interpret_board as rib
from Lazor_solver import Lazor_solver
from permutator import permutator

if __name__ == "__main__":
    print('this is from debug_script.py, the ONLY debugging script that' +
          'should be used!')
    board, blocks, lasers, points, playGrid = rib.board_interpretor(
        rib.read_bff_file("../showstopper_4"), verbose=False)
    # print(playGrid)
    # print(blocks)
    # playGrid[1][5] = 'C'
    # playGrid[3][7] = 'A'
    # playGrid[5][1] = 'A'
    # playGrid[5][5] = 'C'
    lazor = Lazor_solver(board, blocks, lasers, points, playGrid)
    # print(lazor.playGrid)
    permutator(lazor)
