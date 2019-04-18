import collections
import random
import math

# 7245_6831
#1253_7468
# 78654_321
#_42135678

def main():
    #print(len(generate_states()))
    initial = str(random.choice(generate_states()))
      
    print('BFS starts with: ' + initial)
    print('The shortest path length is: ' + str(BFS(initial)))

    '''print('DFS starts with: ' + initial)
    print('The solution path length is: ' + str(DFS(initial)))#'''
    #print(cost('_12345678'))


def swap(state, i, j): # precondition: i < j
    return str(state[:i] + state[j] + state[i + 1:j] + state[i] + state[j + 1:])

def generate_children(state):
    children = []
    i = state.index('_')
    if i >= 3: # we aren't in the first row
        children.append(swap(state, i - 3, i))
    if i <= 5: # we aren't in the third row
        children.append(swap(state, i, i + 3))
    if i % 3 != 0: # not in first column
        children.append(swap(state, i - 1, i)) # I-1!!!!
    if (i + 1) % 3 != 0: # not in third column
        children.append(swap(state, i, i + 1))
    return children
    
def cost(state):
   cost = 0
   if state == '':
      return math.inf # we use this to start out infinite to minimize it
   else:
      for i in range(9):
         if state[i] == '_':
            val = 0
         else:   
            val = int(state[i])
         cost += abs((val % 3) - (i % 3)) + abs((val // 3) - (i // 3))
      return cost      

def BFS(initial_state):
    explored = {initial_state : ''} # the explored dictionary will contain a state as key and its parent as value
    frontier = collections.deque([initial_state])

    while len(frontier)< 10:
        current_state = frontier.popleft()
        #print(explored.keys())
        #rprint(frontier)
        #print(current_state) # '1423_5678': '1_2345678'
        # and '1_2345678': '1423_5678' are in the list dictionary, somehow they are both added?!
        if current_state == '_12345678':
            path = generate_path(explored)
            print(path)
            return len(path)
        min_child = '' # this assumes there is a valid child below
        print(current_state)
        for c in generate_children(current_state):
            print('c' + str(cost(c)))
            print('min_child' + str(cost(min_child)))
            print( cost(c) < cost(min_child))
            if c not in explored and c != initial_state and cost(c) < cost(min_child):
               min_child = c
               explored[c] = current_state ## argghh heuristic wont work
        print(min_child)
        frontier.append(min_child)
        explored[min_child] = current_state # assigns a new key and set the value as the parent who generated children
    return 'No Solution'

def DFS(initial_state):
    explored = {initial_state : ''} # the explored dictionary will contain a state as key and its parent as value
    frontier = [initial_state] #LIST in DFS

    while len(frontier) > 0:
        current_state = frontier.pop() # just POP in DFS
        if current_state == '_12345678':
            path = generate_path(explored)
            print(path)
            return len(path)
        #print(current_state)
        for c in generate_children(current_state):
            if c not in explored:
                frontier.append(c)
                explored[c] = current_state # assigns a new key and set the value as the parent who generated children
    return 'No Solution'

def generate_path(explored):
    current_state = '_12345678'
    path = collections.deque([current_state])
    while current_state in explored: # if not, then it can't have a parent since it was never added
        path.appendleft(explored[current_state]) # add to path from the left to right
        current_state = explored[current_state] # go up one in the tree
   
    return path # basically return two things at once by PRINTING the path

def generate_states():
    explored = {'_12345678' : ''} # the explored dictionary will contain a state as key and its parent as value
    frontier = collections.deque(['_12345678'])

    while len(frontier) > 0:
        current_state = frontier.popleft()
        # DON'T CHECK for goal state
        #print(explored.keys())
        #print(explored)
        for c in generate_children(current_state):
            #print(explored.keys())
            if c not in explored:
                frontier.append(c)
                explored[c] = current_state # assigns a new key and set the value as the parent who generated children
    
    return list(explored.keys())

def print_state(state):
    for i in range(3):
        print(state[3 * i:3 * (i + 1)])
    print()  # add something to print the move

if __name__ == '__main__':
    main()