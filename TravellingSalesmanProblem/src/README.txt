D�marche de Julia Nemeth et Nicolas Gonin

Notre algorithme consiste en une selection �litiste de la moiti� de la population.
Puis nous faisons un croisement en deux points � partir de deux membres de la population �litiste.
Ensuite nous faisons muter les enfants en un point avec une probabilit� de 1%.
Finalement nous ajoutons les enfants � la population �litiste.

Nous avons impl�ment� les op�rations ci-dessous sans les avoir utilis�es car elles r�duisaient nos performances.

S�l�ction gloutonne en utilisant l'algorithme du plus proche voisin en faisant varier al�atoirement la ville de d�part.
S�l�ction par roulette en prennat prennant la distance relative de chaque individu par rapport � la population
afin de d�terminer sa probabilit� d'�tre s�l�ctionn�.

Notre algorithme tombe r�guli�rement dans des minimums locaux � cause de notre s�l�ction �litiste.
Cela dit, tous nos efforts pour impl�menter une s�l�ction moins restrictives ont donn� des r�sultats qui convergeaient plus lentement vers
des minimums locaux.
