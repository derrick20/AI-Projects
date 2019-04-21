import random, math, time

BORDER = '#' # '?'
SPACE = '.'
WHITE = 'O'
BLACK = 'X' # '@'
dir_lookup = {} # pos -> valid directions (1, -1, 11, etc)
moves_lookup = {} # pos -> all positions reachable (like queen)
inf = math.inf
AI = BLACK
OPP = WHITE
stability_table = []
'''
[
'', '', '', '', '', '', '', '', '', '',
'', 200, -100, 100,  50,  50, 100, -100,  200, '',
'', -100, -200, -50, -50, -50, -50, -200, -100, '',
'', 100,  -50, 100,   0,   0, 100,  -50,  100, '',
'', 50,  -50,   0,   0,   0,   0,  -50,   50, '',
'', 50,  -50,   0,   0,   0,   0,  -50,   50, '',
'', 100,  -50, 100,   0,   0, 100,  -50,  100, '',
'', -100, -200, -50, -50, -50, -50, -200, -100, '',
'', 200, -100, 100,  50,  50, 100, -100,  200, '',
'', '', '', '', '', '', '', '', '', '',
]
[
 '', '', '', '',  '',  '',  '',  '',  '',  '',
 '', 4, -3, 2, 2, 2, 2, -3, 4, '',
 '', -3, -4, -1, -1, -1, -1, -4, -3, '',
 '', 2, -1, 1, 0, 0, 1, -1, 2, '',
 '', 2, -1, 0, 1, 1, 0, -1, 2, '',
 '', 2, -1, 0, 1, 1, 0, -1, 2, '',
 '', 2, -1, 1, 0, 0, 1, -1, 2, '',
 '', -3, -4, -1, -1, -1, -1, -4, -3, '',
 '', 4, -3, 2, 2, 2, 2, -3, 4, '',
 '', '', '', '',  '',  '',  '',  '',  '',  ''
]'''


# initialize board with border as '#' and inside as '.'
def get_empty_board():
    board = [BORDER if is_edge(i) else SPACE for i in range(100)]
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board
def set_initial_board(initial):
    curr = 0  # simultaneous tracking of positions to go into the fuller board
    board = []
    for pos in range(100):
        if not is_edge(pos):
            board.append(initial[curr])
            curr += 1
        else:
            board.append(BORDER)

    return board
def is_edge(i):
    return i < 10 or i > 90 or i % 10 == 0 or i % 10 == 9
def set_directions(board): # Void method, just set them up
    directions = [-1, 1, -10, 10, -11, -9, 11, 9]  # 8 directions of the array
    global dir_lookup  # 8 vectors of motion
    for i in range(11, 91, 10):
        for j in range(8):
            pos = i + j
            for delta in directions:
                if board[pos + delta] != BORDER:  # then this is a valid direction
                    if pos not in dir_lookup:  # regular dictionary setup to input all possible deltas
                        dir_lookup[pos] = [delta]
                    else:
                        dir_lookup[pos].append(delta)

    global moves_lookup  # for each position, store a tuple of (pos, dir) which points to the list of positions it can go, specifically in that direction
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
def is_opposite(player, adj, board):
    if player == WHITE:
        return adj == BLACK
    else:  # player is binary, so this is fine. If adj is a dot, it'll be false
        return adj == WHITE
def count_pieces(player, board):  # later, convert it into string and use regular expression instead
    return sum([1 for i in board if i == player])
def terminal_test(board):
    if len(get_my_moves(WHITE, board)) == 0 and len(get_my_moves(BLACK, board)) == 0:
        return True
