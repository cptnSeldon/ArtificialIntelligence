"""
    PARSER : population process
"""
from vertex import City
from graph import Graph


class PopulatedGraph:
    # constructor
    def __init__(self):
        self.graph = Graph()

    # PARSE : cities_to_choose_from(x,y)
    def get_coordinates(self, file):
        try:
            # OPEN FILE : readonly
            with open(file, 'r') as openfile:
                for line in openfile:

                    # DATA RETRIEVAL
                    name, x, y = line.split(" ")
                    # GRAPH POPULATION : vertex -> params
                    self.graph.add_vertex(City(name, x, y))

        except IOError:
            print("Error : file (coordinates) could not open")

    # PARSE : cities_to_choose_from A(cities_to_choose_from B(distance), cities_to_choose_from C (distance), ..)
    def get_connections(self, file):
        try:
            # OPEN FILE : readonly
            with open(file, 'r') as openfile:
                for line in openfile:

                    # DATA RETRIEVAL
                    lines = line.split(" ")
                    if lines[0] in self.graph.cities and lines[1] in self.graph.cities:
                        # GRAPH POPULATION : edge -> vertex1, vertex2, distance
                        self.graph.add_edge(self.graph.cities[lines[0]], self.graph.cities[lines[1]], lines[2][:-1])
                        self.graph.add_edge(self.graph.cities[lines[1]], self.graph.cities[lines[0]], lines[2][:-1])

        except IOError:
            print("Error : file (connected_to) could not open")


"""
    MAIN : code testing
"""
if __name__ == "__main__":

    init = PopulatedGraph()
    init.get_coordinates("positions.txt")
    init.get_connections("connections.txt")

    # print(init.graph.get_vertex(init.graph.cities["Vienna"]))
    # print(init.graph.get_vertices())

    keys = init.graph.get_adjacency_list((init.graph.cities["Vienna"]))
    # print(keys)
    for key in keys:
        neighbour = init.graph.cities[key.get_name()]
        city = init.graph.cities["Vienna"]
        print(key.get_name() + " : " + str(city.get_distance(neighbour)))
