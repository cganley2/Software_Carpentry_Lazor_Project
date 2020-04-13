def win_condition_check(lazor_board):
    '''
    This function checks if a given playGrid has satisfied the puzzle win
    criteria i.e. all the points have been crossed by a laser
    '''
    if any('P' in row for row in lazor_board.playGrid):
        return False

    else:
        print('\n\n')
        print('Winning play grid:\n')
        for i in lazor_board.playGrid:
            print(i)
        return True
