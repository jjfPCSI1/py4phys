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
for i in range(20):
    down()                  # On pose le stylo
    forward(10)            # et tracé effectif
    up()
    forward(10)

n = 2.0
speed(10)
COLORS = ['red','blue']
color('red')
radians()
for i in range(1,91):
    if i > 80: speed(2)
    if i%10 == 9: color(COLORS[(i//10+1)%2])
    i = pi*i/180
    r = asin(sin(i)/n)
    up()
    goto(-2*R*cos(i),-2*R*sin(i))
    left(i)
    down()
    forward(2*R)
    right(i-r)
    forward(2*R)
    up()
    right(r)

import time

time.sleep(10)



