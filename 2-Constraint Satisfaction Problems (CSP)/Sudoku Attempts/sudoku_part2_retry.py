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
domain = set([str(i) for i in range(1, 10)])
count = 0  # counting the explored states
assignment = []  # TODO to be assigned

N, h, w = 0, 0, 0


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
    w = h = 3
    N = 9
    top_left_corners = find_top_left_corners()
    row_increment = [i for i in range(w)]
    col_increment = [N * j for j in range(h)]
    for corner in top_left_corners:
        boxes.append(set([corner + i + j for i in row_increment for j in
                          col_increment]))  # set up a box, using the corner, and adding 0,1,2 and 0,9,18
    rows = [set([N * r + c for c in range(N)]) for r in
            range(N)]  # starting from 0th row, the elements of a row are 0-9 plus a 9*what row it's on
    cols = [set([N * r + c for r in range(N)]) for c in
            range(N)]  # start from 0th column, (0,9,18...). Inner array is modifying more rapidly

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
        adjset = adjset | rows[var // N].copy() | cols[var % N].copy()
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
    return var_domains
    # else:
    # var_domain[var] = None # cannot modify it


def display_var_domains():
    for var in var_domains:
        print(var, var_domains[var])


def backtracking_search(symbols, assignment):
    qtable = {
        i: 0 for i in range(1, 10)
    }
    domains = create_domains(symbols, assignment)
    print(domains)
    return recursive_backtrack(assignment, domains, qtable)


def recursive_backtrack(assignment, domains, qtable):
    global var_domains
    if is_complete(assignment):
        return assignment
    var, possible = select_minimum_remaining_values_var(assignment)
    if not possible:  # this means one of the unassigned has 0 possibilities, so have to backtrack
        return None
    print(var, domains)
    for value in domains:  # the 9 choices - we will modify this later, to update the domain over and over. For now be inefficient
        assignment[var] = value
        result = recursive_backtrack(assignment, update_domains(domains.copy(), var, value), qtable)  # go one layer deeper
        if result != None:
            return result  # no worries about reverting domains back
        else:
            assignment[var] = '.'  # this means that it ended up not working, so we need to try others
    return None


# ..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
# 4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
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

def update_domains(domains, var, value):  # go through all of var's adjacencies and fix their domains.
    if len(domains[var]) == 1: # only has that one value
        domains[var] = None
    else:
        domains[var].remove(value)
    for adj in adjacencies[var]:
        if domains[adj] != None and value in domains[adj]:
            domains[adj].remove(value)
    return domains


def min_conflicts_value(var, assignment):  # returns an ascending list of the values ranked by # conflicts
    conflicts = {}
    for value in var_domains[var]:
        conflicts[value] = sum(
            [1 if assignment[adj] != "." and value == assignment[adj] else 0 for adj in adjacencies[var]])
    # go through all of the adjacents and count the number of conflicts whenever it's assigned and has a different number
    return sorted(conflicts, key=conflicts.get)


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
    # for var in variables:
    #    print(var, variables[var])
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


def select_unassigned_var(assignment):
    for i in range(len(assignment)):
        if assignment[i] == ".":
            return i


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

    # display_assignment(assignment)
    cur_time = time.time()
    solution = backtracking_search(symbols, assignment)
    next_time = time.time()
    print("Time: " + str(next_time - cur_time))
    print("Count: " + str(count))

    display_assignment(solution)


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
        # print(count, backtracking_search())
        solution = backtracking_search(symbols, assignment)
        # print(solution)ligence/PycharmProjects/2-Constraint Satisfaction Problems (CSP)/sudoku_part2_retry.py", line 258, in solve_one_puzzle
        #     display_assignment(solution)
        # display_assignment(solution)
        print(count, check_sum(backtracking_search()))
        count += 1
    next_time = time.time()
    print("Time: " + str(next_time - cur_time))  # '''


def main():
    symbols = "123456789"
    puzzle = list(input("Input state: "))

    solve_one_puzzle(symbols, puzzle)  # '''

    # solve_puzzles(symbols)


''' 57th CASE IS SLOW


..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
..7369825632158947958724316825437169791586432346912758289643571573291684164875293
.3..5..4...8.1.5..46.....12.7.5.2.8....6.3....4.1.9.3.25.....98..1.2.6...8..6..2.
....8....27.....54.95...81...98.64...2.4.3.6...69.51...17...62.46.....38....9....
hard ones:
4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....

8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..
Time: 218.7625458240509
Count: 1489082
4 1 6  8 3 7  5 2 9
9 8 2  4 6 5  3 7 1
7 3 5  1 2 9  4 6 8

5 7 1  2 9 8  6 4 3
2 9 3  7 4 6  1 8 5
8 6 4  3 5 1  2 9 7

6 4 7  9 1 3  8 5 2
3 5 9  6 8 2  7 1 4
1 2 8  5 7 4  9 3 6


Input state: 4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
Minimum time and nodes with min-conflicts and least constraining value
Time: 24.02471923828125
Count: 152913
4 1 7  3 6 9  8 2 5
6 3 2  1 5 8  9 4 7
9 5 8  7 2 4  3 1 6

8 2 5  4 3 7  1 6 9
7 9 1  5 8 6  4 3 2
3 4 6  9 1 2  7 5 8

2 8 9  6 4 3  5 7 1
5 7 3  2 9 1  6 8 4
1 6 4  8 7 5  2 9 3

Somehow same one but much faster
Time: 0.5854053497314453
Count: 2781
4 1 7  3 6 9  8 2 5
6 3 2  1 5 8  9 4 7
9 5 8  7 2 4  3 1 6

8 2 5  4 3 7  1 6 9
7 9 1  5 8 6  4 3 2
3 4 6  9 1 2  7 5 8

2 8 9  6 4 3  5 7 1
5 7 3  2 9 1  6 8 4
1 6 4  8 7 5  2 9 3


Process finished with exit code 0



 Input state: 52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
 Best with minconflicts and least constraining
Time: 13.723663806915283
Count: 92139
5 2 7  3 1 6  4 8 9
8 9 6  5 4 2  7 3 1
3 1 4  9 8 7  5 6 2

1 7 2  4 5 3  8 9 6
6 8 9  2 7 1  3 5 4
4 5 3  6 9 8  2 1 7

9 4 1  8 2 5  6 7 3
7 6 5  1 3 4  9 2 8
2 3 8  7 6 9  1 4 5

Input state: 6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....
1/3 time with min conflicts, fastest with simple forward checking
Time: 4.043241262435913
Count: 25252
6 1 7  4 5 9  8 2 3
2 4 8  7 3 6  9 1 5
5 3 9  1 2 8  4 6 7

9 8 2  5 6 4  3 7 1
3 7 4  2 9 1  5 8 6
1 5 6  8 7 3  2 9 4

8 2 3  6 4 7  1 5 9
7 9 1  3 8 5  6 4 2
4 6 5  9 1 2  7 3 8

'''

if __name__ == '__main__':
    main()
