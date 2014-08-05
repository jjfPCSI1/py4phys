# coding: latin1

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.
# 
# Si l'encodage vous pose problème, vous pouvez réencoder le fichier à l'aide 
# de la commande
# 
# recode l1..utf8 monfichier.py
# 
# Il faudra alors modifier la première ligne en # coding: utf8
# pour que Python s'y retrouve.





'''
Programme conçu par Tom Morel (PCSI, lycée Jean Jaurès) pour visualiser
l'influence de la couleur du rayon incident sur la distance focale d'une
lentille sphérique
'''

from math import *      # Pour les fonctions mathématiques
from turtle import *    # Pour les dessins à l'écran (appelé après math pour radians())


def Cauchy(x):
    '''Fonction donnant l'indice du milieu en suivant la loi de Cauchy en
    fonction de la longueur d'onde x donnée en mètres.'''
    A=1.2
    B=171*1e-16
    n=A+(B/x**2)
    return n

N= 10                   # nombre de rayons à dessiner
xi= - 200               # coordonnée xi de départ
yi= -50                 # coordonnée yi de départ
longueur=[400,800]      # différentes longueurs d'onde
pal=['blue','red']      # et les couleurs associées
R = 100                 # Le rayon de courbure de la lentille

up()                    # On soulève le crayon
goto(0,R)               # On va en haut à gauche de la lentille
right(90)               # On tourne pour commencer à descendre
down()                  # On pose le crayon
forward(2*R)            # On dessine le côté plat de la lentille
left(90)                # On se remet dans l'axe
circle(R,180)           # On trace le cercle sur 180 degrés
up()                    # On soulève
goto(-200,0)            # Pour aller tracer l'axe optique
down()                  # On pose le stylo
right(180)              # Retour dans l'axe
forward(800)            # et tracé effectif

radians()               # On passe les angles en radians.

for j in range(len(longueur)): # On boucle sur les couleurs
    color(pal[j])              # Sélection de la couleur
    n=Cauchy(longueur[j]*1e-9) # On récupère l'indice optique
    yi=-R/2                    # Ordonnée initiale
    for i in range(N):         # On boucle sur les rayons à dessiner
        up()                   # On lève le crayon
        goto(-200,yi)          # On se place
        down()                 # et c'est parti !
        goto(sqrt(100**2-yi**2),yi) # On traverse jusqu'à la face sphérique
        alpha=asin(yi/100)     # Angle d'incidence sur la face de sortie
        theta=asin(n*yi/100)   # Angle après réfraction dans l'air
        right(theta-alpha)     # On tourne de l'angle de déviation
        forward(450)           # On complète le tracé
        left(theta-alpha)      # et on se remet dans l'axe
        yi=yi+(R/N)            # Définition de la prochaine ordonnée

# L'important est bien sûr de montrer le dessin se construire en direct, mais
# si on veut en conserver une trace, on peut utiliser ce hack:

base_name = 'PNG/S05_distortion_chromatique'

ts = getscreen()
ts.getcanvas().postscript(file=base_name + ".eps")

import os # Pour pouvoir appeler BBcut et convert
os.system('./BBcut {}.eps'.format(base_name))         # Pour tailler la bounding box
os.system('convert {0}.eps {0}.png'.format(base_name))# Pour convertir en png




