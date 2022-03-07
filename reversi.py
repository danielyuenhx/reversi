""" Reversi

Runs Reversi in the command line that can be played as 2-player
or 1-player VS CPU.
"""
__author__ = 'Daniel Yuen'

import copy

def new_board():
    """Creates a new board to be played on."""
    board = [[0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,2,1,0,0,0],
    [0,0,0,1,2,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]]
    return board

def score(board):
    """
    Calculates the score of both players based on the
    current state of the board
    """
    s1 = 0
    s2 = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                s1 += 1
            if board[i][j] == 2:
                s2 += 1
    return (s1,s2)
    
def print_board(board):
    """Prints out current board state to the command line""" 
    print('   +---+---+---+---+---+---+---+---+')
    for i in range(8): 
        print('',(i+1), end = ' '), 
        for j in range(8):
            if board[i][j] == 0: 
                print('|  ', end = ' ') 
            elif board[i][j] == 1:
                print('| B', end = ' ') 
            else:
                print('| W', end = ' ')
        print('|') 
        print('---+---+---+---+---+---+---+---+---+')
    print('   | a | b | c | d | e | f | g | h')

def on_board(y,x):
    """
    Recieves a position on the board and returns False if out
    of bounds
    """
    if y >= 0 and y <= 7 and x >= 0 and x <= 7:
        return True
    else:
        return False

def enclosing(board,player,pos,dir):
    """
    Returns True if a move can be made in that position,
    False otherwise
    """

    #converts tuples to integers
    y = pos[0] 
    x = pos[1]
    y_dir = dir[0]
    x_dir = dir[1]

    if player == 1:
        enemy = 2
    elif player == 2:
        enemy = 1
    #if position is not empty, returns False
    if board[y][x] != 0: 
        return False

    x += x_dir 
    y += y_dir

    #checks if adjacent position is inside bounds
    #and contains an opposing stone
    if on_board(y,x) and board[y][x] == enemy: 
        #loops the move in the direction as long as
        #inside bounds and contains an opposing stone
        while on_board(y,x) and board[y][x] == enemy: 
            y += y_dir
            x += x_dir
            #returns True if remains inside bounds and meets another
            #player stone
            if on_board(y,x) and board[y][x] == player: 
                return True
            #returns False if goes out of bounds or meets an empty spot
            elif not on_board(y,x) or board[y][x] == 0: 
                return False
    else:
        return False 
        
def valid_pos(board,player,pos):
    """
    Returns True if a valid move can be made in a position
    and False otherwise
    """

    #checks in all directions
    for dir in [(1,0),(0,1),(1,1),(-1,0),(0,-1),(-1,-1),(-1,1),(1,-1)]: 
        if enclosing(board,player,pos,dir) == True:
            return True
        else:
            continue
            
def valid_moves(board,player):
    """
    Returns a list containing valid moves that can be made
    by a player
    """
    
    list = []
    
    for y in range(8): #checks every spot on the board
        for x in range(8):
            #checks whether if a valid move can be made in a
            #certain position
            if valid_pos(board,player,(y,x)) == True: 
                list.append((y,x))
    return list

def valid_dir(board,player,pos):
    """
    Returns a list containing valid direction(s) of a valid
    move similar to valid_pos but instead returns valid directions
    instead of Boolean
    """
    
    list_dir = [] 
    
    for dir in [(1,0),(0,1),(1,1),(-1,0),(0,-1),(-1,-1),(-1,1),(1,-1)]:
        if enclosing(board,player,pos,dir) == True:
            list_dir.append(dir)
        else:
            continue
    return list_dir
        
def flipstones(board,player,pos,dir):
    """
    Returns a board with opposing stones flipped according
    to current player's move
    """
    
    y = pos[0] 
    x = pos[1]
    y_dir = dir[0]
    x_dir = dir[1]
    n = 0
    
    y += y_dir
    x += x_dir

    if player == 1:
        enemy = 2
    elif player == 2:
        enemy = 1

    while board[y][x] == enemy: #flips enemy stones to current player stones        
        board[y][x] = player 
        y += y_dir 
        x += x_dir
        
        if board[y][x] == player: #stops when it meets a current player stone
            break

    return board
    
def next_state(board,player,pos):
    """
    Returns the next board configuration resulting from the current
    player's move and the configuration (1 or 2) of the next player
    """
    
    if valid_pos(board,player,pos) == True:
        y = pos[0]
        x = pos[1]

        #takes all valid directions to flip
        for dir in valid_dir(board,player,pos): 
            board = flipstones(board,player,pos,dir)
        board[y][x] = player #changes the empty spot to a player stone
        next_board = board

        if player == 1: 
            next_player = 2
        elif player == 2:
            next_player = 1
            
        return next_board,next_player

    #returns next_player = 0 if it is not a valid move
    elif valid_pos(board,player,pos) == False: 
        next_player = 0
        next_board = board
        return next_board,next_player
        
def position(string):
    """
    Changes player input into a list of lists form,
    returns None otherwise
    """

    letters = ['a','b','c','d','e','f','g','h']
    num = [0,1,2,3,4,5,6,7]

    #ensures that input is in the form of (letter)(number)
    if len(string) == 2:
        if str.isdigit(string[0]) == False and str.isdigit(string[1]) == True: 
            letter = string[0]
            number = int(string[1])

            #ensures letters and numbers are valid
            if letter not in letters or number - 1 not in range(8): 
                return None

            else:
                index = letters.index(letter)
                y = number - 1
                x = num[index]

                pos = (y,x)
                return pos
        else:
            return None
    else:
        return None

