# ..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
# ..7369825632158947958724316825437169791586432346912758289643571573291684164875293
# .3..5..4...8.1.5..46.....12.7.5.2.8....6.3....4.1.9.3.25.....98..1.2.6...8..6..2.
# ....8....27.....54.95...81...98.64...2.4.3.6...69.51...17...62.46.....38....9....
# hard ones:
# 4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
# 52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
# 6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....
import time

adjacencies = {}
domain = set([str(i) for i in range(1, 10)])
boxes = []
rows = []
cols = []
assignment = []  # TODO to be assigned
# it's good to make them into sets early on, that way you don't repeatedly have to waste time converting it into set
# converting list to set is N*1 = O(N)
top_left_corners = [0, 3, 6, 27, 30, 33, 54, 57, 60]
for corner in top_left_corners:
    boxes.append(set([corner + i + j for i in [0, 1, 2] for j in
                      [0, 9, 18]]))  # set up a box, using the corner, and adding 0,1,2 and 0,9,18
rows = [set([9 * r + c for c in range(9)]) for r in
        range(9)]  # starting from 0th row, the elements of a row are 0-9 plus a 9*what row it's on
cols = [set([9 * r + c for r in range(9)]) for c in
        range(9)]  # start from 0th column, (0,9,18...). Inner array is modifying more rapidly

'''for i in range(9):
    print(rows[i])
    print(cols[i])'''
# create adjacencies
for var in range(81):
    adjset = set()
    for box in boxes:
        if var in box:
            adjset = adjset | box.copy()
            break  # we found a box that contains it
    adjset = adjset | rows[var // 9].copy() | cols[var % 9].copy()
    adjset.remove(var)  # we don't consider itself to be adjacent
    # print(adjset)
    adjacencies[var] = adjset

count = 0


def backtracking_search():
    return recursive_backtrack(assignment)

def recursive_backtrack(assignment):
    if is_complete(assignment):
        return assignment
    var = select_least_constraining_var(assignment)  # TODO you can swap this for any of the three selection methods
    for value in min_conflicts_value(var, assignment):  # the 9 choices - we will modify this later, to update the domain over and over. For now be inefficient
        assignment[var] = value
        if not is_valid(var, value, assignment):
            assignment[var] = '.'  # remove the assignment of that color, since it was invalid
        else:  # it worked
            result = recursive_backtrack(assignment)  # go one layer deeper
            if result != None:
                return result
            else:
                assignment[var] = '.'  # this means that it ended up not working, so we need to try others
    return None


def min_conflicts_value(var, assignment): # returns an ascending list of the values ranked by # conflicts
    conflicts = {}
    for value in domain:
        conflicts[value] = sum([1 if assignment[adj] != "." and value == assignment[adj] else 0 for adj in adjacencies[var]])
    # go through all of the adjacents and count the number of conflicts whenever it's assigned and has a different number
    #print(var)
    #print(conflicts)
    #display_assignment(assignment)
    return sorted(conflicts, key=conflicts.get)


def select_minimum_remaining_values_var(assignment):
    unassigned_variables = [var for var in range(len(assignment)) if
                            assignment[var] == '.']  # they haven't been assigned here
    var_domains = {}
    for var in unassigned_variables:
        excluded = set()
        for adj in adjacencies[var]:
            if assignment[adj] != ".":  # it has a value, which means the current var cannot have that value
                excluded.add(assignment[adj])
        var_domains[var] = domain - excluded  # these are the only allowed domain of the var
    return min(var_domains, key=var_domains.get)

def is_unassigned(var, assignment):
    return assignment[var] == "."

def select_least_constraining_var(assignment):
    constraints = {}
    unassigned_variables = [var for var in range(len(assignment)) if
                            assignment[var] == '.']  # they haven't been assigned here
    unassigned_variables = [var for var in range(len(assignment)) if
                            is_unassigned(var, assignment)]  # they haven't been assigned here
    constraints = {
        var: sum([1 if is_unassigned(adj, assignment) else 0 for adj in adjacencies[var]]) for var in
    unassigned_variables
    }
    #for var in unassigned_variables:
    #    constraints[var] = sum([1 if assignment[adj] == "." else 0 for adj in adjacencies[var]])

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
    # display_assignment(assignment)
    if "." in assignment:  # didn't fill in all the numbers yet
        return False
    for var in adjacencies:
        adjlist = list(adjacencies[var])
        for adj in adjlist:
            if assignment[var] == assignment[adj]: # can't list comprehend this because this will automatically break, so probably best to leave it as is
                return False
    return True

def is_valid(var, value, assignment): # O(N), N = # adjacents. Can't improve this
    return sum([1 if assignment[adj] == value else 0 for adj in adjacencies[var]]) == 0
# if we search through all the values in adjacent and counted 0 that were equal to the value, then return True

'''def set_assignment(str):
   assignment = list(str)
   print(assignment[0:3])
   for i in range(9):
      assignment.append([]) # a new row of variables is added
      for j in range(9): # to that new row, append the variables themselves
         assignment[i].append(str[9*i + j]) # this tracks the position while going through the string 9*0+0, 9*0+1, 9*0+2... 9*1+0...9*8+8'''


def display_assignment(assignment):
    for r in range(9):  # print solution
        row = assignment[9 * r:9 * (r + 1)]
        print(" ".join(row[:3]) + "  " + " ".join(row[3:6]) + "  " + " ".join(row[6:]))
        if r % 3 == 2:
            print()


def main():
    '''global assignment
    assignment = list(input("Input state: "))
    display_assignment(assignment)
    # display_assignment(assignment)
    cur_time = time.time()
    solution = backtracking_search()
    next_time = time.time()
    print("Time: " + str(next_time - cur_time))
    print("Count: " + str(count))

    display_assignment(solution)  # '''
    global assignment
    puzzles = []
    with open("puzzles.txt") as f: # set
      for line in f:
         puzzles.append(list(line)[:-1])
    print(len(puzzles[0]))
    cur_time = time.time()
    count = 1
    for puzzle in puzzles:
      assignment = puzzle
      print(count,backtracking_search())
      count += 1
    next_time = time.time()
    print("Time: " + str(next_time - cur_time))
    #print("Count: " + str(count))

if __name__ == '__main__':
    main()
'''
..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
..7369825632158947958724316825437169791586432346912758289643571573291684164875293
.3..5..4...8.1.5..46.....12.7.5.2.8....6.3....4.1.9.3.25.....98..1.2.6...8..6..2.
....8....27.....54.95...81...98.64...2.4.3.6...69.51...17...62.46.....38....9....
hard ones:
4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....

8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..


 
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

