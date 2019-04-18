# Derrick Liang 10/26/18
import collections, heapq, random, pickle, math, time
from math import pi, acos, sin, cos

import tkinter
root = tkinter.Tk()
root.configure(highlightthickness = 0, borderwidth = 0)
lines = {} # tuple of ids points to the config thing

width = 1000
height = 800
root.geometry(str(width) + "x" + str(height))
canvas = tkinter.Canvas(root, width = 1000, height = 800)
canvas.pack()

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

    def contains(self, nodeId):  # checks if path is in there
        for node in self.queue:
            if node[1][-1] == nodeId:
                return True
        return False

    def get(self, nodeId):
        for node in self.queue:
            if node[1][-1] == nodeId:
                return node
        return None

    def __eq__(self, other):
        return self == other

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue = []

    def top(self):
        return self.queue[0]

    __next__ = next


'''Making class Graph(), Node(), and Edge() are optional'''
'''You can make any helper methods'''
def make_line(n1, n2, graph, color):
    y1 = 12 * (130.35722 + graph['nodes'][n1][1])  # y is latitude
    x1 = 12.9 * (-14.68673 + graph['nodes'][n1][0])
    y2 = 12 * (130.35722 + graph['nodes'][n2][1])
    x2 = 12.9 * (-14.68673 + graph['nodes'][n2][0])
    if (n1, n2) not in lines:
        line = canvas.create_line(75 + y1, 650 - x1, 75 + y2, 650 - x2, fill = color)
        lines[(n2, n1)] = line
        lines[(n1, n2)] = line
    else: # just change existing line color
        canvas.itemconfig(lines[(n1, n2)], fill = color)

def make_graph(nodes_file, node_city_file, edge_file):
    graph = {'nodes': {}, 'edges': {}, 'adj_list': {}, 'nodeToCity': {}, 'cityToNode': {}}
    global canvas
    global root
    minlat = 100000
    maxlat = 0
    minlong = 100000
    maxlong = 0
    with open(nodes_file) as f:
        for line in f:
            node_id, x, y = [i for i in line.split(' ')]
            tup = (float(x), float(y))
            if tup[0] < minlong:
                minlong = tup[0]
            if tup[1] < minlat:
                minlat = tup[1]
            if tup[0] > maxlong:
                maxlong = tup[0]
            if tup[1] > maxlat:
                maxlat = tup[1]
            graph['nodes'][node_id] = tup
    # print(minlong, minlat, maxlong, maxlat)
    with open(node_city_file) as f:
        for line in f:
            i = line.index(' ')
            node_id = line[:i].strip()
            city_name = line[i + 1:].strip()
            graph['nodeToCity'][node_id] = city_name
            graph['cityToNode'][city_name] = node_id

    with open(edge_file) as f:
        for line in f:
            n1, n2 = [x.strip() for x in line.split(' ')]
            edge_cost = calc_edge_cost(n1, n2, graph)  # use the graph id coordinates

            make_line(n1, n2, graph, "black")

            graph['edges'][(n1, n2)] = edge_cost
            graph['edges'][(n2, n1)] = edge_cost

            if n1 not in graph['adj_list']:
                graph['adj_list'][n1] = set([n2])
            else:
                graph['adj_list'][n1].add(n2)
            if n2 not in graph['adj_list']:
                graph['adj_list'][n2] = set([n1])
            else:
                graph['adj_list'][n2].add(n1)
    root.update()
    return graph


def calc_edge_cost(start, goal, graph):  # start and goal are node ids!!!
    # TODO: calculate the edge cost from start city to end city
    #       by using the great circle distance formula.
    #       Refer the distanceDemo.py
    start_node = graph['nodes'][start]
    goal_node = graph['nodes'][goal]
    x1 = float(start_node[1]) # LONGITUDE is X
    y1 = float(start_node[0]) # LATITUDE IS Y
    x2 = float(goal_node[1])
    y2 = float(goal_node[0])
    #
    R = 3958.76  # miles = 6371 km
    #
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos(min(1, sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1))) * R

