# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




""" 
Contribution de Bruno Martens (PTSI, Annecy) pour visualiser la 
trajectoire d'une particule chargée dans un champ magnétique, avec ou sans 
frottements.
"""

import numpy as np
import matplotlib . pyplot as plt # 2D
from mpl_toolkits . mplot3d import Axes3D # 3D
from scipy.integrate import odeint
from matplotlib import animation # Pour l'animation progressive

#mouvement dans B uniforme sans frottements
fig = plt . figure (1)
ax = Axes3D ( fig )
#Donnees
t=np.linspace(0,5,1000)
v0,w0=10,10 #v0 est selon Ox
z=v0*t     #mvt selon OZ
# Veut-on un animation ou non ?
faire_animation = True

#definition du systeme differentiel
def sol(y,t):
    return (w0*y[1]+v0,-w0*y[0])

#resolution
y=odeint(sol,(0,0),t)

#tracé
 
mvt=ax.plot(y[:,0],y[:,1],z,label='mouvement dans un champ B uniforme sans frottements')[0]
ax.legend() #sans cela, le label ne s'affiche pas
# Axes
ax . set_xlabel ( 'x axis ')
ax . set_ylabel ( 'y axis ')
ax . set_zlabel ( 'z axis ')

plt.savefig('PNG/M5_mouvement_helicoidal_sans_frottement.png')

if faire_animation:
    def init():
        mvt.set_data([1,2],[1,2])
        mvt.set_3d_properties([1,2])
       
    def animate(i):
        mvt.set_data(y[:i,0],y[:i,1])
        mvt.set_3d_properties(z[:i])

    anim = animation.FuncAnimation(fig,animate,frames=len(t),interval=1)

plt.show()

#mouvement dans B uniforme avec frottements
fig = plt . figure (2)
ax = Axes3D ( fig )
#Donnees
t=np.linspace(0,7,1000)
v0,w0,a=10,10,1 #v0 est selon Ox et a=k/m
def sol(y,t):
    return (w0*y[1]+v0-a*y[0],-w0*y[0]-a*y[1],v0-a*y[2])

y=odeint(sol,(0,0,0),t)
z = y[:,2]
mvt = ax.plot(y[:,0],y[:,1],z,label='mouvement dans un champ B uniforme avec frottements')[0]
ax.legend()
# Axes
ax . set_xlabel ( 'x axis ')
ax . set_ylabel ( 'y axis ')
ax . set_zlabel ( 'z axis ')

plt.savefig('PNG/M5_mouvement_helicoidal_avec_frottement.png')

if faire_animation:
    def init():
        mvt.set_data([1,2],[1,2])
        mvt.set_3d_properties([1,2])
       
    def animate(i):
        mvt.set_data(y[:i,0],y[:i,1])
        mvt.set_3d_properties(z[:i])

    anim = animation.FuncAnimation(fig,animate,frames=len(t),interval=1)

plt.show()



