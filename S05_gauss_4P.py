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
Programme conçu par Tom Morel (PCSI, lycée Jean Jaurès) pour visualiser 
l'influence de la position du côté plat pour la qualité d'une image. On se 
rend compte que lorsque le côté plat est du côté où l'objet/image est au plus 
près (règle des 4P), les aberrations géométriques sont moins prononcées. 
Effets de bords intéressants: 
 * la lentille étant non-symétrique, le centre optique n'est pas au milieu 
 (d'où le décalage observé pour le foyer dans les deux positions).
 * dans le 2e cas, certains rayons ne peuvent pas ressortir de la lentille du 
 fait du phénomène de réflexion totale.
"""

from math   import *   # Pour les calculs
from turtle import *   # Pour la tortue du LOGO

n = 1.4                # Indice choisi pour le verre
N = 20                 # Nombre de rayons à dessiner
xi= - 400              # Coordonnée xi de départ des rayons
yi= 80                 # Coordonnée relative yi de départ du premier rayon

R = 100                # Rayon de courbure de la lentille
decal = 1.5*R          # Moitié du décalage vertical entre les deux images
ylim = 60              # À partir de quand colorie-t-on les rayons en rouge

# Dessin de la première lentille
up()                   # On lève le crayon
goto(xi+2*R,-R+decal)  # Position de départ en bas à droite
left(90)               # On va vers le haut
down()                 # On pose le crayon
forward(2*R)           # Tracé de la partie plane
left(90)               # On se positionne vers la gauche
circle(R,180)          # et on fait le demi-cercle
up()                   # On lève le crayon
goto(xi,decal)         # Préparation de l'axe optique
down()                 # On pose le crayon
forward(800)           # et on le trace

# Dessin de la seconde lentille
up()                   # On lève le crayon
goto(xi+R,-R-decal)    # Position de départ en bas à gauche
left(90)               # On va vers le haut
down()                 # On pose le crayon
forward(2*R)           # Tracé de la partie plane
right(90)              # On se positionne vers la droite
circle(-R,180)         # et on fait le demi-cercle
up()                   # On lève le crayon
goto(xi,-decal)        # Préparation de l'axe optique
right(180)             # Demi-tour droite !
down()                 # On pose le crayon
forward(800)           # et on le trace

radians()              # À partir d'ici, on passe en radians pour les angles

for i in range(N):     # Boucle sur les rayons à tracer
    up()               # On lève le crayon
    goto(xi,yi+decal)  # pour se mettre au point de départ
    down()             # puis on le repose pour commencer le tracé
    alpha=asin(yi/R)   # Angle par rapport à la normale 1ère interface
    beta=asin(yi/(n*R))# Angle de réfraction 1ère interface air/verre
    xa=-R*cos(alpha)-2*R # Là où on va toucher la 1ère interface
    if abs(yi)>=ylim:  # On met les rayons extrêmes
        color('red')   # en rouge
    else:              # et les autres
        color('blue')  # en bleu
    goto(xa,yi+decal)  # Allons jusqu'au contact avec la lentille
    # Un petit calcul pour la position du contact avec la 2e interface
    yb=yi+(xa+2*R)*tan(alpha-beta) 
    goto(-2*R,yb+decal)# On y va !
    # Et on calcule l'angle de réfraction en sortie de cette 2e interaface
    gamma=asin(n*sin(alpha-beta)) 
    right(gamma)       # La tortue étant toujours horizontale, on tourne de cet angle
    forward(550)       # On avance tout droit
    left(gamma)        # et on se remet à l'horizontale pour le tracé suivant

    up()               # On passe à présent au second schéma avec un levé de crayon
    goto(xi,yi-decal)  # pour se mettre au point de départ
    down()             # et on repose le crayon.
    alpha=asin(yi/R)   # Angle par rapport à la normale 2ère interface
    xa= R*cos(alpha)-3*R # Contact avec la 2ère interface (la partie plane est sans effet)
    if abs(yi)>=ylim:  # On met les rayons extrêmes
        color('red')   # en rouge
    else:              # et les autres
        color('blue')  # en bleu
    goto(xa,yi-decal)  # On va jusqu'au contact
    try:               # Attention, il est possible qu'il y ait réflexion totale
        beta=asin(n*yi/R) # si ce calcul échoue...
        right(-alpha+beta)# Si tout va bien, on tourne
        forward(550)      # on avance
        left(-alpha+beta) # et on se remet dans l'axe
    except: pass       # Cas de la réflexion totale: on ne fait rien de plus
    
    yi=yi-(160/(N-1))      # Passage au rayon suivant.

# L'important est bien sûr de montrer le dessin se construire en direct, mais
# si on veut en conserver une trace, on peut utiliser ce hack:

base_name = 'PNG/S05_gauss_4P'

ts = getscreen()
ts.getcanvas().postscript(file=base_name + ".eps")

import os # Pour pouvoir appeler BBcut et convert
os.system('./BBcut {}.eps'.format(base_name))         # Pour tailler la bounding box
os.system('convert {0}.eps {0}.png'.format(base_name))# Pour convertir en png
        



