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


T1,V1,P1 = 300,10e-3,1e5
gamma = 1.4
nR = P1*V1/T1
# Compression Isotherme:
T2 = T1
V2 = V1/10
P2 = nR*T2/V2
# Détente adiabatique
# avec isochore pour finir
V3 = V1 
P3 = P2 * (V2/V3)**gamma
T3 = P3*V3/nR


V = np.linspace(0.9e-3,12e-3,100)
T = np.linspace(100,320,100)
V,T = np.meshgrid(V,T)
R = 8.314
P = nR*T/V

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(V,T,P,cmap='jet')

plt.title('Cycle isentropique, isotherme, isochore')

plt.xlabel('Volume V')
plt.ylabel('Temperature T')
ax.set_zlabel('Pression P')
#plt.zlabel('Pression P')

# Isotherme
V = np.linspace(V1,V2,100)
T = T1*np.ones(100)
P = nR*T/V
ax.plot(V,T,P,'k',linewidth=4)

# Isentropique
V = np.linspace(V2,V3,100)
P = P2 * (V2/V)**gamma
T = P*V/nR
ax.plot(V,T,P,'k',linewidth=4)

# Isochore
T = np.linspace(T3,T1,100)
V = V3*np.ones(100)
P = nR*T/V
ax.plot(V,T,P,'k',linewidth=4)

plt.show()



