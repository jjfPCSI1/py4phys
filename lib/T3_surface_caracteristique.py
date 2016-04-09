# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




"""
Visualisation 3D de l'équation d'état d'un gaz parfait en coordonnées (P,V,T) 
ainsi que le tracé d'un cycle sur un tel diagramme. 
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.xkcd()

V = np.linspace(10,30,200)
T = np.linspace(200,450,200)
V,T = np.meshgrid(V,T)
R = 8.314
P = R*T/V


fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(V,T,P,cmap='jet')

plt.title('Cycle isobare, isotherme, isochore')
plt.xlabel('Volume V')
plt.ylabel('Temperature T')
ax.set_zlabel('Pression P')
#plt.zlabel('Pression P')

# Isotherme
V = np.linspace(15,25,100)
T = 250*np.ones(100)
P = R*T/V
ax.plot(V,T,P,'k',linewidth=4)

# Isochore
V = 25 * np.ones(100)
T = np.linspace(250,415,100)
P = R*T/V
ax.plot(V,T,P,'k',linewidth=4)

# Isobare
P = R*250/15
T = np.linspace(250,415,100)
V = R*T/P
ax.plot(V,T,P,'k',linewidth=4)

plt.show()



