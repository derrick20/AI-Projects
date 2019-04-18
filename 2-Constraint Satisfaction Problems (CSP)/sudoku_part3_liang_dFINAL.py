# ..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
# ..7369825632158947958724316825437169791586432346912758289643571573291684164875293
# .3..5..4...8.1.5..46.....12.7.5.2.8....6.3....4.1.9.3.25.....98..1.2.6...8..6..2.
# ....8....27.....54.95...81...98.64...2.4.3.6...69.51...17...62.46.....38....9....
# hard ones:
# 4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
# 52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
# 6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....
# ----------------------------------------------
import time

# below are set up by the get_adjacencies method
symbols_dict = {
        9: "123456789",
        12: "123456789ABC",
        16: "0123456789ABCDEF"
}
var_domains = {}
adjacencies = {}  # var -> adjset, but not those assigned in initial
adjacencies_unfiltered = {}  # var -> adjset
count = 0  # counting the number of is_complete calls
assignment = []

# -------------------------------------
# below are set up by the set_up method
boxes, rows, cols = [], [], []
constraints = boxes + rows + cols
domain = set()  # initial domain for all vars
symbols = ""
N, h, w = 0, 0, 0
boxDict, rowDict, colDict = {}, {}, {}  # arcs, var -> box that it is adjacent to. Use arc-consistency to reduce domain


# also allows us to deduce that if a value only occurs in an arc once, the var that has it must be set.

