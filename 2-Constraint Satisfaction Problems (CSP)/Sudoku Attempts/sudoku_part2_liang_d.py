# ..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
# ..7369825632158947958724316825437169791586432346912758289643571573291684164875293
# .3..5..4...8.1.5..46.....12.7.5.2.8....6.3....4.1.9.3.25.....98..1.2.6...8..6..2.
# ....8....27.....54.95...81...98.64...2.4.3.6...69.51...17...62.46.....38....9....
# hard ones:
# 4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
# 52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
# 6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....
import time

#var_domains = {}  # TODO New part for part 2
adjacencies = {}
adjacencies_unfiltered = {}
domain = set()  # = set([str(i) for i in range(1, 10)])
count = 0  # counting the explored states
# assignment = []  # TODO to be assigned DON"T MAKE THIS GLOBAL

N, h, w = 0, 0, 0

top_left_corners = [0, 3, 6, 27, 30, 33, 54, 57, 60]
boxes = [] # TODO make a boxDict, rowDict, colDict for each var to point to
for corner in top_left_corners:
    boxes.append(set([corner + i + j for i in [0, 1, 2] for j in
                      [0, 9, 18]]))  # set up a box, using the corner, and adding 0,1,2 and 0,9,18
rows = [set([9 * r + c for c in range(9)]) for r in
        range(9)]  # starting from 0th row, the elements of a row are 0-9 plus a 9*what row it's on
cols = [set([9 * r + c for r in range(9)]) for c in
        range(9)]  # start from 0th column, (0,9,18...). Inner array is modifying more rapidly

# these dictionaries give the neigbors of each var to some spot
boxDict = {}
for box in boxes:
    for var in box:
        boxDict[var] = box
rowDict = {}
for row in rows:
    for var in row:
        rowDict[var] = row
colDict = {}
for col in cols:
    for var in col:
        colDict[var] = col

