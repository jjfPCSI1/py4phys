# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




""" 
Résolution de l'exercice du chien C qui course son maître M qui fait son 
jogging à une vitesse v0 suivant vex en le visant à une vitesse v suivant le 
vecteur vect(CM)/CM.

L'idée est de pouvoir faire varier les différents paramètres, notamment le 
rapport de vitesse, pour voir l'impact sur les trajectoires possibles.

"""

import numpy as np
import scipy as sp
import scipy.integrate
import matplotlib.pyplot as plt

v = 1         # Vitesse du chien
v0= 1         # Vitesse du maître

# Position initiale du chien (cf coordonnees de l'exercice)
theta0 = np.pi/2
rho0   = 4
y0 = [rho0,theta0]

# Distribution des temps
tmin, tmax, dt = 0, 20, 0.1
nb_t = int((tmax-tmin)/dt)
t = np.linspace(tmin,tmax,nb_t)


def f(y,t):
    """ Fonction permettant la résolution du système différentiel
          drho/dt       = -v + v0*cos(theta)
          rho*dtheta/dt =     -v0*sin(theta)
    """
    rho,theta = y
    return [-v + v0*np.cos(theta), -v0*np.sin(theta)/rho]
    
sol = sp.integrate.odeint(f,y0,t)

# Position du maître dans le référentiel du chien.

rho  = sol[:,0]
theta= sol[:,1]

# Trajectoire du chien
XC = v0*t - rho*np.cos(theta)
YC =      - rho*np.sin(theta)

fig = plt.figure()

maitre_traj,= plt.plot(v0*t,t*0+0.1,'k')
chien_traj, = plt.plot(XC,YC,'k')
maitre_pos, = plt.plot([0],[0],'ob')
chien_pos,  = plt.plot([XC[-1]],[YC[-1]],'or')

plt.title('Un chien (en rouge) court apres son maitre (en bleu)')

def animate(i):
    maitre_traj.set_data(v0*t[:i],t[:i]*0)
    chien_traj.set_data(XC[:i],YC[:i])
    maitre_pos.set_xdata([v0*t[i]])
    chien_pos.set_data([XC[i]],[YC[i]])


from matplotlib import animation # Pour l'animation progressive

# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=nb_t,interval=20,blit=False)

plt.show()



