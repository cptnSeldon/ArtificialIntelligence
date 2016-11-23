"""
    PATH FINDING : A*
        -> G cost : distance from START node
        -> H cost : distance from END node
        -> F cost : G cost + H cost

        FRONTIER    : set to be evaluated
        HISTORY     : set of nodes already evaluated
"""
from populateGraph import *
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
    PATH FINDING : A*
"""


def pathfinder(start_vertex, end_vertex):
    # frontier
    frontier = list()
    frontier.append(start_vertex)

    # dictionaries' declaration
    came_from = {}
    cost_so_far = {}

    # dictionaries' initialization
    came_from[start_vertex] = 0
    cost_so_far[start_vertex] = 0

    # loop
    while not len(frontier) == 0:
        # search node with lowest f_cost
        current_node = frontier.pop()

        # check if got to goal
        if current_node == end_vertex:
            break

        # iterate over neighbours' list
        for key in init.graph.get_adjacency_list((init.graph.cities[current_node.get_name()])):
            neighbour = init.graph.get_vertex(key)
            city = init.graph.get_vertex(start_vertex)
            a = cost_so_far[current_node]
            b = city.get_distance(neighbour)
            new_g_cost = a + b
            print(new_g_cost)

            if neighbour not in cost_so_far or new_g_cost < cost_so_far[neighbour]:
                cost_so_far[neighbour] = new_g_cost
                f_cost = new_g_cost + h3(end_vertex, neighbour)
                key.set_f_cost(f_cost)
                frontier.append(key)
                came_from[neighbour] = current_node

    return came_from, cost_so_far

if __name__ == "__main__":
    print("Path finding algorithm : A*")
    init = PopulatedGraph()
    init.get_coordinates("positions.txt")
    init.get_connections("connections.txt")

    v = init.graph.get_vertex(init.graph.cities["Vienna"])
    l = init.graph.get_vertex(init.graph.cities["Lisbon"])

    """ print(h0(v, l))
    print(h1(v, l))
    print(h2(v, l))
    print(h3(v, l))
    print(h4(v, l)) """

    history, path = pathfinder(v, l)

    """ print("HISTORY")
    print(came_from.items())
    print("PATH COST")
    print(path.items()) """


