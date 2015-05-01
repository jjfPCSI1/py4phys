# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




""" 
Programme permettant de visualiser l'effet de l'intégration par méthode de 
Verlet (aussi appelée leap-frog dans une formulation légèrement différente 
mais équivalente) sur le problème pythagoricien où trois masses (m=3,4 et 5) 
sont placées au repos aux sommets d'un triangle pythagoricien, chaque masse à 
l'opposé du côté dont la longueur lui correspond (voir 
http://articles.adsabs.harvard.edu/cgi-bin/nph-iarticle_query?1967AJ.....72..876S&amp;data_type=PDF_HIGH&amp;whole_paper=YES&amp;type=PRINTER&amp;filetype=.pdf 
"Complete solution of a general problem of three bodies" par Szebehely et 
Peters, 1967 )

L'idée est principalement de vérifier que mon implémentation du schéma 
d'intégration proposé dans le sujet d'informatique commune Centrale 2015 tient 
à peu près la route.
"""

# Les paramètres principaux de la simulation
m = [3.0,4.0,5.0]  # Les masses des trois points
v0= [[0,0,0] for i in range(3)]    # Les particules sont au repos
p0= [[1.0,3,0], [-2,-1,0], [1,-1,0]] # Les trois sommets du triangle
deltat = 0.0001        # Le pas de temps
mult = int(0.01/deltat+1)
tmax = 17           # Le temps total
n = int(tmax/deltat)# Le nombre total de pas
tfantome = 1
ifantome = int(tfantome/deltat)

# D'abord quelques fonctions pour faire "comme si" les listes étaient en fait 
# des vecteurs.

def smul(nombre,liste):
    """ Multiplication d'un vecteur par un scalaire. """
    L = []                       # Initialisation à une liste vide
    for element in liste:        # On itère sur les éléments
        L.append(nombre*element) # On rajoute la valeur idoine
    return L                     # On n'oublie pas de renvoyer le résultat

def vsom(L1,L2):
    """ Fais l'addition vectorielle L1+L2 de deux listes. """
    L = [0] * len(L1)        # Inialisation à une liste de 0
    for i in range(len(L1)): # On regarde toutes les positions
        L[i] = L1[i] + L2[i] # Addition
    return L 

def vdif(L1,L2):
    """ Fait la différence vectorielle L1-L2 de deux listes. """
    L = []                      # Initialisation à une liste vide
    for i in range(len(L1)):    # On regarde toutes les positions
        L.append(L1[i] - L2[i]) # Rajout de la soustraction
    return L 

def norme(v):
    """ Calcule la norme euclidienne d'un vecteur dont on donne ses
    composantes dans une base orthonormée. """
    norme2 = 0                   # Initialisation de la norme carrée
    for i in range(len(v)):      # On passe toutes les composantes
        norme2 = norme2 + v[i]**2# Ajout du carré de la composante
    return norme2**0.5           # Le résultat est la racine carrée de la somme


# La partie physique à présent. On commence par le calcul des forces    

def force2(m1,p1,m2,p2):
    """ Renvoie une liste représentative de la force exercée par la particule 
    2 sur la particule 1. """
    P1P2 = vdif(p2,p1)           # Le vecteur P1P2
    G = 6.67e-11                 # Constante universelle de gravitation
    G = 1
    a = G*m1*m2 / norme(P1P2)**3 # Constante multiplicative devant le vecteur
    return smul(a,P1P2)          # Renvoie du vecteur a*P1P2

def forceN(j,m,pos):
    """ Force gravitationnelle totale exercée par toutes les particules sur la 
    particule j. """
    force = smul(0,pos[j])  # Initialisation au vecteur nul de bonne taille
    for k in range(len(m)): # On passe toutes les particules en revue
        if k != j:          # Si on n'est pas sur la particule concernée
            f_k_sur_j = force2(m[j],pos[j],m[k],pos[k]) # Force individuelle
            force = vsom(force,f_k_sur_j) # et ajout à la force totale
    return force            # Renvoi de la force total après sommation

# Puis l'utilisation de l'intégrateur pour calculer la position suivante de 
# chaque particule.

