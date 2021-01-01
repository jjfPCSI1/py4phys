# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber.
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.


"""
Illustration des effets non linéaires dans le cadre d'un pendule pesant
notamment le non isochronisme des grandes oscillations
"""

import numpy as np
import scipy as sp
import scipy.integrate
import matplotlib.pyplot as plt
from portrait_de_phase import portrait_de_phase,diagramme_energetique

tmax = 8                            # Temps d'intégration
nb_points = 100                      # Nb de point pour l'échantillonnage en temps
decalage = 70
mgOG = 1                             # m*g*OG
J = 1                                # Moment d'inertie
omega0 = np.sqrt(mgOG/J)             # Pulsation propre
theta0 = np.arange(0.1,2.1,0.1)      # Positions initiales
thetapoint0 = np.array([0]*len(theta0))  # Vitesses initiales (nulles)

colors = ["blue","red","green","magenta","cyan","yellow",
          "darkblue","darkred","darkgreen","darkmagenta","darkcyan"]*10

def pesant(y,t):
    theta,thetapoint = y
    return [thetapoint,-omega0**2 * np.sin(theta)]

def Em(theta,thetapoint):                      # Énergie mécanique
    return 0.5*J*thetapoint**2 - mgOG * np.cos(theta)

t = np.linspace(0,tmax,nb_points) # Échantillonnage en temps
x,v = [],[]                       # Initialisation
for xi,vi in zip(theta0,thetapoint0):          # Itération sur les conditions initiales
    print(xi,vi)                  # Un peu de feedback
    sol = sp.integrate.odeint(pesant,[xi,vi],t) # On intègre
    x.append(sol[:,0])            # et on stocke à la fois les positions
    v.append(sol[:,1])            # et les vitesses

fig = plt.figure(figsize=(8,8)) # Création de la figure

vlim = (np.min(v),np.max(v))      # Limites verticales (horizontales imposées par les CI)

def init():
    pass

from matplotlib import animation # Pour l'animation progressive

def animate(i):
    plt.clf()
    ti = t[i]
    print(ti)
    xi = [xp[:i+1] for xp in x]   # On stocke l'avancement
    vi = [vp[:i+1] for vp in v]   # jusqu'à l'instant présent
    plt.suptitle('Pendule pesant, $t={}$'.format(round(ti,2)))
    plt.subplot(2,2,1)            # Première sous-figure
    plt.ylabel('$x$')
    plt.title('Evolution temporelle de $\\theta$ (en fonction de $t$)')
    for j in range(len(xi)):
        plt.plot(t[:i+1],xi[j],color=colors[j])
    xlim = min(x[-1]),xi[-1][0]
    plt.ylim(xlim)
    if i < decalage: plt.xlim(0,t[decalage])
    else: plt.xlim(t[i-decalage],t[i])
    plt.subplot(2,2,3)            # Seconde sous-figure
    portrait_de_phase(xi,vi,fantome=50,clearfig=False,color=colors,ylim=vlim,xlim=xlim)
    plt.xlabel('')
    plt.subplot(1,2,2)            # Troisième sous-figure
    diagramme_energetique(xi,vi,Em,color=colors,clearfig=False,fantome=50,xlim=xlim)
#    plt.savefig('{}_{:04d}.png'.format(base_name,i))

# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=len(t),interval=200)

plt.show()
