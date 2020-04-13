def win_condition_check(lazor_board):
    '''
    This function checks if a given playGrid has satisfied the puzzle win
    criteria i.e. all the points have been crossed by a laser
    '''
    if any('P' in row for row in lazor_board.playGrid):
        return False

    else:  # if a winner is found, print playGrid and board
        print('\n\n')
        print('Winning play grid:\n')
        for row in lazor_board.playGrid:
            print(row)

        # convert playGrid to board for easy output
        lazor_board.board = [
            [
                lazor_board.playGrid[row][col]
                for col in range(1, len(lazor_board.playGrid[0]), 2
                                 )
            ]
            for row in range(1, len(lazor_board.playGrid), 2)
        ]

        print('\n\n')
        print('Winning board:\n')
        for row in lazor_board.board:
            print(row)
        print('\n')
        
        return True
