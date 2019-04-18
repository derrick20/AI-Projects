import collections
import random


# 7245_6831
# 1253_7468
# 78654_321
# _42135678

def main():
    # PART 1
    print('Part 1: ' + str(len(generate_states())))

    # PART 2 # idea: make a new node class that tracks the node depths and then
    x = len(BFS('_12345678'))
    print('Part 2: ' + str(x))

    # PART 3, it's the same thing
    print('Part 3: ' + str(x))

def BFS(initial):  # initial is a string representing initial state
    explored = set([initial])
    initial_state = (initial, '')
    frontier = collections.deque([initial_state])
    unique = {}  # key is a tuple state, the value is the length
    not_unique = set()  # set of keys of states from unique that aren't unique

    while len(frontier) > 0:

        current_state = frontier.popleft()
        explored.add(current_state[0]) # need to add to explored not when generating children because it's
        # has to try checking it another time?
        if current_state[0] in unique and unique[current_state[0]] == length(
                current_state):  # but you will find states in order of shortest to longest so we're good
            unique.pop(current_state[0])
            not_unique.add(current_state[0])  # may be possible that you see something in unique twice but second one is shorter

        elif current_state[0] not in unique and current_state[0] not in not_unique:  # never seen before, so first time
            unique[current_state[0]] = length(current_state)
        possible = generate_children(current_state)
        for s in possible:
            if s[0] in unique and unique[s[0]] == length(s):  # but you will find states in order of shortest to longest so we're good
                unique.pop(s[0])
                not_unique.add(s[0]) #4321_5678
            if s[0] not in explored:
                frontier.append(s) # normally we add to explored here, we want to expand its children in another
                # round of looping to make sure
                # originally i put add to explored here but that didn't work,
                  # we don't want to add things to frontier if they have already been added
                # those haven't been explored, but we need to track them either way
    #print(unique)
    #print(not_unique)
    #print(len(not_unique))

    return unique


def length(state):
    return len(state[1].split(' ')) + 1


def generate_states():  # method for generating all states for sampling. Starting from the goal state, keep branching
    initial = '_12345678'  # out until the entire tree has been explored
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
    return state[0] == '_12345678'


def generate_children(state):
    children = []
    str = state[0]
    i = str.index('_')
    if i >= 3:  # we aren't in the first row
        children.append(swap(state, i - 3, i))
    if i <= 5:  # we aren't in the third row
        children.append(swap(state, i, i + 3))
    if i % 3 != 0:  # not in first column
        children.append(swap(state, i - 1, i))  # I-1!!!!
    if (i + 1) % 3 != 0:  # not in third column
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


if __name__ == '__main__':
    main()
