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
Mise en place d'ondes stationnaires par superposition d'ondes qui se propagent 
dans les deux sens
"""

import numpy as np              # Boîte à outils numériques
import matplotlib.pyplot as plt # Boîte à outils graphiques
import film                     # Boîte à outils vidéos

def source(x,t,x0=0,phi=0):
    '''La fonction représentant notre source située en x0.'''
    k,w = 5,1                        # Quelques constantes 
    r = np.sqrt((x-x0)**2)           # La distance à la source
    u = k*r - w*t + phi              # La variable de déplacement
    res =  np.sin(u)                 # Simple sinus
    res[u > 0] = 0.0                 # Pour s'assurer qu'à t<0, il n'y a pas d'onde
    return res

x2  = 5                              # Position de la deuxième source (première en 0)
xmin,xmax = 0,x2                     # Limites de la fenêtre d'échantillonnage
nb_points = 1000                     # Nombre de points d'échantillonnage
phi = np.pi/2                        # Déphasage de la deuxième source
tmin,tmax = 0,60                     # L'intervalle de temps d'étude
dt = 0.1                             # Incrément de temps

base_name = 'PNG/S03_ondes_stationnaires'

t = tmin
i = 0
while t < tmax:                      # On commence la boucle temporelle
    print(t)                         # Un peu de feedback
    x = np.linspace(xmin,xmax,nb_points) # Échantillonnage horizontal
    S1= source(x,t,0)                # Effet de la première source
    S2= source(x,t,x2,phi)           # Effet de la seconde source
    S =  S1+S2                       # Effet résultant
    plt.plot(x,S1,alpha=0.5)         # Affichage première source (bleu)
    plt.plot(x,S2,alpha=0.5)         # Affichage seconde source (vert)
    plt.plot(x,S,'k',linewidth=2)    # Affichage résultante (noir)
    plt.ylim(-2,2)                   # On contraint l'échelle verticale
    plt.savefig(base_name + '_{:04d}.png'.format(i)) # Sauvegarde
    plt.clf()                        # Nettoyage
    i+= 1                            # et incrémentation
    t+=dt                            # des compteurs

film.make_film(base_name)  # Fabrication du film à la fin



