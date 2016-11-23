"""
    GRAPH ->
    dict : key, value
"""
from vertex import *


class Graph:
    # constructor
    def __init__(self):
        self.cities = {}
        self.connection_number = 0

    # add CITY to GRAPH
    def add_vertex(self, city):
        self.connection_number += 1
        self.cities[city.get_name()] = City(city.get_name(), city.get_coordinate_x(), city.get_coordinate_y())
        return self.cities[city.get_name()]

    # check if VERTEX exists in CITIES
    def get_vertex(self, city):
        if city.get_name() in self.cities.keys():
            return self.cities[city.get_name()]
        else:
            return None

    # add NEW CONNECTION
    def add_edge(self, city_a, city_b, distance=0):
        self.cities[city_a.get_name()].add_neighbour(city_b, distance)
        # city_a.add_neighbour(city_b, distance)

    # get VERTICES
    def get_vertices(self):
        return self.cities.keys()

    # get ADJACENCY LIST
    def get_adjacency_list(self, city):
        return self.cities[city.get_name()].get_neighbours()

    # get DISTANCE
    def get_distance(self, me, neighbour):
        return (self.cities[me.get_name()]).get_distance(neighbour)

    # CONTAINS redefinition
    def __contains__(self, city):
        return city in self.cities

    # ITER redefinition
    def __iter__(self):
        return iter(self.cities.values())


"""
    MAIN : code testing
"""
if __name__ == "__main__":
    graph = Graph()
    city1 = City("London", 1, 2)
    city2 = City("Paris", 2, 3)
    city3 = City("Bern", 5, 6)
    city4 = City("Lugano", 2, 2)

    graph.add_vertex(city1)
    graph.add_vertex(city2)
    graph.add_vertex(city3)
    graph.add_vertex(city4)

    # print(graph.get_vertices())

    graph.add_edge(city1, city2, 100)
    graph.add_edge(city2, city1, 10)
    graph.add_edge(city3, city1, 200)
    graph.add_edge(city1, city3, 15)

    # print(cities_to_choose_from.get_neighbours())
    # print(city2.get_neighbours())

    # graph.get_vertex(city2)
    # print(graph.get_vertex(city2))
    # print(graph.get_vertex(city4))

    print(*graph.get_adjacency_list(city1))
    print(graph.get_distance(city1, city2))
