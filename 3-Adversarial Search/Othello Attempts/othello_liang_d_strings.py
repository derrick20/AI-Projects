import random, math

inf = math.inf
max_depth = 3 # subject to change
BORDER = '#'
SPACE = '.'
WHITE = 'O'
BLACK = 'X'
dir_lookup = {}
moves_lookup = {}

# initialize board with border as '#' and inside as '.'
def get_empty_board():
    board = ""
    for i in range(100):
        if is_edge(i):
            board += BORDER
        else:
            board += SPACE

    board = board[:44] + WHITE + board[45:]
    board = board[:54] + BLACK + board[55:]
    board = board[:45] + BLACK + board[46:]
    board = board[:55] + WHITE + board[56:]
    print(board[11])
    return board

def is_edge(i):
    return i < 10 or i > 90 or i % 10 == 0 or i % 10 == 9

def display_board(board):
    alpha = "_ABCDEFGH"
    print(" ", end='')
    for i in range(1, 9): # the top indicator
        print(i, end='')
    print()

    for i in range(11, 91, 10):  # go from 11 to 81, and each time go up 0 through 7
        print(alpha[i // 10], end='') # left indicator
        for j in range(8):
            print(board[i+j], end='')
        print()

def set_directions(board):
    directions = [-1, 1, -10, 10, -11, -9, 11, 9]  # 8 directions of the array
    global dir_lookup # 8 vectors of motion
    for i in range(11, 91, 10):
        for j in range(8):
            pos = i + j
            for delta in directions:
                if board[pos + delta] != BORDER:  # then this is a valid direction
                    if pos not in dir_lookup:  # regular dictionary setup to input all possible deltas
                        dir_lookup[pos] = [delta]
                    else:
                        dir_lookup[pos].append(delta)

    global moves_lookup # for each position, store a tuple of (pos, dir) which points to the list of positions it can go, specifically in that direction
    for pos in dir_lookup:
        for delta in dir_lookup[pos]:
            current = pos
            move = (pos, delta)
            while board[current + delta] != BORDER:
                current += delta

                if move not in moves_lookup:  # setup the moves_lookup and generate the path of moves on an empty board
                    moves_lookup[move] = [current]
                else:
                    moves_lookup[move].append(current)
    return dir_lookup, moves_lookup

def is_opposite(player, adj, board):
    if player == WHITE:
        return adj == BLACK
    else: # player is binary, so this is fine. If adj is a dot, it'll be false
        return adj == WHITE

def legal_moves_at_pos(pos, player, board):
    moves = set() # all positions reachable from pos by player on board
    for dir in dir_lookup[pos]: # in 8 directions
        if is_opposite(player, board[pos + dir], board): # then it may be jumpable
            #print(pos+dir, board[pos + dir])
            for move in moves_lookup[(pos, dir)]: # moves_lookup has strictly positions within board
                #print(moves_lookup[(pos, dir)])
                if board[move] == SPACE: # we kept traversing in that direction, until it was a stop
                    moves.add(move)
                    break
                elif board[move] == player: # that means we met ourself and can't go
                    break
    return moves # from list, pick one position

def get_my_moves(player, board): # list of tuples with pos, and direction
    my_moves = set() # avoid repeats TODO potentially sort this later for heuristic
    #print(board)
    for i in range(11, 91, 10):  # go from 11 to 81, and each time go up 0 through 7
        for j in range(8):
            pos = i + j
            if board[pos] == player:
                my_moves = my_moves | legal_moves_at_pos(pos, player, board)
    return list(my_moves)

def change_player(player):
    return WHITE if player == BLACK else BLACK

def make_move(move, player, board): # after picked a certain position, radiate out and see which may be valid (opposite)
    opponent = change_player(player)
    print(move) # TODO WTF
    pos = move  # move is pos, dir. From this point on, we don't care about the direction since we have placed a piece there
    board = board[:pos] + player + board[pos + 1:] # set it, and radiate out from it
    to_take = set() # pieces to flip

    for dir in dir_lookup[pos]: # radiate from that position to see if other pieces would be flanked
        might_take = set()
        if is_opposite(player, board[pos + dir], board):
            for piece in moves_lookup[(pos, dir)]: # continue all along that ray of direction from that point
                if board[piece] == player: # terminate the eating since we have finished flanking
                    to_take = to_take | might_take
                    break
                elif board[piece] == SPACE: # since we ended up not flanking, don't add to the taken set
                    break
                else: # because it's just an opponent to flank
                    might_take.add(piece)
                    continue
    # simply perform void action on a board
    for piece in to_take: # convert all pieces
        board = board[:piece] + player + board[piece+1:]
        # board[piece] = player
    return board

def count_pieces(player, board):
    return board.count(player)

def pick_move_random(my_moves):
    return my_moves[random.randint(0, len(my_moves) - 1)] # just some value

def open_eval(board):
    return len(get_my_moves(BLACK, board)) - len(get_my_moves(WHITE, board)) # maximize the mobility of the AI

def pick_move_minimax(board): # returns best position to move and the value of that position
    alpha = inf
    beta = -inf
    depth = 0
    return max_value(board, depth, alpha, beta) # kick off the recursion

def max_value(board, depth, alpha, beta):
    my_moves = get_my_moves(BLACK, board)
    if len(my_moves) == 0: # TODO time left/depth might need to add in
        return None, open_eval(board)
    if depth >= max_depth:
        return open_eval(board)
    best_move = -1 # just do this to start
    best_val = -inf
    for move in my_moves:
        print(move, my_moves, "hi")
        forecast = make_move(move, BLACK, board) # since it's a string, it just returns a new board
        dummy, value = min_value(forecast, depth + 1, alpha, beta)
        if value > best_val:
            best_val = value
            best_move = move
        if best_val >= beta: # this means that we've exceeded the upper bound for the parent min node, so they'll never pick us
            return best_move, best_val # what we return won't matter; we won't ever be picked
        alpha = max(alpha, best_val)
        if beta <= alpha: # not sure if it's right
            break
    return best_move, best_val

def min_value(board, depth, alpha, beta):
    my_moves = get_my_moves(WHITE, board)
    if len(my_moves) == 0:
        return None, open_eval(board)
    if depth >= max_depth:
        return -1, open_eval(board)
    best_move = -1
    best_val = inf
    for move in my_moves:
        print(move, my_moves, "hi")
        forecast = make_move(move, WHITE, board)
        dummy, value = max_value(forecast, depth + 1, alpha, beta)
        if value < best_val:
            best_val = value
            best_move = move
        if best_val <= alpha:
            return best_move, best_val
        beta = min(beta, best_val)
        if beta <= alpha:
            break
    return best_move, best_val

def terminal_test(board):
    if len(get_my_moves(WHITE, board)) == 0 and len(get_my_moves(BLACK, board)) == 0:
        return True

def play_game(board):
    current_player = BLACK # X starts
    skips = False
    while not terminal_test(board):
        opponent = change_player(current_player)
        my_moves = get_my_moves(current_player, board)
        opp_moves = get_my_moves(opponent, board)
        if len(my_moves) == 0 and len(opp_moves) == 0: # skip a turn
            break
        if len(my_moves) == 0:
            current_player = opponent
            continue
        if current_player == BLACK:
            move = pick_move_minimax(board) # black will perform minimax stuff
        else:
            move = pick_move_random(my_moves) # white will either be random or human
        board = make_move(move, current_player, board)
        display_board(board)
        current_player = opponent

    print("White had:", count_pieces(WHITE, board))
    print("Black had:", count_pieces(BLACK, board))

board = get_empty_board()
display_board(board)
dir_lookup, moves_lookup = set_directions(board)
play_game(board)

'''make_move(46, WHITE, board)
display_board(board)

print(get_my_moves(WHITE, board))
print(dir_lookup)
print(moves_lookup)'''