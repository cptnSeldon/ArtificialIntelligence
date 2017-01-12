# -*- coding: utf-8 -*-
__author__ = 'jeremy.wirth & jeshon.assuncao'

import itertools
import time
import random
from math import sqrt

import math

#valeurs constantes utiles pour le profilage
MUTATION_RATE=0.01

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

class Chromosome:
    def __init__(self, c_list):
        self.score = self.fitness()
        self.cities_list = c_list

    #TODO vérifier perfomance et justesse de cette fonction
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
            score += self.weight(city, city2)  # score calculation
        self.score = score
        # print(self.score)
        return self.score

    def __str__(self):
        return str(self.cities_list) + " : " + str(self.fitness()) + "\n"

    def __getitem__(self, index):
        return self.cities_list[index]

    def __setitem__(self, index, value):
        self.cities_list[index] = value

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

def ga_solve(file=None, gui=True, maxtime=0):
    if file == None:
        showGame()
    else:
        openFile = open(file, "r")
        parseFile(openFile.read())

    #Création d'une liste contenant différentes permutations des villes. On a donc une liste de chromosomes aka une population
    population = list(itertools.islice(itertools.permutations(cities), 50))

    timeStart = time.time()
    actualTime = -1
    #TODO si maxtime n'est pas une valeur positive, la fonction devra s’arrêter lorsqu’on constate une stagnation de l’amélioration des solutions.
    while actualTime < maxtime:

        #---------------DESSIN----------------
        if gui:
            drawPath()
        print(population[0].score)

        # A partir de maintenant on va appliquer le processus de séléction génétique.

        # --------------EVALUATION-------------------------
        population.sort(key=lambda chromosome: chromosome.score)

        #---------------SElECTION--------------------------
        # TODO la séléction doit retenir qu'une partie de la population
        # matingPool = selection(population) retient la moitiée des chromosomes
        matingPool=list(population[0:len(population)/2]) #hack elitisme
        population=[] #hack pour faire de la place à la nouvelle génération

        #------------------REPRODUCTION-------------------
        for i in range(0, len(matingPool) - 1, 2):

            # choix de deux individus qui vont produire deux enfants
            newChromosome1 = random.choice(matingPool)
            newChromosome2 = random.choice(matingPool)
            crossover(newChromosome1, newChromosome2)

            # Mutation du chromosome en permuttant deux gènes (villes)
            newChromosome1 = mutation(newChromosome1, MUTATION_RATE)
            newChromosome2 = mutation(newChromosome2, MUTATION_RATE)

            #Ajout des nouveaux chromosomes dans la nouvelle génération
            population[i]=newChromosome1
            population[i+1] = newChromosome2

        if maxtime > 0:
            actualTime = time.time() - timeStart

    population.sort(key=lambda chromosome: chromosome.score)
    return population[0].score, population[0].cities_list

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


def crossover(chromosome1, chromosome2):
    size = len(chromosome1)
    a, b = random.sample(range(0, size-1), 2)
    temp1, temp2 = list(chromosome1), list(chromosome2)  # sauvegarde la liste des villes
    if a > b:
        a, b = b, a
    # remplacement des villes à échanger par un drapeau
    for i in range(a, b+1):
        for c in range(1, size):
            if chromosome1[c] == temp2[i]:
                chromosome1[c] = False
            if chromosome2[c] == temp1[i]:
                chromosome2[c] = False
    # tassement des villes dans l'ordre à partir du deuxième point de croisement
    for i in range(size - (b - a + 1)):

        if chromosome1[(b + 1 + i) % size] == False:  # on cherche un trou
            j = (b + 2 + i) % size
            while chromosome1[j % size] == False or j == 0:  # on cherche la prochaine ville à droite et on ne prend pas en compte la ville de départ
                j += 1
                if j%size == 0: # on ne prend pas en compte la ville de départ
                    j += 1
            chromosome1[(b + 1 + i) % size] = chromosome1[j % size]  # remplacement du trou par la ville trouvée
            chromosome1[j % size] = False  # la ville déplacée devient un trou

        if chromosome2[(b + 1 + i) % size] == False:  # on cherche un trou
            j = (b + 2 + i) % size
            while chromosome2[j % size] == False or j == 0:  # on cherche la prochaine ville à droite et on ne prend pas en compte la ville de départ
                j += 1
            chromosome2[(b + 1 + i) % size] = chromosome2[j % size]  # remplacement du trou par la ville trouvée
            chromosome2[j % size] = False  # la ville déplacée devient un trou

    # on rempli les trous en faisant le crossover
    for i in range(a, b + 1):
        chromosome1[i], chromosome2[i] = temp2[i], temp1[i]
    return chromosome1, chromosome2

