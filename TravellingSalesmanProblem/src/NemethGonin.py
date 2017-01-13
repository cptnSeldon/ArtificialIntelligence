# -*- coding: utf-8 -*-
__author__ = 'Julia Nemeth et Nicolas Gonin'

import itertools
import time
import random
from math import sqrt
from copy import deepcopy

# valeurs constantes utiles pour le profilage
MUTATION_RATE = 0.01
POPULATION_SIZE = 50

# Valeurs constantes utiles pour le fonctionnement du programme
STAGNATION_WAIT_GENERATION = 10


class City:
    """
        01. GENE : City
    """

    def __init__(self, name, x, y):
        self.name = name
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.name == other.name \
               and self.x == other.x and \
               self.y == other.y


class Chromosome:
    def __init__(self, c_list):
        self.cities_list = list(c_list)
        self.score = 0

    def calcFitness(self):
        """
        Calculate a chromosome's path's weight (score)
        :return:
        """
        # calculate effective score
        score = 0
        for i in range(0, len(self.cities_list) - 2):
            city = self.__getitem__(i)
            city2 = self.__getitem__(i + 1)
            score += self.weight(city, city2)  # score calculation
        city = self.__getitem__(len(self) - 1)
        city2 = self.__getitem__(0)
        score += self.weight(city, city2)  # score calculation
        self.score = score
        return score

    def __str__(self):
        return str(self.cities_list) + " : " + str(self.score)

    def __getitem__(self, index):
        return self.cities_list[index]

    def __setitem__(self, index, value):
        self.cities_list[index] = value

    def __len__(self):
        return len(self.cities_list)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(0, len(self)):
            if self.cities_list[i] != other.cities_list[i]:
                return False
        return isinstance(other, self.__class__)

    def weight(self, city_a, city_b):
        """
        Calculate path's weight between two cities
        :param city_a:
        :param city_b:
        :return:
        """
        x = abs(city_a.x - city_b.x) ** 2
        y = abs(city_a.y - city_b.y) ** 2
        return sqrt(x + y)


def ga_solve(file=None, gui=True, maxtime=0):
    if file == None:
        showGame()
    else:
        parseFile(file)
    population = []
    # Création d'une liste contenant différentes permutations des villes.
    listCities = list(itertools.islice(itertools.permutations(cities), POPULATION_SIZE))

    # on a une liste de villes qu'on veut transformer en liste de Chromosome. En même temps une évalutation est faite
    for chromosome in listCities:
        chromosome = Chromosome(chromosome)
        population.append(chromosome)

    # --------------EVALUATION PRELIMINAIRE-------------------------
    population.sort(key=lambda chromosome: chromosome.calcFitness())
    # variables d'arrêt
    timeStart = time.time()
    actualTime = -1
    stagnation = False
    lastScore = population[0].score
    generationWithoutProgress = 0
    nbGeneration = 0
    while actualTime < maxtime and stagnation == False:

        # ---------------DESSIN----------------
        if gui:
            drawPath(population[0].cities_list)
        print("Generation:", nbGeneration, "score=", int(population[0].score))
        # A partir de maintenant on va appliquer le processus de séléction génétique.

        # ---------------SElECTION--------------------------
        # TODO la séléction par roulette est très peu efficace
        # population=selection(population)  # retient la moitiée des chromosomes
        # elitisme
        matingPoolSize = int(len(population) / 2)
        population = deepcopy(population[0:matingPoolSize])
        # ------------------REPRODUCTION-------------------
        for i in range(0, int(len(population)), 2):
            # choix de deux individus qui vont produire deux enfants
            a, b = random.sample(range(0, len(population)), 2)
            newChromosome1 = deepcopy(population[a])
            newChromosome2 = deepcopy(population[b])

            crossover(newChromosome1, newChromosome2)
            # Mutation du chromosome en permuttant deux gènes (villes)
            mutation(newChromosome1, MUTATION_RATE)
            mutation(newChromosome2, MUTATION_RATE)
            # Ajout des nouveaux chromosomes dans la nouvelle génération
            population.append(newChromosome1)
            population.append(newChromosome2)
        # --------------EVALUATION-------------------------
        population.sort(key=lambda chromosome: chromosome.calcFitness())
        # Conditions d'arrêt
        if maxtime > 0:
            actualTime = time.time() - timeStart
        else:
            if lastScore == population[0].score:
                generationWithoutProgress += 1
            else:
                generationWithoutProgress = 0
                lastScore = population[0].score
            if generationWithoutProgress == STAGNATION_WAIT_GENERATION:
                stagnation = True
        nbGeneration += 1
    pauseGui()
    return population[0].score, population[0].cities_list


