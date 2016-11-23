"""
    PARSER : population process
"""
from vertex import City

cities = []
connections = {}


# PARSE : cities_to_choose_from(x,y)
def get_coordinates(file):

    try:
        # OPEN FILE : readonly
        with open(file, 'r') as openfile:
            for line in openfile:

                # DATA RETRIEVAL
                name, x, y = line.split(" ")

                # LIST POPULATION : Node(params)
                cities.append(City(name, int(x), int(y)))

    except IOError:
        print("Error : file (coordinates) could not open")


# PARSE : cities_to_choose_from A(cities_to_choose_from B(distance), cities_to_choose_from C (distance), ..)
def get_connections(file):

    try:
        # OPEN FILE : readonly
        with open(file, 'r') as openfile:
            for line in openfile:

                # DATA RETRIEVAL
                city_a, city_b, distance = line.split(" ")

                # LIST POPULATION : Node(params)
                me = None
                other = None

                # CITY SORTING
                for city in cities:
                    if city.name == me:
                        city_a = city
                    elif city.name == other:
                        city_b = city

                # CONNECT FOR BOTH SIDES
                """ try:
                    connected_to[city_a][city_b] = [int(distance)]
                except:
                    connected_to[city_a] = {city_b: int(distance)}
                try:
                    connected_to[city_b][city_a] = [int(distance)]
                except:
                    connected_to[city_b] = {city_a: int(distance)} """

    except IOError:
        print("Error : file (connected_to) could not open")

# START
if __name__ == "__main__":
    pass
