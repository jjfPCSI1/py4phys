# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




""" 
Résolution de l'exercice de l'insecte qui tourne autour d'une lumière avec une 
vitesse faisant un angle alpha constant avec la direction du centre.
"""

import numpy as np
import scipy as sp
import scipy.integrate
import matplotlib.pyplot as plt

v0= 1         
alpha = np.pi/2 + np.pi/2 * 0.1

theta0 = 0
r0     = 4
y0 = [r0,theta0]

# Distribution des temps
tmin, tmax, dt = 0, 30, 0.01
nb_t = int((tmax-tmin)/dt)
t = np.linspace(tmin,tmax,nb_t)


def f(y,t):
    """ Fonction permettant la résolution du système différentiel
          dr/dt       = v0*cos(alpha)
          r*dtheta/dt = v0*sin(alpha)
    """
    r,theta = y
    return [v0*np.cos(alpha), v0*np.sin(alpha)/r]
    
sol = sp.integrate.odeint(f,y0,t)

# Position de l'insecte

r    = sol[:,0]
theta= sol[:,1]
X,Y = r*np.cos(theta),r*np.sin(theta)

fig = plt.figure()

insecte_traj, = plt.plot(X,Y,'k')
insecte_pos,  = plt.plot([X[-1]],[Y[-1]],'ob')

plt.title("Un insecte (en bleu) va s'ecraser sur le point lumineux central...")

def animate(i):
    insecte_traj.set_data(X[:i],Y[:i])
    insecte_pos.set_data([X[i]],[Y[i]])


from matplotlib import animation # Pour l'animation progressive

# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=nb_t,interval=30,blit=False)

plt.show()



