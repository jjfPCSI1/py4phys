# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.



"""
Simulation d'un corde de Melde. Le but est de visualiser comment une onde de 
faible amplitude au départ peut s'amplifier à mes que se réflexions 
successives se superposent. On introduit une atténuation arbitraire de l'onde 
pour forcer la convergence.
"""

import numpy as np              # Boîte à outils numériques
import matplotlib.pyplot as plt # Boîte à outils graphiques
import film                     # Boîte à outils vidéos

def corde_de_melde(base_name,w=1,k=1,L=1,A=0.1,tmax=10,N=1000,ylim=None):
    """ 
    Produit un film (base_name + '_film.mpeg') d'une corde de Melde de 
    longueur L, fixée à droite et excitée à gauche par un moteur de pulsation 
    w imposant la propagation d'une onde d'amplitude de nombre d'onde k en 
    observant les réflexions régulière de l'onde jusqu'au temps tmax sur un 
    total de N images. Si ylim est précisé, il contiendra les limites 
    verticales, sinon c'est matplotlib qui décidera, ce qui déclenchera une 
    adaptation progressive de l'amplitude.
    """
    t = np.linspace(0,tmax,N)  # Échantillonnage en temps
    for i,ti in enumerate(t):  # On les prends l'un après l'autre
        print(ti)              # Un peu de feedback
        fichier = base_name + '{:04d}'.format(i) # Nom du fichier
        fait_corde(ti,file=fichier,w=w,k=k,L=L,A=A,ylim=ylim) # Dessin de la corde
    film.make_film(base_name)  # Fabrication du film à la fin

def fait_corde(t,file=None,w=1,k=1,L=1,A=0.1,ylim=None,nb_points=400):
    """ 
    Dessine effectivement la corde de Melde à l'instant t.
    Si 'file' n'est pas renseigné, on l'affiche à l'écran.
    """
    x = np.linspace(0,L,nb_points)
    plt.plot(x,corde(x,t,w,k,L,A),'k',linewidth=2.0)
    if ylim: plt.ylim(ylim)
    plt.title('Corde de Melde, $t={}$'.format(t))
    plt.xlabel('x')
    if file:
        plt.savefig(file)
        plt.clf()
    else: 
        plt.show()

def corde(x,t,w,k,L,A):
    """ 
    Calcul itératif de l'état de la corde
    """
    c = w/k                              # Vitesse de l'onde
    u = w*t - k*x                        # Phase courante
    u0= w*t                              # Phase maximale
    resultat = A*f(u,u0)*be_positive(u)  # On commence par l'onde primordiale
    plt.plot(x,resultat,alpha=0.4)       # que l'on représente en sus
    for i in range(1,int(c*t/L)+1):      # Puis, on va "déplier la corde"
        u -= k*L                         # On l'a déjà parcourue une fois
        if i%2 == 0:                     # Si on cogne à gauche
            addition = A*f(u,u0)*be_positive(u) # propagation vers la droite
        else:                            # Sinon, il faut inverser (vers la gauche)
            addition = list(reversed(- A*f(u,u0)*be_positive(u)))
        plt.plot(x,addition,alpha=0.4)   # On représente l'onde après i réflexions
        resultat += addition             # et on ajoute au total
    return resultat                      # que l'on renvoie.

def be_positive(u):
    """Fonction qui vaut 1 quand la phase est positive et zéro sinon."""
    res = np.ones(u.shape)
    res[u<0] = 0.0
    return res    

def f(u,u0):
    """Fonction correspondant à l'onde proprement dite avec une atténuation 
    (un peu) arbitraire pour améliorer la convergence."""
    return np.sin(u)/(1 + u0-u)**0.3

L=10                     # Longueur totale de la corde

lambda1 = 2*L/(3)        # Résonance:      L = n * lambda/2
lambda2 = 2*L/(3+0.5)    # Anti-résonance: L = (n+1/2) * lambda/2

# Appel aux fonctions qui font effectivement les films.
corde_de_melde('PNG/S03_corde_de_melde_amplif',
               L=L,k=2*np.pi/lambda1,N=1500,ylim=(-1,1),tmax=150)
corde_de_melde('PNG/S03_corde_de_melde_non_amplif',
               L=L,k=2*np.pi/lambda2,N=1500,ylim=(-1,1),tmax=150)



