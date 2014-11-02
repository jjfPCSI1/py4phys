# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




"""

Le programme suivant est quasiment entièrement repris depuis le MOOC 
Statistical Mechanics: Algorithms and Computations de Werner Krauth (ENS) avec 
la participation de Michaël Kopf, Vivien Lecomte et Alberto Rosso.

Le programme a été adapté d'un programme fourni dans le tutorial 5 concernant 
l'évolution temporelle (en partant du concept de "temps imaginaire") en 
mécanique quantique.

L'idée est de partir de la fonction d'onde et de lui appliquer le formalisme 
d'évolution à partir d'opérateur exponentiels faisant intervenir à la fois le 
potentiel V(x) dans lequel on place la particule (cas des multiplications 
simples) et le hamiltonien de la particule libre (H_free = p^2/2m).

Tout ceci est extrêmement bien expliqué dans le tutorial 5 du MOOC à suivre 
sur la page https://www.coursera.org/course/smac

Bien sûr tout ceci est normalisé de sorte que hbar=1 et m=1

"""

import numpy as np               # Boîte à outils numériques
import scipy as sp               # Simple alias
import scipy.integrate           # Pour l'intégration (cumtrapz)
import matplotlib.pyplot as plt  # Boîte à outils graphiques
from matplotlib import animation # Pour l'animation progressive

def funct_potential(x):
    """ 
    Le potentiel dans lequel est plongé la particule. On fournit plusieurs 
    types de potentiel, il suffit de commenter/décommenter les zones 
    intéressantes pour changer selon les besoins.
    """
    # Potentiel de la boîte fermée:
    #if abs(x) > 3: return 1e150 # Presque l'infini...
    #else:  return 0.0
    #
    # Potentiel pour voir l'effet tunnel
    if x < -3: return 1e150
    elif 3 <= x <= 4: return 1.0
    else: return 0.0
    #
    # Potentiel pour un oscillateur harmonique
    #return x**2/9

steps = 500     # Echantillonnage en x et p
x_min,x_max = -5.0,30.0
affiche_xmin,affiche_xmax =-5,10 # On réduit l'affichage pour éviter les effets de bords
grid_x, dx = np.linspace(x_min, x_max, steps, retstep = True) # Grille des valeurs en x
p_max = 1/dx
p_min = -p_max
grid_p, dp = np.linspace(p_min, p_max, steps, retstep = True) # ainsi qu'en p
delta_t = 0.01  # Pas de temps
t = 0
nb_images = 10000


# Échantillonage du potentiel utilisé
potential = np.array([funct_potential(x) for x in grid_x])

# Définition de la fonction d'onde que l'on va faire évoluer temporellement 
# par la suite. Ici, on donne l'exemple d'une combinaison de deux états 
# propres du puit infini. (à changer si vous changer de potentiel...)

psi = np.sin(np.pi*(grid_x+3)/6) + np.sin(2*np.pi*(grid_x+3)/6)
psi[abs(grid_x)>3] = 0.0  # La fonction d'onde est nulle en dehors du puit infini
norm = ((np.abs(psi)**2).sum() * dx)
psi /= norm**0.5  # Normalisation (ne pas oublier la racine...)

def fourier_x_to_p(phi_x, dx):
    """ 
    Transformée de Fourier de la fonction d'onde psi(x) 
    Ne pas oublier de définir grid_x et grid_p "accordingly" et en variables globales.
    """
    phi_p = [(phi_x * np.exp(-1j * p * grid_x)).sum() * dx for p in grid_p]
    return np.array(phi_p)

def fourier_p_to_x(phi_p, dp):
    """ 
    Transformée de Fourier inverse de la fonction d'onde hat{psi}(p) dans le 
    domaine impulsionnel.    
    Ne pas oublier de définir grid_x et grid_p "accordingly" et en variables globales.
    """
    phi_x = [(phi_p * np.exp(1j * x * grid_p)).sum() for x in grid_x]
    return np.array(phi_x) /  (2.0 * np.pi)

def time_step_evolution(psi0, potential, grid_x, grid_p, dx, dp, delta_t):
    """ 
    Évolution temporelle proprement dite. On utilise l'approximation

    psi(t+dt) = exp(-i*dt*V(x)/2) * exp(-i*dt*H_free) * exp(-i*dt*V(x)/2) * psi(t)

    Voir tutorial 5 du MOOC https://www.coursera.org/course/smac pour le 
    détail des explications.
    """
    psi0 = np.exp(-1j * potential * delta_t / 2.0) * psi0  # Multiplication réelle
    psi0 = fourier_x_to_p(psi0, dx)                        # Passage dans le domaine impulsionnel
    psi0 = np.exp(-1j * grid_p**2 * delta_t / 2.0) * psi0  # Où H est simple ! (p^2/2m)
    psi0 = fourier_p_to_x(psi0, dp)                        # Repassage en coordonnées réelles
    psi0 = np.exp(-1j * potential * delta_t / 2.0) * psi0  # donc simple multiplication 
    norm = ((np.abs(psi0)**2).sum() * dx) # On renormalise (pour éviter les dérives?)
    psi0/= norm**0.5
    return psi0  # Renvoi de la fonction d'onde


# Définition de la figure (on fait deux "axes" de sorte à mettre deux échelles 
# graduées, une pour la fonction d'onde et l'autre pour le potentiel)

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()         # Making an evil twin :o)
#ax2 = ax1
# On dessine la fonction d'onde sur l'axe de gauche (ax1)
psi_line, = ax1.plot(grid_x, np.abs(psi)**2, 'g', linewidth = 2.0, label = '$|\psi(x)|^2$')
#ax1.set_xlim(-6, 6)
ax1.set_ylim(0, max(np.abs(psi)**2)*1.5)
plt.xlim((affiche_xmin,affiche_xmax))
ax1.set_xlabel('$x$', fontsize = 20)
ax1.set_ylabel('Densite de probabilite $|\psi|^2$')
ax1.legend(loc=2)
# En revanche, on fait le potentiel sur l'axe de droite (ax2)
ax2.plot(grid_x, potential, 'k', linewidth = 2.0, label = '$V(x)$')
ax2.set_ylabel('Potentiel')
ax2.set_ylim(0, max(np.abs(psi)**2)*1.5)
ax2.set_ylim(0,2)
plt.title('time = {}'.format(t))
plt.legend(loc=1)

def init():
    pass

def animate(i):
    global psi
    t = i*delta_t
    psi = time_step_evolution(psi, potential, grid_x, grid_p, dx, dp, delta_t)
    # Je n'arrive pas à comprendre pourquoi une fois sur deux on se récupère 
    # une facteur correctif de 3600... Ca ne semble pas dépendre du nombre de 
    # points d'échantillonnage, ni de l'extension de l'intervalle initial en 
    # x. Le problème est déjà présent sur les fichiers proposés par le MOOC de 
    # l'ENS, mais ils ont gentiment mis cela sous le tapis en ne prenant 
    # qu'une image sur 4...
    #if i%2 == 0: 
    #    psi_line.set_ydata(np.abs(psi)**2)
    #else:
    #    correction = 3*1e3*1.2
    #    correction = 1
    #    psi_line.set_ydata(np.abs(psi)**2*correction)
    # Trouvé !!! C'est la normalisation à qui il manquait une racine 
    # (forcément, on normalisait avec la somme des psi**2, il fallait bien 
    # prendre la racine...). Donc plus besoin de correction :o)
    psi_line.set_ydata(np.abs(psi)**2)
    plt.title('time = {}'.format(t))
    

# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=nb_images,interval=33)

plt.show()



