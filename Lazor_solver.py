import read_and_interpret_board as rib
import numpy as np
from copy import deepcopy
# Current Problems: laser.x and .y don't eveolve at same rate as laser.position. Should I just make laser.x/y constant?
#.x and .y updated during laser.move() but not during laser pop
# When laser changes, .x and .y are not updated
# Block C is still issue


class Lazor_solver:
    '''
    The Lazor_solver class contains all information about a board from the
    input file.

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
        self.block_types = [
            [blocks[i][0]] * int(blocks[i][1]) for i in range(len(blocks))
        ]
        self.lasers = lasers
        self.points = points
        self.path = [
            [(lasers[i][0], lasers[i][1])] for i in range(len(lasers))
        ]
        self.playGrid = playGrid
        self.barePlayGrid = deepcopy(playGrid)
        self.solver()

    def solver(self):
        '''
        Docstring for solver. Nelson can describe this
        '''
        # Has to be up here otherwise we are re-storing
        # all lasers in while loop each time
        all_lasers = [Laser(each_laser) for each_laser in self.lasers]

        print('looking at:')
        for i in self.playGrid:
            print(i)
        print('\n')

        C_collision = None  # C_collision is a flag for if laser hits a C block

        while len(all_lasers) > 0:
            # Updates the current laser must be relating to all_laser list
            # that we defined above
            current_laser = all_lasers[0]
            current_laser.x = current_laser.position[0]
            current_laser.y = current_laser.position[1]

            # Once laser popped (cause met B or went outside, current laser
            # should come back here)
            print(f"current laser main: {current_laser}")

            # when laser encounters B, it sets position arbitrarily out of
            # bounds, and this removes the laser
            if current_laser.position[0] > len(self.playGrid):
                all_lasers.pop(0)

            while (current_laser.position[0] <= (len(self.playGrid[0]) - 1) and
                   current_laser.position[1] <= (len(self.playGrid) - 1)):

                next_move = np.add(current_laser.position,
                                   current_laser.velocity)
                print(f"current pos: {list(current_laser.position)}")
                print(f"next move is: {next_move}")

                # checking if next move is in grid. No need to check later.
                if self.is_valid(next_move):
                    print('valid move')
                    # TODO: Laser should immediately move, an edge case is if
                    # next_move is a block. Overaccounted for this edge case.
                    # TODO 2: Laser should immediately move, otherwise edge
                    # case where laer stats at edge will check everywhere and
                    # index error will occur

                    # returns true if there is collision aka right,left,
                    # top,bottom in [a,b,c]
                    check, direction, block_type = self.collision_check(
                        current_laser)  # tuple of Bool and type of block

                    if check:
                        # Rotates the laser AND moves out. This is in case B
                        # kicks you out
                        C_collision = current_laser.collide(
                            self, block_type, direction)

                        if C_collision is not None:
                            # path around C skips a few coordinates due to
                            # collision errors, so these put 1s on the board
                            # in those spots
                            if C_collision.x <= (len(self.playGrid[0]) - 1) and \
                                    C_collision.x >= 0 and \
                                    C_collision.y <= (len(self.playGrid) - 1) and \
                                    C_collision.y >= 0:
                                self.playGrid[C_collision.y
                                              ][
                                    C_collision.x] = "1"
                        if current_laser.x <= (len(self.playGrid[0]) - 1) and \
                                current_laser.x >= 0 and \
                                current_laser.y <= (len(self.playGrid) - 1) and \
                                current_laser.y >= 0:
                            self.playGrid[current_laser.y][current_laser.x] = "1"

                    else:  # no collision, move is valid
                        current_laser.move()
                        print("laser moved uninterrupted")
                        self.playGrid[current_laser.y
                                      ][current_laser.x] = "1"

                else:  # If next move is invalid e.g. hit B or go out of bounds

                    self.playGrid[current_laser.position[1]
                                  ][current_laser.position[0]] = "1"
                    print(len(all_lasers))
                    all_lasers.pop(0)
                    break

            for i in self.playGrid:
                print(i)

        if C_collision is not None:  # same as loop above, but for new C laser
            current_laser = C_collision
            current_laser.x = current_laser.position[0]
            current_laser.y = current_laser.position[1]
            print(f"current laser C_coll not none: {current_laser}")

            while current_laser.position[0] <= (len(self.playGrid[0]) - 1) and \
                    current_laser.position[1] <= (len(self.playGrid) - 1):

                next_move = np.add(current_laser.position,
                                   current_laser.velocity)
                print(f"current pos: {list(current_laser.position)}")
                print(f"next move is: {next_move}")
                # checking if next move is in grid. No need to check later.
                if self.is_valid(next_move):

                    check, direction, block_type = self.collision_check(
                        current_laser)  # tuple of Bool and type of block
                    # returns true if there is collision aka right,left,
                    # top,bottom in [a,b,c]
                    if check:
                        # Rotates the laser AND moves out. This is in case B
                        # kicks you out
                        C_collision = current_laser.collide(
                            self, block_type, direction)

                        self.playGrid[current_laser.y][current_laser.x] = "1"

                    else:  # no collision, move is valid
                        current_laser.move()
                        print("laser moved uninterrupted")

                        self.playGrid[current_laser.y
                                      ][current_laser.x] = "1"

                else:  # If next move is invalid e.g hit B or you go outside

                    self.playGrid[current_laser.position[1]
                                  ][current_laser.position[0]] = "1"
                    break
                # Go to next laser. break or not

            for i in self.playGrid:
                print(i)

    def is_valid(self, move):
        '''
        Checks if proposed move is valid i.e. in bounds
        '''
        if (
            (move[0] <= (len(self.playGrid[0]) - 1)) and
            (move[1] <= (len(self.playGrid) - 1)) and
            (move[0] >= 0 and move[1] >= 0)
        ):
            return True
        else:
            False

    def collision_check(self, current_laser):  # New one
        '''
        Once checked if next move is valid, this function checks if the laser
        has hit a block and adjusts its path accordingly
        '''
        # Order is important, it will never hit a top and left but may hit
        # left and right
        directions = []

        # adjust possible check directions to account for edge cases
        # X DIRECTION
        if current_laser.x == (len(self.playGrid[0]) - 1):
            left = {"left": self.playGrid[current_laser.y
                                          ][current_laser.x - 1]}
            directions.append(left)

        elif current_laser.x == 0:
            right = {"right": self.playGrid[current_laser.y
                                            ][current_laser.x + 1]}
            directions.append(right)

        else:
            left = {"left": self.playGrid[current_laser.y
                                          ][current_laser.x - 1]}
            right = {"right": self.playGrid[current_laser.y
                                            ][current_laser.x + 1]}
            directions.append(left)
            directions.append(right)

        # Y DIRECTION
        if current_laser.y == (len(self.playGrid) - 1):
            top = {"top": self.playGrid[current_laser.y -
                                        1][current_laser.x]}
            directions.append(top)

        elif current_laser.y == 0:
            bottom = {"bottom": self.playGrid[current_laser.y +
                                              1][current_laser.x]}
            directions.append(bottom)

        else:
            top = {"top": self.playGrid[current_laser.y -
                                        1][current_laser.x]}
            bottom = {"bottom": self.playGrid[current_laser.y +
                                              1][current_laser.x]}
            directions.append(top)
            directions.append(bottom)

        # check if there is an adjacent A, B, or C block #EDGE CASE, laser in
        # left AND right
        for each_direction in directions:
            for j in each_direction:
                # Don't know direction just that it collides or right in
                # {'A', 'B', 'C'} or top in {'A', 'B', 'C'} or bottom in
                # {'A', 'B', 'C'}:
                if each_direction.get(j) in {'A', 'B', 'C'}:
                    # returns tuple #j is the direction str, direction.get(i)
                    # is the block
                    return True, j, each_direction.get(j)

        # Returning 3 things because we unpack 3 outputs for the collide_check
        return False, None, None


class Block():
    '''
    Class for placeable blocks A/B/C
    '''

    def __init__(self, type_and_number, position=(0, 0)):
        '''
        type_and_number is a str
        position is a tuple initialized at (0,0)
        '''
        self.type = type_and_number[0]
        self.number = int(type_and_number[1:])
        self.position = position

    def __str__(self):
        return "-Block object"


class Laser():
    '''
    Class for moving laser with support for collisions with placeable blocks
    and transforming velocities accordingly
    '''

    def __init__(self, laser_attributes):

        self.x = laser_attributes[0]
        self.y = laser_attributes[1]
        self.vx = laser_attributes[2]
        self.vy = laser_attributes[3]
        self.start = (self.x, self.y)
        self.position = (self.x, self.y)
        self.velocity = [self.vx, self.vy]

    def __str__(self):
        return f"{[self.x,self.y,self.vx,self.vy]}"

    def move(self):  # Update laser position
        self.position = np.add(self.position, self.velocity)
        self.x = self.position[0]
        self.y = self.position[1]
        return

    def collide(self, lazor, block_type, direction):
        # Update the velocity based on block type AND move it.
        if block_type == "A":
            self.transform(direction)  # Rotate
            self.move()
            return
        elif block_type == "B":
            # set laser arbitrarily out of bounds so that movement ends here
            self.position = (999, 0)

        elif block_type == "C":
            # create new laser object in same position as when the laser hit
            # the C block, return to solver() with velocity before transform()
            # is called
            new_laser_obj = deepcopy(self)
            # need to move twice so that collision_checker() does not see
            # the same block over and over
            new_laser_obj.move()
            lazor.playGrid[new_laser_obj.y][new_laser_obj.x] = "1"
            new_laser_obj.move()
            new_laser_obj.start = (self.x, self.y)
            new_laser_obj.position = [new_laser_obj.x, new_laser_obj.y]

            self.transform(direction)
            self.move()

            return new_laser_obj

    def transform(self, direction):
        '''
        Transform updates ONLY the velocity of a laser.
        '''

        # If you hit the box horizontally (left or right) you multiply x by -1
        # if you hit the box vertically (top, bottom) you multiply y by -1

        if direction in ("left", "right"):
            self.velocity[0] = -1 * self.velocity[0]
        else:
            self.velocity[1] = -1 * self.velocity[1]

    def define(self):
        return [self.x, self.y, self.vx, self.vy]


class Play_Grid():  # Not really needed might delete later
    def __init__(self, playgrid_info):
        self.p = playgrid_info
        self.size = len(playgrid_info)

    def pos(self, x, y):  # Add a case where hte position next to you is out of bounds
        return self.p[y][x]  # flip so it's easier to write everytime

    def add_block(self, block_type, position):
        '''
        block_type is a string, A, B or C
        position is a tuple indicating where
        the block should go in the gird.
        '''
        self.p[position[1]][position[0]] = block_type
        return