constraints = boxes + rows + cols

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
                adjset = adjset | box
                break  # we found a box that contains it
        adjset = adjset | rows[var // 9] | cols[var % 9]
        adjset.remove(var)  # we don't consider itself to be adjacent
        adjacencies_unfiltered[var] = adjset

        adjset_filtered = adjset.copy()
        for adj in list(adjset):
            if adj in assigned:
                adjset_filtered.remove(adj)  # since it is basically not part of the problem anymore
        adjacencies[var] = adjset_filtered

def create_domains(symbols, assignment):  # takes a string, "123456789" as the symbol set
    global domain, adjacencies_unfiltered, N  # we use unfiltered adjacencies for creating domains. We reduce problem size, then go back to filtered adjacencies
    domain = set(list(symbols))
    N = 9
    var_domains = {}
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

def display_var_domains(var_domains):
    for var in var_domains:
        print(var, var_domains[var])

def fastCopy(var_domain):
    toReturn = {}
    for i in var_domain:
        if var_domain[i] != None:
            tmp = var_domain[i].copy()
        else:
            tmp = None
        toReturn[i] = tmp
    return toReturn

def select_most_used_values(var, assignment, qtable, var_domains):
    allowed = {}
    for value in qtable:
        if var_domains[var] != None and value in var_domains[var]:
            allowed[value] = qtable[value]
    return (sorted(allowed, key=allowed.get)[::-1])

def fill_deduced_squares(var, assignment):  # TODO can't figure out how do deduce things
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

def is_unassigned(var, assignment):
    return assignment[var] == "."

def get_unassigned_variables(assignment):
    return [var for var in range(len(assignment)) if is_unassigned(var, assignment)]

def select_least_constraining_var(candidates, assignment):  # least constraining var of candidate list
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
    assignment = puzzle
    create_adjacencies(symbols, assignment)
    var_domains = create_domains(symbols, assignment)

    display_assignment(assignment)
    cur_time = time.time()
    solution = backtracking_search(assignment, var_domains)
    display_assignment(solution)
    next_time = time.time()
    print("Time: " + str(next_time - cur_time))
    print("Count: " + str(count))

def solve_puzzles(symbols):
    puzzles = []
    with open("puzzles.txt") as f:  # set
        for line in f:
            puzzles.append(list(line)[:-1])
    cur_time = time.time()
    count = 1  # track which puzzle we are on
    for puzzle in puzzles:
        assignment = puzzle
        create_adjacencies(symbols, assignment)
        var_domains = create_domains(symbols, assignment)
        solution = backtracking_search(assignment, var_domains)
        print(count, check_sum(solution), ''.join(solution))

        count += 1
    next_time = time.time()
    print("Time: " + str(next_time - cur_time))  # '''

def backtracking_search(assignment, var_domains):
    qtable = {
        str(i): 0 for i in range(1, 10)
    }
    return recursive_backtrack(assignment, qtable, var_domains)

def prune(assignment, var_domains):
    for var in var_domains:
        if is_unassigned(var, assignment) and len(var_domains[var]) == 1:
            assignment[var] = var_domains[var]
            var_domains[var] = None

def is_valid(assignment):  # O(N), N = # adjacents. Can't improve this. wrong again...
    for cs in constraints:
        vals = [assignment[pos] for pos in cs if assignment[pos] != '.']
        if len(vals) != len(set(vals)):  # somehow this correct logic fails.
            return False
    return True

def auto_fill_group(var, value, assignment, var_domains):
    # this strategy applies how you would normally do sudoku by hand, and is massive speed-up
    for group in [boxDict, rowDict, colDict]:
        determined = {
            str(i): [] for i in range(1, N + 1)
        }  # don't quite understand why the below comment doesn't work?
        for val in domain:  # rather than domain, it might be for val in var_domains[var] - set(value), like those are the ones actually changing!
            for adj in group[var]: # group is a dictionary pointing to its neighbors
                if adj in var_domains and var_domains[adj] != None and val in var_domains[adj]:  # it does have that value (potentially uniquely)
                    determined[val].append(adj)
        # print(determined)
        for val, adjlist in determined.items():  # go through and assign the determined values
            if len(adjlist) == 1:
                display_var_domains(var_domains)
                print('yippee', adjlist[0], val, var, value)
                display_assignment(assignment)
                adj = adjlist[0]
                assignment[adj] = val  # '''
                possible = update_domains(adj, val, assignment, var_domains)
                if not possible:
                    return None

def remove_and_process(var, value, assignment, var_domains):
    var_domains[var].remove(value)
    if is_unassigned(var, assignment) and len(var_domains[var]) == 1:
        assignment[var] = var_domains[var] # it can ONLY be that
        possible = update_domains(var, value, assignment, var_domains)
        if not possible:
            return False
    elif is_unassigned(var, assignment) and len(var_domains[var]) == 0:  # return None, because this should not be possible
        return False

def update_domains(var, value, assignment, var_domains):  # go through all of var's adjacencies and fix their domains
    var_domains[var] = None # since it is now set
    for adj in adjacencies[var]:
        if var_domains[adj] != None and value in var_domains[adj]:
            possible = remove_and_process(adj, value, assignment, var_domains)
            if not possible:
                return False

def NOT_WORKINGselect_minimum_remaining_values_var(assignment, var_domains):
    variables = {}
    unassigned_variables = get_unassigned_variables(assignment)
    for var in unassigned_variables:
        if var_domains[var] == None:
            return (-1, False, False)  # all of the unassigned variables must have some domain left, so we need to backtrack
        domain = len(var_domains[var])
        variables[var] = domain
        '''domain = len(var_domains[var])
        if domain == 1:
            #display_var_domains(var_domains)
            assignment[var] = var_domains[var].pop() # pops a random, but only 1 so not random actually
            possible = update_domains(var, assignment[var], assignment, var_domains)
            if not possible:
                return (-1, False, False)'''
         # if domain isn't 1, don't automatically set

   # display_assignment(assignment)
    # auto set anything with only one left
   # print(variables)

    '''for var in variables:
        if variables[var] == 1:
            display_var_domains(var_domains)
            assignment[var] = var_domains[var].pop() # pops a random, but only 1 so not random actually
            if not update_domains(var, assignment[var], assignment, var_domains):
                display_assignment(assignment)
                print(var)
                return (-1, False, False) # it is impossible and not complete
            variables[var] = 10 # an impossible amount, because only 9 values, just so the MRV won't pick it# '''

    # Need to update domains after setting these
    '''MRV = sorted(variables, key=variables.get) # sorted order Still doesn't automatically set single valued vars
    candidates = []
    min_rem_values = 10 # an impossible number
    for var in MRV:
        if variables[var] == 1: # it can only be one value
            value = var_domains[var].pop() # only one left
            assignment[var] = value # how could we update qtable?
            possible = update_domains(var, value, assignment, var_domains)
            if not possible:
                return (-1, False, False)
        elif variables[var] <= min_rem_values:
            min_rem_values = variables[var] # once it's selected, only the same level can match it
            candidates.append(var)
    display_assignment(assignment)
    display_var_domains(var_domains)

    print(candidates)

    return (select_least_constraining_var(candidates, assignment), True, False) #'''


def select_minimum_remaining_values_var(assignment, var_domains):
    variables = {}
    unassigned_variables = get_unassigned_variables(assignment)
    for var in unassigned_variables:
        if var_domains[var] == None:
            return (-1, False, False)  # all of the unassigned variables must have some domain left, so we need to backtrack
        variables[var] = len(var_domains[var])

    MRV = min(variables, key=variables.get)
    return MRV, True, False
    candidates = []
    for var in variables:
        if variables[var] == variables[MRV]:
            candidates.append(var)

    return (select_least_constraining_var(candidates, assignment), True, False) #'''

def recursive_backtrack(assignment, qtable, var_domains):
    if is_complete(assignment):
        return assignment

    var, possible, complete = select_minimum_remaining_values_var(assignment, var_domains)
    if complete:
        return assignment
    if not possible:
        return None
    #display_assignment(assignment)
    #display_var_domains(var_domains)
    values = select_most_used_values(var, assignment, qtable, var_domains)
    #print(values)

    for value in values:  # 3 possible ways to pick this
        assignment[var] = value
        qtable[value] += 1
        old_var_domains = fastCopy(var_domains)
        old_assignment = assignment[:]
        possible = update_domains(var, value, assignment, var_domains)
        #possible2 = auto_fill_group(var, value, assignment, var_domains)

        #print("VAR", var)
        if not possible:# or not possible2:
            return None
        #if is_valid(assignment): # TODO should be implied that it was valid from update_domains!
        result = recursive_backtrack(assignment, qtable, var_domains)  # go one layer deeper
        if result != None:
            return result  # no worries about reverting domains back
        else:
            #print("VAR",var)
            assignment = old_assignment  # this means that it ended up not working, so we need to try others
            qtable[value] -= 1  # that value is not used anymore
            var_domains = old_var_domains
            #print('broke')
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
    #print(is_valid(list('483921657967345821221876493458162976729594148196738243372689584814253769695417382')))
    #solve_puzzles(symbols)


if __name__ == '__main__':
    main()

# best = 102.6
