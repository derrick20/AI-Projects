import collections

def main():
        try:
            file = open('words.txt', 'r')
            words = set([line.strip() for line in file])
            graph = {}
            for word in words:
                graph[word] = Node(word)
                for adjacent in generate_adj(word):
                    if adjacent in words:
                        graph[word].add_neighbor(adjacent) # add this new neighbor (a string)
            #print(graph)
            start = input('Starting 6-letter word: ')
            goal = input('Goal word: ')
            if len(start) != 6 or len(goal) != 6:# or start not in graph or goal not in graph:
                print('Word(s) are invalid')
                exit()

            explored = set([start])
            node = DFS_recur(start, goal, graph, explored)#'''
            print_path(node, graph)

        except FileNotFoundError:
            print('words.txt was not found')
            exit()


def DFS_recur(start, goal, graph, explored): # takes strings as the states
    if start == goal:
        return start # start will have a chain of predecessors up to the original
    else:
        for child in graph[start].get_neighbors(): # basically the graph has nodes, but the nodes all point to strings
            if child not in explored: # the graph access using a dict
                graph[child].set_pred(start)
                explored.add(child)
                #print(explored)
                result = DFS_recur(child, goal, graph, explored) #WHY YOU HAVE TO CHECK TWICE??
                if result == goal:
                    return result


def print_path(name, graph): # repeatedly gets pred and prints
    path = collections.deque()
    node = graph[name]
    while node.get_pred() != '':
        #print(node)
        #print(node.get_value())
        path.appendleft(node.get_value())
        node = graph[node.get_pred()]
    path.appendleft(node.get_value()) # need one more because the start's pred is '' but it didn't get printed
    print('The shortest path: ' + ', '.join(path))
    print('The number of steps: ' + str(len(path)))

class Node:
    def __init__(self, key): # the key and predecessors are strings, since the graph dict is a look up table
        self.value = key
        self.neighbors = []
        self.predecessor = ''

    def __repr__(self):
        return self.value + ' ' + self.predecessor

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def get_neighbors(self):
        return self.neighbors

    def set_pred(self, pred): # set predecessor
        self.predecessor = pred

    def get_pred(self):
        return self.predecessor

    def get_value(self):
        return self.value


def generate_adj(word):
    l = len(word)
    adj = []
    for i in range(l): # O(25 * 6) = O(150)
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c != word[i]: # so that you don't put in the own word
                adj.append(word[:i] + c + word[i + 1:])
    return adj

if __name__ == '__main__':
    main()