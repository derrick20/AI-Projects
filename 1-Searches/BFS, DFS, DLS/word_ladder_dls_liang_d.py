import collections

# vaguer, drifts: 28 steps GAVE UP!!!!
def main():
   try:
      file = open('words.txt', 'r')
      words = set([line.strip() for line in file])
      graph = {}
      for word in words:
         graph[word] = Node(word)
         for adjacent in generate_adj(word):
            if adjacent in words:
               graph[word].add_neighbor(adjacent)  # add this new neighbor (a string)
              # print(graph)
      start = 'foiled'  # input('Starting 6-letter word: ')
      end = 'cooper'  # input('Goal word: ')
      if len(start) != 6 or len(end) != 6:  # or start not in graph or goal not in graph:
         print('Word(s) are invalid')
         exit()
      print('hello')
      # generate all the depths in the graph now
      generate_depths(start, graph)
      #print(explored)
      limit = 8
      final = depth_limited_search(start, end, graph, limit)  # '''
      print(', '.join(final))
   #deque(['foiled', 'fooled', 'footed', 'hooted', 'hooter', 'hooper', 'cooper'])
   #foiled, coiled, cooled, cooped, cooper
   except FileNotFoundError:
      print('words.txt was not found')
      exit()


def generate_depths(start, graph):
   explored = {start : ''} # MUST HAVE INITIAL!!!!
   frontier = [start]
   graph[start].set_depth(0) # since it is the start
   while len(frontier) > 0:
      current = frontier.pop() # current is just a string
      # we use the graph to give us more strings for future 'currents'
      for state in graph[current].get_neighbors(): # we cannot do a for each because that doesn't modify the graph
         if graph[state].get_depth() >= graph[start].get_depth():
            graph[state].set_depth(graph[current].get_depth() + 1)
            explored[state] = current #CHILD, PARENT
            frontier.append(state) # added as a string, because this makes it more convenient here.
        #print(graph[current].get_neighbors())

def depth_limited_search(start, end, graph, limit):
    # explored is a dict with child, parent
   explored = {start : ''}
   #print(explored)
   return recur_DLS(start, end, graph, explored, limit)


def recur_DLS(start, end, graph, explored, limit):  ## MODIFY WITH DEREK
   if start == end:
      print(end)
      return path(end, explored)
   elif limit == 0:
      return None
   else:
      #print(str(graph[start].depth) + start + str(limit))
      #print(graph[start].get_neighbors())
   
      for adj in graph[start].get_neighbors():
      
         if graph[adj].get_depth() >= graph[start].get_depth(): # this means that it is not one of start's ancestors
            explored[adj] = start
            print(limit-1)
            print(adj)
            # No need to keep track of the path of each node, just form it at the end when it's needed
            result = recur_DLS(adj, end, graph, explored, limit - 1)
            if result != None:
               return result
   return None

def path(end, explored):
   current = explored[end]
   path = collections.deque([end])
   while current != '':
      path.appendleft(current)
      current = explored[current]
   return path # in order start to end

def print_path(name, graph):
   path = graph[name].get_path()

   print('The shortest path: ' + ', '.join(path))
   print('The number of steps: ' + str(len(path)))


class Node:
   def __init__(self, key):  # the key and predecessors are strings, since the graph dict is a look up table
      self.value = key
      self.path = [key]
      self.depth = -100
      self.neighbors = []

   def __repr__(self):
      return self.value + ': ' + self.depth

   def add_neighbor(self, adj):
      self.neighbors.append(adj)

   def get_neighbors(self):
      return self.neighbors

   def get_path(self):
      return self.path

   def set_depth(self, d):
      self.depth = d

   def get_depth(self):
      return self.depth


def generate_adj(word):
   l = len(word)
   adj = []
   for i in range(l):  # O(25 * 6) = O(150)
      for c in 'abcdefghijklmnopqrstuvwxyz':
         if c != word[i]:  # so that you don't put in the own word
            adj.append(word[:i] + c + word[i + 1:])
   return adj


if __name__ == '__main__':
   main()