import read_and_interpret_board as rib
import numpy as np


class Lazor_solver:
    '''
    The Lazor_solver class yada yada

    ** Attributes **
        board: *list* *list* *str*
            List m x n grid of x's and o's representing the SPACES in the board
            given by the input file
        blocks: *list* *str*
            List of strings containing the number and type of block available
        lasers: *list* *list* *int*
            List of lists containing integer information about the lasers in
            the puzzle of the form [x, y, vx, vy] where x and y are coordinates
            and vx and vy are velocities. +x goes right and +y goes down
        points: *list* *tuple*
            List of (x, y) coordinates that the lasers must pass through in
            order for the puzzle to be considered solved
        path: *list* *list* *tuple*
            List of list of tuples of (x, y) coordinates that all the lasers
            on the board currently pass through
        playGrid: *list* *list* *str*
            Expansion of board_layout that explicitly denotes the LINES in the
            board, allowing for easier calculation of laser movement. 'o' is
            a space where a block can be, 'x' is a space where a black cannot
            be, 'P' is a point that must be intersected, 'L' is a point where a
            laser starts

    ** Returns **
        None
    '''

    def __init__(self, board_layout, blocks, lasers, points, playGrid):
        '''
        Initialize a Lazor solution object
        '''
        self.board = board_layout
        self.blocks = blocks
        self.lasers = lasers
        self.points = points
        self.path = [[(lasers[i][0], lasers[i][1])]
                     for i in range(len(lasers))]
        self.playGrid = playGrid
        self.extend_lazor()

    # extend_lazor
    def extend_lazor(self):
        '''
        This module extends all lasers across the board based on their (x, y)
        positions and velocities. Laser paths are represented by a '1' in the
        playGrid
        '''
        for i in range(len(self.lasers)):
            velocity = [self.lasers[i][2], self.lasers[i][3]]
            current_point = self.path[i][0]

            while (
                current_point[0] < (len(self.playGrid) - 1) and
                current_point[1] < (len(self.playGrid) - 1)
            ):
                current_point = np.add(current_point, velocity)
                # need block collision checker call here
                # if yes, decide what to do
                self.path[i].append(tuple(current_point))
                self.playGrid[current_point[1]][current_point[0]] = '1'

        for i in self.playGrid:
            print(i)


if __name__ == "__main__":
    board, blocks, lasers, points, playGrid = rib.board_interpretor(
        rib.read_bff_file("../mad_1"), verbose=True)
    lazor = Lazor_solver(board, blocks, lasers, points, playGrid)