def cost(node_path, graph):
    previous = node_path[0]
    cost = 0
    for i in range(1, len(node_path)):
        current = node_path[i]
        cost += graph['edges'][(previous, current)]
        previous = current
    return cost

def BFS_path(start, goal, explored, graph):  # this time, start and goal are the actual ids
    current = goal
    node_path = collections.deque([current])
    city_path = collections.deque([graph['nodeToCity'][current]])
    count = 0
    while current != start:
        previous = current
        current = explored[current]
        make_line(previous, current, graph, "green")
        if count % 50 == 0:
            root.update()
        if current in graph['nodeToCity'] and graph['nodeToCity'][current] in graph[
            'cityToNode']:  # if it's a major city, add to city path
            city_path.appendleft(graph['nodeToCity'][current])
        node_path.appendleft(current)  # the path is just node ids
    print('Cost: ' + str(cost(node_path, graph)))
    print('node path: ' + str(list(node_path)))
    print('number of explored: ' + str(len(explored)))
    print(len(node_path))
    return list(city_path)  # (l, graph) # a bit less efficient since two loops rather than at same time, but only run once so not significant


def city_path(node_path, graph):  # for some reason, you can't pass a deque into this
    city_path = []
    for node_id in node_path:
        if node_id in graph['nodeToCity'] and graph['nodeToCity'][node_id] in graph[
            'cityToNode']:  # if it's a major city, add to city path
            city_path.append(graph['nodeToCity'][node_id])
    return city_path


def breadth_first_search(start_id, goal_id,
                         graph):  # convert the city name into node, which is what we use when searchin when searching, use node ids, then when printing path convert into city names
    # TODO: finish this method
    #       print the number of explored nodes somewhere
    frontier = collections.deque([start_id])
    explored = {start_id: ''}
    count = 0
    while len(frontier) > 0:
        current = frontier.popleft()
        if count % 100 == 0:
            root.update()
        if current == goal_id:
            return BFS_path(start_id, goal_id, explored, graph)

        for adj in graph['adj_list'][current]:
            if adj not in explored:
                make_line(current, adj, graph, "red")
                count +=1
                explored[adj] = current
                frontier.append(adj)


def dist_heuristic(v, goal, graph):
    return calc_edge_cost(v, goal, graph)

def A_star_path(node_path, g, graph):
    print('Cost: ' + str(cost(node_path, graph)))#str(g[node_path[-1]]))
    print('node path: ' + str(node_path))
    print('number of explored: ' + str(len(g)))
    print(len(node_path))
    count = 0
    for i in range(1, len(node_path)):
        if count % 100 == 0:
            root.update()
        make_line(node_path[i-1], node_path[i], graph, "green")
        count += 1
    return city_path(node_path, graph)


def a_star(start_id, goal_id, graph, heuristic=dist_heuristic):  # use the ids
    # TODO: Implement A* search algorithm
    #       print the number of explored nodes somewhere
    frontier = PriorityQueue()
    if start_id == goal_id: return []
    # TODO 4: A* Search
    initial_dist = heuristic(start_id, goal_id, graph)
    initial_node = (initial_dist, [start_id])  # (f, path (which has the current at the end))
    frontier.append(initial_node)  # initialize frontier
    g = {start_id: 0}  # cost stores
    count = 0

    while frontier.size() > 0:
        v = frontier.pop()  # pop the first in the frontier
        v_current = v[1][-1]  # end of current list is the current v
        if v_current == goal_id:  # goal test achieved
            return (v[1], g)  # the path it had, explored, and the graph
        count += 1
        if count % 100 == 0:
            root.update()
        adj_list = graph['adj_list'][v_current]
        for adj_current in adj_list:  # adj is just the name, not the node itself
            if adj_current not in set(v[1]):  # avoid sets to avoid checking path again
                dist = graph['edges'][(v_current, adj_current)]  # the direct cost
                current_length = g[v_current] + dist  # track a new cost in path

                new_f = current_length + heuristic(adj_current, goal_id, graph)
                new_path = v[1] + [adj_current]
                adj = (new_f, new_path)  # f, current, old_path + the current

                make_line(v_current, adj_current, graph, "red")

                if adj_current not in g: # not yet explored
                    g[adj_current] = current_length  # new cost determined from start to current
                    frontier.append(adj)  # update frontier
                else:
                    if current_length < g[adj_current]:  # this means that the value stored in explored may not be correct
                        g[adj_current] = current_length
                        frontier.remove(adj_current)  # remove the node that had the lower path length
                        frontier.append(adj)  # now we will put in something that reaches that location faster
    return None #'''


