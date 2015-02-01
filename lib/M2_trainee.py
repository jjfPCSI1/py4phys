# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




""" 
Illustration de l'influence de la trainée pour une chute dans un champ de 
pesanteur constant. 

Il faut penser à définir les valeurs voulue pour alpha et beta de sorte que la 
force s'écrive alpha*v ou beta*v**2 en norme.
"""

import numpy as np
import scipy as sp
import scipy.integrate
import matplotlib.pyplot as plt

# On prend un parachutiste de 100kg. On suppose que la vitesse limite atteinte 
# est de l'ordre de 200km/h.
m = 100
g = 9.81
vlim = 200/3.6 # Conversion en m/s
# On se débrouille pour atteindre la même vitesse dans le cadre de ces deux modèles
alpha = m*g/vlim
beta  = m*g/vlim**2
# Paramètres d'intégration
tmin,tmax,nb_t = 0,2,1000
# Conditions initiales
x0,z0 = 0,2
v0  = 10
theta0 = np.pi/4
vx0,vz0  = v0*np.cos(theta0),v0*np.sin(theta0)

def k(v,type="sans"):
    """ Constante prévectorielle pour les frottements. v est supposée être la 
    norme de la vitesse de la particule. Différents cas sont disponibles:
    * "lineaire": k est constant égal à alpha, variable globale définie ailleurs
    * "quadratique": k est proportionnel à v, de coeff de proportionnalité beta défini ailleurs
    * "sans": pas de frottement: k=0
    """
    if   type == "lineaire":
       return alpha
    elif type == "quadratique":
       return beta*v
    else:
       return 0.0

# Définition de la fonction permettant l'intégration
def f(y,t,type):
    """ Fonction d'intégration pour une chute libre. y est un "quadri"-vecteur 
    contenant les positions et vitesses [x,z,vx,vz]. Le type permet de définir 
    s'il on veut des frottements de type linéaire, quadratique ou pas de 
    frottement du tout. """
    x,z,vx,vz = y            # Récupération des positions et vitesses
    v = np.sqrt(vx**2+vz**2) # Norme de la vitesse
    return [vx,vz,-k(v,type)*vx/m,-k(v,type)*vz/m-g]

t = np.linspace(tmin,tmax,nb_t)
y0 = [x0,z0,vx0,vz0]
sans        = sp.integrate.odeint(f,y0,t,args=('sans',))
lineaire    = sp.integrate.odeint(f,y0,t,args=('lineaire',))
quadratique = sp.integrate.odeint(f,y0,t,args=('quadratique',))

def rajoute_courbe(sol,plots,i):
    x = sol[:i+1,0]
    z = sol[:i+1,1]
    vx= sol[:i+1,2]
    vz= sol[:i+1,3]
    ti= t[:i+1]
    plots[0][0].set_xdata(ti)
    plots[0][0].set_ydata(z)
    plots[1][0].set_xdata(x)
    plots[1][0].set_ydata(z)
    plots[2][0].set_xdata(ti)
    plots[2][0].set_ydata(vz)
    plots[3][0].set_xdata(z)
    plots[3][0].set_ydata(vz)

fig = plt.figure(figsize=(10,10))

ax1= plt.subplot2grid((2,2),(0,0))
ax2= plt.subplot2grid((2,2),(0,1),sharey=ax1)
ax3= plt.subplot2grid((2,2),(1,0),sharex=ax1)
ax4= plt.subplot2grid((2,2),(1,1),sharey=ax3)

ax1.set_xlabel('$t$ en s')
ax1.set_ylabel('$z$ en m')
ax2.set_xlabel('$x$ en m')
ax2.set_ylabel('$z$ en m')
ax3.set_xlabel('$t$ en s')
ax3.set_ylabel('$v_z$ en m/s')
ax4.set_xlabel('$z$ en m')
ax4.set_ylabel('$v_z$ en m/s')

plt.tight_layout()


from matplotlib import animation # Pour l'animation progressive

def init():
    pass

axes = [ax1,ax2,ax3,ax4]
plt_sans = [a.plot([],[]) for a in axes]
plt_lin  = [a.plot([],[]) for a in axes]
plt_quad = [a.plot([],[]) for a in axes]

def animate(i):
    rajoute_courbe(sans,plt_sans,i)
    rajoute_courbe(lineaire,plt_lin,i)
    rajoute_courbe(quadratique,plt_quad,i)
    ax1.set_title('t={}'.format(t[i]))

# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=nb_t,interval=20)

plt.show()



