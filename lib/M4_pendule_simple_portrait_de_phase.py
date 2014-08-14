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

tmax = 20
nb_points = 1000
thp0 = np.arange(-8,8.1,0.3)
th0  = np.array([0]*len(thp0))
k,m,d,ell0 = 1,1,3,5
g,m,ell = 9.81,1,1

colors = ["blue","red","green","magenta","cyan","yellow",
          "darkblue","darkred","darkgreen","darkmagenta","darkcyan"]*10

def Ep(th,thp):
    return m*g*ell*(1-np.cos(th)) +  0.5*m*(ell*thp)**2

def pendule(y,t):
    th,thp = y
    return [thp,-g/ell * np.sin(th)]

t = np.linspace(0,tmax,nb_points)
th,thp = [],[]
for thi,thpi in zip(th0,thp0):
    sol = sp.integrate.odeint(pendule,[thi,thpi],t)
    theta = sol[:,0]%(6*np.pi)
    theta[theta > 3*np.pi] = theta[theta > 3*np.pi] - 6*np.pi
    th.append(theta)
    thp.append(sol[:,1])

fig = plt.figure(figsize=(10,10))

th_lim = (np.min(th),np.max(th))
base_name='PNG/M4_pendule_simple_portrait_de_phase'

for i,ti in enumerate(t):
    print(ti)
    thi = [th_p[:i+1] for th_p in th]
    thpi= [thp_p[:i+1] for thp_p in thp]
    plt.suptitle('Pendule simple, $t={}$'.format(round(ti,2)))
    plt.subplot(2,1,1)
    portrait_de_phase(thi,thpi,fantome=50,clearfig=False,color=colors,xlim=th_lim)
    plt.xlabel('')
    plt.subplot(2,1,2)
    diagramme_energetique(thi,thpi,Ep,color=colors,clearfig=False,fantome=50,xlim=th_lim)
    plt.savefig('{}_{:04d}.png'.format(base_name,i))
    plt.clf()

from film import make_film

make_film(base_name)





# On peut aussi regarder juste sur juste 2pi d'intervalle, avec les mêmes 
# résultats

for theta in th: # On sait que theta est déjà entre -3pi et 3pi
    theta[theta> np.pi] = theta[theta> np.pi] - 2*np.pi
    theta[theta<-np.pi] = theta[theta<-np.pi] + 2*np.pi

fig = plt.figure(figsize=(10,10))

th_lim = (np.min(th),np.max(th))
base_name='PNG/M4_pendule_simple_portrait_de_phase_2pi'

for i,ti in enumerate(t):
    print(ti)
    thi = [th_p[:i+1] for th_p in th]
    thpi= [thp_p[:i+1] for thp_p in thp]
    plt.suptitle('Pendule simple, $t={}$'.format(round(ti,2)))
    plt.subplot(2,1,1)
    portrait_de_phase(thi,thpi,fantome=50,clearfig=False,color=colors,xlim=th_lim)
    plt.xlabel('')
    plt.subplot(2,1,2)
    diagramme_energetique(thi,thpi,Ep,color=colors,clearfig=False,fantome=50,xlim=th_lim)
    plt.savefig('{}_{:04d}.png'.format(base_name,i))
    plt.clf()

make_film(base_name)







# Voyons ce qui se passe quand on rajoute un peu d'amortissement

alpha = 0.1

def pendule(y,t):
    th,thp = y
    return [thp,-g/ell * np.sin(th) - alpha*thp]

t = np.linspace(0,tmax,nb_points)
th,thp = [],[]
for thi,thpi in zip(th0,thp0):
    sol = sp.integrate.odeint(pendule,[thi,thpi],t)
    theta = sol[:,0]%(6*np.pi)
    theta[theta > 3*np.pi] = theta[theta > 3*np.pi] - 6*np.pi
    th.append(theta)
    thp.append(sol[:,1])

fig = plt.figure(figsize=(10,10))

th_lim = (np.min(th),np.max(th))
base_name='PNG/M4_pendule_simple_portrait_de_phase_amorti'

for i,ti in enumerate(t):
    print(ti)
    thi = [th_p[:i+1] for th_p in th]
    thpi= [thp_p[:i+1] for thp_p in thp]
    plt.suptitle('Pendule simple, $t={}$'.format(round(ti,2)))
    plt.subplot(2,1,1)
    portrait_de_phase(thi,thpi,fantome=50,clearfig=False,color=colors,xlim=th_lim)
    plt.xlabel('')
    plt.subplot(2,1,2)
    diagramme_energetique(thi,thpi,Ep,color=colors,clearfig=False,fantome=50,xlim=th_lim)
    plt.savefig('{}_{:04d}.png'.format(base_name,i))
    plt.clf()

make_film(base_name)