def bidirectional_BFS_path(start_id, goal_id, explored, graph):
    current = goal_id
    node_path = collections.deque([current])
    city_path = collections.deque([])

    if current in graph['nodeToCity']:
        city_path.append(graph['nodeToCity'][current])  # if the middle has some city Name
    while current != start_id:
        previous = current
        current = explored[
            current]  # goes from child to parent repeatedly, once current = start and is appended, return path

        if current in graph['nodeToCity'] and graph['nodeToCity'][current] in graph[
            'cityToNode']:  # if it's a major city, add to city path
            city_path.appendleft(graph['nodeToCity'][current])
        node_path.appendleft(current)  # the path is just node ids
    node_path = list(node_path)
    return {'cost': cost(node_path, graph), 'node path': node_path,
            'city path': list(city_path)}  # dictionary of some values needed to be combined


def bidirectional_BFS(start_id, goal_id, graph):
    # TODO: Implement bi-directional BFS
    #       print the number of explored nodes somewhere
    frontier_f = collections.deque([start_id])
    explored_f = {start_id: ''}
    frontier_b = collections.deque([goal_id])
    explored_b = {goal_id: ''}
    count = 0

    while len(frontier_f) > 0 and len(frontier_b) > 0:
        # forward BFS
        current_f = frontier_f.popleft()
        count += 2
        if count % 100 == 0:
            root.update()

        if current_f in frontier_b:  # if you find something in the other one's frontier, then we have met
            f_info = bidirectional_BFS_path(start_id, current_f, explored_f, graph)
            b_info = bidirectional_BFS_path(goal_id, current_f, explored_b, graph)
            total_cost = f_info['cost'] + b_info['cost']
            node_path = f_info['node path'] + b_info['node path'][:-1][::-1]  # combine the paths, remove the double counted middle
            if current_f in graph['nodeToCity']:  # this means that we need to cut out the duplicate
                city_path = f_info['city path'] + b_info['city path'][:-1][::-1]
            else:  # no overlap
                city_path = f_info['city path'] + b_info['city path'][::-1]
            show_node_path(node_path, graph)
            print('Cost: ' + str(total_cost))
            print('node path: ' + str(node_path))
            print('number of explored forward: ' + str(len(explored_f)))
            print('number of explored backward: ' + str(len(explored_b)))
            print(len(node_path))
            return city_path

        for adj in graph['adj_list'][current_f]: # Apply BFS for the forward direction
            if adj not in explored_f:
                explored_f[adj] = current_f
                make_line(current_f, adj, graph, "red")
                frontier_f.append(adj)
        # backwards BFS
        current_b = frontier_b.popleft()

        if current_b in frontier_f:  # same as above, but reverseed
            f_info = bidirectional_BFS_path(start_id, current_b, explored_f, graph)
            b_info = bidirectional_BFS_path(goal_id, current_b, explored_b, graph)
            total_cost = f_info['cost'] + b_info['cost']
            node_path = f_info['node path'] + b_info['node path'][:-1][::-1]  # combine the paths, remove the double counted middle
            if current_b in graph['nodeToCity']:  # this means that we need to cut out the duplicate
                city_path = f_info['city path'] + b_info['city path'][:-1][::-1]
            else:  # no overlap
                city_path = f_info['city path'] + b_info['city path'][::-1]
            show_node_path(node_path, graph)
            print('Cost: ' + str(total_cost))
            print('node path: ' + str(node_path))
            print('number of explored forward: ' + str(len(explored_f)))
            print('number of explored backward: ' + str(len(explored_b)))
            print(len(node_path))
            return city_path

        for adj in graph['adj_list'][current_b]:# Apply BFS for the backward direction
            if adj not in explored_b:
                explored_b[adj] = current_b
                make_line(current_b, adj, graph, "red")
                frontier_b.append(adj)

