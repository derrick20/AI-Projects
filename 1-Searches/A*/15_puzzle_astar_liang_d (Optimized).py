# Derrick Liang 10/5/18
# Gaborian improvements
import math, random, time, heapq, collections


class PriorityQueue():
    """Implementation of a priority queue
            to store nodes during search."""

    # TODO 1 : finish this class

    # HINT look up/use the module heapq.

    def __init__(self):
        self.queue = []  # queue holds the nodes
        self.current = 0  # current is the index of the first

    def next(self):
        if self.current >= len(self.queue):
            self.current
            raise StopIteration

        out = self.queue[self.current]
        self.current += 1

        return out

    def pop(self):
        return heapq.heappop(self.queue)

    def remove(self, nodeId):
        # print(len(self.queue))
        self.queue = [node for node in self.queue if node[1][-1] != nodeId]
        # for i in range(len(self.queue) - 1):
        # if self.queue[-1-i][1][-1] == nodeId:
        #   return(self.queue.pop(i)) # find the first instance of

    def __iter__(self):
        return self

    def __str__(self):
        return 'PQ:[%s]' % (', '.join([str(i) for i in self.queue]))

    def append(self, node):
        heapq.heappush(self.queue, node)

    def __contains__(self, key):  # checks if path is in there
        self.current = 0
        return key in [n for v, n in self.queue]

    def __eq__(self, other):
        return self == other

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue = []

    def top(self):
        return self.queue[0]

    __next__ = next


def check_pq():
    ''' check_pq is checking if your PriorityQueue
    is completed or not'''
    pq = PriorityQueue()
    temp_list = []

    for i in range(10):
        a = random.randint(0, 10000)
        pq.append((a, 'a'))
        temp_list.append(a)

    temp_list = sorted(temp_list)

    for i in temp_list:
        j = pq.pop()
        if not i == j[0]:
            return False

    return True

# Extension #1
def inversion_count(new_state, size):
    ''' Depends on the size(width, N) of the puzzle,
    we can decide if the puzzle is solvable or not by counting inversions.
    If N is odd, then puzzle instance is solvable if number of inversions is even in the input state.
    If N is even, puzzle instance is solvable if
       the blank is on an even row counting from the bottom (second-last, fourth-last, etc.) and number of inversions is odd.
       the blank is on an odd row counting from the bottom (last, third-last, fifth-last, etc.) and number of inversions is even.
    '''
    inversions = 0
    for a in range(len(new_state)):
        a_count = 0
        for b in range(a + 1, len(new_state)):
            if new_state[a] != '_' and new_state[b] != '_' and get_value(new_state[a]) > get_value(new_state[b]):
                a_count += 1
        print(a_count)
        inversions += a_count

    if size % 2 == 1:  # odd size grid
        if inversions % 2 == 0:  # the number of inversions is even, like the solution state
            return True
        return False
    else:  # even size grid
        blank_row = new_state.index(
            '_') // size  # note, blank starts at odd row. Each vertical move causes an odd number of inversions (size - 1)
        print(inversions)
        if (
                inversions + blank_row) % 2 == 1:  # and also changes parity of the row. So if they have opposite parity it is solvable
            return True
        return False


def get_value(x):
    if x == '_':
        return 0
    elif x in 'ABCDEF':
        return 'ABCDEF'.index(x) + 10
    else:
        return int(x)


def getInitialState(sample):
    sample_list = list(sample)
    random.shuffle(sample_list)
    new_state = ''.join(sample_list)
    if (inversion_count(new_state, 4)):
        return new_state
    else:
        return None


def swap(n, i, j):  # precondition: i < j
    return str(n[:i] + n[j] + n[i + 1:j] + n[i] + n[j + 1:])


def generateChild(n, size):
    # Your code goes here
    adj_list = []
    i = n.index('_')  # assuming n is the node value
    if i >= size:  # we aren't in the first row ### NOOOOOOO it was 3 not size shoot
        adj_list.append(swap(n, i - size, i))
    if i < size * (size - 1):  # we aren't in the size-1 th row
        adj_list.append(swap(n, i, i + size))
    if i % size != 0:  # not in first column
        adj_list.append(swap(n, i - 1, i))  # I-1!!!!
    if (i + 1) % size != 0:  # not in size-1 th column
        adj_list.append(swap(n, i, i + 1))
    return adj_list


def display_path(path_list, size):
    for n in range(size):
        for i in range(len(path_list)):
            print(path_list[i][n * size:(n + 1) * size], end=" " * size)
        print()
    print("\nThe shortest path length is :", len(path_list))
    return ""


