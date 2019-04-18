import random
board = {} # a dict of column, row of the queen
variables = []
N = 0 # size of board
domain = [] # 8 spots, the value is the row it is situated. One queen per column
adjacencies = []

def initial_assignment(N):
    for col in range(N):
        row = min_conflicts_value(col, board)
        board[col] = row
    display_board(board, N)
    return board

def display_board(board, N):
    for row in range(N):
        line = ""
        for col in range(N):
            if board[col] == row:
                line += 'Q'
            else:
                line += '-'
        print(line)


def min_conflicts_value(var, board):
    global domain # stays constant
    conflicts = {
        value: 0 for value in domain
    }
    for value in domain:
        tmp_queen = (var, value)
        for col in board:
            queen = (col, board[col])
            if queen[0] != var and is_attacking(queen, tmp_queen):
                conflicts[value] += 1
    first_min = min(conflicts, key=conflicts.get)
    if var >= 1 and board[var - 1] + 2 < N:
        L_row = board[var - 1] + 2
        if conflicts[L_row] == conflicts[first_min]: # equal, so no better
            return L_row # we want those preferentially
    return first_min

def min_conflicts_search(max_steps): #returns solution or failure
    global variables
    board = initial_assignment(N)
    for i in range(1, max_steps + 1):
        if is_valid(board):
            return board
        var = random.choice(variables) # random conflicted variable
        value = min_conflicts_value(var, board)
        board[var] = value

def is_valid(board):
    for var1 in board:
        queen1 = (var1, board[var1])
        for var2 in board:
            queen2 = (var2, board[var2])
            if var1 != var2 and is_attacking(queen1, queen2):
                return False
    return True

def is_attacking(queen, tmp_queen):
    col1, row1 = queen
    col2, row2 = tmp_queen
    return col1 == col2 or row1 == row2 or abs(col1 - col2) == abs(row1 - row2) #row, col, diagonal

def main():
    global board, variables, N, domain
    N = 7#int(input("N: "))
    domain = [i for i in range(N)]
    variables = [i for i in range(N)] # coincidentally same as domain
    initial_assignment(N)

if __name__ == '__main__':
    main()