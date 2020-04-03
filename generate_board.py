import copy

def print_board(board):
    for i in range(len(board)):
        print(board[i])


def generate_board(filename):

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

        boardCopy = copy.deepcopy(board)

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


generate_board('mad_7.bff')
