import read_and_interpret_board as rib
import numpy as np
from copy import deepcopy

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
    This function simulates the laser's behavior on the grid.
    It deflects and moves the laser around by updating the laser's
    position and velocity.

    ** Parameters **
        self: ** Lazor_Solver Object **
            List m x n grid of x's and o's representing the SPACES in the board
            given by the input file
        
    ** Returns **
        None
        '''
        all_lasers = [Laser(each_laser) for each_laser in self.lasers]

        C_collision = None  # C_collision is a flag for if laser hits a C block

        while len(all_lasers) > 0:

            current_laser = all_lasers[0]
            current_laser.x = current_laser.position[0]
            current_laser.y = current_laser.position[1]
            
            # if laser hits B block, exit loop bc arbitrarily out of bounds
            if current_laser.position[0] > len(self.playGrid):
                all_lasers.pop(0)

            # while laser is in bounds, continue extending it
            while (current_laser.position[0] <= (len(self.playGrid[0]) - 1) and
                   current_laser.position[1] <= (len(self.playGrid) - 1)):

                next_move = np.add(current_laser.position,
                                   current_laser.velocity)

                # checking if next move is in grid.
                if self.is_valid(next_move):

                    check, direction, block_type = self.collision_check(
                        current_laser)

                    # accounts for case when block is adjacent laser start
                    if check and (self.playGrid[current_laser.position[1]
                                                ][
                            current_laser.position[0]] is not "L" or
                            block_type is "C"):

                        C_collision = current_laser.collide(
                            self, block_type, direction)

                        # extend laser past C block
                        if C_collision is not None:
                            if C_collision.x <= (
                                len(self.playGrid[0]) - 1
                            ) and \
                                    C_collision.x >= 0 and \
                                    C_collision.y <= (
                                        len(self.playGrid) - 1
                            ) and \
                                    C_collision.y >= 0:
                                self.playGrid[C_collision.y
                                              ][
                                    C_collision.x] = "1"
                        if current_laser.x <= (len(self.playGrid[0]) - 1) and \
                                current_laser.x >= 0 and \
                                current_laser.y <= (
                                    len(self.playGrid) - 1
                        ) and \
                                current_laser.y >= 0:
                            self.playGrid[current_laser.y
                                          ][
                                current_laser.x] = "1"

                    else:  # no collision, move is valid
                        current_laser.move()
                        self.playGrid[current_laser.y
                                      ][current_laser.x] = "1"

                else:  # If next move is invalid e.g. hit B or go out of bounds

                    self.playGrid[current_laser.position[1]
                                  ][current_laser.position[0]] = "1"
                    all_lasers.pop(0)
                    break

        if C_collision is not None:
            # Running new refracted "C" laser with same rules as above
            current_laser = C_collision
            current_laser.x = current_laser.position[0]
            current_laser.y = current_laser.position[1]

            while current_laser.position[0] <= (
                len(self.playGrid[0]) - 1
            ) and \
                    current_laser.position[1] <= (len(self.playGrid) - 1):

                next_move = np.add(current_laser.position,
                                   current_laser.velocity)

                if self.is_valid(next_move):

                    check, direction, block_type = self.collision_check(
                        current_laser)
                    if check:
                        C_collision = current_laser.collide(
                            self, block_type, direction)

                        self.playGrid[current_laser.y][current_laser.x] = "1"

                    else:  # no collision, move is valid
                        current_laser.move()

                        self.playGrid[current_laser.y
                                      ][current_laser.x] = "1"

                else:  # If next move is invalid e.g hit B or you go outside

                    self.playGrid[current_laser.position[1]
                                  ][current_laser.position[0]] = "1"
                    break


    def is_valid(self, move):
        '''
    This function determines whether a laser's move
    is valid(within the board).

    ** Parameters **
        self: * Lazor_Solver Object *
            List m x n grid of x's and o's representing the SPACES in the board
            given by the input file
        move: *list* *int*
            This is the coordinates of the next move of the laser
            in the form [x,y]        
    ** Returns **
        True or False: *Bool*
            Returns true if the move is within the grid else, false.
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
    This function determines whether a laser's move
    is valid(within the board).

    ** Parameters **
        self: ** Lazor_Solver Object **
            List m x n grid of x's and o's representing the SPACES in the board
            given by the input file
        current_laser: **Laser Object**
            This is the laser that is being checked.        
    ** Returns **
        True or False: **Bool**
            Returns true if the move is within the grid else, false.
        direction: **str**
            Returns the direction so that the laser rotater knows
            how to update the velocity/direction of the laser after
            a collision.
        each_directions.get(direction): **str**
            Returns the corresponding block to the direction.
            For example an A-block is on left so returns "A"
        None: **NoneType**
            If there is no collision.
        '''

        directions = []

        # X DIRECTION
        # We use a dictionary as a useful way to couple the direction
        # And the coordinates on the grid.
        # order matters because laser will never hit left and right,
        # but it may hit left and bottom for example
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

        for each_direction in directions:
            for dir_name in each_direction:
                if each_direction.get(dir_name) in {"A", "B", "C"}:
                    return True, dir_name, each_direction.get(dir_name)

        # Returning 3 items because we unpack 3 outputs for the collide_check
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
    The Laser class represents a laser that moves around
    the playgrid.

    ** Attributes **
        x: *int*
            positive x direction in grid.
        y: *int*
            positive y direction in grid.
        vx: *int*
            Velocity in x direction the sign of this
            parameter dictates where the laser moves.
            -1 or 1.
        vy: *int*
            Velocity in y direction the sign of this
            parameter dictates where the laser moves.
            -1 or 1.
        start:  *tuple* *int*
            Conains the start of the laser in an immutable
            tuple.
        position: *list* *int*
            Contains the x and y position of the laser.
        velocity: *list* *int*
            Contains the x and y velocities.

    ** Returns **
        None
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
        '''
        This function wraps the movement and rotation
        of a laser after it collides on a type of
        block.

        ** Parameters **
            self: ** Laser Object**
                Laser to undergo collision.
            lazor: *Lazor_Solver Object**
                The solver object is needed in order
                to have access to the playgrid and update
                with the laser's movement denoted by "1"
            block_type: *str*
                This is the blocktype upon which collision
                will occur.  
            direction: *str*
                The direction (left,right,top,bottom) that
                relative to the laser, where the collision
                is occuring.      
        ** Returns **
            new_laser: *Laser Object*
                If a C block is hit, then a new,
                refracted laser will be created and returned
        '''
        if block_type == "A":
            self.transform(direction)
            self.move()
            return
        elif block_type == "B":
            # set laser arbitrarily out of bounds so that movement ends here
            self.position = (999, 0)

        elif block_type == "C":
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
        This rotates the laser depending on which direction
        it is hitting either an A or C block. It does this
        by changin its velocity vx and vy.

        ** Parameters **
            self: * Laser Object*
                Laser to be rotated.
            direction: *str*
                This is the direction the laser is hit from.        
        ** Returns **
            None
        '''
        if direction in ("left", "right"):
            self.velocity[0] = -1 * self.velocity[0]
        else:
            self.velocity[1] = -1 * self.velocity[1]

    def define(self):
        return [self.x, self.y, self.vx, self.vy]
