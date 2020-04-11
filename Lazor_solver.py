import read_and_interpret_board as rib
import numpy as np
#Current Problems: laser.x and .y don't eveolve at same rate as laser.position. Should I just make laser.x/y constant?
#.x and .y updated during laser.move() but not during laser pop
#When laser changes, .x and .y are not updated
#Block C is still issue

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
        self.path = [[(lasers[i][0], lasers[i][1])] # could not find use for this yet.
                     for i in range(len(lasers))] # the laser location and not direction x,y
        self.playGrid = playGrid
        # self.c_lasers = [[1,0,0,0]]
        #self.extend_lazor()
        self.solver()

    def solver(self):
        all_lasers = [Laser(each_laser) for each_laser in self.lasers] # Has to be up here otherwise we are re-storing all lases in while loop each time
        while len(all_lasers) > 0: 
        
            current_laser = all_lasers[0] # Updates the current laser must be relating to all_laser list we defined above
            current_laser.x = current_laser.position[0]
            current_laser.y = current_laser.position[1]
            #Once laser popped (cos met B or went outside, current laser should come bak here)
            #current_grid = Play_Grid
            print(f"current laser: {current_laser}")

            while current_laser.position[0] < (len(self.playGrid) - 1) and current_laser.position[1] < (len(self.playGrid) - 1):
                #TODO
                print(type(current_laser))
                next_move = np.add(current_laser.position, current_laser.velocity)
                print(f"current pos: {list(current_laser.position)}")
                print(f"next move is: {next_move}")
                if self.is_valid(next_move): #checking if next move is in grid. No need to check later.
                    #TODO: Laser should immediately move, an edge case is if next_move is a block. Overaccounted for this edge case.
                    #TODO 2: Laser should immediately move, otherwise edge case where laer stats at edge will check everywhere and index erro will ovvur
                    check, direction, block_type = self.collision_check(current_laser) #tuple of Bool and type of block
                    if check: #returns true if there is collision aka right,left,top,bottom in [a,b,c]
                        current_laser.collide(block_type, direction) # Rotates the laser AND moves out. This is incase B kicks you out
                        #There is no need for a is_valid check for next move because next move after collision is ALWAYS valid
                        #Except B which will ideally break the while loop
                        #laser.path.append(laser.position)# Now add your new point to path
                        self.playGrid[current_laser.y][current_laser.x] = "1"
                    else: #no collision, move is valid
                        current_laser.move()
                        print("laser moved uninterrupted")
                        self.playGrid[current_laser.position[1]][current_laser.position[0]] = "1" #pseudocode
                        #laser.path.append(laser.position)
                else: #If next move is invalid. Eg you hit B or you go outside. 
                    current_laser.move()
                    self.playGrid[current_laser.position[1]][current_laser.position[0]] = "1"
                    print(len(all_lasers))
                    all_lasers.pop(0) # From the list of Laser OBject we created
                    print("POP POP!")
                    print(f"Number of lasers left: {len(all_lasers)}")
                    break
                # Go to next laser. break or not
            for i in self.playGrid:
                print(i)
        
    def is_valid(self, move): # works
        if ((move[0] < (len(self.playGrid) - 1)) and (move[1] < (len(self.playGrid) - 1)) and (move[0] >= 0 and move[1] >= 0)):
            return True 
        else:
            print("outta bound")
            False

    def collision_check(self, current_laser): #New one
        '''
        Once checked if next move is valid, This function checks if the laser has hit a block and adjusts its path
        accordingly
        '''
        #FROM NOW ON: We will use laser position as indication not the playgrid position.
        # Playgrid will be edited by laser until it goes out or winning condition is found 
        if (
            current_laser.x < (len(self.playGrid) - 1) and
            current_laser.y < (len(self.playGrid) - 1)
        ):
           
            # direction : value
            left = {"left" : self.playGrid[current_laser.y
                                 ][current_laser.x - 1]}
            top = {"top" : self.playGrid[current_laser.y -
                                1][current_laser.x]}
            right = {"right": self.playGrid[current_laser.y
                                  ][current_laser.x + 1]}
            bottom = {"bottom" : self.playGrid[current_laser.y +
                                   1][current_laser.x]}
            directions = [left,right,top,bottom] #Order is important, it will never hit a top and left but may hit left and right

            # check if there is an adjacent A,B or C block #EDGE CASE, laser in left AND right
            for each_direction in directions:
                for j in each_direction:
                    if each_direction.get(j) in {'A', 'B', 'C'}: #  Don't know direction just that it collides or right in {'A', 'B', 'C'} or top in {'A', 'B', 'C'} or bottom in {'A', 'B', 'C'}:
                        print("oi")
                        return True,j, each_direction.get(j) #returns tuple #i is the direction str, direction.get(i) is the block
            return False, None, None # Returning 3 things because we unpack 3 outputs for the collide_check


