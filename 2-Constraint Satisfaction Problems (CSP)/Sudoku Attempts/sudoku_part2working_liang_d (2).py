# ..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
# ..7369825632158947958724316825437169791586432346912758289643571573291684164875293
# .3..5..4...8.1.5..46.....12.7.5.2.8....6.3....4.1.9.3.25.....98..1.2.6...8..6..2.
# ....8....27.....54.95...81...98.64...2.4.3.6...69.51...17...62.46.....38....9....
# hard ones:
# 4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
# 52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
# 6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....
import time

var_domains = {}  # TODO New part for part 2
adjacencies = {}
adjacencies_unfiltered = {}
boxes = []
rows = []
cols = []
constraints = boxes + rows + cols
domain = set()  # = set([str(i) for i in range(1, 10)])
count = 0  # counting the explored states
assignment = []  # TODO to be assigned

N, h, w = 0, 0, 0

top_left_corners = [0, 3, 6, 27, 30, 33, 54, 57, 60]
for corner in top_left_corners:
    boxes.append(set([corner + i + j for i in [0, 1, 2] for j in
                      [0, 9, 18]]))  # set up a box, using the corner, and adding 0,1,2 and 0,9,18
rows = [set([9 * r + c for c in range(9)]) for r in
        range(9)]  # starting from 0th row, the elements of a row are 0-9 plus a 9*what row it's on
cols = [set([9 * r + c for r in range(9)]) for c in
        range(9)]  # start from 0th column, (0,9,18...). Inner array is modifying more rapidly


# it's good to make them into sets early on, that way you don't repeatedly have to waste time converting it into set
# converting list to set is N*1 = O(N)

# create adjacencies

