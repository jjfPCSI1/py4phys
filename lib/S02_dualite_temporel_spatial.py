# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.



"""
Petite animation pour montrer ce qui se passe au passage d'une onde à la fois 
par une vue de profil et selon l'évolution temporelle de l'altitude de 
certains points.
"""

import matplotlib.pyplot as plt
from matplotlib import animation # Pour l'animation progressive
import numpy as np

fig = plt.figure(figsize=(10,10))

def f(u,k=10):
    """Le profil de l'onde à propager: une gaussienne multipliée par un cosinus."""
    return np.exp(-3*u**2) * np.cos(k*u-5)

nb_points  = 1000   # Le nombre de points d'échantillonnage du graphe
nb_images  = 1000   # Le nombre d'images à créer.

x = np.linspace(-10,10,nb_points)   # Echantillonnage en position
t = np.linspace(-1,5,nb_images)   # On regarde le profil à différents temps
c = 3
eps =-1 # 1 si vers la droite, -1 si vers la gauche

X0= [-2,2,4]  # Les positions initiales à regarder

COLORS = ['red','blue','green','cyan','yellow']

def animate(i):
    plt.clf()
    plt.subplot(211)
    plt.title('$t = {}$'.format(round(t[i],2)))
    plt.plot(x,f(t[i]-eps*x/c))
    plt.ylim(-1,1)
    plt.xlim(min(x),max(x))
    plt.xlabel('Position $x$')
    plt.ylabel('Altitude $y$')
    plt.subplot(212)
    plt.ylim(-1,1)
    plt.xlim(min(t),max(t))    
    plt.xlabel('Temps $t$')
    plt.ylabel('Altitude $y$')
    for j,x0 in enumerate(X0):
        plt.subplot(212)
        ti = t[i]
        y = f(ti-eps*x0/c)
        plt.plot(t[:i+1],f(t[:i+1]-eps*x0/c),color=COLORS[j])
        plt.plot(ti,y,'o',color=COLORS[j])
        plt.subplot(211)
        plt.plot(x0,y,'o',color=COLORS[j])

# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=len(t),interval=2)

anim.save('PNG/S02_dualite_temporel_spatial_gauche.mp4', fps=30)

#plt.show()




