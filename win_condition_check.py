import read_and_interpret_board as rib
from Lazor_solver import Lazor_solver


def win_condition_check(lazor_board):
    if any('P' in row for row in lazor_board.playGrid):
        return False

    else:
        print('\n\n')
        print('Winning play grid:\n')
        for i in lazor_board.playGrid:
            print(i)
        return True


if __name__ == "__main__":
    board, blocks, lasers, points, playGrid = rib.board_interpretor(
        rib.read_bff_file("unit_test_2x2"), verbose=True)
    # playGrid[3][5] = 'A'
    # playGrid[1][3] = 'A' # shouldn't get win without this line!!!!!
    # playGrid[]
    # playGrid[1][5] = 'C' # need C suppport to continue
    # playGrid[5][1] = 'A'
    lazor = Lazor_solver(board, blocks, lasers, points, playGrid)
    win_condition_check(lazor)