'''def dist_heuristic(start, lookup):
    # Your code goes here
    cost = 0
    hex = 'ABCDEF'
    for i in range(1, 16): # 1 to 15, since we want to see where each of these tiles properly are, and the dist
        char = start[i]
        if char == '_':
            continue # we don't want to compare distances of the blank space
        elif char in hex:
            val = 10 + hex.index(char) # trick to get the value of hexadecimals
        else:
            val = int(char)
        # technically don't need goal if we know what it is
        cost += abs((i % 4) - (val % 4)) + abs((i // 4) - (val // 4)) # subtract the value's row (currently at i) from it's proper row (at val), same for column
        # gets manhattan distance
        # Potentiall could use linear conflicts ( manhat + 2 * linear conflict, things that are in same row/col but path direction conflicts
    return cost#'''


def dist_heuristic(start, lookup):
    # Your code goes here
    cost = 0
    for i in range(0, 16):  # NEED 1 TO LEN!!
        cost += lookup[i][start[i]]
    return cost


def dist(index, char, size):
    hex = 'ABCDEF'
    if char == '_':
        return 0  # we don't want to compare distances of the blank space
    elif char in hex:
        val = 10 + hex.index(char)  # trick to get the value of hexadecimals
    else:
        val = int(char)
    # technically don't need goal if we know what it is
    return abs((index % size) - (val % size)) + abs((index // size) - (val // size))

size = 4
lookup = dict([])
for index in range(16):  # MAKE IT FASTER
    lookup[index] = dict([])
    for char in '_123456789ABCDEF':
        lookup[index][char] = dist(index, char, size)

f_incr = {}  # character, position, second position, all pointing to manhattan dist. Triple lookup incremental f
for index in range(16):
    f_incr[index] = {}
    for char in '123456789ABCDEF':
        f_incr[index][char] = {}
        old_dist = dist(index, char, size)
        if index >= size:  # we aren't in the first row, so down row is valid
            f_incr[index][char][index - size] = lookup[index - size][char] - old_dist + 1  # level always +1,
        if index < size * (size - 1):  # we aren't in the size-1 th row, so up a row is valid
            f_incr[index][char][index + size] = lookup[index + size][char] - old_dist + 1
        if index % size != 0:  # not in first column, so can go left
            f_incr[index][char][index - 1] = lookup[index - 1][char] - old_dist + 1
        if (index + 1) % size != 0:  # not in size-1 th column, so can go right
            f_incr[index][char][index + 1] = lookup[index + 1][char] - old_dist + 1

nbr_pos = {}
for index in range(16):
    nbr_pos[index] = []
    if index >= size:  # we aren't in the first row, so down row is valid
        nbr_pos[index].append(index - size)
    if index < size * (size - 1):  # we aren't in the size-1 th row, so up a row is valid
        nbr_pos[index].append(index + size)
    if index % size != 0:  # not in first column, so can go left
        nbr_pos[index].append(index - 1)
    if (index + 1) % size != 0:  # not in size-1 th column, so can go right
        nbr_pos[index].append(index + 1)

# keep going later with making more lookup table for a neighbor, that way when you want to recursively
# form the path/incremental heuristic, you have quick neighbor access/ also need to add spacePos characteristic
# to the tuples. Then, we can think about how the min dist changes with only one tile moved
# quaadruple swap, and then toting level reconstruct by lowering level each time..until no more parents (goal!))


def a_star(start, goal='_123456789ABCDEF', heuristic=dist_heuristic):
    '''A* algorithm use the sum of cumulative path cost and the heuristic value for each loop
    Update the cost and path if you find the lower-cost path in your process.
    You may start from your BFS algorithm and expand to keep up the total cost while moving node to node.
    '''
    # frontier = PriorityQueue()
    open_set = [[] for i in range(81)]


    if start == goal: return []
    # TODO 4: A* Search
    global lookup
    global f_incr
    global nbr_pos
    global size
    f = heuristic(start, lookup)
    open_set[f] = [(0, start)]  # set the first bucket, and also uses the level = 0
    closed_set = {}  # no longer use parents, or costs, since the open set now indicates the cost automatically (which bucket it's in)

    pos = 0  # the position with a certain bucket
    while True:
        if pos >= len(open_set[f]):  # this means we've finished that bucket and can toss it and proceed
            open_set[f] = []
            f += 1  # next bucket is f+1 index
            pos = 0  # new bucket, start over
            continue
        level, puzzle = open_set[f][pos]  # popping lowest cost in 'frontier'
        pos += 1  # step forward
        if puzzle in closed_set:  # this puzzle isn't good to explore
            continue
        closed_set[puzzle] = level  # otherwise, we add to explored. So 0-4 of the adjacencies
        if puzzle == goal:
            return path_to_root(closed_set, puzzle, nbr_pos)

        old_sp = puzzle.index('_')
        for nbr, new_sp in neighbors(puzzle, old_sp, nbr_pos):
            if nbr not in closed_set:
                delta_f = f_incr[new_sp][nbr[old_sp]][
                    old_sp]  # it's confusing, but new_sp is where the old char was, and old_sp is new char pos
                open_set[f + delta_f].append((level + 1, nbr))  # increased level, and new neighbor at that f

    return None


def neighbors(puzzle, sp_pos, nbr_pos):  # nbr_pos is the lookup table so we know an array of potential indices a space could move to
    pzl = list(puzzle)
    prior_pos = sp_pos
    nbrs = []
    for next_pos in nbr_pos[sp_pos]:
        pzl[prior_pos], pzl[sp_pos], pzl[next_pos], prior_pos = pzl[sp_pos], pzl[next_pos], pzl[prior_pos], next_pos
        # quadruple swap, kind of like spinning the neigbors/space in a circle
        nbrs.append((''.join(pzl), next_pos))  # so we don't have to make a copy of the puzzle every time
    return nbrs  # next_pos is where the space goes, that way we can use it for incremental cost finding (two in one function for finding space here)

def path_to_root(closed_set, pzl, nbr_pos):  # recursive...
    if closed_set[pzl] == 0:  # the level is 0, so we've reached the root
        return [pzl]
    else:  # we don't need to use the space component, but that's how the nodes are designed in neighbors() since we needed them for calculation earlier
        for nbr, sp in neighbors(pzl, pzl.index('_'), nbr_pos):  # use the nbr_pos lookup table
            if nbr in closed_set and closed_set[nbr] == closed_set[
                pzl] - 1:  # only one of these neighbors will be the correct one (1 level lower, closer to root)
                path = path_to_root(closed_set, nbr, nbr_pos)
                path.append(pzl)  # the pzl begins as goal state
                return path

def read_puzzles(file):
    # Eckel's 52 puzzle tester
    puzzles = []
    with open(file) as f:
        for line in f:
            puzzles.append(convert_puzzle(line))
    return puzzles

def convert_puzzle(puzzle):
    keys = '0ABCDEFGHIJKLMNO'
    values = '_123456789ABCDEF'
    ret = []
    map = {}
    for i in range(16):
        map[keys[i]] = values[i]
    for c in puzzle:
        ret.append(map[c])
    return ''.join(ret)

def main():

    initial_state = ''.join(input("Type initial state (Ex: 2_63514B897ACDEF): "))
    # convert_puzzle(input("Type initial state (Using letters): "))

    cur_time = time.time()
    path = (a_star(initial_state))
    if path != None:
        display_path(path, 4)
    else:
        print("No Path Found.")
    print("Duration: ", (time.time() - cur_time))  # '''

    '''puzzles = read_puzzles("Puzzles.txt")
    print(a_star(puzzles[0]))
    cur_time = time.time()
    for pzl in puzzles:
        print(a_star(pzl))
    print("Duration: ", (time.time() - cur_time))  # basically 30 minutes for 51'''


if __name__ == '__main__':
    main()
'''
 Sample output 1
PriorityQueue is good to go.

Initial State: 152349678_ABCDEF
1523    1523    1_23    _123    
4967    4_67    4567    4567    
8_AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 4
Duration:  0.0

Sample output 2
PriorityQueue is good to go.

Initial State: 2_63514B897ACDEF
2_63    _263    5263    5263    5263    5263    5263    5263    5263    52_3    5_23    _523    1523    1523    1_23    _123    
514B    514B    _14B    1_4B    14_B    147B    147B    147_    14_7    1467    1467    1467    _467    4_67    4567    4567    
897A    897A    897A    897A    897A    89_A    89A_    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    89AB    
CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 16
Duration:  0.005984306335449219

Sample output 3
PriorityQueue is good to go.

Initial state: 8936C_24A71FDB5E
8936    8936    8936    893_    89_3    8943    8943    8_43    84_3    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    8423    _423    4_23    4123    4123    4123    4123    _123    
C_24    C2_4    C24_    C246    C246    C2_6    C_26    C926    C926    C9_6    C916    C916    C916    C916    C916    C916    C916    C916    C916    _916    9_16    91_6    916_    9167    9167    9167    9167    9167    9167    _167    8167    8167    8_67    8567    8567    _567    4567    
A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A71F    A7_F    A_7F    AB7F    AB7F    AB7F    AB7_    AB_7    A_B7    _AB7    CAB7    CAB7    CAB7    CAB7    CAB_    CA_B    C_AB    C5AB    C5AB    _5AB    95AB    95AB    95AB    95AB    9_AB    _9AB    89AB    89AB    
DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    DB5E    D_5E    D5_E    D5E_    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D5EF    D_EF    _DEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    CDEF    

The shortest path length is : 37
Duration:  0.34381628036499023

E19648C5723_ABDF hard case

69FB83A1_57EC2D4
'''
