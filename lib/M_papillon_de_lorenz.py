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
Animation montrant l'apparition de l'attracteur étrange dit du "papillon 
de Lorenz" (NB: ce n'est pas le Lorentz des transformations relativistes: il 
n'a pas de 't'), qui correspond à la solution du système différentiel
	dx/dt = a*(y-x)
	dy/dt = b*x - y - x*z
	dz/dt =-c*z + x*y
Les valeurs "simple" de (a,b,c) qui mènent au chaos sont (10,28,8/3).
On va essayer d'illustrer deux phénomènes différents: la sensibilité aux 
conditions initiales et le fait qu'un certain ordre se cache tout de même dans 
le chaos (voir Ian Stewart, Dieu joue-t-il aux dés, p196 et suivantes pour 
plus de détails)
"""

import numpy as np              # Boîte à outils numérique
import scipy as sp
import scipy.integrate          # Pour l'intégration numérique
import matplotlib.pyplot as plt # Boîte à outil graphique

# Nécessaire pour la 3D, même si cela n'apparaît pas explicitement
from mpl_toolkits.mplot3d import Axes3D 

tmax = 30                       # Tfinal d'intégration
nb_points = 3000                # Nombre de points pour l'échantillonnage en t
yvect0 = np.array([1.0,1.0,1.0])# Position initiale (x,y,z)
ecart_relatif = 0.01            # Écart relatif des deux positions initiales

def systeme_de_Lorenz(yvect,t): # Système différentiel à intégrer
    a,b,c = 10,28,8/3.0         # Les constantes du système
    x,y,z = yvect               # Les variables
    return [a*(y-x),b*x-y-x*z,-c*z+x*y]

# Échantillonnage en temps et intégration numérique
t = np.linspace(0,tmax,nb_points)
sol1 = sp.integrate.odeint(systeme_de_Lorenz,yvect0,t)
sol2 = sp.integrate.odeint(systeme_de_Lorenz,yvect0*(1+ecart_relatif),t)

# Récupération des positions pour les deux solutions recherchées
X1,Y1,Z1 = sol1[:,0],sol1[:,1],sol1[:,2]
X2,Y2,Z2 = sol2[:,0],sol2[:,1],sol2[:,2]

# Détection des maximum dans l'idée de représenter la position d'un maximum en 
# fonction de la position du maximum précédent pour Z -> l'ordre dans le chaos!
def trouve_positions_maximums(X):
    """ Renvoie la liste des indices correspondant aux maximums de la liste X 
    fournie en paramètre. """
    positions = []
    for i in range(1,len(X)-1):
        if X[i] > X[i-1] and X[i] > X[i+1]:
            positions.append(i)
    return positions



def both_plot(ax,X1,Y1,X2,Y2):
    ax.plot(X1,Y1,'b',X2,Y2,'r')               # Les deux tracés continus
    ax.plot(X1[-1],Y1[-1],'o',color='cyan')    # Dernier point premier tracé
    ax.plot(X2[-1],Y2[-1],'o',color='magenta') # Dernier point second tracé
    

def fait_plot(X,Y,Z,Xp,Yp,Zp,t,i): # Routine pour faire le plot effectif
    ax1 = fig.add_subplot(2,4,1)   # Sous-figure 1 (en haut à gauche)
    both_plot(ax1,X,Z,Xp,Zp)       # Tracé
    plt.xlabel('X')                # Labels
    plt.ylabel('Z')
    plt.xlim(-20,20)               # et limites 
    plt.ylim(0,50)
    ax2 = fig.add_subplot(2,4,2)   # Sous-figure 2 (en haut au milieu)
    both_plot(ax2,Y,Z,Yp,Zp)       # Tracé
    plt.xlabel('Y')                # Labels
    plt.ylabel('Z') 
    plt.xlim(-30,30)               # et limites
    plt.ylim(0,50)
    ax3 = fig.add_subplot(2,4,6)   # Sous-figure 6 (en bas au milieu)
    both_plot(ax3,Y,X,Yp,Xp)       # Tracé
    plt.xlabel('Y')                # Labels
    plt.ylabel('X')
    plt.ylim(-20,20)               # et limites
    plt.xlim(-30,30)
    ax4 = fig.add_subplot(2,4,5)   # Sous-figure 5 (en bas à gauche)
    # On cherche les maxima de Z et, si on en a trouvé, on trace le maximum 
    # courant en fonction du précédent
    pos = trouve_positions_maximums(Z)
    if len(pos) > 1: ax4.plot(Z[pos[:-1]], Z[pos[1:]], 'b.')
    if len(pos) > 0: ax4.plot(Z[pos[-1]] , Z[-1], 'o', color='cyan')
    # Pareil pour la 2e condition initiale
    pos = trouve_positions_maximums(Zp)
    if len(pos) > 1: ax4.plot(Zp[pos[:-1]],Zp[pos[1:]],'r.')
    if len(pos) > 0: ax4.plot(Zp[pos[-1]] ,Zp[-1], 'o', color='magenta')
    plt.xlabel('Z$_k$')            # Labels
    plt.ylabel('Z$_{k+1}$')
    plt.ylim(25,50)                # et limites
    # La dernière sous-figure occupe les 4 carrés de droite
    ax5 = plt.subplot2grid((2,4),(0,2),colspan=2,rowspan=2,projection='3d')
    ax5.set_xlabel('X')            # Labels
    ax5.set_ylabel('Y')
    ax5.set_zlabel('Z')
    ax5.set_xlim(-20,20)           # Limites
    ax5.set_ylim(-30,30)
    ax5.set_zlim(0,50)
    ax5.plot(X,Y,Z,'b')            # et tracés
    ax5.plot(Xp,Yp,Zp,'r')
    ax5.plot([X[-1]],[Y[-1]],[Z[-1]],'o', color='cyan')
    ax5.plot([Xp[-1]],[Yp[-1]],[Zp[-1]],'o', color='magenta')
    # On modifie l'angle de vue au fur et à mesure
    ax5.view_init(elev=10,azim=i%360)
    # Titre global de la figure
    plt.suptitle('Papillon de Lorenz, $t={}$'.format(t))
    # Sauvegarde et nettoyage
    plt.savefig('{}{:05d}.png'.format(base_name,i))
    plt.clf()

# Le programme proprement dit

base_name = 'PNG/M_papillon_de_lorenz_' # Nom des figures

fig = plt.figure(figsize=(16,8))        # Définition de la figure

# For debugging purposes
#i = 1000
#fait_plot(X1[:i],Y1[:i],Z1[:i],X2[:i],Y2[:i],Z2[:i],round(t[i],3),i)


for i in range(5,len(t)):  # La ronde des images
    print(i)
    fait_plot(X1[:i],Y1[:i],Z1[:i],X2[:i],Y2[:i],Z2[:i],round(t[i],2),i)

# Ne reste plus qu'à rassembler en un fichier mpeg à l'aide de convert puis de
# ppmtoy4m et mpeg2enc (paquet mjpegtools à installer sur la machine)
    
import os

cmd = '(for f in ' + base_name + '*png ; '
cmd+= 'do convert -density 100x100 $f -depth 8 -resize 1200x600 PNM:- ; done)'
cmd+= ' | ppmtoy4m -S 420mpeg2'
cmd+= ' |  mpeg2enc -f1 -b 12000 -q7 -G 30 -o {}film.mpeg'.format(base_name)

print("Execution de la commande de conversion")
print(cmd)
os.system(cmd)
print("Fin de la commande de conversion")