def show_node_path(node_path, graph):
    count = 0
    for i in range(1, len(node_path)):
        count += 1
        if count % 100 == 0:
            root.update()
        make_line(node_path[i - 1], node_path[i], graph, "green")

def bidirectional_a_star(start_id, goal_id, graph, heuristic=dist_heuristic):
    # TODO: Implement bi-directional A*
    #       print the number of explored nodes somewhere
    frontier_f = PriorityQueue()
    frontier_b = PriorityQueue()


    if start_id == goal_id: return []
    # TODO 4: A* Search
    initial_dist = heuristic(start_id, goal_id, graph)
    initial_node_f = (initial_dist, [start_id])  # (f, path (which has the current at the end))
    initial_node_b = (initial_dist, [goal_id])
    frontier_f.append(initial_node_f)  # initialize frontier
    frontier_b.append(initial_node_b)
    g_f = {start_id: 0}  # cost stores
    g_b = {goal_id: 0}
    count = 0

    while frontier_f.size() > 0 and frontier_b.size()> 0:
        v_f = frontier_f.pop()  # pop the first in the frontier
        v_current_f = v_f[1][-1]  # end of current list is the current v
        count += 2
        if count % 100 == 0:
            root.update()

        if frontier_b.contains(v_current_f):  # goal test achieved
            v2 = frontier_b.get(v_current_f)
            node_path = v_f[1] + v2[1][:-1][::-1]
            print('Cost: ' + str(cost(node_path, graph)))
            print('node path: ' + str(node_path))
            show_node_path(node_path, graph)
            return city_path(node_path, graph)  # the path it had, explored, and the graph

        adj_list_f = graph['adj_list'][v_current_f]
        for adj_current in adj_list_f:  # adj is just the name, not the node itself
            if adj_current not in set(v_f[1]):  # avoid sets to avoid checking path again
                dist = graph['edges'][(v_current_f, adj_current)]  # the direct cost
                current_length = g_f[v_current_f] + dist  # track a new cost in path

                new_f = current_length + heuristic(adj_current, goal_id, graph)
                new_path = v_f[1] + [adj_current]
                adj = (new_f, new_path)  # f, current, old_path + the current
                make_line(v_current_f, adj_current, graph, "red")

                if adj_current not in g_f:
                    g_f[adj_current] = current_length  # new cost determined from start to current
                    frontier_f.append(adj)  # update frontier
                else:
                    if current_length < g_f[
                        adj_current]:  # this means that the value stored in explored may not be correct
                        g_f[adj_current] = current_length
                        frontier_f.remove(adj_current)  # remove the node that had the lower path length
                        frontier_f.append(adj)  # now we will put in something that reaches that location faster

        v_b = frontier_b.pop()  # pop the first in the frontier
        v_current_b = v_b[1][-1]  # end of current list is the current v

        if frontier_f.contains(v_current_b):  # goal test achieved
            v2 = frontier_f.get(v_current_b)
            node_path = v2[1] + v_b[1][:-1][::-1]
            print('Cost: ' + str(cost(node_path, graph)))
            print('node path: ' + str(node_path))
            show_node_path(node_path, graph)
            return city_path(node_path, graph)  # the path it had, explored, and the graph

        adj_list_b = graph['adj_list'][v_current_b]
        for adj_current in adj_list_b:  # adj is just the name, not the node itself
            if adj_current not in set(v_b[1]):  # avoid sets to avoid checking path again
                dist = graph['edges'][(v_current_b, adj_current)]  # the direct cost
                current_length = g_b[v_current_b] + dist  # track a new cost in path

                new_f = current_length + heuristic(adj_current, goal_id, graph)
                new_path = v_b[1] + [adj_current]
                adj = (new_f, new_path)  # f, current, old_path + the current
                make_line(v_current_b, adj_current, graph, "red")
                if adj_current not in g_b:
                    g_b[adj_current] = current_length  # new cost determined from start to current
                    frontier_b.append(adj)  # update frontier
                else:
                    if current_length < g_b[
                        adj_current]:  # this means that the value stored in explored may not be correct
                        g_b[adj_current] = current_length
                        frontier_b.remove(adj_current)  # remove the node that had the lower path length
                        frontier_b.append(adj)  # now we will put in something that reaches that location faster



    return None


