"""
    EVOLUTIONARY PARADIGM :

    1. initialization
    2. evaluation           [1]-- -->[2]-- -->[5]
    3. selection               ^        ˇ
    4. variation                [4]<-----[3]
    5. termination

"""
from math import sqrt
import random

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

    def __init__(self, c_list):
        self.score = 0
        self.cities_list = c_list

    def fitness(self):
        """
        Calculate a chromosome's path's weight (score)
        :return:
        """
        # calculate effective score
        score = 0
        for c in range(0, len(self.cities_list) - 1):
            city = cities.get(self.cities_list[c])  # compare name in dict with city's name
            city2 = cities.get(self.cities_list[c + 1])  # again
            score += weight(city, city2)  # score calculation
        self.score = score
        # print(self.score)
        return self.score

    def __str__(self):
        return str(self.cities_list) + " : " + str(self.fitness()) + "\n"

    def __getitem__(self, index):
        return self.cities_list[index]

    def __setitem__(self, index, value):
        self.cities_list[index] = value


cities = dict()


def city_dictionary_population(file):
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
                cities[city.get_name()] = city  # key : name, value : city
                # print(*self.cities)
    except IOError:
        print("Error : file not found")


def path_generation():
    """
    Generate a single chromosome.
    :return: path
    """
    cities_ = list(cities.values())  # generate a list containing only Cities' name
    path = [cities_[0].name]  # add first city to head of list
    sublist = cities_[1:len(cities_)]  # sublist that doesn't contains the first city
    random.shuffle(sublist)  # shuffle sublist
    for city in sublist:  # iter through shuffled sublist
        path.append(city.name)  # add it to chromosome
    path.append(cities_[0].name)  # add first city to queue of list
    # print(path)
    return Cities(path)


def paths_list_generation(sample_size):
    """
    Generate chromosome population.
    :param sample_size: population size
    :return: paths_list
    """
    paths_list = []
    # for each iteration generate a new chromosome
    for i in range(0, sample_size):
        paths_list.append(path_generation())
    return paths_list


def weight(city_a, city_b):
    """
    Calculate path's weight between two cities
    :param city_a:
    :param city_b:
    :return:
    """
    x = abs(city_a.get_x() - city_b.get_x()) ** 2
    y = abs(city_a.get_y() - city_b.get_y()) ** 2

    # print("x: %r y: %r" % (x, y))
    return sqrt(x + y)


def selection(population):
    """
    Select a chromosome from population using stochastic roulette method
    :param population: chromosome population
    :return:
    """
    # calculate total weight
    total_weight = 0

    for chromo in chromosomes:
        total_weight += chromo.fitness()

    print("Total weight : %f" % total_weight)

    # sort by score (descending order)
    population = sorted(population, key=lambda c: c.score)
    # population.reverse()

    # random number generation
    random_value = random.uniform(0.0, 1.0) * total_weight
    # print(random_value)
    # print(*population)

    # locate the closest value in fitness list
    for chromo in population:
        random_value -= chromo.fitness()
        if random_value <= 0:
            return chromo
    return chromo


def crossover(population):
    for ind in range(0, len(population) - 1, 2):
        ind1 = population[ind].cities_list
        ind2 = population[ind + 1].cities_list
        size = len(ind1) - 1  # ne prend pas la dernière ville
        a, b = random.sample(range(1, size), 2)  # ne prend pas la première ville
        temp1, temp2 = list(ind1), list(ind2)  # sauvegarde la liste des villes
        if a > b:
            a, b = b, a
        # remplacement des villes à échanger par un drapeau
        for i in range(a, b+1):
            for c in range(1, size):
                if ind1[c] == temp2[i]:
                    ind1[c] = False
                if ind2[c] == temp1[i]:
                    ind2[c] = False
        # tassement des villes dans l'ordre à partir du deuxième point de croisement
        for i in range(size - (b - a + 1)):
            if ind1[(b + 1 + i) % size] == False:  # on cherche un trou
                j = (b + 2 + i) % size
                while ind1[j % size] == False or j == 0:  # on cherche la prochaine ville à droite et on ne prend pas en compte la ville de départ
                    j += 1
                    if j%size == 0: # on ne prend pas en compte la ville de départ
                        j += 1
                ind1[(b + 1 + i) % size] = ind1[j % size]  # remplacement du trou par la ville trouvée
                ind1[j % size] = False  # la ville déplacée devient un trou

            if ind2[(b + 1 + i) % size] == False:  # on cherche un trou
                j = (b + 2 + i) % size
                while ind2[j % size] == False or j == 0:  # on cherche la prochaine ville à droite et on ne prend pas en compte la ville de départ
                    j += 1
                ind2[(b + 1 + i) % size] = ind2[j % size]  # remplacement du trou par la ville trouvée
                ind2[j % size] = False  # la ville déplacée devient un trou
        # on rempli les trous en faisant le crossover
        for i in range(a, b + 1):
            ind1[i], ind2[i] = temp2[i], temp1[i]
        population[ind].cities_list = ind1
        population[ind + 1].cities_list = ind2
    return population


def mutation(chromosome):
    chrom_size = len(cities)
    a = random.randrange(1, chrom_size - 1)
    b = random.randrange(1, chrom_size - 1)
    print("a: %r b: %r" % (a, b))
    print("before change : %s" % chromosome)
    if a != b:
        chromosome[a], chromosome[b] = chromosome[b], chromosome[a]
        chromosome.fitness()
        print("after change : %s" % chromosome)
    a = random.randrange(1, chrom_size - 1)
    b = random.randrange(1, chrom_size - 1)
    print("a: %r b: %r" % (a, b))
    print("before change : %s" % chromosome)
    if a != b:
        chromosome[a], chromosome[b] = chromosome[b], chromosome[a]
        chromosome.fitness()
        print("after change : %s" % chromosome)


if __name__ == "__main__":

    city_dictionary_population("data.txt")
    chromosomes = paths_list_generation(5)  # list of City()s
    # 1. selection by roulette
    selected_chromosome = selection(chromosomes)
    # print(selection(chromosomes))
    # 2. crossover
    for chromosome in chromosomes:
        print(chromosome, end="")
    print("crossover")
    chromosomes = crossover(chromosomes)
    for chromosome in chromosomes:
        print(chromosome, end="")
    # 3. mutation
    mutation(selected_chromosome)
    # 4. termination
