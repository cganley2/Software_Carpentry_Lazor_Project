# run this script to see how lasers interact with each of the block types

import read_and_interpret_board as rib
from Lazor_solver import Lazor_solver

if __name__ == '__main__':

    Aboard, Ablocks, Alasers, Apoints, AplayGrid = rib.board_interpretor(
        rib.read_bff_file('boards/unit_test_A'), verbose=False)

    Bboard, Bblocks, Blasers, Bpoints, BplayGrid = rib.board_interpretor(
        rib.read_bff_file('boards/unit_test_B'), verbose=False)

    Cboard, Cblocks, Clasers, Cpoints, CplayGrid = rib.board_interpretor(
        rib.read_bff_file('boards/unit_test_C'), verbose=False)

    print('Demonstration of A block behavior:\n')
    A_test = Lazor_solver(Aboard, Ablocks, Alasers, Apoints, AplayGrid)

    print('Demonstration of B block behavior:\n')
    B_test = Lazor_solver(Bboard, Bblocks, Blasers, Bpoints, BplayGrid)

    print('Demonstration of C block behavior:\n')
    C_test = Lazor_solver(Cboard, Cblocks, Clasers, Cpoints, CplayGrid)
