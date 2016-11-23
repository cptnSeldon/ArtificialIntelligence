"""
    VERTEX : City
"""


# VERTEX : City(name, x, y)
class City:
    # constructor
    def __init__(self, name, pos_x, pos_y):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.connected_to = {}

    # get NAME
    def get_name(self):
        return self.name

    # get COORDINATES : x, y
    def get_coordinate_x(self):
        return int(self.pos_x)

    def get_coordinate_y(self):
            return int(self.pos_y)

    # get DISTANCE
    def get_distance(self, neighbour):
        return int(self.connected_to[neighbour])

    # add NEIGHBOUR
    def add_neighbour(self, neighbour, distance):
        self.connected_to[neighbour] = distance

    # get CONNECTION
    def get_neighbours(self):
        return self.connected_to

    # STRING redefinition
    def __str__(self):
        return str(self.name)


"""
    MAIN : code testing
"""
if __name__ == "__main__":

    print("Vertex : test")

    city1 = City("London", 1, 2)
    city2 = City("Paris", 2, 3)
    city3 = City("Bern", 5, 2)

    print(city1.get_name())
    print(city1.get_coordinate_x())
    print(city1.get_coordinate_y())

    city1.add_neighbour(city2, 20)
    city1.add_neighbour(city3, 30)
    print(*city1.get_neighbours())
    print(city1.get_distance(city2))
