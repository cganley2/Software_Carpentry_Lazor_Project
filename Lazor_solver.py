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
                     for i in range(len(lasers))] # the laser location and not direction x,y
        self.playGrid = playGrid
        self.c_lasers = [[1,0,0,0]]
        self.extend_lazor()
        

    # extend_lazor
    def extend_lazor(self):
        '''
        This module extends all lasers across the board based on their (x, y)
        positions and velocities. Laser paths are represented by a '1' in the
        playGrid
        '''
        l_i = -1 #laser index
        while (
            self.c_lasers != [[0,0,0,0]] and
            l_i <= len(self.lasers) -1
            ):
            l_i += 1 #everytime laser gets out of bound, add 1 to go to next laser
            print(f"we are at l_i: {l_i}")
            self.velocity = [self.lasers[l_i][2], self.lasers[l_i][3]]
            self.path = [[(lasers[i][0], lasers[i][1])]
                     for i in range(len(lasers))]
            self.current_point = self.path[l_i][0] #for each laser i, always starting the source of laser [0].
            print(f"calculating for laser {self.lasers[l_i]}")

            while (
                self.current_point[0] < (len(self.playGrid) - 1) and
                self.current_point[1] < (len(self.playGrid) - 1) and
                self.current_point[0] > 0 and
                self.current_point[1] > 0
            ): # if/while within board
                if self.lasers[l_i] not in self.c_lasers:
                    self.current_point = np.add(self.current_point, self.velocity) #current point + up in velocity direction, always add vx and vy to point messes up new c_laser placement
                # need block collision checker call here
                # if yes, decide what to do
                self.path[l_i].append(tuple(self.current_point)) #append new point to path
                self.playGrid[self.current_point[1]
                              ][self.current_point[0]] = '1'
                self.collision_checker(i_laser=self.lasers[l_i]) # this updates position

        for i in self.playGrid:
            print(i)

    def collision_checker(self, i_laser):
        '''
        This function checks if the laser has hit a block and adjusts its path
        accordingly
        '''
        if (
            self.current_point[0] < (len(self.playGrid) - 1) and
            self.current_point[1] < (len(self.playGrid) - 1)
        ):
            left = self.playGrid[self.current_point[1]
                                 ][self.current_point[0] - 1]
            top = self.playGrid[self.current_point[1] -
                                1][self.current_point[0]]
            right = self.playGrid[self.current_point[1]
                                  ][self.current_point[0] + 1]
            bottom = self.playGrid[self.current_point[1] +
                                   1][self.current_point[0]]

            # check if hit movable block on LEFT side
            if left in {'A', 'B', 'C'}:
                if left is 'A': # change laser velocity
                    self.velocity[0] = -1 * self.velocity[0]
                elif left is 'B': # set position arbitrarily out of bounds
                    self.current_point = (len(self.playGrid) + 1, 0)
                else: # can't figure out how to account for C blocks
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
                    self.current_point = (len(self.playGrid) + 1, 0)
                else: # TRYING TO FIX C: new laser created will ALWAYS start at C by definition: WILL have to automate C reflection
                    print(self.lasers)
                    if i_laser in self.c_lasers:
                        print("oi")
                        self.velocity[1] = -1 * self.velocity[1]
                        self.c_lasers = [[0,0,0,0]]

                    else:
                        print(f"i_laser is {i_laser}")
                        print(f"Running {self.lasers} Nothing is in c_lasers ")
                        self.lasers.append(
                            [
                                self.current_point[0],
                                self.current_point[1],
                                self.velocity[0],
                                self.velocity[1]
                            ]
                        )
                        self.c_lasers.pop()  # remove current c_laser & replace
                        self.c_lasers.append(
                            [
                                self.current_point[0],
                                self.current_point[1],
                                self.velocity[0],
                                self.velocity[1]
                            ]
                        )
                    print(self.c_lasers)
                    pass #We are going to create a new laser and make the old one pass through C
                    print(self.lasers) 
            # RIGHT check
            elif right in {'A', 'B', 'C'}:
                if right is 'A':
                    self.velocity[0] = -1 * self.velocity[0]
                elif right is 'B':
                    self.current_point = (len(self.playGrid) + 1, 0)
                else:
                    print(self.lasers)
                    print(self.lasers[-1])
                    if i_laser in self.c_lasers: #ROBUST
                        print("c is on right but we have already went through c")
                        self.velocity[1] = -1 * self.velocity[1]
                        self.c_lasers = [[0,0,0,0]]
                    elif [self.lasers[-1]] == self.c_lasers:
                        print("Passed through C-block, now getting out")  # NEED to change for more lasers
                        #self.current_point = np.add(self.current_point, self.velocity) #moving back because the while loop will move us forward
                        pass


                    else:
                        print(f"i_laser is {i_laser}")
                        print(f"Running {self.lasers} Nothing is in c_lasers ")
                        self.lasers.append(
                            [
                                self.current_point[0],
                                self.current_point[1],
                                self.velocity[0],
                                self.velocity[1]
                            ]
                        )
                        self.c_lasers.pop()  # remove current c_laser & replace
                        self.c_lasers.append(
                            [
                                self.current_point[0],
                                self.current_point[1],
                                self.velocity[0],
                                self.velocity[1]
                            ]
                        )
                    print(self.c_lasers)
                    pass #We are going to create a new laser and make the old one pass through C
                    print(self.lasers) 
                    print("c on right")
                    

            # BOTTOM check
            elif bottom in {'A', 'B', 'C'}:
                if bottom is 'A':
                    self.velocity[1] = -1 * self.velocity[1]
                elif bottom is 'B':
                    self.current_point = (len(self.playGrid) + 1, 0)
                else:
                    pass


if __name__ == "__main__":
    board, blocks, lasers, points, playGrid = rib.board_interpretor(
        rib.read_bff_file("mad_1"), verbose=True)
    playGrid[3][7] = 'A'
    playGrid[1][5] = 'C'
    lazor = Lazor_solver(board, blocks, lasers, points, playGrid)
    print(lazor.path)
