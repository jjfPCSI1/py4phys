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
import matplotlib.pyplot as plt
from portrait_de_phase import portrait_de_phase,diagramme_energetique

tmax = 40
nb_points = 2000
x0 = np.arange(-8,8.1,0.79999999)
v0 = np.array([0]*len(x0))
k,m,d,ell0 = 1,1,3,5

colors = ["blue","red","green","magenta","cyan","yellow",
          "darkblue","darkred","darkgreen","darkmagenta","darkcyan"]*10

def landau(y,t):
    x,v = y
    return [v,-k*x/m*(np.sqrt(d**2+x**2) - ell0)/(np.sqrt(d**2+x**2))]

def Ep(x,v):
    return 0.5*k*(np.sqrt(x**2+d**2) - ell0)**2 + 0.5*m*v**2

t = np.linspace(0,tmax,nb_points)
x,v = [],[]
print(x0,v0)
for xi,vi in zip(x0,v0):
    print(xi,vi)
    sol = sp.integrate.odeint(landau,[xi,vi],t)
    x.append(sol[:,0])
    v.append(sol[:,1])

fig = plt.figure(figsize=(10,10))

vlim = (np.min(v),np.max(v))
base_name='PNG/M4_oscillateur_de_landau_portrait_de_phase'

for i,ti in enumerate(t):
    print(ti)
    xi = [xp[:i+1] for xp in x]
    vi = [vp[:i+1] for vp in v]
    plt.suptitle('Oscillateur de Landau, $t={}$'.format(round(ti,2)))
    plt.subplot(2,1,1)
    portrait_de_phase(xi,vi,fantome=50,clearfig=False,color=colors,ylim=vlim)
    plt.xlabel('')
    plt.subplot(2,1,2)
    diagramme_energetique(xi,vi,Ep,color=colors,clearfig=False,fantome=50)
    plt.savefig('{}_{:04d}.png'.format(base_name,i))
    plt.clf()

from film import make_film

make_film(base_name)



