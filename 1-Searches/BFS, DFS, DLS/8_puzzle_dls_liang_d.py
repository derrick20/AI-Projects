import collections
import random

# 7245_6831
#1253_7468
# 78654_321
#_42135678

def main():
    #print(len(generate_states()))
    initial = input("initial: ")#'7245_6831'#str(random.choice(generate_states()))
    l = list(solve(initial, int(input('depth: '))))
    
    print('Path: ' + ', '.join(l[1:]))


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

def solve(start, limit):
   ''' you can modify this method '''
   explored = {start: ''}
   return recur(start, explored, limit)

def recur(start, explored, limit):
   ''' your code goes here '''
   if start == '_12345678': 
      return generate_path(explored)
   elif limit <= 0:
      return None
   else:
      for adj in generate_children(start):
         if adj not in explored: # something to do with each person's explored is unique, so you'd need a class for it?
            explored[adj] = start
            if adj == '_12345678':  # need to check here other wise it continues further
                return generate_path(explored)
            result = recur(adj, explored, limit - 1)
            if result != None:
               return result
   return None
   
def DFS(initial_state):
    explored = {initial_state : ''} # the explored dictionary will contain a state as key and its parent as value
    frontier = [initial_state] #LIST in DFS

    while len(frontier) > 0:
        current_state = frontier.pop() # just POP in DFS
        if current_state == '_12345678':
            path = generate_path(explored)
            #print(path)
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