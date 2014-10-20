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

Petite animation turtle pour illustrer les lois de Descartes pour la 
réfraction. L'idée est de simuler la "classique" illustration par envoi d'un 
faisceau lumineux sur un hémicylindre de plexiglas et d'observer la direction 
prise par le rayon réfracté.

On va colorer différemment les rayons tous les 10 degrés pour suivre que le 
"tassement" s'observe principalement lorsque les angles incidents sont presque 
à la perpendiculaire de la normale.

"""


from math import *
from turtle import *

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
right(180)              # Retour dans l'axe
for i in range(20):     # On va tracer la normale en pointillés
    down()              # On pose le stylo,
    forward(10)         # on avance en traçant,
    up()                # on relève le stylo,
    forward(10)         # on avance sans tracer

n = 2.0                 # Indice du plexiglas
speed(10)               # On accélère un peu
COLORS = ['red','blue'] # Les deux couleurs tous les 10° incidents
color('red')            # On commence sur le rouge
radians()               # On passe en radians (pour turtle) pour utiliser sin et cos
for i in range(1,91):   # Un rayon tous les degrés
    if i > 80: speed(2) # Si on est proche de la fin, on ralentit un peu
    if i%10 == 9: color(COLORS[(i//10+1)%2]) # Changement de couleur
    i = pi*i/180        # Conversion en radians
    r = asin(sin(i)/n)  # Calcul de l'angle réfracté
    up()                # On soulève le stylo pour se placer au bon endroit
    goto(-2*R*cos(i),-2*R*sin(i))
    left(i)             # On prend la bonne direction
    down()              # On pose le stylo
    forward(2*R)        # jusqu'à atteindre l'interface
    right(i-r)          # Là, on est réfracté
    forward(2*R)        # et on continue notre route
    up()                # On se relève
    right(r)            # et on se remet dans l'axe.


# À la fin, on attend 10s que l'orateur puisse expliquer aux élèves.
import time
time.sleep(10)