def pos_suiv(m,pos,vit,h):
    """ Version où l'on parcourt manuellement les trois dimensions d'espace. 
    Attention, l'accélération vaut la force divisée par la masse (on aurait 
    mieux fait de calculer les accélérations directement pour économiser 
    quelques calculs...). """
    L = []                   # Initialisation des nouvelles positions
    for j in range(len(m)):  # On parcourt les particules une à une
        mj,pj,vj = m[j], pos[j], vit[j]  # Des raccourcis pour la lisibilité
        force = forceN(j,m,pos)          # Vecteur force totale sur j
        next = smul(0,pj)                # Initialisation nouvelle position pour j
        for k in range(len(pj)):         # Boucle sur les dimensions d'espace
            next[k] = pj[k] + vj[k]*h + h**2/2 * force[k]/mj  # et Verlet
        L.append(next)       # Ajout du résultat à la liste
    return L                 # et renvoi final une fois complètement remplie

# dont on a besoin pour déterminer la vitesse et donc l'ensemble de l'état 
# suivant du système

def etat_suiv(m,pos,vit,h):
    """ Calcul de l'état suivant (position et vitesse) pour toutes les 
    particules connaissant ces valeurs à la date t_i. """
    new_pos = pos_suiv(m,pos,vit,h) # On calcule tout de suite les nouvelles positions
    new_vit = []                    # Liste vide pour les nouvelles vitesses
    for j in range(len(m)):         # Les particules, une à une
        mj,vj= m[j],vit[j]          # Raccourcis
        fi   = smul(1/mj,forceN(j,m,pos))     # Accélération à t_i
        fip1 = smul(1/mj,forceN(j,m,new_pos)) # Accélération à t_{i+1}
        next_vj = smul(0,vj)        # Initialisation à la vitesse nulle pour la taille
        for k in range(len(vj)):    # Boucle sur les dimensions d'espace
            next_vj[k] = vj[k] + h/2 * (fi[k] + fip1[k]) # Application de Verlet
        new_vit.append(next_vj)     # Ajout à la liste des vitesses
    return new_pos,new_vit          # Renvoi des nouvelles positions et nouvelles vitesses


def simulation_verlet(deltat,n):
    """ Simulation globale avec un pas de temps deltat (il a fini par 
    sortir du bois :o) et un nombre n de pas de temps à effectuer."""
#    pos = smul(1.5e11,p0)  # Conversion des UA en m   
#    vit = smul(1e3,v0)     # Conversion des km/s en m/s
    pos = p0
    vit = v0
    liste_positions = [pos]# Initialisation de la liste à renvoyer
    for i in range(n):     # Autant de fois que demandé,
        if i%1000 == 0: print(i) # Un peu de feedback
        pos,vit = etat_suiv(m,pos,vit,deltat)      # on détermine l'état suivant
#        liste_positions.append(smul(1/1.5e11,pos)) # Ajout avec conversion inverse
        liste_positions.append(pos) # Ajout (sans conversion inverse)
    return liste_positions

# Maintenant, on va quand même utiliser les facilités de Numpy pour effectuer le calcul 

import numpy as np

positions = np.array(simulation_verlet(deltat,n))

# Et à présent, les animations proprement dites

import matplotlib.pyplot as plt
from matplotlib import animation # Pour l'animation progressive

fig = plt.figure(figsize=(10,10))
ax = fig.gca()
plt.title("Evolution jusqu'a $t={}$".format(tmax))

plt.xlim((-3,3))
plt.ylim((-3,3))

lignes = []

#print(positions[:,0,0])

for i in range(len(m)):
    ligne, = plt.plot(positions[:,i,0],positions[:,i,1])
    lignes.append(ligne)

plt.savefig('PNG/M_schema_de_verlet_total.png')

#plt.show()

def init():
    for l in lignes:
        l.set_xdata([])
        l.set_ydata([])

def animate(i):
    ax.set_title('$t={}$'.format(round(mult*i*deltat,1)))
    for j in range(len(lignes)):
        l = lignes[j]
        if mult*i < ifantome:
            pos = positions[:mult*i,j,:]
        else: pos = positions[mult*i-ifantome:mult*i,j,:]
        l.set_ydata(pos[:,1])
        l.set_xdata(pos[:,0])

# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=int(n/mult),interval=20)

anim.save('PNG/M_schema_de_verlet.mp4', fps=30)

plt.show()




