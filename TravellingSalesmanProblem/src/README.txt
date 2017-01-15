Démarche de Julia Nemeth et Nicolas Gonin

Notre algorithme consiste en une selection élitiste de la moitié de la population.
Puis nous faisons un croisement en deux points à partir de deux membres de la population élitiste.
Ensuite nous faisons muter les enfants en un point avec une probabilité de 1%.
Finalement nous ajoutons les enfants à la population élitiste.

Nous avons implémenté les opérations ci-dessous sans les avoir utilisées car elles réduisaient nos performances.

Séléction gloutonne en utilisant l'algorithme du plus proche voisin en faisant varier aléatoirement la ville de départ.
Séléction par roulette en prennat prennant la distance relative de chaque individu par rapport à la population
afin de déterminer sa probabilité d'être séléctionné.

Notre algorithme tombe régulièrement dans des minimums locaux à cause de notre séléction élitiste.
Cela dit, tous nos efforts pour implémenter une séléction moins restrictives ont donné des résultats qui convergeaient plus lentement vers
des minimums locaux.
