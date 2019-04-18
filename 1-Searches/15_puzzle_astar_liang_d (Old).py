# Derrick Liang 10/5/18
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
      
    if size % 2 == 1: # odd size grid
      if inversions % 2 == 0: # the number of inversions is even, like the solution state
         return True
      return False
    else: # even size grid
      blank_row = new_state.index('_') // size # note, blank starts at odd row. Each vertical move causes an odd number of inversions (size - 1) 
      print(inversions)
      if (inversions + blank_row) % 2 == 1: # and also changes parity of the row. So if they have opposite parity it is solvable
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

def swap(n, i, j): # precondition: i < j
    return str(n[:i] + n[j] + n[i + 1:j] + n[i] + n[j + 1:])

def generateChild(n, size):
    # Your code goes here
    adj_list = []
    i = n.index('_') # assuming n is the node value
    if i >= 3:  # we aren't in the first row
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


def dist_heuristic(start, goal, size):
    # Your code goes here
    cost = 0
    hex = 'ABCDEF'
    for i in range(1, size*size): # 1 to 15, since we want to see where each of these tiles properly are, and the dist
        if start[i] == '_':
            continue # we don't want to compare distances of the blank space
        elif start[i] in hex:
            val = 10 + hex.index(start[i]) # trick to get the value of hexadecimals
        else:
            val = int(start[i])
        # technically don't need goal if we know what it is
        cost += abs((i % size) - (val % size)) + abs((i // size) - (val // size)) # subtract the value's row (currently at i) from it's proper row (at val), same for column
        # gets manhattan distance
        # Potentiall could use linear conflicts ( manhat + 2 * linear conflict, things that are in same row/col but path direction conflicts
    return cost

def a_star(start, goal = '_123456789ABCDEF', heuristic=dist_heuristic):
    '''A* algorithm use the sum of cumulative path cost and the heuristic value for each loop
    Update the cost and path if you find the lower-cost path in your process.
    You may start from your BFS algorithm and expand to keep up the total cost while moving node to node.
    '''
    frontier = PriorityQueue()
    size = 4
    if start == goal: return []
    # TODO 4: A* Search
    
    initial_dist = heuristic(start, goal, size)
    initial_node = (initial_dist, [start]) # initial
    #explored = set(start)  # MUST HAVE INITIAL; explored only stores the names of nodes visited
    frontier.append(initial_node) # initialize frontier
    explored = {start: 0} # dictionary of costs to vertex V from start

    while frontier.size() > 0:
        v = frontier.pop() # pop the first in the frontier
        v_current = v[1][len(v[1])- 1] # last element of path is retrieved, aka current
        if v_current == goal: # goal test achieved
            return v[1] # the path

        adj_list = generateChild(v_current, size)
        for adj_current in adj_list: # adj is just the name, not the node itself
            if adj_current not in set(v[1]): # don't check if it is in V's path already
                adj_dist = explored[v_current] + 1 #TODO 1 # Use the already stored dist from start to v, then add 1 since g (v_current, adj) = 1 always
                new_path = v[1] + [adj_current] # make a new adjacent path

                adj = (adj_dist + heuristic(adj_current, goal, size), new_path) # new vertex with estimated cost and new path
                
                if adj_current not in explored:
                    explored[adj_current] = adj_dist # put in this dist if we have never seen this node before
                    frontier.append(adj) # update frontier
                else:
                    if adj_dist < explored[adj_current]: # we reached this spot before, let's see if we have found a better route
                        explored[adj_current] = adj_dist # update distance
                        frontier.remove(adj_current)
                        frontier.append(adj) # append a new adj that has a shorter path to the same node
                # adj is a node, adj_current is the value, v is a node, v_current is the value
    return None


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
    initial_state = convert_puzzle(input("Type initial state: "))

    cur_time = time.time()
    path = (a_star(initial_state))
    if path != None:
        display_path(path, 4)
    else:
        print("No Path Found.")
    print("Duration: ", (time.time() - cur_time))  # '''


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
'''