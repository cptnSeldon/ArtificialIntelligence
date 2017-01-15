# -*- coding: utf-8 -*-
from itertools import islice, permutations
from time import time
import random
from math import sqrt
from copy import deepcopy
import pygame
from sys import argv
from pygame.locals import KEYDOWN, K_RETURN

__author__ = 'Julia Nemeth et Nicolas Gonin'

# valeurs constantes utiles pour le profilage
MUTATION_RATE = 0.2

POPULATION_SIZE = 70

# Valeurs constantes utiles pour le fonctionnement du programme
STAGNATION_WAIT_GENERATION = 15


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

    # Util pour PVC-tester
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        return False

    # Util pour PVC-tester
    def __hash__(self):
        return hash(self.name)


class Chromosome:
    def __init__(self, c_list):
        self.cities_list = list(c_list)
        self.score = 0

    def calcFitness(self):
        score = 0
        for i in range(0, len(self.cities_list) - 1):
            city = self.__getitem__(i)
            city2 = self.__getitem__(i + 1)
            score += self.weight(city, city2)
        city = self.__getitem__(len(self) - 1)
        city2 = self.__getitem__(0)
        score += self.weight(city, city2)
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
        :return: path's weight
        """
        x = abs(city_a.x - city_b.x) ** 2
        y = abs(city_a.y - city_b.y) ** 2
        return sqrt(x + y)


def ga_solve(file=None, gui=True, maxtime=0):
    cities = []
    if file is None:
        showGame(cities)
    else:
        parseFile(file, cities)
    population = []
    # Création d'une liste contenant différentes permutations des villes.
    listCities = list(islice(permutations(cities), POPULATION_SIZE))

    # on a une liste de villes qu'on veut transformer en liste de Chromosome.
    for chromosome in listCities:
        chromosome = Chromosome(chromosome)
        population.append(chromosome)

    # Séléction gourmande: les résultats ne sont pas bons alors nous ne l'avons pas utilisée
    # insertFitChromosomes(population,cities,60)


    # variables d'arrêt
    timeStart = time()
    actualTime = 0
    stagnation = False
    lastScore = population[0].score
    generationWithoutProgress = 0
    nbGeneration = 0
    if maxtime <= 0:
        maxtime = float("inf")

    # --------------EVALUATION PRELIMINAIRE-------------------------
    population.sort(key=lambda chromosome: chromosome.calcFitness())

    while actualTime < maxtime and stagnation is False:
        # ---------------DESSIN----------------
        if gui:
            drawPath(population[0].cities_list, cities)

        # A partir de maintenant on va appliquer le processus de séléction génétique.

        # ---------------SElECTION--------------------------
        # la séléction par roulette + un peu d'élitisme est très peu efficace alors nous ne l'avons pas utiliée.
        # matingPool = deepcopy(population[0:5])
        # matingPool.extend(selection(population))  # retient la moitiée des chromosomes

        # elitisme pour 50% de la population
        matingPoolSize = int(len(population) / 2)
        population = deepcopy(population[:matingPoolSize])
        # ------------------REPRODUCTION-------------------
        # On garde la meilleure moitié de la population et on y ajoute des croisements et mutations à partir de
        # cette même moitié.
        for i in range(0, int(matingPoolSize), 2):
            # choix de deux individus qui vont produire deux enfants
            a, b = random.sample(range(0, matingPoolSize), 2)
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
        actualTime = time() - timeStart
        if lastScore == population[0].score:
            generationWithoutProgress += 1
        else:
            generationWithoutProgress = 0
            lastScore = population[0].score
        if generationWithoutProgress == STAGNATION_WAIT_GENERATION:
            stagnation = True
        nbGeneration += 1
        #DEBUG
        # print("time=",'%.3f'%(actualTime),"generation number=", nbGeneration, "score=", int(population[0].score),"path=",population[0].cities_list)
    if gui:
        pauseGui()
    return population[0].score, population[0].cities_list


def insertFitChromosomes(population, cities, n):
    """
        Ajoute n Chromosomes formés des gènes trouvés dans cities dans population.
        Ces Chromosomes sont construits à l'aide de l'algorithme des plus proches voisins puis mutés 3 fois.
        :param population: liste de Chromosome
        :param cities: liste de City
        :param n: nombre de Chromosome à ajouter
        """
    indexStartList = []
    cities_size = len(cities)
    if n <= cities_size:
        indexStartList = random.sample(range(cities_size), n)
    else:
        for i in range(n):
            indexStartList.append(random.randint(0, cities_size - 1))
    for i in range(n):
        fitChromosome = createFitChromosome(cities, indexStartList[i])
        mutation(fitChromosome, 100)
        mutation(fitChromosome, 100)
        mutation(fitChromosome, 100)
        population.append(fitChromosome)


def createFitChromosome(cities, startIndex):
    chromosomeSize = len(cities)
    fitGeneIndiceList = []
    fitGeneList = []
    weightList = []
    fitGeneIndiceList.append(startIndex)
    for i in range(0, chromosomeSize):  # pour chaque ville on cherche son plus proche voisin
        currentCity = cities[(startIndex + i) % chromosomeSize]
        weightList.clear()
        for j in range(chromosomeSize):  # pour chaque voisin on calcule sa distance
            if j not in fitGeneIndiceList:  # test si pas déjà ajouté
                weightList.append(weight(currentCity, cities[j]))
            else:
                weightList.append(0)
        ppvWeight = float("inf")
        for j in range(chromosomeSize):  # on cherche le plus proche voisin de la ville actuelle.
            currentWeight = weightList[j]
            if currentWeight != 0 and currentWeight < ppvWeight:  # test si pas un doublon et meilleur que les précédents
                ppvWeight = weightList[j]
                ppvIndice = j
        fitGeneIndiceList.append(ppvIndice)
    for i in range(chromosomeSize):  # construction de la liste de ville
        fitGeneList.append(cities[fitGeneIndiceList[i]])
    return Chromosome(fitGeneList)


def weight(city_a, city_b):
    """
    Calculate path's weight between two cities
    :param city_a:
    :param city_b:
    :return:
    """
    x = abs(city_a.x - city_b.x) ** 2
    y = abs(city_a.y - city_b.y) ** 2

    return sqrt(x + y)


def selection(population):
    """
    Selectionne la moitié de la population à partir de l'algorithme de la roulette
    :param population: liste de Chromosome
    :return: nouvelle population
    """
    total_weight = 0
    newPopulation = []
    propability = [0] * len(population)
    total_weight = sum(chromosome.score for chromosome in population)
    for chromosome in population:  # Calcule du score relatif
        chromosome.score /= total_weight
    for i in range(len(population)):
        for chromosome in population[:i + 1]:
            propability[i] += chromosome.score
    for i in range(int(len(population) / 2)):
        target = random.random()
        for (i, chromosome) in enumerate(population):
            if target <= propability[i]:
                newPopulation.append(deepcopy(chromosome))
                break
    newPopulation.sort(key=lambda chromosome: chromosome.calcFitness())
    return deepcopy(newPopulation)


def crossover(chromosome1, chromosome2, a=-1,b=-1):
    """
        Croisment de deux Chromosomes avec la méthode des deux points. Croisement OX.
        Il est possible de spécifier les points de croisement.
        :param chromosome1: premier Chromosome à croiser
        :param chromosome2: deuxième Chromosome à croiser
        :param a: premier point de croisement
        :param b: deuxième point de croisement
        """
    size = len(chromosome1)
    if(a <0 or b<0):
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
def parseFile(fname, cities):
    with open(fname) as f:
        lines = f.readlines()
    for line in lines:
        word = line.split(" ")
        name = word[0]
        x = int(word[1])
        y = int(word[2])
        cities.append(City(name, x, y))


def showGame(cities):
    draw(cities)

    running = True
    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Click at (%d, %d)" % event.pos)

            name = "v%i" % len(cities)
            x, y = event.pos
            cities.append(City(name, x, y))
            draw(cities)

        elif event.type == KEYDOWN and event.key == K_RETURN:
            running = False

        pygame.display.flip()


def drawPath(listCities, cities):
    screen = pygame.display.set_mode((screenSize, screenSize))
    draw(cities)

    # dessine tout les chemins
    listCityStart = listCities[0]
    for i in range(1, len(listCities)):
        listCityEnd = listCities[i]
        pygame.draw.line(screen, pathColor, (listCityStart.x, listCityStart.y),
                         (listCityEnd.x, listCityEnd.y))
        listCityStart = listCityEnd

    # ferme la boucle
    listCityStart = listCities[len(listCities) - 1]
    listCityEnd = listCities[0]
    pygame.draw.line(screen, pathColor, (listCityStart.x, listCityStart.y), (listCityEnd.x, listCityEnd.y))
    pygame.display.flip()  # refresh


def draw(cities):
    screen = pygame.display.set_mode((screenSize, screenSize))
    screen.fill(0)
    i = 0
    for listCity in cities:
        pygame.draw.circle(screen, listCityColor, (listCity.x, listCity.y), listCityWidth)
        # Show labels of cities
        font = pygame.font.Font(None, 12)
        text = font.render("%s (%i;%i)" % (listCity.name, listCity.x, listCity.y), True, fontColor)
        screen.blit(text, (listCity.x + 2, listCity.y - 10))
        i += 1
    font = pygame.font.Font(None, 30)
    text = font.render("Nombre : %i" % len(cities), True, fontColor)
    textRect = text.get_rect()
    screen.blit(text, textRect)

    pygame.display.flip()  # Repaint


def pauseGui():
    # Met la gui en pause. presser enter ou cliquer pour quitter
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == KEYDOWN and event.key == K_RETURN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
            running = False


def testCrossover():
    '''
    Test unitaire de la fonction crossover(chromosome1, chromosome2)
    '''
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
    crossover(testChromosome1, testChromosome2, 2, 4)

    assert (testChromosome1 == targetChromosome1), "crossover incorrecte!"
    assert (testChromosome2 == targetChromosome2), "crossover incorrecte!"


def testPerformance(file, targetLength, iteration):
    """
   Test la performance de la fonction ga_solve
   :param file: chemin du fichier à tester
   :param targetLength: Score minimum que à atteindre
   :param iteration: nombre de test à effectuer
   :return:
   """
    print("Test de performance")
    totalDuration = 0
    totalLength = 0
    bestDuration = float("inf")
    bestLength = float("inf")
    for i in range(iteration):
        start = time()
        length, path = ga_solve(file, False, 0)
        duration = time() - start
        if duration < bestDuration:
            bestDuration = duration
        if length < bestLength:
            bestLength = length
        totalDuration += duration
        totalLength += length
    print("temps moyen=", '%.3f' % (totalDuration / iteration))
    print("meilleur temps=", '%.3f' % bestDuration)
    print("score moyen=", '%.f' % (totalLength / iteration))
    print("meilleur score=", '%.f' % bestLength)
    print("consistance={:.1f}%".format((targetLength / (totalLength / iteration)) * 100))


if __name__ == "__main__":
    pygame.init()
    screenSize = 500
    pathColor = 0, 0, 255  # Blue
    listCityColor = 255, 0, 0  # Red
    fontColor = 255, 255, 255  # White
    listCityWidth = 2  # Width of one point

    #testCrossover()
    if False:  # pour le profilage!
        #testPerformance("data/pb010.txt", 1490, 20)
        testPerformance("data/pb020.txt", 1869,10)

    else:
        try:
            ga_solve(argv[1], bool(argv[2]) is True, float(argv[3]))
        except:
            print("Paramètres invalides!")
