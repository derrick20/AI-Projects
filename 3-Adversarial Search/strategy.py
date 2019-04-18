import math
SPACE, BLACK, WHITE, BORDER = '.', '@', 'o', '?'

dir_lookup = {} # pos -> valid directions (1, -1, 11, etc)
moves_lookup = {} # pos -> all positions reachable (like queen)
inf = math.inf
AI = BLACK
OPP = WHITE
weight_matrix = []
def is_edge(i):
    return i < 10 or i > 90 or i % 10 == 0 or i % 10 == 9
tiles = [i for i in range(100) if not is_edge(i)] # shortcut because the method is below the global declaration :(
stability_table = [
    [True, True, True, True] if is_edge(i) or i in [11, 18, 81, 88] else [False, False, False, False] for i in range(100)
] # pos -> (NS, EW, NE, NW) A tuple of booleans, telling if they are filled
# the corners and the walls are by default going to be stable
NS_lengths = [] # stores the lengths indices from one wall to the other
EW_lengths = []
NE_lengths = []
NW_lengths = []
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
                if board[piece] == player:  # terminate the taking since we have finished flanking
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
def pick_move_alphabeta(player, board, max_d): # returns best position to move and the value of that position
    alpha = -inf
    beta = inf
    depth = 0
    global max_depth
    max_depth = max_d
    if board.count(".") <= 8:
        max_depth = 10 # just set it high enough so that it will definitely finish the game
    move, value = max_value_ab(player, board, depth, alpha, beta) # kick off the recursion
    return move, value
def order_moves(player, my_moves, board):
    move_value_pairs = [] # move -> evaluation of that state
    for move in my_moves:
        forecast = make_move(move, player, board[:])
        move_value_pairs.append((open_eval(forecast), move))
    ordered = []
    for value, move in sorted(move_value_pairs):
        ordered.append(move)
    # print(sorted(move_value_pairs, reverse=True))
    return ordered
    # TODO SORT DICTIONARY BY VALUe
def max_value_ab(player, board, depth, alpha, beta): # since whoever starts it off wants to maximize themselves
    my_moves = get_my_moves(player, board)
    opponent = change_player(player)
    if len(my_moves) == 0 or depth >= max_depth: # TODO time left/depth might need to add in=
        return -1, open_eval(board)
    best_move = -1 # just do this to start
    best_val = -inf
    for move in order_moves(player, my_moves, board):
        forecast = make_move(move, player, board[:]) # since it's a string, it just returns a new board
        dummy, value  = min_value_ab(opponent, forecast, depth + 1, alpha, beta) # perform search with the opponent
        if value > best_val:
            best_val = value
            best_move = move
        if best_val >= beta: # this means that we've exceeded the upper bound for the parent min node, so they'll never pick us
            return best_move, best_val # what we return won't matter; we won't ever be picked
        alpha = max(alpha, best_val)
        if beta <= alpha: # not sure if it's right
            break
    return best_move, best_val
def min_value_ab(player, board, depth, alpha, beta):
    my_moves = get_my_moves(player, board)
    opponent = change_player(player)
    if len(my_moves) == 0 or depth >= max_depth:
        return -1, open_eval(board)
    best_move = -1
    best_val = inf
    for move in order_moves(player, my_moves, board):
        forecast = make_move(move, player, board[:])
        dummy, value = max_value_ab(opponent, forecast, depth + 1, alpha, beta)
        if value < best_val:
            best_val = value
            best_move = move
        if best_val <= alpha:
            return best_move, best_val
        beta = min(beta, best_val)
        if beta <= alpha:
            break
    return best_move, best_val
def get_potential_mobility_of_player(player, board): # one for each player, just compartmentalize to organize
    frontier_total = 0 # number of frontier discs (adj to empty square)
    empty_adj_set = set()
    empty_adj_total = 0 # number of empty squares adj to opponent discs
    sum_empty_adj = 0 # slightly different, repeats some squares,
    opponent = change_player(player) # NOTE, we do mobility by looking at the opponent, which we jump over
    global tiles
    for pos in tiles: # just to save some time, use the 8x8 not 10x10
        if board[pos] == opponent: # then we have our hypothetical frontier disc
            is_frontier = False
            for delta in dir_lookup[pos]:
                if board[pos + delta] == '.': # it's empty
                    # empty_adj_set.add(pos + delta) # have a no-duplicate track
                    is_frontier = True
                    sum_empty_adj += 1
            if is_frontier:
                frontier_total += 1
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
    return value
