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




import numpy as np
import scipy as sp
import scipy.integrate
from portrait_de_phase import portrait_de_phase

tmax = 10
nb_points = 1000
x0 = np.arange(0.1,8,0.3)
v0 = np.array([0]*len(x0))

def landau(y,t):
    x,vx = y
    k,m,d,ell0 = 1,1,3,5
    return [vx,-k*x/m*(np.sqrt(d**2+x**2) - ell0)/(np.sqrt(d**2+x**2))]

t = np.linspace(0,tmax,nb_points)
x,v = [],[]
print(x0,v0)
for xi,vi in zip(x0,v0):
    print(xi,vi)
    sol = sp.integrate.odeint(landau,[xi,vi],t)
    x.append(sol[:,0])
    v.append(sol[:,1])



portrait_de_phase(x,v,fantome=50)