def tridirectional_search(goals, graph, heuristic=dist_heuristic):
    # TODO: Do this! Good luck!
    explored = 0
    minCost = float("inf")
    path = []
    for i in range(3): # try the three combinations of which one is in the middle
        start = goals[i - 1]
        middle = goals[i]
        goal = goals[i - 2] # python will make this work
        tup1 = a_star(start, middle, graph, heuristic) # the tuple with path and g
        tup2 = a_star(middle, goal, graph, heuristic)
        node_path1 = tup1[0]
        node_path2 = tup2[0]
        g1 = tup1[1]
        g2 = tup2[1]
        cost = g1[node_path1[-1]] + g2[node_path2[-1]]
        if cost < minCost: # minimizing the cost
            minCost = cost
            path = node_path1 + node_path2[1:][::-1] # combine pths
            explored = len(g1) + len(g2)
        reset_graph(graph)
    show_node_path(path, graph)
    print('cost: ' + str(minCost))
    print('node path: ' + str(path))
    print('number of explored: ' + str(explored))
    print('Tridirectional Search Path: ' + str(city_path(path, graph)))

def reset_graph(graph):
    edges = list(graph['edges'].keys())
    for edge in edges:
        make_line(edge[0], edge[1], graph, "black")
    root.update()

def main():
    '''depends on your data setup, you can change this part'''
    graph = make_graph("rrNodes.txt", "rrNodeCity.txt", "rrEdges.txt")

    start = graph['cityToNode']['Los Angeles']#input("Start city: ")] Los Angeles
    goal = graph['cityToNode']['Chicago']#input("Goal city: ")] Chicago
    ##print(graph['nodes'][goal])
    # print(graph['edges'][('1701265', '1701291')])
    #print(calc_edge_cost(start, goal, graph))

    print("\nBFS Summary")
    cur_time = time.time()
    bfs_path = breadth_first_search(start, goal, graph)
    next_time = time.time()
    print("BFS path: ", bfs_path)
    print("BFS Duration: ", (next_time - cur_time))

    reset_graph(graph)

    print("\nA* Search Summary")
    cur_time = time.time()
    result = a_star(start, goal, graph)
    a_star_path = A_star_path(result[0], result[1], graph) # workaround, since we need A* differently for tri
    next_time = time.time()
    print("A* path: ", a_star_path)
    print("A* Duration: ", (next_time - cur_time))

    reset_graph(graph)

    print("\nBi-directional BFS Summary")
    cur_time = time.time()
    bi_path = bidirectional_BFS(start, goal, graph)
    next_time = time.time()
    print("Bi-directional BFS path: ", bi_path)
    print("Bi-directional BFS Duration: ", (next_time - cur_time))
    
    reset_graph(graph)

    print("\nBi-directional A* Summary")
    cur_time = time.time()
    bi_a_path = bidirectional_a_star(start, goal, graph)
    next_time = time.time()
    print("Bi-directional A* path: ", bi_a_path)
    print("Bi-directional A* Duration: ", (next_time - cur_time))

    reset_graph(graph)

    # TODO: check your tridirectional search algorithm here
    goals = []
    goals.append(graph['cityToNode'][input('Goal1: ')])
    goals.append(graph['cityToNode'][input('Goal2: ')])
    goals.append(graph['cityToNode'][input('Goal3: ')])
    print("\nTri-directional Search Summary")
    cur_time = time.time()
    tridirectional_search(goals, graph)
    next_time = time.time()
    # print("Bi-directional A* path: ", bi_a_path)
    print("Tri-directional A* Duration: ", (next_time - cur_time))#'''
    root.mainloop()