# Old collision checker
    # def collision_checker(self, i_laser):
    #     '''
    #     This function checks if the laser has hit a block and adjusts its path
    #     accordingly
    #     '''
    #     if (
    #         self.current_point[0] < (len(self.playGrid) - 1) and
    #         self.current_point[1] < (len(self.playGrid) - 1)
    #     ):
    #         left = self.playGrid[self.current_point[1]
    #                              ][self.current_point[0] - 1]
    #         top = self.playGrid[self.current_point[1] -
    #                             1][self.current_point[0]]
    #         right = self.playGrid[self.current_point[1]
    #                               ][self.current_point[0] + 1]
    #         bottom = self.playGrid[self.current_point[1] +
    #                                1][self.current_point[0]]

    #         # check if hit movable block on LEFT side
    #         if left in {'A', 'B', 'C'}:
    #             if left is 'A': # change laser velocity
    #                 self.velocity[0] = -1 * self.velocity[0]
    #             elif left is 'B': # set position arbitrarily out of bounds
    #                 self.current_point = (len(self.playGrid) + 1, 0)
    #             else: # can't figure out how to account for C blocks
    #                 self.lasers.append(
    #                     [
    #                         self.current_point[1],
    #                         self.current_point[0],
    #                         -1 * self.velocity[0],
    #                         self.velocity[1]
    #                     ]
    #                 )
    #         # TOP check
    #         elif top in {'A', 'B', 'C'}:
    #             if top is 'A':
    #                 self.velocity[1] = -1 * self.velocity[1]
    #             elif top is 'B':
    #                 self.current_point = (len(self.playGrid) + 1, 0)
    #             else: # TRYING TO FIX C: new laser created will ALWAYS start at C by definition: WILL have to automate C reflection
    #                 print(self.lasers)
    #                 if i_laser in self.c_lasers:
    #                     print("oi")
    #                     self.velocity[1] = -1 * self.velocity[1] #behave like A
    #                     self.c_lasers = [[0,0,0,0]]

    #                 else:
    #                     print(f"i_laser is {i_laser}")
    #                     print(f"Running {self.lasers} Nothing is in c_lasers ")
    #                     self.lasers.append(
    #                         [
    #                             self.current_point[0],
    #                             self.current_point[1],
    #                             self.velocity[0],
    #                             self.velocity[1]
    #                         ]
    #                     )
    #                     self.c_lasers.pop()  # remove current c_laser & replace
    #                     self.c_lasers.append(
    #                         [
    #                             self.current_point[0],
    #                             self.current_point[1],
    #                             self.velocity[0],
    #                             self.velocity[1]
    #                         ]
    #                     )
    #                 print(self.c_lasers)
    #                 pass #We are going to create a new laser and make the old one pass through C
    #                 print(self.lasers) 
    #         # RIGHT check
    #         elif right in {'A', 'B', 'C'}:
    #             if right is 'A':
    #                 self.velocity[0] = -1 * self.velocity[0]
    #             elif right is 'B':
    #                 self.current_point = (len(self.playGrid) + 1, 0)
    #             else:
    #                 print(self.lasers)
    #                 print(self.lasers[-1])
    #                 if i_laser in self.c_lasers: #ROBUST
    #                     print("c is on right but we have already went through c")
    #                     self.velocity[1] = -1 * self.velocity[1]
    #                     self.c_lasers = [[0,0,0,0]]
    #                 elif [self.lasers[-1]] == self.c_lasers:
    #                     print("Passed through C-block, now getting out")  # NEED to change for more lasers
    #                     #self.current_point = np.add(self.current_point, self.velocity) #moving back because the while loop will move us forward
    #                     pass


    #                 else:
    #                     print(f"i_laser is {i_laser}")
    #                     print(f"Running {self.lasers} Nothing is in c_lasers ")
    #                     self.lasers.append(
    #                         [
    #                             self.current_point[0],
    #                             self.current_point[1],
    #                             self.velocity[0],
    #                             self.velocity[1]
    #                         ]
    #                     )
    #                     self.c_lasers.pop()  # remove current c_laser & replace
    #                     self.c_lasers.append(
    #                         [
    #                             self.current_point[0],
    #                             self.current_point[1],
    #                             self.velocity[0],
    #                             self.velocity[1]
    #                         ]
    #                     )
    #                 print(self.c_lasers)
    #                 pass #We are going to create a new laser and make the old one pass through C
    #                 print(self.lasers) 
    #                 print("c on right")
                    

    #         # BOTTOM check
    #         elif bottom in {'A', 'B', 'C'}:
    #             if bottom is 'A':
    #                 self.velocity[1] = -1 * self.velocity[1]
    #             elif bottom is 'B':
    #                 self.current_point = (len(self.playGrid) + 1, 0)
    #             else:
    #                 pass

