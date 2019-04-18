# 724506831
#125307468
# 786540321
#042135678
# 
import collections
import random

def main():
    initial = '724506831'  # input('Initial State: ')

    #print(BFS(initial))
    print(DFS(initial))
    #print(generate_children(('724506831', 'nothin')))
    print('done')

    # extension. Again, this works for BFS alone reasonable well (~1-2 minutes), but fails for DFS
    '''all_states = generate_states()
    sample_list = random.sample(all_states, 100)
    print(sample_list)
    bfs_total = 0
    dfs_total = 0
    for s in sample_list:
        bfs_total += BFS(s)
        dfs_total += DFS(s)
    bfs_total /= 100
    dfs_total /= 100
    print('BFS Average States Exanded: ' + str(bfs_total))
    print('DFS Average States Exanded: ' + str(dfs_total))'''



def DFS(initial):
    explored = set([initial])
    initial_state = (initial, '')
    frontier = [initial_state]
    count = 0

    while len(frontier) > 0:
        '''
        print('Explored r', end=' ')
        print(explored)
        print('Frontier ', end=' ')
        print(frontier)  # '''
        current_state = frontier.pop()
        if goal_test(current_state):
            path = current_state[1] + ' ' + current_state[0]
            print('States expanded: ' + str(count))
            return path.split(' ')
            #print(count) # Note that the above three lines are commented out because of the extension, same applies for BFS
            #return count

        possible = generate_children(current_state)

        #print(possible)
        for s in possible:
            if s[0] not in explored:
                frontier.append(s)
                #print(s[0], end=' ')
                explored.add(s[0])  # we don't want to add things to frontier if they have already been added
                count += 1  # those haven't been explored, but we need to track them either way
    return 'No solution'
    #return count # the above line is commented out for the extension, again for BFS


def BFS(initial):  # initial is a string representing initial state
    explored = set([initial])
    initial_state = (initial, '')
    frontier = collections.deque([initial_state])
    count = 0

    while len(frontier) > 0:
        current_state = frontier.popleft()
        # print(count)
        if goal_test(current_state):
            #path = current_state[1] + ' ' + current_state[0]
            #print('States expanded: ' + str(count))
            #return path.split(' ')
            return count

        # explored.add(current_state[0])
        possible = generate_children(current_state)
        for s in possible:
            if s[0] not in explored:
                frontier.append(s)
                explored.add(s[0])  # we don't want to add things to frontier if they have already been added
                count += 1  # those haven't been explored, but we need to track them either way
    return count #return 'No solution'


def generate_states(): # method for generating all states for sampling. Starting from the goal state, keep branching
    initial = '012345678'  # out until the entire tree has been explored
    explored = set([initial])
    initial_state = (initial, '')
    frontier = collections.deque([initial_state])
    while len(frontier) > 0:
        current_state = frontier.popleft()
        possible = generate_children(current_state)
        explored.add(current_state[0])

        for s in possible:
            if s[0] not in explored and s[0]:
                frontier.append(s)
                explored.add(s[0])  # we don't want to add things to frontier if they have already been added
    return explored


def goal_test(state):
    return state[0] == '012345678'


'''def generate_children(state, size):  # STATE is a TUPLE
    # print(state[0])
    i = str(state[0]).index('0')
    children = []
    if i < size * (size - 1):  # D
        children.append(swap(state, i, i + size))
    if (i + 1) % size != 0:  # R
        children.append(swap(state, i, i + 1))
    if i >= size:  # U
        children.append(swap(state, i - size, i))
    if i % size != 0:  # L
        children.append(swap(state, i - 1, i))  # first index must be less than second index
    return children
wasn't working'''
def generate_children(state):
    children = []
    str = state[0]
    i = str.index('0')
    if i >= 3: # we aren't in the first row
        children.append(swap(state, i - 3, i))
    if i <= 5: # we aren't in the third row
        children.append(swap(state, i, i + 3))
    if i % 3 != 0: # not in first column
        children.append(swap(state, i - 1, i)) # I-1!!!!
    if (i + 1) % 3 != 0: # not in third column
        children.append(swap(state, i, i + 1))
    return children

def swap(state, i, j):
    s = str(state[0])
    # print(s)
    new_state = str(s[:i]) + str(s[j]) + str(s[i + 1:j]) + str(s[i]) + str(s[j + 1:])

    if state[1] == '':
        return (new_state, str(state[0]))
    else:
        return (new_state, str(state[1]) + ' ' + str(state[0]))  # there is actually a path to add onto


def print_path(path, size):
    for state in path:
        for i in range(size):
            print(state[size * i:size * (i + 1)])
        print()  # add something to print the move


# 724506831
if __name__ == '__main__':
    main()
