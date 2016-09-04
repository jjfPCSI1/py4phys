# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




"""
Programme proposé par Antoine Senger (MP*, Lycée Poincaré, Nancy).
Il s'agit d'une résolution numérique de l'équation de la diffusion 1D, avec 
une conductivité et une capacité thermique variables, et diverses conditions 
aux bords possibles.
"""

# Les packages à récupérer.
import pylab as pl
import numpy as np
import scipy as sp

#Définition des paramètres du problème.

alpha = 0.2 #Coefficient donnant le pas temporel.
# Plus alpha est faible, plus la simulation est précise mais plus ele prend de temps.
# alpha > 0,5 donne systématiquement des résultats instables. 

n = 100 # nombre de points utilisé. 
L = 1 # Longueur totale (en unités arbitraires)
tmax = 0.01 # Temps d'observation (en unités arbitraires)
dx = float(L)/(n-1) # Pas de discrétisation
x = np.linspace(0,L,n) # Positions des différents points.
D = np.ones(n) #Coefficient de diffusion en chaque point: 1 par défaut.
lam = np.ones(n) #Conductivité thermique en chaque point: 1 par défaut.
T0 = np.zeros(n) #Température initiale de chaque point: 0 par défaut. Ici aussi, on a des unités arbitraires, et un zéro arbitraire.


for i in range(int(n/2)):
    D[i] = 9 # Coefficient de diffusion pour x < L/2
    T0[i] = 1 # Température initiale pour x < L/2
    lam[i] = 9 #Conductivité thermique pour x < L/2

dt = alpha*dx*dx/max(D) #pas de temps. 

D2 = D*dt/(dx*dx) #Coefficient de diffusion adimensionné, qui sera utilisé dans la suite.

beta = np.zeros(n) #Coefficient devant T[i+1] - T[i]
gamma = np.zeros(n) #Coefficient devant T[i-1] - T[i]
for i in range(1,n-1):
    beta[i] = D2[i]*(lam[i+1]-lam[i])/(2*lam[i])
    gamma[i] = D2[i]*(lam[i-1]-lam[i])/(2*lam[i])

def next(T):
    """
    Donne T(t+dt) en fonction de T(t).
    """
    newT = np.zeros(n) #Le futur T(t+dt)
    for i in range(1,n-1): # Les extrêmités sont exclues
        newT[i] = T[i] + D2[i]*(T[i+1]+T[i-1]-2*T[i]) + beta[i]*(T[i+1] - T[i]) + gamma[i]*(T[i-1] - T[i])
    #Equation de la diffusion discretisée
    # Reste à définir les conditions aux bords:
    #Conditions au bord isolantes.        
    newT[0] = newT[1] 
    newT[-1] = newT[-2]
    #Conditions aux bords à température imposée.
    #newT[0] = T0[0]
    #newT[-1] = T0[-1]
    #Conditions aux bords de type Newton.
    #h1 = 2
    #h2 = 2
    #newT[0] = T[0] + (h1*D2[0]*dx/lam[0])*(T0[0]-T[0]) + D2[0]*(T[1] - T[0])
    #newT[-1] = T[-1] + (h2*D2[-1]*dx/lam[-1])*(T0[-1]-T[-1])+D2[-1]*(T[-2]-T[-1])
    return(newT)

T = T0 # Température initiale
for t in range(int(tmax/dt)):
    T = next(T) #On fait un pas de temps dt.


pl.plot(x,T,'-',color='k')
pl.title("Profil de temperature lors du contact entre deux metaux")
pl.xlim([0,L])
pl.ylim([0,1])
#pl.grid(True,lw=1,linestyle='solid')
pl.show()