def propagate_corners(board): # not 100% correct, but it should generally help us
    # only counts the stable pieces
    # essentially, my idea is that once one corner is taken,
    # keep propagating through the table and increase the weights of things that are "corners"
    # In the top left quadrant, if all above and all left are black, it's a corner, follow for each quadrant
    close_corner = -100
    corner = 300
    if board.count(SPACE) <= 40:
        edge = 100
    else:
        edge = 10
    mid_edge = 0.5*edge
    weight_matrix = [
        '', '', '', '', '', '', '', '', '', '',
        '', corner, close_corner, edge, mid_edge, mid_edge, edge, close_corner, corner, '',
        '', close_corner, close_corner, -4, 1, 1, -4, close_corner, close_corner, '',
        '', edge, -4, 2, 2, 2, 2, -4, edge, '',
        '', mid_edge, 1, 2, -3, -3, 2, 1, mid_edge, '',
        '', mid_edge, 1, 2, -3, -3, 2, 1, mid_edge, '',
        '', edge, -4, 2, 2, 2, 2, -4, edge, '',
        '', close_corner, close_corner, -4, 1, 1, -4, close_corner, close_corner, '',
        '', corner, close_corner, edge, mid_edge, mid_edge, edge, close_corner, corner, '',
        '', '', '', '', '', '', '', '', '', ''
    ]

    # The stability table is propagated each time. Just redo it each time, to lazy to make global
    right = 1
    down = 10
    left = -1
    up = -10

    corners = [11, 18, 81, 88]
    directions = [(right, down), (left, down), (right, up), (left, up)]

    # copy the original and produce a new one. Like in minimax, where we made many copies of the board, here, we
    # make copies of the stabilities. The one board that is picked decides which stability table is used

    for i in range(4):
        root = corners[i] # branch from a corner
        vert, horiz = directions[i] # how we propagate out

        # Now, perform BFS in each corner
        # If the corner is black, we want to propagate weights to be positive, if white then negative
        weight = 20

        if board[root] == BLACK: # We must have a corner to begin with
            player = BLACK
        elif board[root] == WHITE:
            player = WHITE
        else:
            continue
        opponent = change_player(player)

        queue = [root]
        while len(queue) > 0:
            tile = queue.pop()
            # if we regress back vert/horiz, and is either wall or us and we are a player piece, we are safe and stable
            # if it is an opponent, then unstable and don't continue propagating.
            if board[tile - vert] in (BORDER + player) and board[tile - horiz] in (BORDER + player) and board[tile] == player:
                weight_matrix[tile] = weight
                if board[tile + vert] == player: # Then, we see if we can add its child. If its child is the same, then it is unflippable
                    queue.append(tile + vert)
                if board[tile + horiz] == player:
                    queue.append(tile + horiz)

    return weight_matrix # that way we don't have to reBFS each time
def get_weights(board):
    global tiles
    value = 0
    weight_matrix = propagate_corners(board)
    #display_board(weight_matrix)
    for tile in tiles:
        if board[tile] == BLACK:
            value += weight_matrix[tile]
        elif board[tile] == WHITE:
            value -= weight_matrix[tile]
    return value
def is_filled(length, board): # tells if the whole length is filled
    for pos in length:
        if board[pos] == SPACE:
            return False
    return True
def is_stable(pos, table, board):
    return is_half_surrounded(pos, table, board)# is_surrounded(pos, table) or is_half_surrounded(pos, table, board)
# XXXOOOOO..XOX................................................... Test case
def is_half_surrounded(pos, table, board): # it is protected on one of each side
    # is_half_surrounded = True # see if in the 4 directions, is there all stable pieces of its own color
    directions = [(10, -10), (-1, 1), (-9, 9), (-11, 11)] # pos -> (NS, EW, NE, NW)
    player = board[pos] #
    if player != BLACK and player != WHITE: # it must be a valid player
        return False
    for i in range(4):
        pair = directions[i]
        # need to add in knowing it's our own color
        protected0 = is_surrounded(pos + pair[0], table) and (board[pos + pair[0]] == player or board[pos + pair[0]] == BORDER)
        protected1 = is_surrounded(pos + pair[1], table) and (board[pos + pair[1]] == player or board[pos + pair[1]] == BORDER)
        if protected0 or protected1:
            table[pos][i] = True
            # is_half_surrounded = False # if one side is unstable, it's all unstable
    #if is_half_surrounded:
    #    table[pos] = [True, True, True, True] # update the table after noting one is half_surrounded
    #return is_half_surrounded
    list = table[pos]
    return list[0] and list[1] and list[2] and list[3]
#  basically, the issue is that it isn't getting stored between games correctly
def is_surrounded(pos, table):
    list = table[pos]
    return list[0] and list[1] and list[2] and list[3]  # surrounded in each lengt
def get_stability(board):
    global stability_table
    table = stability_table[:] # we copy it, because our move here might not be the chosen move later
    corners = [11, 18, 81, 88] # these are required in order to get more stable pieces
    # quick check, since early game won't need this function
    has_corners = False
    for c in corners:
        if board[c] == SPACE:
            has_corners = True
    if not has_corners: # if we have a single area, then it's possible to have stable pieces
         return 0 # return early

    for i in range(4):
        direction = [NS_lengths, EW_lengths, NE_lengths, NW_lengths][i] # pick one of those directions, then within the stability table, we can see if a pos is filled in that direction
        for length in direction:
            if is_filled(length, board):
                for pos in length:
                    table[pos][i] = True # one of those directions is now filled
    stability = 0


    for pos in tiles: # go through the tiles (8x8)
        if is_stable(pos, table, board):
            if board[pos] == BLACK:
                stability += 1
            elif board[pos] == WHITE:
                stability -= 1
    return stability