def selection(population):
    """
    Select a chromosome from population using stochastic roulette method
    :param population: chromosome population
    :return:
    """
    total_weight = 0
    newPopulation = []
    for chromosome in population:
        total_weight += int(chromosome.score)
    for i in range(int(len(population) / 2)):
        target = random.randint(0, int(total_weight))
        # locate the closest value in score list
        for chromosome in population:
            target -= chromosome.score
            if target <= 0:
                newPopulation.append(deepcopy(chromosome))
                break
    return deepcopy(newPopulation)


def crossover(chromosome1, chromosome2):
    size = len(chromosome1)
    a, b = random.sample(range(0, size), 2)
    temp1, temp2 = list(chromosome1), list(chromosome2)  # sauvegarde la liste des villes
    if a > b:
        a, b = b, a
    # remplacement des villes à échanger par un drapeau
    for i in range(a, b + 1):
        for c in range(0, size):
            if chromosome1[c] == temp2[i]:
                chromosome1[c] = False
            if chromosome2[c] == temp1[i]:
                chromosome2[c] = False

    # tassement des villes dans l'ordre à partir du deuxième point de croisement
    for i in range(size - (b - a + 1)):

        if chromosome1[(b + 1 + i) % size] == False:  # on cherche un trou
            j = (b + 2 + i)
            while chromosome1[j % size] == False:  # on cherche la prochaine ville à droite
                j += 1
            chromosome1[(b + 1 + i) % size] = chromosome1[j % size]  # remplacement du trou par la ville trouvée
            chromosome1[j % size] = False  # la ville déplacée devient un trou

        if chromosome2[(b + 1 + i) % size] == False:  # on cherche un trou
            j = (b + 2 + i)
            while chromosome2[j % size] == False:  # on cherche la prochaine ville à droite
                j += 1
            chromosome2[(b + 1 + i) % size] = chromosome2[j % size]  # remplacement du trou par la ville trouvée
            chromosome2[j % size] = False  # la ville déplacée devient un trou
    # on rempli les trous en faisant le crossover
    for i in range(a, b + 1):
        chromosome1[i], chromosome2[i] = temp2[i], temp1[i]


def mutation(chromosome, probability):
    if (random.randint(0, 100) < probability * 100):
        a, b = random.sample(range(0, len(chromosome) - 1), 2)
        temp = list(chromosome)
        chromosome[b] = temp[a]
        chromosome[a] = temp[b]


# Fonctions utiles pour l'affichage graphique et le parsing------------------------------------------------------------
def parseFile(fname):
    with open(fname) as f:
        lines = f.readlines()
    for line in lines:
        word = line.split(" ")
        print(line)
        name = word[0]
        x = int(word[1])
        y = int(word[2])
        cities.append(City(name, x, y))


def showGame():
    draw(cities)

    running = True
    while running:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:  # Quit the game
            running = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Click
            print("Click at (%d, %d)" % event.pos)

            name = "v%i" % len(cities)
            x, y = event.pos
            cities.append(City(name, x, y))
            draw(cities)

        elif event.type == KEYDOWN and event.key == K_RETURN:  # Key Return press
            running = False

        pygame.display.flip()  # Repaint


def drawPath(listCities):
    draw(cities)

    # dessine tout les chemins
    listCityStart = listCities[0]
    for i in range(1, len(listCities)):
        listCityEnd = listCities[i]
        pygame.draw.line(screen, pathColor, (listCityStart.x, listCityStart.y),
                         (listCityEnd.x, listCityEnd.y))  # Show path
        listCityStart = listCityEnd

    # ferme la boucle
    listCityStart = listCities[len(listCities) - 1]
    listCityEnd = listCities[0]
    pygame.draw.line(screen, pathColor, (listCityStart.x, listCityStart.y), (listCityEnd.x, listCityEnd.y))  # Show path
    pygame.display.flip()  # refresh