def display_board(board):
    alpha = "_ABCDEFGH"
    print("  ", end='')
    for i in range(1, 9): # the top indicator
        print(alpha[i], end=' ')# print(i, end='')
    print()

    for i in range(11, 91, 10):  # go from 11 to 81, and each time go up 0 through 7
        print(i // 10, end=' ') # print(alpha[i // 10], end='') # left indicator
        for j in range(8):
            print(board[i+j], end=' ')
        print()
    print()
def display_pos(pos):
    alpha = "_ABCDEFGH"
    row = pos % 10 # 1's digit
    col = (pos // 10) % 10  # 10's digit
    return alpha[row] + str(col)
def change_player(player):
    return WHITE if player == BLACK else BLACK
def legal_moves_at_pos(pos, player, board):
    moves = set()  # all positions reachable from pos by player on board
    for dir in dir_lookup[pos]:  # in 8 directions
        if is_opposite(player, board[pos + dir], board):  # then it may be jumpable
            # print(pos+dir, board[pos + dir])
            for move in moves_lookup[(pos, dir)]:  # moves_lookup has strictly positions within board
                # print(moves_lookup[(pos, dir)])
                if board[move] == SPACE:  # we kept traversing in that direction, until it was a stop
                    moves.add(move)
                    break
                elif board[move] == player:  # that means we met ourself and can't go
                    break
    return moves  # from list, pick one position
def get_my_moves(player, board):
    my_moves = set()  # avoid repeats TODO potentially sort this later for heuristic
    for i in range(11, 91, 10):  # go from 11 to 81, and each time go up 0 through 7
        for j in range(8):
            pos = i + j
            if board[pos] == player:
                my_moves = my_moves | legal_moves_at_pos(pos, player, board)
    return list(my_moves)
def make_move(move, player, board):  # after picked a certain position, radiate out and see which may be valid (opposite)
    board[move] = player  # set it, and radiate out from it
    to_take = set()

    for dir in dir_lookup[move]:  # radiate from that choice to see if other pieces would be flanked
        might_take = set()
        if is_opposite(player, board[move + dir], board):
            for piece in moves_lookup[(move, dir)]:
                if board[piece] == player:  # terminate the eating since we have finished flanking
                    to_take = to_take | might_take
                    break
                elif board[piece] == SPACE:  # since we ended up not flanking, don't add to the taken set
                    break
                else:  # because it's just an opponent to flank
                    might_take.add(piece)
                    continue
    # simply perform void action on a board
    for piece in to_take:  # convert all pieces
        board[piece] = player
    return board
def pick_move_human(my_moves, board):
    choices = {}
    for move in my_moves:
        # set up a choice array that maps the readable name of a position to the actual index
        show = display_pos(move)
        choices[show] = move

        board[move] = '*' # make the moves more readable
    display_board(board)
    print("Choices:")
    for show, move in choices.items():
        print(show)
    choice = input("Pick the move. Starred positions are valid (e.g. B4):")
    while choice not in choices:
        choice = input("Pick the move. Starred positions are valid (e.g. B4):")
    return choices[choice]  # reverse the display to the index
def pick_move(my_moves):  # TODO better heuristic value
    return random.choice(my_moves)  # just some value
def pick_move_minimax(player, board, max_d):
    depth = 0
    global max_depth
    max_depth = max_d
    if board.count(".") < 7:
        max_depth = 10 # just set it high enough so that it will definitely finish the game
    move, value = max_value(player, board, depth)
    return move, value
def max_value(player, board, depth):
    my_moves = get_my_moves(player, board)
    opponent = change_player(player)
    if len(my_moves) == 0:  # TODO time left/depth might need to add in
        return -1, open_eval(board)
    best_move = -1  # just do this to start
    best_val = -inf
    for move in my_moves:
        forecast = make_move(move, player, board[:])  # since it's a string, it just returns a new board
        dummy, value = min_value(opponent, forecast, depth + 1)
        if value > best_val:
            best_val = value
            best_move = move
    return best_move, best_val
def min_value(player, board, depth):
    my_moves = get_my_moves(player, board)
    opponent = change_player(player)
    if len(my_moves) == 0 or depth >= max_depth:
        return -1, open_eval(board)
    best_move = -1
    best_val = inf
    for move in my_moves:
        forecast = make_move(move, player, board[:])
        dummy, value = max_value(opponent, forecast, depth + 1)
        if value < best_val:
            best_val = value
            best_move = move
    return best_move, best_val
def pick_move_alphabeta(player, board, max_d): # returns best position to move and the value of that position
    alpha = -inf
    beta = inf
    depth = 0
    global max_depth, stability_table
    max_depth = max_d
    if board.count(".") < 7:
        max_depth = 10 # just set it high enough so that it will definitely finish the game
    move, value, updated_stability_table = max_value_ab(player, board, depth, alpha, beta) # kick off the recursion
    if updated_stability_table != []: # we essentially don't care about the stability table at the end, so this doesn't matter really
        # basically just return [] towards the endgame
        stability_table = updated_stability_table
    return move, value

def max_value_ab(player, board, depth, alpha, beta): # since whoever starts it off wants to maximize themselves
    my_moves = get_my_moves(player, board)
    opponent = change_player(player)
    if len(my_moves) == 0 or depth >= max_depth: # TODO time left/depth might need to add in=
        value, stability_table = open_eval(board)
        return -1, value, stability_table
    best_move = -1 # just do this to start
    best_val = -inf
    stability_table = []
    for move in my_moves:
        forecast = make_move(move, player, board[:]) # since it's a string, it just returns a new board
        dummy, value, stability_table = min_value_ab(opponent, forecast, depth + 1, alpha, beta) # perform search with the opponent
        if value > best_val:
            best_val = value
            best_move = move
        if best_val >= beta: # this means that we've exceeded the upper bound for the parent min node, so they'll never pick us
            return best_move, best_val, stability_table # what we return won't matter; we won't ever be picked
        alpha = max(alpha, best_val)
        if beta <= alpha: # not sure if it's right
            break
    return best_move, best_val, stability_table

def min_value_ab(player, board, depth, alpha, beta):
    my_moves = get_my_moves(player, board)
    opponent = change_player(player)
    if len(my_moves) == 0 or depth >= max_depth:
        value, stability_table = open_eval(board)
        return -1, value, stability_table
    best_move = -1
    best_val = inf
    stability_table = []
    for move in my_moves:
        forecast = make_move(move, player, board[:])
        dummy, value, stability_table = max_value_ab(opponent, forecast, depth + 1, alpha, beta)
        if value < best_val:
            best_val = value
            best_move = move
        if best_val <= alpha:
            return best_move, best_val, stability_table
        beta = min(beta, best_val)
        if beta <= alpha:
            break
    return best_move, best_val, stability_table

def get_potential_mobility_of_player(player, board): # one for each player, just compartmentalize to organize
    frontier_total = 0 # number of frontier discs (adj to empty square)
    empty_adj_set = set()
    empty_adj_total = 0 # number of empty squares adj to opponent discs
    sum_empty_adj = 0 # slightly different, repeats some squares,
    opponent = change_player(player) # NOTE, we do mobility by looking at the opponent, which we jump over
    global tiles
    for pos in tiles: # just to save some time, use the 8x8 not 10x10
        if board[pos] == opponent: # then we have our hypothetical frontier disc
            frontier_total += 1
            for delta in dir_lookup[pos]:
                if board[pos + delta] == '.': # it's empty
                    empty_adj_set.add(pos + delta) # have a no-duplicate track
                    sum_empty_adj += 1
    empty_adj_total = len(empty_adj_set) # FOR NOW, NOT USED
    return frontier_total, sum_empty_adj

def get_potential_mobility(board):
    frontier_total1, sum_empty_adj1 = get_potential_mobility_of_player(BLACK, board)
    frontier_total2, sum_empty_adj2 = get_potential_mobility_of_player(WHITE, board)
    potential_mobility = sum_empty_adj1 - sum_empty_adj2
    combined_frontier = frontier_total1 + frontier_total2
    # we want to scale the mobility based on big the frontier is. This means midgame is more weighted
    return 100 * potential_mobility / combined_frontier

def CMAC(): # weight the mobility based on move number. Current mobility application coefficient
    global move_num
    if 1 <= move_num <= 25: # mobility more important initially
        return 2 * move_num
    else:
        return move_num

def get_corner_score(board):
    corners = [11, 18, 81, 88]
    value = 0
    for c in corners:
        if board[c] == BLACK:  # if AI, which is BLACK, gets one, boost it
            value += 1
        elif board[c] == WHITE:
            value -= 1
        '''for delta in dir_lookup[c]: # see if any pieces are adjacent. If so, lose some points
            # if the piece is white, then AI has a good shot at getting it later
            if board[c + delta] == WHITE:
                value -= 0.5
            elif board[c + delta] == BLACK:
                value += 0.5 # '''
    return value

def propagate_corners(board): # only counts the stable pieces
    # essentially, my idea is that once one corner is taken,
    # keep propagating through the table and increase the weights of things that are "corners"
    # In the top left quadrant, if all above and all left are black, it's a corner, follow for each quadrant

    # The stability table is propagated each time
    right = 1
    down = 10
    left = -1
    up = -10

    corners = [11, 18, 81, 88]
    directions = [(right, down), (left, down), (right, up), (left, up)]
    global stability_table
    updated_stability_table = stability_table[:]
    # copy the original and produce a new one. Like in minimax, where we made many copies of the board, here, we
    # make copies of the stabilities. The one board that is picked decides which stability table is used

    for i in range(4):
        root = corners[i] # branch from a corner
        vert, horiz = directions[i] # how we propagate out

        # Now, perform BFS in each corner
        # If the corner is black, we want to propagate weights to be positive, if white then negative

        if board[root] == BLACK: # We must have a corner to begin with
            player = BLACK
            weight = 20 # If it becomes a black corner
        elif board[root] == WHITE:
            player = WHITE
            weight = 20 # White corner
        else:
            continue
        opponent = change_player(player)

        queue = [root]
        while len(queue) > 0:
            tile = queue.pop()
            # if we regress back vert/horiz, and is either wall or us and we are a player piece, we are safe and stable
            # if it is an opponent, then unstable and don't continue propagating.
            if board[tile - vert] in (BORDER + player) and board[tile - horiz] in (BORDER + player) and board[tile] == player:
                updated_stability_table[tile] = weight
                if board[tile + vert] == player: # Then, we see if we can add its child. If its child is the same, then it is unflippable
                    queue.append(tile + vert)
                if board[tile + horiz] == player:
                    queue.append(tile + horiz)

    return updated_stability_table # that way we don't have to reBFS each time


def get_stability(board):
    global tiles
    value = 0
    corners = [11, 18, 81, 88]
    stability_table = propagate_corners(board)

    for tile in tiles:
        if board[tile] == BLACK:
            value += stability_table[tile]
        elif board[tile] == WHITE:
            value -= stability_table[tile]
    return value, stability_table

def parity(total_discs): # tells us whether we will play the last move or not
    return -1 if (64 - total_discs) % 2 == 0 else 1

def open_eval(board): # always use this, if it's positive, max will want it, if negative, min will want it
    # basically, I merged utility and open_eval
    if terminal_test(board): # game-over
        return 10000*(count_pieces(BLACK, board) - count_pieces(WHITE, board)), []

    # Prioritize killer moves first
    black_count = count_pieces(BLACK, board)
    white_count = count_pieces(WHITE, board)
    total_discs = black_count + white_count
    if black_count == 0:
        return -inf, []
    if white_count == 0:
        return inf, []

    # Next, prioritize making them have no moves
    b = len(get_my_moves(BLACK, board))
    w = len(get_my_moves(WHITE, board))
    if w == 0: # since then we can move again
        return inf, []

    piece_score = (black_count - white_count)/(black_count + white_count)

    # Mobility
    current_mobility = 100 * (b - w) / (b + w + 1)  # since 4 to 1 is better than 15 to 11
    # global move_num
    # current_mobility = CMAC() * actual_mobility

    potential_mobility = get_potential_mobility(board) # WHITE is opponent here
    corner_score = get_corner_score(board)

    # Stability, always weighted highly
    stability, stability_table = get_stability(board)
    # print(piece_score, potential_mobility, current_mobility, corner_score, stability)

    # Weighting based on part of game. Parity and disc difference matter more at end, mobility less
    if total_discs <= 20: # TODO not sure if a linear weighting would be better?
        # Opening game
        return 300 * (potential_mobility + current_mobility) \
               + 20000 * corner_score \
               + 1000 * stability, stability_table
    elif total_discs <= 58:
        # Midgame
        return 10 * piece_score \
               + 200 * (potential_mobility + current_mobility) \
               + 100 * parity(total_discs) \
               + 20000 * corner_score \
               + 1000 * stability, stability_table
    else:
        # Endgame
        return 1500 * piece_score \
               + 500 * parity(total_discs) \
               + 20000 * corner_score \
               + 1000 * stability, stability_table

def play_game(board, gamemode, max_d): # gamemode is RR, RH, or HH
    current_piece = BLACK # X starts starts
    current_player = 0
    global move_num # track move, for application coefficient function weighting
    move_num = 1 # each game, it starts at 1
    global stability_table
    stability_table = [
        '', '', '', '', '', '', '', '', '', '',
        '', 20, -3, 11, 8, 8, 11, -3, 20, '',
        '', -3, -7, -4, 1, 1, -4, -7, -3, '',
        '', 11, -4, 2, 2, 2, 2, -4, 11, '',
        '', 8, 1, 2, -3, -3, 2, 1, 8, '',
        '', 8, 1, 2, -3, -3, 2, 1, 8, '',
        '', 11, -4, 2, 2, 2, 2, -4, 11, '',
        '', -3, -7, -4, 1, 1, -4, -7, -3, '',
        '', 20, -3, 11, 8, 8, 11, -3, 20, '',
        '', '', '', '', '', '', '', '', '', ''
    ]

    while not terminal_test(board): # if both players have no moves
        opponent = change_player(current_piece)
        my_moves = get_my_moves(current_piece, board)

        if len(my_moves) == 0: # skip a turn
            current_piece = opponent
            current_player = 1 - current_player
            continue

        player = gamemode[current_player] # trick since the gamemode is a string of 2 player types
        if player == 'R':
            move = pick_move(my_moves)
        elif player == 'A': # alphabeta move
            move, value = pick_move_alphabeta(current_piece, board, max_d)
            display_board(stability_table)
        elif player == 'M':  # minimax move
            move, value = pick_move_minimax(current_piece, board, max_d)
        elif player == 'H':
            move = pick_move_human(my_moves, board[:])
        make_move(move, current_piece, board)

        print(current_piece + " played " + display_pos(move))
        display_board(board)
        current_piece = opponent
        current_player = 1 - current_player
        move_num += 1

    white_pieces = count_pieces(WHITE, board)
    black_pieces = count_pieces(BLACK, board)
    #print("White had:", white_pieces)
    #print("Black had:", black_pieces)
    if white_pieces > black_pieces:
        #print("White won!")
        return 0
    elif black_pieces > white_pieces:
        #print("Black won!")
        return 1
    else:
        #print("Tie!")
        return 0

def main():
    global tiles
    tiles = [i for i in range(100) if not is_edge(i)] # shortcut because the method is below the global declaration :(
    b = "-1"# "XOOOOX..XXOOOX.OXXOXOXOXXOXXOOOXOOOXOXXXXXXOXXXX..XOOX...XXXXXX." # input("Initial board (type -1 if default): ")
    if b == "-1":
        board = get_empty_board()
    else:
        board = set_initial_board(b)
    display_board(board)
    set_directions(board)

    max_d = 4
    gamemode = "AR"# A = alphabeta, M = minimax, R = random, H = human. AI always goes first
    print()

    count = 0
    total = 1
    for i in range(total):
        # cur_time = time.time()
        result = play_game(board, gamemode, max_d)
        # next_time = time.time()
        board = get_empty_board()
        # print("Time: " + str(next_time - cur_time))
        count += result
    print(count/total)

if __name__ == '__main__':
    main()