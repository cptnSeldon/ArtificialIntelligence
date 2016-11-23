"""
    PATH FINDING : A*
        -> G cost : distance from START node
        -> H cost : distance from END node
        -> F cost : G cost + H cost

        FRONTIER    : set to be evaluated
        HISTORY     : set of nodes already evaluated
"""
from populateGraph import *
from customQueue import *
from customPriorityQueue import *
from math import sqrt

"""
    HEURISTICS
"""


# H 0 : nul
def h0(city_a, city_b):
    return 0


# H 1 : x coordinates comparison
def h1(city_a, city_b):
    x1 = city_a.get_coordinate_x()
    x2 = city_b.get_coordinate_x()
    return abs(x1 - x2)


# H 2 : y coordinates comparison
def h2(city_a, city_b):
    y1 = city_a.get_coordinate_y()
    y2 = city_b.get_coordinate_y()
    return abs(y1 - y2)


# H 3 : diagonal comparison
def h3(city_a, city_b):
    return sqrt(pow(h1(city_a, city_b), 2) +
                    pow(h2(city_a, city_b), 2))


# H 4 : X + Y
def h4(city_a, city_b):
    return h1(city_a, city_b) + h2(city_a, city_b)

"""
    PATH FINDING : BREADTH FIRST SEARCH (test)
    link : http://www.redblobgames.com/pathfinding/a-star/implementation.html#org1d80056
"""


def breadth_first_search(populated_graph, start_node):
    # frontier
    frontier = Queue()
    frontier.put(start_node)
    # history
    history = dict()
    history[start_node] = True

    # until frontier is empty
    while not frontier.empty():
        current = frontier.get()
        print("Visiting %r" % current.get_name())
        # get neighbours' from adjacency list
        for next in populated_graph.graph.get_adjacency_list(current):
            if next not in history:
                frontier.put(next)
                history[next] = True


"""
    PATH FINDING : DIJKSTRA (test)
    link : http://www.redblobgames.com/pathfinding/a-star/implementation.html#org1d80056
"""


def dijkstra(populated_graph, start_node, end_node):
    # frontier
    frontier = PriorityQueue()
    frontier.put(start_node, 0)
    # history
    history = dict()
    history[start_node] = None
    # distance from start node
    g_cost = dict()
    g_cost[start_node] = 0

    # until frontier is empty
    while not frontier.empty():
        current = frontier.get()

        # what is done when goal reached
        if current == end_node:
            break

        # get neighbours' from adjacency list
        for neighbour in populated_graph.graph.get_adjacency_list(current):
            f_cost = g_cost[current] + neighbour.get_distance(current)
            # put right node in history
            if neighbour not in g_cost or f_cost < g_cost[neighbour]:
                g_cost[neighbour] = f_cost
                priority = f_cost
                frontier.put(neighbour, priority)
                history[neighbour] = current

    return history, g_cost

"""
    PATH FINDING : A*
"""


def astar(populated_graph, start_node, end_node, heuristic):
    # frontier
    frontier = PriorityQueue()
    frontier.put(start_node, 0)
    # history
    history = dict()
    history[start_node] = None
    # distance from start_node node
    g_cost = dict()
    g_cost[start_node] = 0

    # until frontier is empty
    while not frontier.empty():
        current = frontier.get()

        # what is done when end_node reached
        if current == end_node:
            break

        # get neighbours' from adjacency list
        for neighbour in populated_graph.graph.get_adjacency_list(current):
            a = neighbour.get_distance(current)
            b = g_cost[current]
            g_cost_ = b + a
            # put right node in history
            if neighbour not in g_cost or g_cost_ < g_cost[neighbour]:
                g_cost[neighbour] = g_cost_
                f_cost = g_cost_ + heuristic(end_node, neighbour)
                frontier.put(neighbour, f_cost)
                history[neighbour] = current

    return history, g_cost


"""
    RECONSTRUCT PATH
    link : http://www.redblobgames.com/pathfinding/a-star/implementation.html#org1d80056
"""


def final_path(history, start_node, end_node):
    current = end_node
    path = [current]
    while current != start_node:
        current = history[current]
        path.append(current)
    path.reverse()
    return path

"""
    MAIN program
"""

if __name__ == "__main__":
    print("*---------------------------------*")
    print("|     PATH FINDING ALGORITHMS     |")
    print("*---------------------------------*")
    # GRAPH POPULATION
    init = PopulatedGraph()
    init.get_coordinates("positions.txt")
    init.get_connections("connections.txt")
    # VARIABLES DECLARATION
    city1 = None
    city2 = None
    heuristic = -1
    h = None
    # CITIES LIST
    cities_to_choose_from = init.graph.get_vertices()
    print(*cities_to_choose_from)

    # CHOOSE CITY 1 + CITY 2
    while True:
        if city1 not in init.graph.cities:
            city1 = input("Choose city 1\n> ")
        else:
            break
    while True:
        if city2 not in init.graph.cities:
            city2 = input("Choose city 2\n> ")
        else:
            break

    # GET VERTICES
    city_a = init.graph.get_vertex(init.graph.cities[city1])
    city_b = init.graph.get_vertex(init.graph.cities[city2])

    # CHOOSE HEURISTIC
    while True:
        heuristic = input("Choose heuristic [0-4]\n> ")
        if int(heuristic) in range(0, 5):
            break

    h = (h0, h1, h2, h3, h4)[int(heuristic)]

    d_history, d_path = dijkstra(init, city_a, city_b)
    a_history, a_path = astar(init, city_a, city_b, h)

    path_d = final_path(d_history, city_a, city_b)
    path_a = final_path(a_history, city_a, city_b)

    # breadth_first_search(init, v)

    print("\n--------")
    print("DIJKSTRA")
    print("--------")
    print("History : " + str(len(d_history)))
    print(*d_history)
    print("Best path : " + str(len(path_d)))
    print(*path_d)

    print("\n---")
    print("A *")
    print("---")
    print("History : " + str(len(a_history)))
    print(*a_history)
    print("Best path : " + str(len(path_a)))
    print(*path_a)
