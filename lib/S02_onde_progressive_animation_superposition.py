# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.



'''
Animation montrant la propagation de trois ondes de profil identique mais de 
vitesse différente ainsi que leur superposition. Peut servir à illustrer 
qualitativement la notion d'étalement du paquet d'onde.
'''

import numpy as np               # Pour np.linspace, np.exp et np.cos
import matplotlib.pyplot as plt  # Pour les dessins


def f(u,k=10):
    '''Le profil de l'onde à propager: une gaussienne multipliée par un cosinus.'''
    return np.exp(-3*u**2) * np.cos(k*u-5)

nb_points  = 1000   # Le nombre de points d'échantillonnage du graphe
nb_courbes = 3      # Le nombre de courbes à représenter
nb_images  = 151    # Le nombre d'images à créer.
c = np.linspace(0.1,0.3,nb_courbes) # Les différentes vitesses de propagation

# On fait une visualisation spatiale

x = np.linspace(- 4, 4,nb_points)   # Echantillonnage en position
t = np.linspace(-15,15,nb_images)   # On regarde le profil à différents temps

base_name = 'PNG/S02_onde_progressive_superposition_'

for i,ti in enumerate(t):
    plt.subplot(211)              # La première sous-figure
    plt.ylim(-3,3)                # et ses limitations
    plt.ylabel("Profil de l'onde")# ainsi que le label des ordonnées
    plt.title('Profil spatial pour $t={}$'.format(round(ti,2)))
    ftot = np.zeros(len(x))       # Initialisation du signal superposé
    for cj in c:                  # On regarde chaque vitesse
        fi = f(x-cj*ti) # Echantillonnage du profil pour les différents x
        plt.plot(x,fi)  # Affichage
        ftot += fi      # On ajoute à l'onde totale
    plt.subplot(212)              # La seconde sous-figure
    plt.ylim(-3,3)                # et ses limitations
    plt.ylabel("Profil de l'onde")# ainsi que le label des ordonnées
    plt.plot(x,ftot)              # Affichage du signal superposé
    plt.xlabel('Position $x$')    # et label des abscisses
    fichier = base_name + '{:03d}'.format(i)
    plt.savefig(fichier)          # On sauvegarde un fichier par temps
    plt.clf()                     # et on nettoie pour le suivant
    
# Ne reste plus qu'à rassembler en un fichier gif à l'aide de convert

import subprocess

cmd = "convert -delay 1 -dispose Background +page {}".format(base_name + '*.png')
cmd+= " -loop 0 {}".format(base_name + 'film.gif') 

print("Execution de la commande de conversion")
print(cmd)
p = subprocess.Popen(cmd, shell=True)
print("Fin de la commande de conversion")