def end_game(board):
    """returns True if there are no more moves to be made by both players"""
    if valid_moves(board,1) == [] and valid_moves(board,2) == []:
        return True
    else:
        return False

def player_check(board,player):
    """Returns False if a player has no more moves to be made"""
    if valid_moves(board,player) == []:
        return False
    else:
        return True
                
def run_two_players():
    """Runs the game for two players"""
    board = new_board() 
    next_player = 1

    while True: #ensures player input is valid before proceeding
        colour = input('Which player goes first? (white or black) ')
        if colour == 'white':
            player = 2
            break
        elif colour == 'black':
            player = 1
            break
        else:
            print('Not valid.')
    
    while end_game(board) == False: #ensures there are always moves to be made
        print_board(board)

        if player == 1:
            print("It is black's turn to move.")
            temp = 2
        elif player == 2:
            print("It is white's turn to move.")
            temp = 1

        #if current player cannot make any valid moves, skips turn
        if player_check(board,player) == False: 
            player = temp
            print(str.capitalize(colour)+' has no valid moves.')
            continue

        move = input('Input a position to drop a stone :')
        if move == 'q':
            break
        
        pos = position(move) #converts position to readable format

        if pos == None:
            print('Invalid move.')
            continue
        elif (pos[0],pos[1]) in valid_moves(board,player): 
            next_board,next_player = next_state(board,player,pos)
            player = next_player
            board = next_board
        else:
            print('Invalid move.')

    #if end_game(board) == True, prints out final board configuration
    #and displays the score
    print_board(board) 
    print('Player 1 (black) has a score of '+str(score(board)[0])+'.')
    print('Player 2 (white) has a score of '+str(score(board)[1])+'.')
    if score(board)[0] >= score(board)[1]:
        print('Player 1 wins!')
    elif score(board)[0] == score(board)[1]:
        print('Tie!')
    else:
        print('Player 2 wins!')

def duplicate_board(board):
    """
    Creates a duplicate board to be altered, since using the
    original board will change all lists referencing the original board
    """

    duplicate = new_board()

    for i in range(8):
        for j in range(8):
            duplicate[i][j] = board[i][j]
    return duplicate
    
def best_choice(board,player):
    """
    Returns the position for the first greatest score
    possible for a certain turn
    """

    scores_list = []
    moves_list = []
    
    for moves in valid_moves(board,player):
        duplicate = duplicate_board(board)
        next_board = next_state(duplicate,player,(moves))
        
        scores = score(duplicate)[1] 
        scores_list.append(scores) #appends the scores and respective moves to two lists
        moves_list.append(moves)

    #prevents error from occuring by retrieving index if list is empty
    if scores_list == []: 
        pos = []
        return pos

    index = scores_list.index(max(scores_list))
    pos = moves_list[index] #retrieves the position with greatest score

    return pos

def location(pos):
    """Returns a computer-readable coordinate into a human-readable form"""

    letters = ['a','b','c','d','e','f','g','h']
    num = [0,1,2,3,4,5,6,7]
    
    x = int(pos[0]) + 1 

    for i in range(len(num)):
        if pos[1] == num[i]:
            y = letters[i]
        else:
            continue

    return y,str(x)
             
def run_single_player():
    """
    Runs the game for single player vs CPU
    where Player 1 is a human and Player 2 is the computer
    """

    board = new_board()
    player = 1
    
    while True:
        first = input('Who goes first? (player or computer) ')
        if first == 'player':
            player = 1
            break
        elif first == 'computer':
            player = 2
            break
        else:
            print('Not valid.')

    while end_game(board) == False: 
        print_board(board)

        if player == 1:
            print("It is black's turn to move.")
            temp = 2
        if player == 2:
            print("It is white's turn to move.")
            temp = 1

        if player_check(board,player) == False:
            player = temp
            print(str.capitalize(first)+' has no valid moves.')
            continue

        if player == 1: 
            move = input('Input a position to drop a stone :')
            if move == 'q':
                break

            pos = position(move)

            if pos == None:
                print('Invalid move.')
                continue
            elif (pos[0],pos[1]) in valid_moves(board,player): 
                next_board,next_player = next_state(board,player,pos)
                player = next_player
                board = next_board
            else:
                print('Invalid move.')
        
        elif player == 2:
            #computer chooses the first position with highest
            #score for given turn
            bot_pos = best_choice(board,player)
            if bot_pos == []:
                break
            else:
                next_board,next_player = next_state(board,player,bot_pos)

                #converts coordinates into human-readable format
                loc = location(bot_pos) 
                print('Computer places white stone at '+loc[0]+loc[1]+'.')

                player = next_player
                board = next_board
                
    print_board(board)
    print('Player (black) has a score of '+str(score(board)[0])+'.')
    print('Computer (white) has a score of '+str(score(board)[1])+'.')

    if score(board)[0] >= score(board)[1]:
        print('Player wins!')
    elif score(board)[0] == score(board)[1]:
        print('Tie!')
    else:
        print('Computer wins!')


if __name__ == '__main__':
    game=input('Would you like to play 2-player or vs CPU? (1/2)\n')
    while game != '1' and game != '2':
        game=input('Please input a valid response. "\
        \nWould you like to play two players or vs CPU? (1/2)\n')

    if game == '1':
        run_two_players()
    elif game == '2':
        run_single_player()
    

