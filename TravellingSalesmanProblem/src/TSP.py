"""
    EVOLUTIONARY PARADIGM :

    1. initialization
    2. evaluation           [1]-- -->[2]-- -->[5]
    3. selection               ^        ˇ
    4. variation                [4]<-----[3]
    5. termination

    => ga_solve(file=None, gui=True, maxtime=0)

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
        self.cities = []
        self.score = 0

    def get_coordinates(self, file):
        """
        Get cities' coordinates from file
        :param file:
        :return:
        """
        try:
            with open(file, 'r') as openfile:
                print("Coordinates taken from file")
                for line in openfile:
                    name, x, y = line.split(" ")
                    self.cities.append(City(name, x, y))
            # debug
            # print(*self.cities)
        except IOError:
            print("Error : file not found")

    def generate_path(self):
        """
        Generate a single path using cities list
        :return: chromosome
        """
        chromosome = [self.cities[0].name]  # add first city to head of list
        sublist = self.cities[1:len(self.cities)]  # sublist that doesn't contains the first city
        shuffle(sublist)  # shuffle sublist
        for city in sublist:  # iter through shuffled sublist
            chromosome.append(city.name)  # add it to chromosome
        chromosome.append(self.cities[0].name)  # add first city to queue of list
        print(chromosome)
        return chromosome

    """def generate_chromosome_set(self, sample_number, chromosome):
        print("Generating chromosomes")
        chromosomes = set()

        for i in range(0, sample_number):
            if chromosome not in chromosomes:
                chromosomes.add(chromosome)

        # debug
        # print(*chromosomes)
        return chromosomes"""

    def selection(self):
        pass

    def variation(self):
        pass

    def mutation(self):
        pass

    def crossover(self):
        pass

    def fitness(self, chromosome):
        """
        Evaluate chromosome's fitness
        :param chromosome:
        :return:
        """
        print("Evaluate chromosome")
        chr_dict = {}

        # cities dictionary : needed for weight check found below
        for city in self.cities:
            chr_dict[city.get_name()] = city    # key : name, value : city

        # calculate effective score
        for c in range(0, len(chromosome) - 1):
            city = chr_dict.get(chromosome[c])  # compare name in dict with city's name
            city2 = chr_dict.get(chromosome[c + 1])  # again
            self.score += weight(city, city2)   # score calculation
        print(self.score)


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
    init.get_coordinates("data.txt")
    chroma = init.generate_path()
    init.fitness(chroma)

"""
    START
"""


# 1. initialization [graph population]


"""
    PROCESSING
"""

# 2. evaluation [fitness]

# 3. selection [tournament, roulette, deterministic, greedy]

# 4. variation [crossover + mutation] [city exchange, reverse path, replace path]

"""
    END
"""

# 5. termination [neuronal network, ant colony, greedy algorithm]

