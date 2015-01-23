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

# Les variables suivantes déterminent ce qui est indiqué sur chaque axe:
# * valeur 0: coordonnée x
# * valeur 1: coordonnée z
# * valeur 2: vitesse vx
# * valeur 3: vitesse vz
# * valeur 4: temps t
Xi = 1
Yi = 3
# Paramètres d'intégration
tmin,tmax,nb_t = 0,20,1000
# Conditions initiales
x0,z0 = 0,2
v0  = 0
theta0 = -np.pi/2
# Possibilité de définir les valeurs limites en x et en y
# (à False, les limites sont posées par la solution quadratique)
XLIM = False # (0,500)
YLIM = False # (0,200)

# On prend un parachutiste de 100kg. On suppose que la vitesse limite atteinte 
# est de l'ordre de 200km/h.
m = 100
g = 9.81
vlim = 200/3.6 # Conversion en m/s
# On se débrouille pour atteindre la même vitesse dans le cadre de ces deux modèles
alpha = m*g/vlim
beta  = m*g/vlim**2
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

sol = [sans,lineaire,quadratique]

fig = plt.figure()

if Xi == 4: X = t
else: X = quadratique[:,Xi]
Y = quadratique[:,Yi]

label = ['$x$ en m', '$z$ en m', '$v_x$ en m/s', '$v_z$ en m/s', '$t$ en s']

plt.xlabel(label[Xi])
plt.ylabel(label[Yi])


plt1, = plt.plot(X,Y,label='Sans frottements')
plt2, = plt.plot(X,Y,label='Frottements lineaires')
plt3, = plt.plot(X,Y,label='Frottements quadratiques')

plots = [plt1,plt2,plt3]

if XLIM: plt.xlim(XLIM)
if YLIM: plt.ylim(YLIM)

plt.legend()

#plt.tight_layout()


from matplotlib import animation # Pour l'animation progressive

def init():
    pass

def animate(i):
    for j in range(3):
        if Xi == 4: X = t[:i]
        else: X = sol[j][:i,Xi]
        Y = sol[j][:i,Yi]
        plot = plots[j]
        plot.set_xdata(X)
        plot.set_ydata(Y)
    plt.title('t={:.2f}'.format(t[i]))

# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=nb_t,interval=20,blit=False)

plt.show()



