# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




"""

Illustration d'un exercice de TD visant à montrer l'évolution temporelle de la 
densité de probabilité pour la superposition équiprobable d'un état n=1 et 
d'un état n quelconque (à fixer) pour le puits quantique infini.

Par souci de simplicité, on se débrouille pour que E_1/hbar = 1

"""

import numpy as np               # Boîte à outils numériques
import matplotlib.pyplot as plt  # Boîte à outils graphiques
from matplotlib import animation # Pour l'animation progressive

# Second état n observer (à fixer)
n = 2

# On met tous les paramètres à 1 (ou presque)
t0 = 0
dt = 0.1
L = 1
hbar = 1
h = hbar * 2 * np.pi
m = (2*np.pi)**2
E1= h**2 / (8*m*L**2)
En= n*E1

x = np.linspace(0,L,1000)

def psi1(x,t):
    return np.sin(np.pi*x/L) * np.exp(1j*E1*t/hbar)

def psin(x,t):
    return np.sin(n*np.pi*x/L) * np.exp(1j*En*t/hbar)

def psi(x,t):
    return 1/L**0.5 * (psi1(x,t) + psin(x,t))

fig = plt.figure()
line, =plt.plot(x,abs(psi(x,t0))**2)
plt.title('$t={}$'.format(t0))
plt.ylabel('$|\psi(x,t)|^2$')
plt.xlabel('$x$')
plt.plot(x,abs(psi1(x,t0))**2,'--',label='$|\psi_1|^2$')
plt.plot(x,abs(psin(x,t0))**2,'--',label='$|\psi_{}|^2$'.format(n))

plt.legend()

def init():
    pass
    
def animate(i):
    t = i*dt + t0
    line.set_ydata(abs(psi(x,t))**2)
    plt.title('$t={}$'.format(t))

anim = animation.FuncAnimation(fig,animate,frames=1000,interval=20)

plt.show()



