import time

# below are set up by the get_adjacencies method
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
    global domain, adjacencies_unfiltered, N  # we use unfiltered adjacencies for creating domains. We reduce problem size, then go back to filtered adjacencies
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


def fast_copy(var_domains):
    ret = {}
    for i in var_domains:
        ret[i] = var_domains[i].copy()
    return ret


def display_var_domains(var_domains):
    for var in var_domains:
        print(var, var_domains[var])


def backtracking(assignment, var_domains):
    return recursive_backtracking(assignment, var_domains)


def recursive_backtracking(assignment, var_domains):  # aassignment and var_domains will have to be passed locally
    if is_complete(assignment):
        return assignment

    var = minimum_remaining_values_var(assignment, var_domains)
    display_assignment(assignment)

    values = var_domains[var].copy()
    print(var, values)
    print(var_domains)
    for value in values:

        old_assignment = assignment[:]
        old_var_domains = fast_copy(var_domains)

        assignment[var] = value
        del var_domains[var]  # it is now forever set
        #update_domains(var, assignment, var_domains) # see how the assignment impacts the other domains
        solve_forward(var, assignment, var_domains)
        #if not allowed:
            #return None

        result = recursive_backtracking(assignment, var_domains)
        if result == None:
            print('helo')
            assignment = old_assignment
            var_domains = old_var_domains
    return None


def remove_inconsistent(i, j, assignment, var_domains):  # AC3 with its helper method
    removed = False
    display_var_domains(
        var_domains
    )
    if j in var_domains and i in var_domains and len(var_domains[j]) == 1 and var_domains[j] in var_domains[i]:  # j has no other values, so i cannot be that value. Delete it
        var_domains[i].remove(var_domains[j])
        removed == True
    return removed


def update_domains(var, assignment, var_domains): # var is to be set. While we're at it, set anything else with only one value
    # furthermore, for each var that becomes set, we must go around and make the domains consistent
    queue = [(var, Xj) for Xj in adjacencies[var]] # clean up adjacents of the changed var, not sure how to reduce this
    while queue:
        Xi, Xj = queue.pop()
        if remove_inconsistent(Xi, Xj, assignment, var_domains):
            for Xk in adjacencies[Xi]:
                queue.append(Xk, Xi)

def solve_forward(v, assignment, var_domains): #not sure how to apply it still
    global domain
    groups = [boxDict, rowDict, colDict]
    changed = [v] # start it off
    while len(changed) > 0:
        var = changed.pop()
        update_domains(var, assignment, var_domains)
        for group in groups:
            arc = group[var] # the group OF var
            unique_domain = domain.copy()
            [unique_domain.remove(list(var_domains[var])[0] for var in arc if len(var_domains[var]) == 1)]
            for value in domain:
                if sum([var_domains[adj].count(value) for adj in arc]) == 1:
                    to_delete = [adj for adj in arc if var_domains[adj].count(value) > 0][0]
                    assignment[to_delete] = var_domains[to_delete].pop()
                    del var_domains[to_delete]
                    changed.append(to_delete)
                    print("deleted", to_delete)




def minimum_remaining_values_var(assignment, var_domains):
    rem_values = {  # var -> domain size
        var: len(var_domains[var]) for var in var_domains
    }
    return min(rem_values, key=rem_values.get)


symbols = "123456789"
assignment = list("63..........5....8..5674.......2......34.1.2.......345.....7..4.8.3..9.29471...8.")
set_up(symbols)
create_adjacencies(assignment)
var_domains = create_domains(symbols, assignment)

solution = backtracking(assignment, var_domains)
display_assignment(solution)
