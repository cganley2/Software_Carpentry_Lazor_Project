import read_and_interpret_board as rib
import numpy as np
from copy import deepcopy
# Current Problems: laser.x and .y don't eveolve at same rate as laser.position. Should I just make laser.x/y constant?
#.x and .y updated during laser.move() but not during laser pop
# When laser changes, .x and .y are not updated
# Block C is still issue


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
        self.block_types = [[blocks[i][0]] * int(blocks[i][1]) for i in range(len(blocks))]
        self.lasers = lasers
        self.points = points
        self.path = [[(lasers[i][0], lasers[i][1])]  # could not find use for this yet.
                     for i in range(len(lasers))]  # the laser location and not direction x,y
        self.playGrid = playGrid
        # self.c_lasers = [[1,0,0,0]]
        # self.extend_lazor()
        self.solver()

    def solver(self):
        # Has to be up here otherwise we are re-storing all lases in while loop each time
        all_lasers = [Laser(each_laser) for each_laser in self.lasers]
        C_collision = None
        # print(all_lasers)
        while len(all_lasers) > 0:
            # Updates the current laser must be relating to all_laser list we defined above
            current_laser = all_lasers[0]
            current_laser.x = current_laser.position[0]
            current_laser.y = current_laser.position[1]
            # Once laser popped (cos met B or went outside, current laser should come bak here)
            #current_grid = Play_Grid
            print(f"current laser: {current_laser}")

            if current_laser.position[0] > len(self.playGrid):
                all_lasers.pop(0)

            while current_laser.position[0] <= (len(self.playGrid[0]) - 1) and \
                    current_laser.position[1] <= (len(self.playGrid) - 1):
                # TODO
                # print(type(current_laser))
                next_move = np.add(current_laser.position,
                                   current_laser.velocity)
                print(f"current pos: {list(current_laser.position)}")
                print(f"next move is: {next_move}")
                # checking if next move is in grid. No need to check later.
                if self.is_valid(next_move):
                    # TODO: Laser should immediately move, an edge case is if next_move is a block. Overaccounted for this edge case.
                    # TODO 2: Laser should immediately move, otherwise edge case where laer stats at edge will check everywhere and index erro will ovvur
                    check, direction, block_type = self.collision_check(
                        current_laser)  # tuple of Bool and type of block
                    # returns true if there is collision aka right,left,top,bottom in [a,b,c]
                    if check:
                        # Rotates the laser AND moves out. This is incase B kicks you out
                        C_collision = current_laser.collide(block_type, direction)
                        if C_collision is not None:
                            print("zabadoo")
                            print(C_collision.velocity)
                            self.playGrid[C_collision.y][C_collision.x] = "1"
                            self.playGrid[C_collision.y - C_collision.vy][C_collision.x - C_collision.vx] = "1"
                            # self.playGrid[C_collision.start[1]][C_collision.start[0]] = "1"
                        # current_laser.move()
                        # There is no need for a is_valid check for next move because next move after collision is ALWAYS valid
                        # Except B which will ideally break the while loop
                        # laser.path.append(laser.position)# Now add your new point to path
                        self.playGrid[current_laser.y][current_laser.x] = "1"
                    else:  # no collision, move is valid
                        current_laser.move()
                        print("laser moved uninterrupted")
                        # pseudocode
                        self.playGrid[current_laser.y
                                      ][current_laser.x] = "1"
                        # laser.path.append(laser.position)
                else:  # If next move is invalid. Eg you hit B or you go outside.
                    # current_laser.move()
                    self.playGrid[current_laser.position[1]
                                  ][current_laser.position[0]] = "1"
                    print(len(all_lasers))
                    # From the list of Laser OBject we created
                    all_lasers.pop(0)
                    # print("POP POP!")
                    # print(f"Number of lasers left: {len(all_lasers)}")
                    break
                # Go to next laser. break or not
            for i in self.playGrid:
                print(i)

        if C_collision is not None:
            current_laser = C_collision
            current_laser.x = current_laser.position[0]
            current_laser.y = current_laser.position[1]
            # Once laser popped (cos met B or went outside, current laser should come bak here)
            #current_grid = Play_Grid
            print(f"current laser: {current_laser}")

            while current_laser.position[0] <= (len(self.playGrid[0]) - 1) and \
                    current_laser.position[1] <= (len(self.playGrid) - 1):
                # TODO
                # print(type(current_laser))
                next_move = np.add(current_laser.position,
                                   current_laser.velocity)
                print(f"current pos: {list(current_laser.position)}")
                print(f"next move is: {next_move}")
                # checking if next move is in grid. No need to check later.
                if self.is_valid(next_move):
                    # TODO: Laser should immediately move, an edge case is if next_move is a block. Overaccounted for this edge case.
                    # TODO 2: Laser should immediately move, otherwise edge case where laer stats at edge will check everywhere and index erro will ovvur
                    check, direction, block_type = self.collision_check(
                        current_laser)  # tuple of Bool and type of block
                    # returns true if there is collision aka right,left,top,bottom in [a,b,c]
                    if check:
                        # Rotates the laser AND moves out. This is incase B kicks you out
                        C_collision = current_laser.collide(block_type, direction)
                        # current_laser.move()
                        # There is no need for a is_valid check for next move because next move after collision is ALWAYS valid
                        # Except B which will ideally break the while loop
                        # laser.path.append(laser.position)# Now add your new point to path
                        self.playGrid[current_laser.y][current_laser.x] = "1"
                    else:  # no collision, move is valid
                        current_laser.move()
                        print("laser moved uninterrupted")
                        # pseudocode
                        self.playGrid[current_laser.y
                                      ][current_laser.x] = "1"
                        # laser.path.append(laser.position)
                else:  # If next move is invalid. Eg you hit B or you go outside.
                    # current_laser.move()
                    self.playGrid[current_laser.position[1]
                                  ][current_laser.position[0]] = "1"
                    # print(len(all_lasers))
                    # From the list of Laser OBject we created
                    # all_lasers.pop(0)
                    # print("POP POP!")
                    # print(f"Number of lasers left: {len(all_lasers)}")
                    break
                # Go to next laser. break or not
            for i in self.playGrid:
                print(i)


    def is_valid(self, move):  # works
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
        Once checked if next move is valid, This function checks if the laser has hit a block and adjusts its path
        accordingly
        '''
        # FROM NOW ON: We will use laser position as indication not the playgrid position.
        # Playgrid will be edited by laser until it goes out or winning condition is found

        # Order is important, it will never hit a top and left but may hit left and right
        directions = []

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

        # check if there is an adjacent A,B or C block #EDGE CASE, laser in left AND right
        for each_direction in directions:
            for j in each_direction:
                # Don't know direction just that it collides or right in {'A', 'B', 'C'} or top in {'A', 'B', 'C'} or bottom in {'A', 'B', 'C'}:
                if each_direction.get(j) in {'A', 'B', 'C'}:
                    # print("oi")
                    # returns tuple #i is the direction str, direction.get(i) is the block
                    return True, j, each_direction.get(j)
        # Returning 3 things because we unpack 3 outputs for the collide_check
        return False, None, None


class Block():
    '''
    Block class.
    '''

    def __init__(self, type_and_number, position=(0, 0)):
        '''
        type_and_number is a str
        position is a tuple initialized at (0,0)
        '''
        self.type = type_and_number[0]
        # will use this to create block in a for loop
        self.number = int(type_and_number[1:])
        self.position = position

    def __str__(self):
        return "-Block object"


class Laser():
    '''
    Laser class.
    '''

    def __init__(self, laser_attributes):

        self.x = laser_attributes[0]  # Does nnot currently change
        self.y = laser_attributes[1]  # Does nnot currently change
        self.vx = laser_attributes[2]
        self.vy = laser_attributes[3]
        self.start = (self.x, self.y)
        self.position = (self.x, self.y)  # changes
        self.velocity = [self.vx, self.vy]

    def __str__(self):
        return f"{[self.x,self.y,self.vx,self.vy]}"

    def move(self):  # Update laser position
        self.position = np.add(self.position, self.velocity)
        #self.x,self.y = np.add([self.x,self.y] , self.velocity)
        self.x = self.position[0]
        self.y = self.position[1]
        return

    def collide(self, block_type, direction):
        # Update the velocity based on block type AND move it.
        if block_type == "A":
            # print("hit A block")
            self.transform(direction)  # Rotate
            # No need to valid_check, always valid
            # But Should probably check collision before moving
            self.move()
            return
        elif block_type == "B":
            # make it go out of bounds #Make playGrid a parameter of laser or object TODO change to a better check
            self.position = (1000 + 1, 0)

        elif block_type == "C":
            new_laser_obj = deepcopy(self)
            new_laser_obj.move()
            new_laser_obj.move()
            new_laser_obj.start = (self.x, self.y)
            new_laser_obj.position = [new_laser_obj.x, new_laser_obj.y]
            print('collide C collision')
            # new_laser_obj.move()
            # new_laser_obj.move()
            print(str(self))
            print(new_laser_obj.start)
            # new_laser = [
            #             new_laser_obj.x,
            #             new_laser_obj.y,
            #             new_laser_obj.vx,
            #             new_laser_obj.vy
            #             ]
            # lazor.lasers.append(new_laser)  # Saving for later TODO might bump into itself
            self.transform(direction)
            # Should probably check collision before moving
            # np.add(self.position, self.velocity) # Pass thru the block.
            self.move()
            # This new laser should collide and move one step. So that the time we handle the laser it will be away from C
            return new_laser_obj

    def transform(self, direction):
        # transform() updates ONLY the velocity of a laser, periodt.

        # If you hit the box horizontally (left or right) you multiply x by -1
        # if you hit the box vertically (top, bottom) you multiply y by -1

        if direction in ("left", "right"):
            # print("hit from left or right!")
            self.velocity[0] = -1 * self.velocity[0]
        else:  # direction in ("top", "bottom"):
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