def draw(cities):
    screen.fill(0)  # Erase all the screen

    i = 0
    for listCity in cities:
        pygame.draw.circle(screen, listCityColor, (listCity.x, listCity.y), listCityWidth)  # Show cities
        # Show labels of cities
        font = pygame.font.Font(None, 12)
        text = font.render("%s (%i;%i)" % (listCity.name, listCity.x, listCity.y), True, fontColor)
        screen.blit(text, (listCity.x + 2, listCity.y - 10))
        i += 1

    # Show the number of listCity
    font = pygame.font.Font(None, 30)
    text = font.render("Nombre : %i" % len(cities), True, fontColor)
    textRect = text.get_rect()
    screen.blit(text, textRect)

    pygame.display.flip()  # Repaint


def pauseGui():
    # Met la gui en pause. presser enter pour quitter
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == KEYDOWN and event.key == K_RETURN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
            running = False


def testCrossover():
    city1 = City("A", 0, 0)
    city2 = City("B", 0, 0)
    city3 = City("C", 0, 0)
    city4 = City("D", 0, 0)
    city5 = City("E", 0, 0)
    city6 = City("F", 0, 0)
    city7 = City("G", 0, 0)
    city8 = City("H", 0, 0)
    testChromosome1 = [city1, city2, city3, city4, city5, city6, city7, city8]
    testChromosome2 = [city2, city5, city6, city8, city1, city4, city7, city3]
    targetChromosome1 = [city4, city5, city6, city8, city1, city7, city2, city3]
    targetChromosome2 = [city8, city1, city3, city4, city5, city7, city2, city6]

    size = len(testChromosome1)
    a, b = (2, 4)
    temp1, temp2 = list(testChromosome1), list(testChromosome2)  # sauvegarde la liste des villes
    # remplacement des villes à échanger par un drapeau
    for i in range(a, b + 1):
        for c in range(0, size):
            if testChromosome1[c] == temp2[i]:
                testChromosome1[c] = False
            if testChromosome2[c] == temp1[i]:
                testChromosome2[c] = False

    # tassement des villes dans l'ordre à partir du deuxième point de croisement
    for i in range(size - (b - a + 1)):

        if testChromosome1[(b + 1 + i) % size] == False:  # on cherche un trou
            j = (b + 2 + i)
            while testChromosome1[j % size] == False:  # on cherche la prochaine ville à droite
                j += 1
            testChromosome1[(b + 1 + i) % size] = testChromosome1[j % size]  # remplacement du trou par la ville trouvée
            testChromosome1[j % size] = False  # la ville déplacée devient un trou

        if testChromosome2[(b + 1 + i) % size] == False:  # on cherche un trou
            j = (b + 2 + i)
            while testChromosome2[j % size] == False:  # on cherche la prochaine ville à droite
                j += 1
            testChromosome2[(b + 1 + i) % size] = testChromosome2[j % size]  # remplacement du trou par la ville trouvée
            testChromosome2[j % size] = False  # la ville déplacée devient un trou
    # on rempli les trous en faisant le crossover
    for i in range(a, b + 1):
        testChromosome1[i], testChromosome2[i] = temp2[i], temp1[i]

    assert (testChromosome1 == testChromosome1), "assert incorrecte!"
    assert (testChromosome1 == targetChromosome1), "crossover incorrecte!"
    assert (testChromosome2 == targetChromosome2), "crossover incorrecte!"


if __name__ == "__main__":
    import sys, pygame
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN

    pygame.init()
    screenSize = 500
    screen = pygame.display.set_mode((screenSize, screenSize))

    cities = []

    pathColor = 0, 0, 255  # Blue
    listCityColor = 255, 0, 0  # Red
    fontColor = 255, 255, 255  # White
    listCityWidth = 2  # Width of one point
    testCrossover()
    try:
        ga_solve(str(sys.argv[1]))
    except:
        ga_solve("data/pb050.txt", True, 0)