def make_lengths(): # generates all of the lengths, which we will have to check during the stability method
    global NS_lengths, EW_lengths, NE_lengths, NW_lengths
    # vert and horiz lengths
    for i in range(1, 8+1):
        v = [] # vertical lengths
        h = [] # horizontal lengths
        for j in range(1, 8+1):
            v.append(10*j+i) # moves down
            h.append(10*i+j) # moves right
        NS_lengths.append(v) # in total, we will have 16
        EW_lengths.append(h)
    # diagonal lengths
    # Note that we skip each corner since they have no lengths to go, (it include just themselves)
    for i in range(2, 8+1): # upright diagonals. Skip top left corner. Also, at 8th row, save the bottom left for the j iterating
        if i == 8:
            for j in range(1, 7+1): # Skip bottom right corner.
                d = moves_lookup[(10*i+j, -9)][:] # here, the column is j, not 1
                d.append(10*i+j) # append itself too
                NE_lengths.append(d)
            break
        d = moves_lookup[(10*i+1, -9)][:] # radiate, in the right up direction (+1 -10). We don't want to modify the original lookup table, so copy
        d.append(10*i+1) # need to include that position
        NE_lengths.append(d)

    for i in range(2, 8+1): # upleft diagonals. Skip top right corner. Also, at 8th row, save the bottom right for the j iterating
        if i == 8:
            for j in range(8, 2-1, -1): # decrement to 1, by -1. Skip bottom left corner. Go from 8 to 2 (since this excludes the stop value, -1)
                d = moves_lookup[(10*i+j, -11)][:] # here, the column is j, not 1
                d.append(10*i+j) # append itself too
                NW_lengths.append(d)
            break
        d = moves_lookup[(10*i+8, -11)][:] # radiate, in the right up direction (-1 -10). Also, we start on 8th column
        d.append(10*i+8) # need to include that position
        NW_lengths.append(d)
def parity(total_discs): # tells us whether we will play the last move or not
    return -1 if (64 - total_discs) % 2 == 0 else 1
def center_square_score(board):
    center_count = 0
    for i in range(33, 73, 10):
        for j in range(0, 4):
            if board[i+j] == WHITE:
                center_count += 1
            elif board[i+j] == BLACK:
                center_count -= 1
    return center_count
def open_eval(board): # always use this, if it's positive, max will want it, if negative, min will want it
    # basically, I merged utility and open_eval
    if terminal_test(board): # game-over
        return 1000000*(count_pieces(BLACK, board) - count_pieces(WHITE, board))

    # Prioritize killer moves first
    black_count = count_pieces(BLACK, board)
    white_count = count_pieces(WHITE, board)
    total_discs = black_count + white_count
    if black_count == 0:
        return -inf
    if white_count == 0:
        return inf

    # Next, prioritize making them have no moves
    b = len(get_my_moves(BLACK, board))
    w = len(get_my_moves(WHITE, board))
    if w == 0: # since then we can move again
        return inf

    piece_score = (black_count - white_count)/(black_count + white_count)

    # Mobility
    current_mobility = 100 * (b - w) / (b + w + 1)  # since 4 to 1 is better than 15 to 11
    # global move_num
    # current_mobility = CMAC() * actual_mobility

    potential_mobility = get_potential_mobility(board) # WHITE is opponent here
    corner_score = get_corner_score(board)

    # Weightings # but it does have propagating corners??
    weights = get_weights(board)
    # print(piece_score, potential_mobility, current_mobility, corner_score, stability)

    # Stability
    stability = get_stability(board)
    # Weighting based on part of game. Parity and disc difference matter more at end, mobility less
    corner_weight = 300000
    stability_weight = 10000
    if total_discs <= 20: # TODO not sure if a linear weighting would be better?
        # Opening game
        return 4000 * (potential_mobility + current_mobility) \
               + corner_weight * corner_score \
               + 1000 * weights \
               + stability_weight * stability #\
               #+ 50000*center_square_score(board)
    elif total_discs <= 57:
        # Midgame
        return 0 * piece_score \
               + 3000 * (potential_mobility + 3*current_mobility) \
               + 100 * parity(total_discs) \
               + corner_weight * corner_score \
               + 1000 * weights \
               + stability_weight * stability
    else:
        # Endgame
        return 0 * piece_score \
               + 2000 * (potential_mobility + 5*current_mobility) \
               + 200 * parity(total_discs) \
               + corner_weight * corner_score \
               + 1000 * weights \
               + stability_weight * stability

def convert_board(board):
    for tile in tiles:
        if board[tile] == BLACK:
            board[tile] = WHITE
        elif board[tile] == WHITE:
            board[tile] = BLACK


class Strategy():
    def best_strategy(self, board, player, best_move, still_running):
        set_directions(board)
        make_lengths()

        max_d = 3
        board_copy = list(board)[:]
        if player == WHITE:  # convert '@' to 'o' and vice versa, since we always think we are x. Too lazy to fix everything else
            convert_board(board_copy)

        while(True):
            best_move.value, value = pick_move_alphabeta(BLACK, board_copy, max_d)
            max_d += 1