def display_assignment(assignment):
    global N, w, h
    for r in range(N):  # print solution
        row = assignment[N * r: N * (r + 1)]
        for incr in range(N // w):
            print(" ".join(row[incr * w: (incr + 1) * w]),
                  end="  ")  # use double space for each horizontal block finished
        print()

        if r % h == h - 1 and r != N - 1:  # this means it has just finished one vertical block, so add a break.
            print()  # Don't do the extra space for last line, since we have a line drawn
    print((2 * (N // w - 1) + (N // w) * (w - 1) + N) * "-")
    # number of horizontal pieces - 1 times 2, width-1 times number of horizontal pieces, then N symbols


def check_sum(assignment):
    return sum(ord(ch) for ch in assignment) - 48 * N ** 2


def is_complete(assignment):
    global count
    count += 1
    print(assignment)
    return ''.join(assignment).find(".") == -1  # this is quicker than doing return "." not in assignment!!


def find_top_left_corners():
    global N, h, w
    tlc = []  # top_left_corners list
    for vertical_block in range(N // h):  # how many can fit vertically. It steps N*h per block (indices)
        for horizontal_block in range(N // w):  # how many fit horizontally. It steps w per block
            tlc.append(N * h * vertical_block + w * horizontal_block)
    return tlc


def set_up(symbolSet):  # create the general
    global symbols, N, h, w, rows, cols, boxes, constraints, boxDict, rowDict, colDict, domain
    symbols = symbolSet
    N = int(len(symbols))  # gabor said int(len**0.5 +0.5)??
    h = int(N ** 0.5)
    w = N // h
    top_left_corners = find_top_left_corners()
    col_increment = [i for i in range(w)]  # increment over the width
    row_increment = [N * j for j in range(h)]  # increment over the height
    for corner in top_left_corners:
        boxes.append(set([corner + i + j for i in col_increment for j in
                          row_increment]))  # set up a box, using the corner, and adding 0,1,2 and 0,9,18
    rows = [set([N * r + c for c in range(N)]) for r in
            range(N)]  # starting from 0th row, the elements of a row are 0-9 plus a 9*what row it's on
    cols = [set([N * r + c for r in range(N)]) for c in
            range(N)]  # start from 0th column, (0,9,18...). Inner array is modifying more rapidly
    boxDict = {
        var: box for box in boxes for var in box
    }
    rowDict = {
        var: row for row in rows for var in row
    }
    colDict = {
        var: col for col in cols for var in col
    }
    constraints = boxes + rows + cols


def create_adjacencies(assignment):  # following setup, it uses the information to create an adjList
    global adjacencies, adjacencies_unfiltered, N, h, w, rows, cols, boxes
    unassigned = []
    assigned = []
    for var in range(len(assignment)):  # categorize variables
        if assignment[var] == ".":
            unassigned.append(var)
        else:
            assigned.append(var)
    for var in unassigned:  # create adjset to each var, then filter out the var, and
        adjset = set()

        adjset = adjset | boxDict[var] | rowDict[var] | colDict[var]  # since we have a way to get the arcs, use it
        adjset.remove(var)  # it is not adjacent to itself
        adjacencies_unfiltered[var] = adjset

        adjset_filtered = adjset.copy()
        for adj in list(adjset):  #
            if adj in assigned:
                adjset_filtered.remove(adj)  # since it is basically not part of the problem anymore

        adjacencies[var] = adjset_filtered


def create_domains(symbols, assignment):  # takes a string, "123456789" as the symbol set
    global var_domains, domain, adjacencies_unfiltered, N  # we use unfiltered adjacencies for creating domains. We reduce problem size, then go back to filtered adjacencies
    domain = set(list(symbols))
    var_domains = {}
    for var in range(
            N ** 2):  # fill up the var_domains with sets of all possible symbols. This saves time so no recalculations.
        if assignment[var] == ".":  # only even have a domain if it is unassigned. Otherwise, it'll stay the same
            var_domains[var] = domain.copy()
            for adj in adjacencies_unfiltered[var]:
                if assignment[adj] != "." and assignment[adj] in var_domains[
                    var]:  # go through with the given information, and eliminate possibilities (just like you'd solve any sudoku)
                    var_domains[var].remove(assignment[adj])
    return var_domains # remember, this is not global

def backtracking_search():
    global N
    qtable = {
        i: assignment.count(str(i)) for i in symbols
    }
    return recursive_backtrack(assignment, qtable)


def display_var_domains():
    for var in var_domains:
        print(var, var_domains[var])


def select_most_used_values(var, assignment, qtable):
    allowed = {}
    for value in qtable:
        if var_domains[var] != None and value in var_domains[var]:
            allowed[value] = qtable[value]
    #print(qtable)
    return (sorted(allowed, key=allowed.get)[::-1])

def select_minimum_remaining_values_var(assignment):
    variables = {}
    unassigned_variables = get_unassigned_variables(assignment)
    for var in unassigned_variables:
        if var_domains[var] == None:
            return (-1, False)  # all of the unassigned variables must have some domain left, so we need to backtrack
        variables[var] = len(var_domains[var])
    MRV = min(variables, key=variables.get)
    candidates = []
    for var in variables:
        if variables[var] == variables[MRV]:
            candidates.append(var)
    if len(candidates) == 1:
        return (candidates[0], True)
    else:  # select_least_constraining
        return (select_least_constraining_var(candidates), True)

def is_unassigned(var, assignment):
    return assignment[var] == "."


def get_unassigned_variables(assignment):
    return [var for var in range(len(assignment)) if is_unassigned(var, assignment)]


def select_least_constraining_var(candidates):  # least constraining var of candidate list
    constraints = {
        var: sum([1 if is_unassigned(adj, assignment) else 0 for adj in adjacencies[var]]) for var in candidates
    } # goes through each var (of the MRV variable list) and counts how mny unassigned neighbors it has (constraining factor)
    return min(constraints, key=constraints.get)  # '''


def is_complete(assignment):
    #global count
    #count += 1
    return ''.join(assignment).find(".") == -1  # this is quicker than doing return "." not in assignment!!


# if we search through all the values in adjacent and counted 0 that were equal to the value, then return True


def check_sum(assignment):
    return sum(ord(ch) for ch in assignment) - 48 * N ** 2


def solve_one_puzzle(symbols, puzzle):
    global assignment
    assignment = puzzle
    set_up(symbols)
    create_adjacencies(assignment)
    create_domains(symbols, assignment)

    display_assignment(assignment)
    cur_time = time.time()
    solution = backtracking_search()
    display_assignment(solution)
    next_time = time.time()
    print("Time: " + str(next_time - cur_time))
    # print("Count: " + str(count)) no need for count anymore


def solve_puzzles(file):
    global assignment, symbols_dict
    puzzles = []
    with open(file) as f:  # set
        for line in f:
            puzzles.append(list(line.strip()))
    cur_time = time.time()
    count = 1  # track which puzzle we are on
    for puzzle in puzzles:
        assignment = puzzle
        size = int(len(puzzle)**0.5)
        symbols = symbols_dict[size]
        set_up(symbols)
        create_adjacencies(assignment)
        create_domains(symbols, assignment)
        solution = backtracking_search()
        print(count, check_sum(backtracking_search()), ''.join(solution))

        count += 1
    next_time = time.time()
    print("Time: " + str(next_time - cur_time))  # '''


def update_domains(var, value):  # go through all of var's adjacencies and fix their domains
    '''delta_var_domains = {var : var_domains[var]} # dictionary of sets for each variable that were removed (and could be added back in)
    del var_domains[var] # it will now be considered assigned
    for adj in adjacencies[var]:
        if var_domains[adj] != None and value in var_domains[adj]:
            delta_var_domains[var_domains] = set(value) # single value
            var_domains[adj].remove(value)  # remove them for now. Later, after recursive call, add back in if failed.
            if len(var_domains[
                       adj]) == 0:  # annoying extra cases, set them to none, so that it is not considered when finding MRV (len/size of domain space)
                del var_domains[adj]


    return delta_var_domains'''
    delta_var_domains = [var]  # a list of variables that need to have this new VALUE removed from domain

    var_domains[var].remove(value)  # but don't put it into delta_var_domains, because now we eliminated tht
    if len(var_domains[
               var]) == 0:  # annoying extra cases, set them to none, so that it is not considered when finding MRV (len/size of domain space)
        var_domains[var] = None

    for adj in adjacencies[var]:  # TODO potentially make it so you do AC-3, propagating through a few layers
        if var_domains[adj] != None and value in var_domains[adj]:
            var_domains[adj].remove(value)  # remove them for now. Later, after recursive call, add back in if failed.
            if len(var_domains[
                       adj]) == 0:  # annoying extra cases, set them to none, so that it is not considered when finding MRV (len/size of domain space)
                var_domains[adj] = None
            delta_var_domains.append(adj)

    return delta_var_domains  # '''

def recursive_backtrack(assignment, qtable):
    global var_domains
    if is_complete(assignment):
        return assignment
    var, possible = select_minimum_remaining_values_var(
        assignment)  # TODO you can swap this for any of the three selection methods
    if not possible:
        return None
    for value in select_most_used_values(var, assignment, qtable):  # 3 possible ways to pick this
        assignment[var] = value
        qtable[value] += 1
        delta_var_domains = update_domains(var, value)
        result = recursive_backtrack(assignment, qtable)  # go one layer deeper
        if result != None:
            return result  # no worries about reverting domains back
        else:
            assignment[var] = '.'  # this means that it ended up not working, so we need to try others
            qtable[value] -= 1 # that value is not used anymore
            for changed_var in delta_var_domains:
                if var_domains[
                    changed_var] == None:  # fix it back if we thought it could've been ruled out. We were wrong
                    var_domains[changed_var] = set(value)
                else:
                    var_domains[changed_var].add(value)
                    # go back and re-add the possibility of being that value, since it is now legal again.
    return None
# main issue is that we want to automatically set vars if the domain is size 1, but we can't keep track of this very easily

def main():
    # Single puzzle test
    #symbols = "123456789"#input("Input symbol set: ")
    #puzzle = list(input("Input puzzle: "))
    #solve_one_puzzle(symbols, puzzle)

    # Multiple puzzle test from file
    file = "puzzlesHarder.txt"#input("File: ")
    solve_puzzles(file)

if __name__ == '__main__':
    main()
# 6.2.5.........3.4..........43...8....1....2........7..5..27...........81...6..... about 3 seconds
# 63..........5....8..5674.......2......34.1.2.......345.....7..4.8.3..9.29471...8.

# 0123456789ABCDEF
# 9...0.E8.7..5..FF......7.A4029.D.5D..9.2C.............1.......06...E..F..0.6.C.1..68D2B1....E...AC29E.8..B.16D...D0...9.F2.4A8....B4C.D3.1...25...821.A..C.5DF49...F....7892B3..C.7.B.2..F..0...34.......5.............FD.B..5A.7.F62A4.0......C5..D..C.1E.F...8
# 123456789ABC
# ..4...8.7...9...3A75.8.....3......C........A82..6....948.A3..4.....3.CB7A91.6.....5..BC.432....6..37A........2......4.....8.9B36...1...A.C...B..

# puzzles best = 95
# puzzlesHard = 104
# puzzzlesHarder = 173
