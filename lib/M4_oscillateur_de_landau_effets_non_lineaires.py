# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




"""
Illustration des effets non linéaires dans le cadre d'un oscillateur de 
Landau, notamment le non isochronisme des oscillations et leur aspect non 
symétrique.
"""

import numpy as np
import scipy as sp
import scipy.integrate
import matplotlib.pyplot as plt
print('working')
from portrait_de_phase import portrait_de_phase,diagramme_energetique
print('not working...')

tmax = 40                         # Temps d'intégration
nb_points = 200                  # Nb de point pour l'échantillonnage en temps
decalage = 40
k,m,d,ell0 = 1,1,3,5              # Quelques constantes
x0 = np.arange(4.1,6.1,0.1)      # Positions initiales
v0 = np.array([0]*len(x0))        # Vitesses initiales (nulles)

colors = ["blue","red","green","magenta","cyan","yellow",
          "darkblue","darkred","darkgreen","darkmagenta","darkcyan"]*10

def landau(y,t):
    x,v = y
    return [v,-k*x/m*(np.sqrt(d**2+x**2) - ell0)/(np.sqrt(d**2+x**2))]

def Em(x,v):                      # Énergie mécanique
    return 0.5*k*(np.sqrt(x**2+d**2) - ell0)**2 + 0.5*m*v**2

t = np.linspace(0,tmax,nb_points) # Échantillonnage en temps
x,v = [],[]                       # Initialisation
for xi,vi in zip(x0,v0):          # Itération sur les conditions initiales
    print(xi,vi)                  # Un peu de feedback
    sol = sp.integrate.odeint(landau,[xi,vi],t) # On intègre
    x.append(sol[:,0])            # et on stocke à la fois les positions
    v.append(sol[:,1])            # et les vitesses

fig = plt.figure(figsize=(10,10)) # Création de la figure

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
    plt.suptitle('Oscillateur de Landau, $t={}$'.format(round(ti,2)))
    plt.subplot(3,1,1)            # Première sous-figure
    plt.plot([t[0],t[-1]],[np.sqrt(ell0**2-d**2)]*2,'k')
    plt.ylabel('$x$')
    plt.title('Evolution temporelle de $x$ (en fonction de $t$)')
    for j in range(len(xi)):
        plt.plot(t[:i+1],xi[j],color=colors[j])
    plt.ylim(max(0,min(x[-1])),xi[-1][0])
    if i < decalage: plt.xlim(0,t[decalage])
    else: plt.xlim(t[i-decalage],t[i])
    plt.subplot(3,1,2)            # Seconde sous-figure
    portrait_de_phase(xi,vi,fantome=50,clearfig=False,color=colors,ylim=vlim)
    plt.xlabel('')
    plt.subplot(3,1,3)            # Troisième sous-figure
    diagramme_energetique(xi,vi,Em,color=colors,clearfig=False,fantome=50)
#    plt.savefig('{}_{:04d}.png'.format(base_name,i))

# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=len(t),interval=20)

plt.show()