if __name__ == '__main__':
    main()
'''
Sample Run
Start city: Los Angeles
Goal city: Chicago

BFS Summary
cost:  2093.868463307088
node path:  ['0600316', '0600089', '0600426', '0600087', '0600531', '0600760', '0600411', '0600027', '0600590', '0600023', '0600899', '0600900', '0600901', '0600902', '0600035', '0600321', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000505', '2000291', '2000289', '2000290', '2000288', '2000292', '2000298', '2000087', '2000093', '2000094', '2000095', '2000096', '2000135', '2000280', '2000133', '2000342', '2000439', '2000358', '2000134', '2000121', '2000442', '2000441', '2000124', '2000125', '2000271', '2000127', '2000272', '2000237', '2000273', '2000353', '2000220', '0000541', '2900116', '2900283', '2900235', '2900198', '2900286', '2900241', '2900103', '2900482', '2900102', '2900545', '2900556', '2900111', '2900120', '2900122', '2900494', '2900355', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701322', '1700287', '1700296', '1701472', '1700303', '1700328', '1700926', '1700582', '1700310', '1700311', '1700312', '1700583', '1700313', '1701182', '1701345', '1700327', '1700432', '1701622', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  13268
BFS path:  ['Los Angeles', 'Chicago']
BFS Duration:  0.03057575225830078

A* Search Summary
cost:  2002.0784404122933
node path:  ['0600316', '0600427', '0600322', '0600751', '0600084', '0600685', '0600085', '0600080', '0600079', '0600686', '0600766', '0600402', '0600799', '0600408', '0600460', '0600588', '0600384', '0600688', '0600463', '0600435', '0600107', '0600775', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000506', '2000294', '2000295', '2000296', '2000514', '2000523', '2000077', '2000292', '2000504', '2000293', '2000092', '2000311', '2000472', '2000470', '2000094', '2000095', '2000404', '2000097', '2000277', '2000102', '2000414', '2000103', '2000104', '2000106', '2000356', '2000114', '2000372', '2000117', '2000465', '2000466', '2000467', '2000270', '2000258', '2000257', '2000256', '2000260', '0000232', '2900371', '2900374', '2900378', '2900238', '2900184', '2900358', '2900343', '2900206', '2900095', '2900598', '2900476', '2900101', '2900212', '2900100', '2900106', '2900281', '2900210', '2900290', '2900291', '2900292', '2900207', '2900558', '2900416', '2900493', '2900253', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701325', '1701326', '1701323', '1700750', '1701328', '1701327', '1700292', '1700281', '1700280', '1701120', '1700301', '1700922', '1701121', '1700487', '1700480', '1700479', '1700478', '1700477', '1700430', '1700431', '1701157', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  1272
A* path:  ['Los Angeles', 'Chicago']
A* Duration:  0.036072492599487305

Bi-directional BFS Summary
cost:  2093.868463307088
node path:  ['0600316', '0600089', '0600426', '0600087', '0600531', '0600760', '0600411', '0600027', '0600590', '0600023', '0600899', '0600900', '0600901', '0600902', '0600035', '0600321', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000505', '2000291', '2000289', '2000290', '2000288', '2000292', '2000298', '2000087', '2000093', '2000094', '2000095', '2000096', '2000135', '2000280', '2000133', '2000342', '2000439', '2000358', '2000134', '2000121', '2000442', '2000441', '2000124', '2000125', '2000271', '2000127', '2000272', '2000237', '2000273', '2000353', '2000220', '0000541', '2900116', '2900283', '2900235', '2900198', '2900286', '2900241', '2900103', '2900482', '2900102', '2900545', '2900556', '2900111', '2900120', '2900122', '2900494', '2900355', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701322', '1700287', '1700296', '1701472', '1700303', '1700328', '1700926', '1700582', '1700310', '1700311', '1700312', '1700583', '1700313', '1701182', '1701345', '1700327', '1700432', '1701622', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  ### Not Shown ###
Bi-directional BFS path:  ['Los Angeles', 'Chicago']
Bi-directional BFS Duration:  0.0

Bi-directional A* Summary
cost:  2002.0784404122933
node path:  ['0600316', '0600427', '0600322', '0600751', '0600084', '0600685', '0600085', '0600080', '0600079', '0600686', '0600766', '0600402', '0600799', '0600408', '0600460', '0600588', '0600384', '0600688', '0600463', '0600435', '0600107', '0600775', '0600769', '0600436', '0600032', '0600414', '0600867', '0600866', '0600031', '0600033', '0600795', '0600602', '0600603', '0600036', '0600604', '0600871', '0600870', '0600872', '0600495', '0000144', '0400113', '0400114', '0400009', '0400010', '0400116', '0400117', '0400148', '0400074', '0400146', '0400147', '0400064', '0400005', '0400006', '0400063', '0400100', '0400075', '0400071', '0400070', '0400002', '0400050', '0000312', '3500036', '3500062', '3500063', '3500068', '3500069', '3500101', '3500111', '3500061', '3500109', '3500084', '3500089', '3500102', '3500065', '3500066', '3500032', '3500027', '3500119', '3500071', '3500070', '3500090', '3500107', '3500072', '3500013', '3500047', '3500039', '3500141', '3500025', '3500099', '0000257', '4801203', '4800003', '4801200', '4800002', '0000248', '4000264', '4000138', '4000231', '0000246', '2000206', '2000503', '2000360', '2000427', '2000500', '2000452', '2000207', '2000419', '2000501', '2000502', '2000073', '2000074', '2000075', '2000473', '2000519', '2000506', '2000294', '2000295', '2000296', '2000514', '2000523', '2000077', '2000292', '2000504', '2000293', '2000092', '2000311', '2000472', '2000470', '2000094', '2000095', '2000404', '2000097', '2000277', '2000102', '2000414', '2000103', '2000104', '2000106', '2000356', '2000114', '2000372', '2000117', '2000465', '2000466', '2000467', '2000270', '2000258', '2000257', '2000256', '2000260', '0000232', '2900371', '2900374', '2900378', '2900238', '2900184', '2900358', '2900343', '2900206', '2900095', '2900598', '2900476', '2900101', '2900212', '2900100', '2900106', '2900281', '2900210', '2900290', '2900291', '2900292', '2900207', '2900558', '2900416', '2900493', '2900253', '2900121', '2900162', '2900165', '2900566', '2900468', '2900164', '0000395', '1900057', '1900382', '1900070', '0000393', '1701225', '1700286', '1701010', '1701170', '1700285', '1701321', '1701325', '1701326', '1701323', '1700750', '1701328', '1701327', '1700292', '1700281', '1700280', '1701120', '1700301', '1700922', '1701121', '1700487', '1700480', '1700479', '1700478', '1700477', '1700430', '1700431', '1701157', '1700449', '1700419', '1700465', '1700418', '1701034', '1701194', '1700417', '1700629', '1701394', '1700653', '1700631', '1700415', '1701267', '1701265', '1701291']
number of explored:  ### Not Shown ###
Bi-directional A* path:  ['Los Angeles', 'Tucson', 'Fort Worth', 'Chicago']
Bi-directional A* Duration:  0.0
'''
