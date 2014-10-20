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




"""

Programme similaire à S04_lois_de_descartes.py si ce n'est que l'on part de la 
droite et que l'on passe d'abord dans l'hémicylindre de plexiglas avant de se 
réfracter dans l'air, ce qui permet d'illustrer la notion de réflexion totale.

"""

# Import des modules importants
from math import *
# NB: comme turtle est importé en second, radians() vient de turtle et non de math
from turtle import *

R = 100                 # Le rayon de courbure du plexiglas

up()                    # On soulève le crayon
goto(0,R)               # On va en haut à gauche de la lentille
right(90)               # On tourne pour commencer à descendre
down()                  # On pose le crayon
forward(2*R)            # On dessine le côté plat de la lentille
left(90)                # On se remet dans l'axe
circle(R,180)           # On trace le cercle sur 180 degrés
up()                    # On soulève
goto(-200,0)            # Pour aller tracer l'axe optique 
right(180)              # Retour dans l'axe
for i in range(20):     # On va tracer la normale en pointillés
    down()              # On pose le stylo,
    forward(10)         # pour faire un trait,
    up()                # on lève le stylo
    forward(10)         # sans faire de trait.

n = 2.0                 # Indice du bloc de plexiglas
speed(10)               # On accélère un peu pour le début
COLORS = ['red','blue'] # La distribution des couleurs
color('red')            # On commence sur le rouge
right(180)              # Et on fait demi-tour (on va de droite à gauche)
radians()               # Passage de la tortue en radians pour les angles
fin = False             # Commutateur quand on aura dépassé l'angle de réflexion totale
for i in range(1,91):   # i est l'angle incident (donc dans le plexiglas)
    if i%10 == 9: color(COLORS[(i//10+1)%2]) # Changement de couleur tous les 10 degrés
    i = pi*i/180        # Conversion en radians
    # Si on peut prendre l'arcsinus
    try:    r = asin(n*sin(i))  # On le fait
    # Sinon, c'est qu'on a fini et on trace l'angle limite en violet
    except: r = pi/2 ; speed(1) ; color('violet') ; fin = True
    up()                # Levé du stylo et 
    goto(2*R*cos(i),2*R*sin(i)) # téléportation au point de départ
    left(i)             # On s'incline vers le bas
    down()              # Début du tracé
    forward(2*R)        # jusqu'à la rencontre de l'interface
    right(i-r)          # On est alors réfracté
    forward(2*R)        # et on continue tout droit
    up()                # On se relève
    right(r)            # et on se remet sur l'axe horizontal

    if fin: break       # Si c'est fini, on sort de la boucle

# On laisse 10s à l'orateur pour finir son explication.
import time
time.sleep(10)



