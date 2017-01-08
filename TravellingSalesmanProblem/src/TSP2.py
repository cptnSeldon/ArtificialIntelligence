"""
    EVOLUTIONARY PARADIGM :

    1. initialization
    2. evaluation           [1]-- -->[2]-- -->[5]
    3. selection               ^        ˇ
    4. variation                [4]<-----[3]
    5. termination

"""
from math import sqrt
from random import shuffle


"""
    PREPARATION
"""


class City:
    """
        01. GENE : City
    """
    def __init__(self, name, x, y):
        self.name = name
        self.x = int(x)
        self.y = int(y)

    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.name == other.name \
               and self.x == other.x and \
               self.y == other.y

    def __hash__(self):
        return hash(self.name) ^ hash(self.x) ^ hash(self.y)

    def __str__(self):
        return str(self.name)


class Cities:
    """
        0.2.  CHROMOSOME : Cities
    """
    def __init__(self):
        self.cities = dict()
        self.score = 0

    def city_dictionary_population(self, file):
        """
        Populate dictionary containing each gene.
        :param file: name, x, y
        :return:
        """
        try:
            city_list = []
            with open(file, 'r') as openfile:

                # populate list
                for line in openfile:
                    name, x, y = line.split(" ")
                    city_list.append(City(name, x, y))

                # populate dictionary
                for city in city_list:
                    self.cities[city.get_name()] = city  # key : name, value : city
            # print(*self.cities)
        except IOError:
            print("Error : file not found")

    def path_generation(self):
        """
        Generate a single chromosome.
        :return: path
        """
        cities = list(self.cities.values())  # generate a list containing only Cities' name
        path = [cities[0].name]  # add first city to head of list
        sublist = cities[1:len(cities)]  # sublist that doesn't contains the first city
        shuffle(sublist)  # shuffle sublist
        for city in sublist:  # iter through shuffled sublist
            path.append(city.name)  # add it to chromosome
        path.append(cities[0].name)  # add first city to queue of list
        # print(path)
        return path

    def paths_list_generation(self, sample_size):
        """
        Generate chromosome population.
        :param sample_size: population size
        :return: paths_list
        """
        paths_list = []
        # for each iteration generate a new chromosome
        for i in range(0, sample_size):
            paths_list.append(self.path_generation())
        return paths_list

    def fitness(self, path_list):
        """
        Calculate a chromosome's path's weight (score)
        :param path_list: chromosome
        :return:
        """
        # calculate effective score
        score = 0
        for c in range(0, len(path_list) - 1):
            city = self.cities.get(path_list[c])  # compare name in dict with city's name
            city2 = self.cities.get(path_list[c + 1])  # again
            score += weight(city, city2)  # score calculation
        self.score = score
        # print(self.score)
        return self.score

    def selection(self):
        pass


def weight(city_a, city_b):
    """
    Calculate path's weight between two cities
    :param city_a:
    :param city_b:
    :return:
    """
    x = pow(abs(city_a.get_x() - city_b.get_x()), 2)
    y = pow(abs(city_a.get_y() - city_b.get_y()), 2)
    return sqrt(x + y)


if __name__ == "__main__":

    init = Cities()
    init.city_dictionary_population("data.txt")
    chromosomes = init.paths_list_generation(5)

    total_weight = 0

    for chromosome in chromosomes:
        print(chromosome)
        total_weight += init.fitness(chromosome)
    print(total_weight)

