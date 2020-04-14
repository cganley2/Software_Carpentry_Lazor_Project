import read_and_interpret_board as rib
from Lazor_solver import Lazor_solver
from permutator import permutator

if __name__ == '__main__':

    board_path = 'boards/mad_7'

    board, blocks, lasers, points, playGrid = rib.board_interpretor(
        rib.read_bff_file(board_path), verbose=True)

    lazor = Lazor_solver(board, blocks, lasers, points, playGrid)

    winning_board = permutator(lazor)

    out_file = 'solutions/' + board_path[7:] + '_solution.bff'

    with open(out_file, 'w') as f:
        for row in winning_board:
            for col in row:
                f.write(col)
            f.write('\n')
    f.close()
