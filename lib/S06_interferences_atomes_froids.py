# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.



"""
Ce programme est proposé par Vincent Grenard (PCSI, Lycée Poincaré, Nancy).

Animation pour le cours "introduction au monde quantique"
Résultat d'interférence lors d'expérience de lacher d'atome à travers des fentes
(ou de passage de photon unique à travers des fentes)
"""

import random as r
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# Tire N nombre au pif, calcule 1+cosinus et si c'est plus petit qu'un nombre 
# aléatoire, on le garde. Ainsi on a une distribution de proba qui a l'air d'être
# en 1+cos, mais on tire plein de nombres aléatoires pour rien
N=500000
L=np.random.uniform(-15,15,N)
proba_affichage=1+np.cos(L)
affiche=proba_affichage<np.random.uniform(0,2,N)
xdata=L[affiche]
ydata=np.random.uniform(0,2,len(xdata))
#plt.figure()
#plt.hist(xdata,100)


fig=plt.figure(facecolor='w')
fig.add_axes([0,0,1,1])
l,=plt.plot(xdata,ydata,'o',markersize=3,markeredgecolor='b')
plt.axis('off')

def animate(n):
#    i=n+np.floor(10**(0.1*n))-1
    i=n+np.floor(2**(0.01*n))-1
    l.set_xdata(xdata[:i])
    l.set_ydata(ydata[:i])
    return l,
    
anim = animation.FuncAnimation(fig,animate,2000,interval=20,blit=False,repeat=False)
#anim.save('PNG/S06_interferences_atomes_froids.mp4', fps=30,bitrate=50)
plt.show()

#fig=plt.figure(facecolor='w')
#fig.add_axes([0,0,1,1])
#l,=plt.plot(xdata[:N/10],ydata[:N/10],'o',markersize=3,markeredgecolor='b')
#plt.axis('off')
#fig.savefig("interference_atome_froid.eps")


