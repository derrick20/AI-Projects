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
        #print(len(self.queue))
        self.queue = [node for node in self.queue if node[1][-1] != nodeId]
        #for i in range(len(self.queue) - 1):
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

def generate_adjacents(current, word_list): # WORKS
    ''' word_list is a set which has all words.
    By comparing current and words in the word_list,
    generate adjacents set and return it'''
    adj_set = set()
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(len(current)): # look through the large adj list
        for j in alpha: # check each character
            word = current[:i] + j + current[i+1:] # make a substition
            if word != current and word in word_list: # Check if it's in the word list (don't waste time if it's still itself)
                adj_set.add(word) # if so, add it to the adjacencies
    return adj_set

def dist_heuristic(v_current, goal): # WORKS
    ''' v is the current node. Calculate the heuristic function
    and then return a numeric value'''
    # TODO 3: heuristic
    return sum(1 for c1, c2 in zip(v_current, goal) if c1 != c2) # counts the # of differences between current and goal

def a_star(word_list, start, goal, heuristic=dist_heuristic):
    '''A* algorithm use the sum of cumulative path cost and the heuristic value for each loop
    Update the cost and path if you find the lower-cost path in your process.
    You may start from your BFS algorithm and expand to keep up the total cost while moving node to node.
    '''
    frontier = PriorityQueue()
    if start == goal: return []
    # TODO 4: A* Search
    initial_dist = heuristic(start, goal)
    initial_node = (initial_dist, [start]) # initial
    #explored = set(start)  # MUST HAVE INITIAL; explored only stores the names of nodes visited
    frontier.append(initial_node) # initialize frontier
    explored = {start: 0} # dictionary of costs to vertex V from start

    while frontier.size() > 0:
        v = frontier.pop() # pop the first in the frontier
        v_current = v[1][len(v[1])- 1] # last element of path is retrieved, aka current
        if v_current == goal: # goal test achieved
            return v[1] # the path

        adj_list = generate_adjacents(v_current, word_list)
        for adj_current in adj_list: # adj is just the name, not the node itself
            if adj_current not in set(v[1]): # don't check if it is in V's path
                adj_dist = explored[v_current] + 1 # Use the already stored dist from start to v, then add 1 since g (v_current, adj) = 1 always
                new_path = v[1] + [adj_current] # make a new adjacent path

                adj = (adj_dist + heuristic(adj_current, goal), new_path) # new vertex with estimated cost and new path

                if adj_current not in explored:
                    #explored.add(adj_current) # update explored
                    explored[adj_current] = adj_dist # put in this dist if we have never seen this node before
                    frontier.append(adj) # update frontier
                else:
                    if adj_dist < explored[adj_current]: # we reached this spot before, let's see if we have found a better route
                        explored[adj_current] = adj_dist # update distance
                        frontier.remove(adj_current)
                        frontier.append(adj) # append a new adj that has a shorter path to the same node
                # adj is a node, adj_current is the value, v is a node, v_current is the value
    return None


def main():
    word_list = set()
    file = open("words_6_longer.txt", "r")
    for word in file.readlines():
        word_list.add(word.rstrip('\n'))
    file.close()
    initial = input("Type the starting word: ")
    goal = input("Type the goal word: ")
    cur_time = time.time()
    path_and_steps = (a_star(word_list, initial, goal))
    if path_and_steps != None:
        print(path_and_steps)
        print("steps: ", len(path_and_steps))
        print("Duration: ", time.time() - cur_time)
    else:
        print("There's no path")#'''


if __name__ == '__main__':
    main()

'''Sample output 1
Type the starting word: listen
Type the goal word: beaker
['listen', 'lister', 'bister', 'bitter', 'better', 'beater', 'beaker']
steps:  7
Duration: 0.000997304916381836

Sample output 2
Type the starting word: vaguer
Type the goal word: drifts
['vaguer', 'vagues', 'values', 'valves', 'calves', 'cauves', 'cruves', 'cruses', 'crusts', 'crufts', 'crafts', 'drafts', 'drifts']
steps:  13
Duration: 0.0408782958984375

Sample output 3
Type the starting word: klatch
Type the goal word: giggle
['klatch', 'clatch', 'clutch', 'clunch', 'glunch', 'gaunch', 'launch', 'launce', 'paunce', 'pawnce', 'pawnee', 'pawned', 'panned', 'panged', 'banged', 'bunged', 'bungee', 'bungle', 'bingle', 'gingle', 'giggle']
steps:  21
Duration:  0.0867915153503418
''' #hmm about 4 times slower
['klatch', 'clatch', 'clutch', 'clunch', 'glunch', 'gaunch', 'paunch', 'paunce', 'pawnce', 'pawnee', 'pawned', 'panned', 'panged', 'banged', 'bunged', 'bungee', 'bungle', 'bingle', 'gingle', 'giggle']
['klatch', 'clatch', 'clutch', 'clunch', 'glunch', 'gaunch', 'paunch', 'paunce', 'pawnce', 'pawnee', 'pawned', 'panned', 'panged', 'ranged', 'ragged', 'raggee', 'raggle', 'gaggle', 'giggle']