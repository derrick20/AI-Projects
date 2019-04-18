# ..9.8.26. 314..69.7...3..4.5..592. ....9..6..5.....436..9.6   ..7...8.76..192.31.9.7..
import time

variables = {}
for i in range(24):
    variables[i] = ['1', '2', '3', '4', '5', '6']

assignment = list("........................")  # 24 spaces
adjacencies = {}
'''rowsets = [set([0, 1, 2, 3, 4]), set([5, 6, 7, 8, 9, 10, 11]), set([12, 13, 14, 15, 16, 17, 18]),
           set([19, 20, 21, 22, 23]),
           set([1, 2, 6, 5, 12]), set([3, 2, 8, 7, 14, 13, 19]), set([4, 10, 9, 16, 15, 21, 20]),
           set([11, 13, 17, 22, 23]),
           set([3, 4, 10, 11, 13]), set([1, 2, 8, 9, 16, 17, 23]), set([0, 6, 7, 14, 15, 21, 22]),
           set([5, 12, 13, 19, 20])]'''
hexsets = [set([0, 1, 2, 6, 7, 8]), set([2, 3, 4, 8, 9, 10]),
           set([5, 6, 7, 12, 13, 14]), set([7, 8, 9, 14, 15, 16]), set([9, 10, 11, 16, 17, 18]),
           set([13, 14, 15, 19, 20, 21]), set([15, 16, 17, 21, 22, 23])]
adjsets = hexsets
count = 0

for i in range(24):
    for hex in adjsets:
        if i in hex: # var i is adjacent to each of these variables
            if i not in adjacencies:
                adjacencies[i] = hex.copy()
            else: # we can append to an old set to expand (repeats will be removed)
                adjacencies[i] = adjacencies[i] | hex.copy() # union
for i in range(24): # sweep through and make sure adjacencies exclude itself
    if i in adjacencies[i]: # Remove if it does include itself
        adjacencies[i].remove(i)

def backtracking_search():
    return recursive_backtrack(assignment)

def recursive_backtrack(assignment):
    if is_complete(assignment):
        return assignment
    var = select_least_constraining_var(assignment) # TODO you can swap this for any of the three selection methods
    for value in variables[
        var]:  # the 6 choices - we will modify this later, to update the domain over and over. For now be inefficient
        assignment[var] = value
        #print(assignment)
        if not is_valid(var, value, assignment):
            assignment[var] = '.'  # remove the assignment of that color, since it was invalid
        else:
            result = recursive_backtrack(assignment)  # go one layer deeper
            if result != None:
                return result
            else:
                assignment[var] = '.'  # this means that it ended up not working, so we need to try others
    return None

def select_minimum_remaining_values_var(assignment):
    unassigned_variables = [var for var in range(len(assignment)) if assignment[var] == '.'] # they haven't been assigned here
    var_domains = {}
    for var in unassigned_variables:
        domain = set([1,2,3,4,5,6])
        excluded = set()
        for adj in adjacencies[var]:
            if assignment[adj] != ".": # it has a value, which means the current var cannot have that value
                excluded.add(assignment[adj])
        var_domains[var] = domain - excluded # these are the only allowed domain of the var
    return min(var_domains, key=var_domains.get)

def is_unassigned(var, assignment):
    return assignment[var] == "."

def select_least_constraining_var(assignment): # somehow seems a lot slower
    constraints = {}
    unassigned_variables = [var for var in range(len(assignment)) if is_unassigned(var, assignment)] # they haven't been assigned here
    constraints = {
        var : sum([1 if is_unassigned(adj, assignment) else 0 for adj in adjacencies[var]]) for var in unassigned_variables
    } # dictionary comprehension
    '''for var in unassigned_variables:
        count = sum([1 if is_unassigned(adj, assignment) else 0 for adj in adjacencies[var]])
        for adj in adjacencies[var]:
            if assignment[adj] == '.':  # hasn't been assigned, so this will constrain it
                count += 1
        constraints[var] = count'''
    # print(constraints)
    return min(constraints, key=constraints.get)  # '''
    # simple forward hcecking
    '''for i in range(len(assignment)):
       if assignment[i] == ".":
          return i'''

def select_unassigned_var(assignment):
    for i in range(len(assignment)):
        if assignment[i] == ".":
            return i


def is_complete(assignment):
    global count
    count += 1
    display_assignment(assignment)
    if "." in assignment: # didn't fill in all the numbers yet
        return False
    for set in adjsets:
        adjset = list(set)
        for i in range(len(
                adjset)):  # check through each adjset and see if any pairwise are equal in the assingment. If so, return false
            var = adjset[i]
            for j in range(i+1, len(adjset)):
                adj = adjset[j]
                if assignment[adj] == assignment[var]:
                    return False
    return True


def is_valid(var, value, assignment):
    for adj in adjacencies[var]:
        if var != adj and assignment[adj] == value:  # this means that they aren't the same, but they are in the same set and have thes ame value, thus not valid anymore
            return False
    return True

# an assignment is a string
# each dot is a triangle
# each has an index
def display_assignment(solution):
    print(" " + ''.join(solution[0:5]) + "\n" + ''.join(solution[5:12]) + "\n" + ''.join(solution[12:19]) + "\n" + " " + ''.join(solution[19:24])) # print solution

def main():
    cur_time = time.time()
    solution = backtracking_search()
    next_time = time.time()
    print("Time: " + str(next_time - cur_time))
    print("Count: " + str(count))

    display_assignment(solution)

'''
Forward Checking
Time: 0.0011150836944580078
Count: 26
 12312
1456451
2631236
 24546

Minimum Remaining Values
Time: 0.001931905746459961
Count: 26
 12312
1456451
2631236
 24546
 
Least Constraining Variable
Time: 0.014110803604125977
Count: 235
 12312
1456451
2631263
 24534
'''

if __name__ == '__main__':
    main()