class Block():
    '''
    Block class.
    '''
    def __init__(self, type_and_number, position=(0,0)):
        '''
        type_and_number is a str
        position is a tuple initialized at (0,0)
        '''
        self.type = type_and_number[0]
        self.number = int(type_and_number[1:]) #will use this to create block in a for loop
        self.position = position
    def __str__(self):
        return "-Block object"

class Laser():
    '''
    Laser class.
    '''
    def __init__(self, laser_attributes):

        self.x = laser_attributes[0] # Does nnot currently change
        self.y = laser_attributes[1] # Does nnot currently change
        self.vx = laser_attributes[2]
        self.vy = laser_attributes[3]
        self.start = (self.x,self.y)
        self.position = (self.x, self.y) #changes
        self.velocity = [self.vx, self.vy]

    def __str__(self):
        return f"{[self.x,self.y,self.vx,self.vy]}"

    def move(self): # Update laser position
        self.position = np.add(self.position, self.velocity)
        #self.x,self.y = np.add([self.x,self.y] , self.velocity)
        self.x = self.position[0]
        self.y = self.position[1]
        return

    def collide(self, block_type, direction):
        # Update the velocity based on block type AND move it.
        if block_type == "A":
            print("hit A block")
            self.transform(direction) # Rotate
            #No need to valid_check, always valid
            #But Should probably check collision before moving
            self.move()
            return
        elif block_type == "B":
            self.position = (1000 + 1, 0) #make it go out of bounds #Make playGrid a parameter of laser or object TODO change to a better check

        else:
            lasers.append(self) #Saving for later TODO might bump into itself
            self.transform(direction)
            #Should probably check collision before moving
            self.move()  # np.add(self.position, self.velocity) # Pass thru the block.
            # This new laser should collide and move one step. So that the time we handle the laser it will be away from C
            return 
    
    def transform(self, direction):
        # transform() updates ONLY the velocity of a laser, periodt.

        #If you hit the box horizontally (left or right) you multiply x by -1
        #if you hit the box vertically (top, bottom) you multiply y by -1
        
        if direction in ("left", "right"):
            print("hit from left or right!")
            self.velocity[0] = -1 * self.velocity[0]
        else: #direction in ("top", "bottom"):
                self.velocity[1] = -1 * self.velocity[1]

    def define(self):
        return [self.x,self.y,self.vx,self.vy]

class Play_Grid(): #Not really needed might delete later 
    def __init__(self, playgrid_info):
        self.p = playgrid_info
        self.size = len(playgrid_info)

    def pos(self, x,y): #Add a case where hte position next to you is out of bounds
        return self.p[y][x] #flip so it's easier to write everytime
    
    def add_block(self, block_type, position):
        '''
        block_type is a string, A, B or C
        position is a tuple indicating where
        the block should go in the gird.
        '''
        self.p[position[1]][position[0]] = block_type
        return

if __name__ == "__main__":
    board, blocks, lasers, points, playGrid = rib.board_interpretor(
        rib.read_bff_file("../mad_7"), verbose=True)
    playGrid[3][7] = 'A'
    playGrid[1][5] = 'A'
    playGrid[3][3] = "A"
    lazor = Lazor_solver(board, blocks, lasers, points, playGrid)
    print(lazor.path)
