import math
inf = math.inf

def terminal_test(state): # had to do manually a bit
    groups = [state[3*i:3*(i+1)] for i in range(3)]
    groups += [state[i]+state[3+i]+state[6+i] for i in range(3)]
    groups += [state[0]+state[4]+state[8], state[2]+state[4]+state[6]]
    if "OOO" in groups:
        return -1
    elif "XXX" in groups:
        return 1
    elif "." not in state: # tied, the board is filled
        return 0
    else:
        return 2 # extra value just to mean that it's not done yet

def display_state(state):
    [print(state[3*i:3*(i+1)]) for i in range(3)]
    print()

def make_move(turn, state, move):
    return state[:move] + turn + state[move+1:]

def successors(turn, state): # return list of tuples (move, child state)
    unfilled = [index for index in range(len(state)) if state[index] not in "XO"]
    children = []
    for move in unfilled:
        child = make_move(turn, state, move)
        children.append((move, child)) # swap that unfilled spot
    return children

def current_turn(state): # returns 1 if X's, 0 if O's
    O_count = state.count("O")
    X_count = state.count("X")
    turn = "X" if X_count == O_count or X_count < O_count else "O" # X goes first if equal. Whoever has fewer goes
    return turn


def max_value(turn, state, alpha, beta, tree):
    terminal = terminal_test(state)
    if terminal != 2: # this means it's done
        tree[state] = terminal
        return terminal
    v = -inf
    next_turn = "X" if turn is "O" else "O"  # just becomes the opposite when the next is tested
    for a, s in successors(turn, state):
        v = max(v, min_value(next_turn, s, alpha, beta, tree))
        if v >= beta: # this means that our potential value will never be selected by the parent, since parent is a min
            #tree[state] = v # this is just a throw away child now, but set it anyway
            return v
        alpha = max(alpha, v) # '''
        if beta <= alpha:
            break

    tree[state] = v
    return v


def min_value(turn, state, alpha, beta, tree):
    terminal = terminal_test(state)
    if terminal != 2: # this means it's done
        tree[state] = terminal
        return terminal
    v = inf
    next_turn = "X" if turn is "O" else "O"  # just becomes the opposite when the next is tested
    for a, s in successors(turn, state):
        v = min(v, max_value(next_turn, s, alpha, beta, tree))
        if v <= alpha: # we need to do at least as well as the best so far. Otherwise, parent won't pick us
            #tree[state] = v  # this is just a throw away child now, but set it anyway
            return v
        beta = min(beta, v) # continually shrink the opponents benefit'''
        if beta <= alpha:
            break
    tree[state] = v
    return v

def alpha_beta_search(state):
    if terminal_test(state) != 2:
        return state
    turn = "X" # current_turn(state) # the players always plays "O"
    # after finding this first turn, we just have to keep track by alternating. Don't recalculate repeatedly
    tree = {}
    max_v = max_value(turn, state, -inf, inf, tree)
      
    next_state = ""
    # tree has now been populated with the values
    for next_move, child in successors(turn, state):
        if child in tree and tree[child] == max_v: # note, it might not be in tree sometimes, since we prune
            next_state = child
    return next_state # what the computer plays
'''state = "..OO...XX"
display_state(state)
print(successors("X", state))
state = alpha_beta_search(state)
display_state(state)'''
def display_tree(tree):
   for state, value in tree.items():
      print(value)
      display_state(state)

def output(terminal):
    if terminal == 2:
        return False
    elif terminal == 0:
        print("It was a tie")
    elif terminal == -1:
        print("Computer lost :(")
    elif terminal == 1:
        print("Computer won!")
    print("Game over")
    return True

def main():
    '''state = alpha_beta_search("O.O..XOXX")
    display_state(state)'''
    state = input("Input: ")
    print("Game start!")
    terminal = terminal_test(state)
    if output(terminal): # base case
        return
    display_state(state)
    turn = current_turn(state)
    print(turn + "'s turn\n")
    
    if turn is "X":
        state = alpha_beta_search(state) # let the computer move once
        display_state(state)

    while terminal_test(state) == 2: # while it isn't done, keep playing
        print("Choices:")

        for move, child in successors("O", state): # turn is always "O"
            print(str(move) + ":", (move // 3, move % 3)) # row, column of position

        user_move = int(input("Pick one (e.g. 1): "))
        state = make_move("O", state, user_move) # turn is always O

        state = alpha_beta_search(state)
        display_state(state)
    output(terminal_test(state)) #'''

#O.O..XOXX

if __name__ == '__main__':
    main() #
    '''
    Input: .........
Game start!
...
...
...

X's turn

...
...
..X

Choices:
0: (0, 0)
1: (0, 1)
2: (0, 2)
3: (1, 0)
4: (1, 1)
5: (1, 2)
6: (2, 0)
7: (2, 1)
Pick one (e.g. 1): 0
O..
...
X.X

Choices:
1: (0, 1)
2: (0, 2)
3: (1, 0)
4: (1, 1)
5: (1, 2)
7: (2, 1)
Pick one (e.g. 1): 7
O.X
...
XOX

Choices:
1: (0, 1)
3: (1, 0)
4: (1, 1)
5: (1, 2)
Pick one (e.g. 1): 5
O.X
.XO
XOX

Computer won!
Game over
    '''