def find_top_left_corners():
    global N, h, w
    tlc = []  # top_left_corners list
    for col in range(N // h):
        for row in range(N // w):
            tlc.append(N * row + col)
    return tlc


# definitely we could somehow use adjacencies more generally so that not all 128 are redoing this calculation
def create_adjacencies(symbols, assignment):  # lots of modifications to be made (generalizations)
    global adjacencies, adjacencies_unfiltered, N, h, w
    # N = int(len(symbols)) # gabor said int(len**0.5 +0.5)??
    # h = int(N**0.5)
    # w = N // h
    # w = h = 3
    # N = 9

    unassigned = []
    assigned = []
    for var in range(len(assignment)):
        if assignment[var] == ".":
            unassigned.append(var)
        else:
            assigned.append(var)

    for var in unassigned:  # range(81):
        adjset = set()
        for box in boxes:
            if var in box:
                adjset = adjset | box.copy()
                break  # we found a box that contains it
        adjset = adjset | rows[var // 9].copy() | cols[var % 9].copy()
        adjset.remove(var)  # we don't consider itself to be adjacent
        adjacencies_unfiltered[var] = adjset

        adjset_filtered = adjset.copy()
        for adj in list(adjset):
            if adj in assigned:
                adjset_filtered.remove(adj)  # since it is basically not part of the problem anymore
        adjacencies[var] = adjset_filtered


def create_domains(symbols, assignment):  # takes a string, "123456789" as the symbol set
    global adjacencies_unfiltered, N  # we use unfiltered adjacencies for creating domains. We reduce problem size, then go back to filtered adjacencies
    domain = set(list(symbols))
    N = 9

    for var in range(
            N ** 2):  # fill up the var_domains with sets of all possible symbols. This saves time so no recalculations.
        if assignment[var] == ".":  # only even have a domain if it is unassigned. Otherwise, it'll stay the same
            var_domains[var] = domain.copy()
            for adj in adjacencies_unfiltered[var]:
                if assignment[adj] != "." and assignment[adj] in var_domains[
                    var]:  # go through with the given information, and eliminate possibilities (just like you'd solve any sudoku)
                    var_domains[var].remove(assignment[adj])
    # else:
    # var_domain[var] = None # cannot modify it


def display_var_domains():
    for var in var_domains:
        print(var, var_domains[var])


def backtracking_search():
    qtable = {
        str(i): 0 for i in range(1, 10)
    }
    return recursive_backtrack(assignment, qtable)


def display_var_domains():
    for var in var_domains:
        print(var, var_domains[var])


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


def select_most_used_values(var, assignment, qtable):
    allowed = {}
    for value in qtable:
        if var_domains[var] != None and value in var_domains[var]:
            allowed[value] = qtable[value]
    return (sorted(allowed, key=allowed.get)[::-1])


def fill_deduced_squares(var, assignment): # TODO can't figure out how do deduce things
    '''values = {}
    for value in var_domains[var]:  # check each value to see how many times other another domain contains it
        overlaps = 0
        for adj in adjacencies[var]:
            if var_domains[adj] != None and value in var_domains[adj]:
                overlaps += 1
        values[value] = overlaps
    # print(sorted(values, key=values.get)[::-1])'''
    possible = var_domains[var]
    impossible_for_others = set()
    for adj in adjacencies[var]:
        if var_domains[adj] != None:
            impossible_for_others = impossible_for_others | var_domains[adj]
    remaining = possible.difference(impossible_for_others)
    if len(remaining) == 1:
        assignment[var] = list(remaining)[0]
        var_domains[var] = None


def is_invalid(var, value, assignment):  # O(N), N = # adjacents. Can't improve this. wrong again...
    for cs in constraints:
        vals = [assignment[pos] for pos in cs if assignment[pos] != '.']
        if len(vals) != len(set(vals)):  # somehow this correct logic fails.
            return True
    return False  # for some reason checking all constraints speeds it up#'''
    # return sum([1 if assignment[adj] == value else 0 for adj in adjacencies[var]]) != 0


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
    }
    return min(constraints, key=constraints.get)  # '''


def is_complete(assignment):
    global count
    count += 1
    return ''.join(assignment).find(".") == -1  # this is quicker than doing return "." not in assignment!!


# if we search through all the values in adjacent and counted 0 that were equal to the value, then return True

def display_assignment(assignment):
    for r in range(9):  # print solution
        row = assignment[9 * r:9 * (r + 1)]
        print(" ".join(row[:3]) + "  " + " ".join(row[3:6]) + "  " + " ".join(row[6:]))
        if r % 3 == 2:
            print()
    print("-------------------")


def check_sum(assignment):
    return sum(ord(ch) for ch in assignment) - 48 * N ** 2


def solve_one_puzzle(symbols, puzzle):
    global assignment
    assignment = puzzle
    create_adjacencies(symbols, assignment)
    create_domains(symbols, assignment)

    display_assignment(assignment)
    cur_time = time.time()
    solution = backtracking_search()
    display_assignment(solution)
    next_time = time.time()
    print("Time: " + str(next_time - cur_time))
    print("Count: " + str(count))
# puzzles takes 100 seconds beset
# hard puzzles takes
def solve_puzzles(symbols):
    global assignment
    puzzles = []
    with open("puzzles.txt") as f:  # set
        for line in f:
            puzzles.append(list(line)[:-1])
    cur_time = time.time()
    count = 1  # track which puzzle we are on
    for puzzle in puzzles:
        assignment = puzzle
        create_adjacencies(symbols, assignment)
        create_domains(symbols, assignment)
        solution = backtracking_search()
        print(count, check_sum(backtracking_search()), ''.join(solution))

        count += 1
    next_time = time.time()
    print("Time: " + str(next_time - cur_time))  # '''


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


# 45.....3....8.1....9...........5..9.2..7.....8.........1..4..........7.2...6..8..
# seems to be bottleneck
'''
4 8 3  9 2 1  6 5 7
9 6 7  3 4 5  8 2 1
2 5 1  8 7 6  4 9 3

5 4 8  1 3 2  9 7 6
7 2 9  5 6 4  1 3 8
1 3 6  7 9 8  2 4 5

3 7 2  6 8 9  5 1 4
8 1 4  2 5 3  7 6 9
6 9 5  4 1 7  3 8 2
'''


def main():
    symbols = "123456789"
    solve_one_puzzle(symbols, list("63..........5....8..5674.......2......34.1.2.......345.....7..4.8.3..9.29471...8."))#input("Input state: ")))  # '''

    #solve_puzzles(symbols)


if __name__ == '__main__':
    main()

# best = 102.6
