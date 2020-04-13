import read_and_interpret_board as rib
from Lazor_solver import Lazor_solver
from permutator import permutator

if __name__ == "__main__":
    print('this is from debug_script.py, the ONLY debugging script that' +
          ' should be used!')
    board, blocks, lasers, points, playGrid = rib.board_interpretor(
        rib.read_bff_file("boards/mad_7"), verbose=True)

    lazor = Lazor_solver(board, blocks, lasers, points, playGrid)

    winning_board = permutator(lazor)
