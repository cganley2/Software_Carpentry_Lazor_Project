import copy

def print_board(board):
    '''
    This function simply prints the 2D list given to it to make it easier
    to visualize.
    '''
    for i in range(len(board)):
        print(board[i])


def generate_board(filename):
    '''
    This function generates a board and the relevant specifications given by
    an input file.

    **Parameters**

        filename: *str*
            name of the file that contains lazor board info

    **Returns**

        playGrid: *2D list* *str*
            list of strings of lazor/block location information. it is 2x the
            size (in both x and y directions) of the board variable indicated
            by GRID START/STOP to allow for whole number steps
        numReflect: *int*
            number of reflect blocks available
        numOpaque: *int*
            number of opaque blocks available
        numRefract: *int*
            number of refract blocks available
        lazors: *list* *int*
            list of ints of format <x, y, vx, vy> of lazor start
        points: *list* *int*
            list of ints of points that must be hit by lazors to complete level
    '''

    numReflect = 0
    numOpaque = 0
    numRefract = 0
    lazors = []
    points = []

    with open(filename, 'r') as f:

        lines = f.readlines()

        board = []
        playGrid = []

        for lineIndex in range(len(lines)):
            if '#' in lines[lineIndex]:
                pass
            else:
                if 'GRID START' in lines[lineIndex]:
                    gridStart = lineIndex
                if 'GRID STOP' in lines[lineIndex]:
                    gridStop = lineIndex

                # A/B/C inputs assume that there will never be more than 9 of
                # any kind of block in the puzzle, which I think is valid
                if 'A ' in lines[lineIndex]:
                    numReflect = int(lines[lineIndex][2])
                if 'B ' in lines[lineIndex]:
                    numOpaque = int(lines[lineIndex][2])
                if 'C ' in lines[lineIndex]:
                    numRefract = int(lines[lineIndex][2])

                if 'L ' in lines[lineIndex]:
                    lazors.append(lines[lineIndex].strip(' '))
                if 'P ' in lines[lineIndex]:
                    points.append(lines[lineIndex].strip(' '))

        for index in range(gridStart + 1, gridStop):
            row = []
            for char in lines[index]:
                if char is 'o' or char is 'x':
                    row.append(char)
            board.append(row)

        # this deep copy is to preserve the original board if it's needed ever
        boardCopy = copy.deepcopy(board)

        # generate playGrid by doubling dimensions in both x and y directions
        expandedRow = []
        for row in boardCopy:
            row[:] = [' ' if entry == 'o' else entry for entry in row]
            expandedRow = [item for item in row for i in range(2)]
            playGrid.append(expandedRow)
            playGrid.append(expandedRow)

        print('original board:')
        print_board(board)
        print('play grid:')
        print_board(playGrid)

    f.close()

    return playGrid, numReflect, numOpaque, numRefract, lazors, points
