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

Ce programme est proposé par Vincent Grenard (PCSI, Lycée Poincaré, Nancy).

Visualisation d'un réseau d'interférences à deux sources en utilisant une 
animation "au vol" plutôt qu'une conversion en images. Nécessite d'avoir 
Python installé sur la machine mais cela permet de modifier les paramètres et 
montrer immédiatement les modifications aux élèves.

Néanmoins, une sauvegarde dans un fichier .mp4 est possible: voir la fin du 
programme !

"""

import numpy as np               # Boîte à outils numériques
import pylab as py               # Boîte à outils graphiques
from matplotlib import animation # Pour l'animation en temps réel

taille=400                       # Largeur en pixels de l'image
lim=10                           # Largeur maximale de l'image
x=np.linspace(-lim,lim,taille)   # L'axe des x
y=x                              # Le même en y

X,Y=np.meshgrid(x,y,indexing='xy') # La "grille" sur laquelle seront évaluées les fonctions

y1=3                             # Position verticale de la première source
y2=-y1                           # Position verticale de la seconde source
r1=np.sqrt(X**2+(Y-y1)**2)       # Grille des distances à la première source
r2=np.sqrt(X**2+(Y-y2)**2)       # Pareil pour la seconde

w=4*np.pi                        # Pulsation des oscillations
delta_t=0.01                     # Intervalle de temps entre deux images
t=0                              # Temps initial
k=1.0*np.pi                      # Nombre d'onde
a1=1                             # Amplitude de la première source
a2=1                             # Amplitude de la seconde source

# Calcul de l'amplitude résultante (ne prend pas en compte la décroissance en 
# 1/r que devrait avoir les ondes)
S1 = a1*np.cos(k*r1-w*t)
S2 = a2*np.cos(k*r2-w*t)
amplitude= S1 + S2

# Préparation des figures
fig=py.figure(figsize=[16,8],facecolor='w')              # Taille globale
fig.add_axes([0.5,0.05,0.45,0.9],aspect='equal')         # Figure de droite
image=py.imshow(amplitude, extent = [-lim,lim,-lim,lim]) # La superposition
py.plot([0],y1,'wo',markersize=5)                        # Position source 1
py.plot([0],y2,'wo',markersize=5)                        # Position source 2
py.axis([-lim,lim,-lim,lim])                             # Avec axes gradués
#py.axis('off')                                          # ou sans (au choix)
fig.add_axes([0.05,0.05,0.4,0.4],aspect='equal')         # Figure en bas à gauche
image2=py.imshow(S1,  extent =[-lim,lim,-lim,lim])       # Action de S1 seule
py.plot([0],y1,'wo',markersize=5)                        # Position source 1
py.plot([0],y2,'wo',markersize=5)                        # Position source 2
py.axis([-lim,lim,-lim,lim])                             # Avec axes gradués
#py.axis('off')                                          # ou sans
fig.add_axes([0.05,0.5,0.4,0.4],aspect='equal')          # Figure en haut à gauche
image3=py.imshow(S2, extent = [-lim,lim,-lim,lim])       # Action de S2 seule
py.plot([0],y1,'wo',markersize=5)                        # Position source 1
py.plot([0],y2,'wo',markersize=5)                        # Position source 2
py.axis([-lim,lim,-lim,lim])                             # Avec axes gradués
#py.axis('off')                                          # ou sans

def animate(i): # Mise à jour des figures à chaque nouvelle frame
    t=i*delta_t                           # Nouveau temps
    print(t)                              # Feedback en cas de sauvegarde
    S1 = a1*np.cos(k*r1-w*t)              # Source 1
    S2 = a2*np.cos(k*r2-w*t)              # Source 2
    amplitude= S1 + S2                    # Superposition
    image.set_data(amplitude)             # Mise à jour données superposition
    py.title('t=%.2f s'%(t))              # Le titre avec l'instant choisi
    image2.set_data(S1)                   # Mise à jour source 1
    image3.set_data(S2)                   # Mise à jour source 2

# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=int(10/delta_t),interval=20)

# À décommenter pour sauvegarder dans un fichier .mp4
#anim.save('PNG/S03_interferences_animation.mp4', fps=30)

# Sinon, on montre en direct
py.show()


