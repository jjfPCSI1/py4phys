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
Simple résolution numérique de l'équation d'un oscillateur harmonique pour 
illustrer l'isochronisme des oscillations quelle que soit l'amplitude de départ
avec animation au cours du temps.
'''

import numpy as np               # Pour np.linspace
import scipy as sp               # Simple alias usuel
import scipy.integrate           # Pour l'intégration
import matplotlib.pyplot as plt  # Pour les dessins
from matplotlib import animation # Pour l'animation progressive

omega0 = 1   # On définit la pulsation propre


def equadiff(y,t):
    '''Renvoie l'action du système dx/dt = vx et dvx/dt = -omega0**2 * x 
    soit bien l'oscillateur harmonique x'' + omega0**2 * x = 0'''
    x,vx = y                     # y contient position et vitesse
    return [vx,- omega0**2 * x]  # On renvoie un doublet pour [dx/dt,dvx/dt]

nb_CI = 10 # Nombre de conditions initiales explorées

t = np.linspace(0,10,1000)       # Le temps total d'intégration
x0= np.linspace(-5,5,nb_CI)      # Les positions initiales choisies
v0= [0]*nb_CI                    # Les vitesses  initiales choisies

oscillateurs = []
lignes = []

fig = plt.figure(figsize=(10,8))
    
for i in range(nb_CI):           # Pour chaque condition initiale
                                 # L'intégration proprement dite
    sol = sp.integrate.odeint(equadiff,[x0[i],v0[i]],t)
    x = sol[:,0]                 # Récupération de la position
    l, = plt.plot(t,x)           # et affichage
    oscillateurs.append(x)
    lignes.append(l)

def init():
    for l in lignes:
        l.set_xdata([])
        l.set_ydata([])

def animate(i):
    for l,x in zip(lignes,oscillateurs):
        l.set_ydata(x[:i])
        l.set_xdata(t[:i])

# Il ne reste que le traitement cosmétique

plt.title('Oscillateur harmonique pour differentes amplitudes initiales')
plt.ylabel('Position (unite arbitraire)')
plt.xlabel('Temps (unite arbitraire)')


anim = animation.FuncAnimation(fig,animate,len(t),interval=20,init_func=init,blit=False)

plt.show()

#plt.savefig('PNG/S01_oscillateur_harmonique_periode.png')