def mutation(chromosome, probability):
    if(random.randint(0,100) > probability*100):
        chrom_size = len(chromosome.cities_list)
        a = random.randint(0,chrom_size)
        b = random.randrange(0,chrom_size)
        while b == a:
            b = random.randrange(1, chrom_size - 1)
        chromosome[a], chromosome[b] = chromosome[b], chromosome[a]
    return chromosome




#Fonctions utiles pour l'affichage graphique et le parsing------------------------------------------------------------
def parseFile(file):
    lines = file.split("\n")
    for line in lines:
        word = line.split(" ")

        name = word[0]
        posX = int(word[1])
        posY = int(word[2])
        cities.append(City(name, posX, posY))


def showGame():
    draw(cities)

    running = True
    while running:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:  # Quit the game
            running = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Click
            print "Click at (%d, %d)" % event.pos

            name = "v%i" % len(cities)
            posX, posY = event.pos
            cities.append(City(name, posX, posY))
            draw(cities)

        elif event.type == KEYDOWN and event.key == K_RETURN:  # Key Return press
            running = False

        pygame.display.flip()  # Repaint

def drawPath():
    draw(cities)
    listCities = population[0].cities_list

    #dessine tout les chemins
    listCityStart = listCities[0]
    for i in range(1, len(listCities)):
        listCityEnd = listCities[i]
        pygame.draw.line(screen, pathColor, (listCityStart.get_x, listCityStart.get_y), (listCityEnd.get_x, listCityEnd.get_y))  # Show path
        listCityStart = listCityEnd

    #ferme la boucle
    listCityStart = listCities[len(listCities)-1]
    listCityEnd = listCities[0]
    pygame.draw.line(screen, pathColor, (listCityStart.posX, listCityStart.posY), (listCityEnd.posX, listCityEnd.posY))  # Show path

    pygame.display.flip() #refresh

    #pause après avoir dessiné un chemin, enter pour quitter
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == KEYDOWN and event.key == K_RETURN:
            running = False

def draw(cities):
    screen.fill(0)  # Erase all the screen

    i = 0
    for listCity in cities:
        pygame.draw.circle(screen, listCityColor, (listCity.get_x, listCity.get_y), listCityWidth)  # Show cities

        # Show labels of cities
        font = pygame.font.Font(None, 12)
        text = font.render("%s (%i;%i)" % (listCity.get_name, listCity.get_x, listCity.get_y), True, fontColor)
        screen.blit(text, (listCity.get_x + 2, listCity.get_y - 10))

        i += 1

    # Show the number of listCity
    font = pygame.font.Font(None, 30)
    text = font.render("Nombre : %i" % len(cities), True, fontColor)
    textRect = text.get_rect()
    screen.blit(text, textRect)

    pygame.display.flip()  # Repaint

if __name__ == "__main__":
    import sys, pygame
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN

    pygame.init()
    screenSize = 500
    screen = pygame.display.set_mode((screenSize, screenSize))

    cities = []
    population = []

    pathColor = 0, 0, 255  # Blue
    listCityColor = 255, 0, 0  # Red
    fontColor = 255, 255, 255  # White
    listCityWidth = 2  # Width of one point

    try:
        ga_solve(str(sys.argv[1]))
    except:
        ga_solve(None,True,10)

