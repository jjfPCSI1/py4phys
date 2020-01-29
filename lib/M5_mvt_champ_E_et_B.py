""" 
Programme permettant de visualiser en 3D le mouvement d'une particule 
chargée dans un champ électrique couplé à un champ magnétique. 
"""

import numpy as np
import scipy as sp
import scipy.optimize
import scipy.integrate

#########################################################################
# Préparation du travail: là où on peut modifier les paramètres de la 
# simulation
#########################################################################

faire_animation = True
en_3D = True
equal = True
m = 1.0
q = 1.0
OM0= np.array([0,0,0])    # Position initiale
nv = 1.0                  # Norme de la vitesse initiale
nE = 1.0                  # Norme du champ électrique
nB = 1.0                  # Norme du champ magnétique
uv = np.array([0.0,1.0,0.0])  # Vecteur directeur de la vitesse initiale
uE = np.array([1.0,0.0,0.0])  # Vecteur directeur du champ électrique
uB = np.array([0.0,0.0,1.0])  # Vecteur directeur du champ magnétique

# Normalisations au cas où
uv = uv/np.linalg.norm(uv)        
uE = uE/np.linalg.norm(uE)
uB = uB/np.linalg.norm(uB)

# Les vecteurs reconstruits
v0 = nv * uv            # Vecteur vitesse initiale
E0 = nE * uE            # Vecteur champ électrique
B0 = nB * uB            # Vecteur champ magnétique

#########################################################################
# À présent intégration de l'équation du mouvement, on essaie de travailler 
# vectoriellement en réarrangeant les dimensions des objets dont on dispose 
# pour se rapprocher de ce qu'on connaît en physique.
#########################################################################

def f(y,t):
    """ Fonction d'intégration du système différentiel: l'accélération est 
    donnée par l'expression de la force de Lorentz """
    y = y.reshape(2,3)  # Passage d'un vecteur 6D à deux vecteurs 3D
    position, vitesse = y 
    # Le produit vectoriel s'écrit np.cross
    acceleration = q/m * (E0 + np.cross(vitesse,B0))
    result = np.array([vitesse,acceleration])
    result = result.reshape(6) # Retour de deux vecteur 3D à un vecteur 6D
    return result

# Condition initiales
y0 = np.array([OM0,v0])
y0 = y0.reshape(6)
# Temps d'intégration
t = np.linspace(0,30,1000)
# Intégration proprement dite
solution = sp.integrate.odeint(f,y0,t)

# On redistribue les 1000 vecteurs 6D en 1000 fois deux vecteurs 3D
solution = solution.reshape(len(solution),2,3)

# La récupération est alors simplifiée
position = solution[:,0]
vitesse  = solution[:,1]

# La transposition (maintenant que vous connaissez les matrices) permet de 
# passer à 3 lignes à 1000 colonnes donc récupérer dans X, Y et Z l'évolution 
# de chaque coordonnée au cours du temps.
X,Y,Z = position.transpose()

#########################################################################
# Ne reste plus qu'à faire la partie graphique
#########################################################################

import matplotlib.pyplot as plt # 2D
from mpl_toolkits.mplot3d import Axes3D # 3D
from matplotlib import animation # Pour l'animation progressive

def arrondi(nb):
    if nb == int(nb): return int(nb)
    else:             return round(nb,2)


def vec(vecteur):
    """ Renvoie une version affichable du vecteur """
    x,y,z = vecteur
    return "({},{},{})".format(arrondi(x),arrondi(y),arrondi(z))

fig = plt.figure()
titre = '$\\vec{{E}}={}$, $\\vec{{B}}={}$ et $\\vec{{v}}_0={}$'.format(vec(E0),vec(B0),vec(v0))
if equal: plt.axis('equal')
if en_3D: ax = Axes3D(fig)     # La 3D demande une syntaxe particulière
else:     ax = plt.axes()

if en_3D: mvt = ax.plot(X,Y,Z)[0]
else:     mvt = plt.plot(X,Y)[0]
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
if en_3D: ax.set_zlabel('$z$')
if en_3D: ax.set_title(titre)
else:     plt.title(titre)

if faire_animation:   
    def init():
        pass
                    
    def animate(i):
        mvt.set_data(X[:i],Y[:i])
        if en_3D: mvt.set_3d_properties(Z[:i])
                                                
    anim = animation.FuncAnimation(fig,animate,frames=len(t),interval=1)

plt.show()


