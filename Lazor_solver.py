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
        self.flat = [item for sublist in self.board for item in sublist]
        # self.extend_lazor()

    # extend_lazor
    def extend_lazor(self):
        '''
        This module extends all lasers across the board based on their (x, y)
        positions and velocities. Laser paths are represented by a '1' in the
        playGrid
        '''
        for i in range(len(self.lasers)):
            self.velocity = [self.lasers[i][2], self.lasers[i][3]]
            self.current_point = self.path[i][0]

            while (
                self.current_point[0] <= (len(self.playGrid[0])) and
                self.current_point[1] <= (len(self.playGrid)) and
                self.current_point[0] > 0 and
                self.current_point[1] > 0
            ):
                self.current_point = np.add(self.current_point, self.velocity)
                # need block collision checker call here
                # if yes, decide what to do
                self.path[i].append(tuple(self.current_point))
                self.playGrid[self.current_point[1]
                              ][self.current_point[0]] = '1'
                print(self.current_point[1], self.current_point[0])
                self.collision_checker()

    def collision_checker(self):
        '''
        This function checks if the laser has hit a block and adjusts its path
        accordingly
        '''
        # NEED TO CHANGE WHAT CHECKER LOOKS AT ON EVERY STEP. DON'T NEED TO
        # LOOK AT ALL 4 POSITIONS OR ELSE IT GETS CONFUSED
        if (
            self.current_point[0] <= (len(self.playGrid[0]) - 1) and
            self.current_point[1] <= (len(self.playGrid) - 1)
        ):
            left = self.playGrid[self.current_point[1]
                                 ][self.current_point[0] + 1]
            top = self.playGrid[self.current_point[1] -
                                1][self.current_point[0]]
            right = self.playGrid[self.current_point[1]
                                  ][self.current_point[0] - 1]
            bottom = self.playGrid[self.current_point[1] +
                                   1][self.current_point[0]]

            # check if hit movable block on LEFT side
            if left in {'A', 'B', 'C'}:
                if left is 'A':  # change laser velocity
                    self.velocity[0] = -1 * self.velocity[0]
                elif left is 'B':  # set position arbitrarily out of bounds
                    self.current_point = (99, 99)
                else:  # can't figure out how to account for C blocks
                    self.lasers.append(
                        [
                            self.current_point[1],
                            self.current_point[0],
                            -1 * self.velocity[0],
                            self.velocity[1]
                        ]
                    )
            # TOP check
            elif top in {'A', 'B', 'C'}:
                if top is 'A':
                    self.velocity[1] = -1 * self.velocity[1]
                elif top is 'B':
                    self.current_point = (99, 99)
                else:
                    pass
            # RIGHT check
            elif right in {'A', 'B', 'C'}:
                print(right)
                if right is 'A':
                    self.velocity[0] = -1 * self.velocity[0]
                elif right is 'B':
                    self.current_point = (99, 99)
                else:
                    pass
            # BOTTOM check
            elif bottom in {'A', 'B', 'C'}:
                if bottom is 'A':
                    self.velocity[1] = -1 * self.velocity[1]
                elif bottom is 'B':
                    self.current_point = (99, 99)
                else:
                    pass


if __name__ == "__main__":
    board, blocks, lasers, points, playGrid = rib.board_interpretor(
        rib.read_bff_file("../showstopper_4"), verbose=True)
    # playGrid[3][7] = 'A'
    # playGrid[1][5] = 'C'
    lazor = Lazor_solver(board, blocks, lasers, points, playGrid)
    print(lazor.path)
