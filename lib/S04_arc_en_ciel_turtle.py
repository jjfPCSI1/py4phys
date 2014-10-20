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
l'influence de la couleur du rayon incident lors de sa réfraction à 
l'intérieur d'une goutte d'eau. Pour alléger les calculs, on approxime un peu 
les expressions des cordes dans la goutte, mais cela reste parfaitement 
correct au tracé.
'''


from turtle import *   # Pour le dessin à l'écran
from math import *     # Pour les fonctions mathématiques

def Cauchy(x):
    '''Fonction donnant l'indice du milieu en suivant la loi de Cauchy en 
    fonction de la longueur d'onde x donnée en mètres.'''
    A=1.58
    B=171*1e-16
    n=A+(B/x**2)
    return n

# On commence par les déclarations
R =100          # Rayon du cercle
yi=R/2          # Coordonnée y du premier rayon
xi=-2*R         # Coordonnée x du premier rayon
longueur=[400,500,600,700,800]                    # Différentes longueurs d'onde
pal=['purple','blue','dark green','orange','red'] # et les couleurs associées
i= asin(yi/R)   # angle d'incidence du premier rayon (en radian)

# On démarre le dessin
up()            # On lève le crayon
goto(0,-R)      # On va au point de coordonnée (0,-R)
down()          # On pose le crayon
circle(R,360)   # On dessine le cercle
up()            # On relève le crayon
goto(xi,yi)     # On va au point de départ du rayon lumineux
down()          # On repose le crayon
goto(-sqrt(R*R-yi*yi),yi) # Et on va jusqu'à toucher la goutte d'eau

def imprime_ecran(n):
    """ Récupère ce qui est affiché à l'écran. """
    base_name = 'PNG/S04_arc_en_ciel_turtle'
    getscreen().getcanvas().postscript(file=base_name + "{:02d}.eps".format(n))
    

delay(40)       # On ralentit un peu Speedy Gonzales...
# À présent, on va boucler sur les couleurs que l'on veut représenter
for j in range(len(longueur)):
    color(pal[j])               # On change la couleur du trait
    n= Cauchy(longueur[j]*1e-9) # Valeur de l'indice optique en fonction de lambda
    r=asin(sin(i)/n)            # Angle de réfraction (en radian)
    right((i-r)*180/pi)         # Tourner à droite d'un angle (i-r) en degré
    forward(190)                # On avance (à peu près) de la distance adéquate
    right(180-(2*r*180/pi))     # On tourne de pi-2*r à droite
    forward(190)                # On réavance (à peu près) de la distance adéquate
    right((i-r)*180/pi)         # Même configuration qu'à l'aller
    forward(200)                # On sort de la goutte
    up()                        # On relève le crayon
    goto(-sqrt(R*R-yi*yi),yi)   # Et on retourne au point de départ
    # Ne reste qu'à tourner à l'envers pour se remettre dans l'axe
    left(2*(i-r)*180/pi+180-(2*r*180/pi)) 
    down()                      # et on repose le crayon
    imprime_ecran(j)            # On prends une petite photo pour la route


import time

time.sleep(30)

# L'important est bien sûr de montrer le dessin se construire en direct, mais 
# si on veut en conserver une trace, on peut utiliser ce hack:

base_name = 'PNG/S04_arc_en_ciel_turtle'

ts = getscreen()
ts.getcanvas().postscript(file=base_name + ".eps")

import os # Pour pouvoir appeler BBcut et convert
os.system('./BBcut {}.eps'.format(base_name))         # Pour tailler la bounding box
os.system('convert {0}.eps {0}.png'.format(base_name))# Pour convertir en png



