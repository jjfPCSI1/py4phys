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
    t = np.linspace(0,tmax,N)
    for i,ti in enumerate(t):
        print(ti)
        fichier = base_name + '{:04d}'.format(i)
        fait_corde(ti,file=fichier,w=w,k=k,L=L,A=A,ylim=ylim)
    film.make_film(base_name)

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
    c = w/k
    u = w*t - k*x
    u0= w*t
    #print(u)
    gauche = A*f(w*t,u0)
    droite = 0.0
    gauche = 0.0
    resultat = A*f(u,u0)*be_positive(u)
    plt.plot(x,resultat)
    for i in range(1,int(c*t/L)+1):
        u -= k*L
        if i%2 == 0: 
            addition = (gauche + A*f(u,u0))*be_positive(u)
        else:        
            addition = list(reversed((droite - A*f(u,u0))*be_positive(u)))
        plt.plot(x,addition)
        resultat += addition
    return resultat

def be_positive(u):
    res = np.ones(u.shape)
    res[u<0] = 0.0
    return res    

def f(u,u0): 
#    if u0 == 0: return 0.0
#    return np.sin(u)*u/u0
    return np.sin(u)/(1 + u0-u)**0.3
#    res = np.sin(u)
#    res[u<0] = 0.0
#    return res    

#fait_corde(0)
#fait_corde(1)
#fait_corde(1.2)
#fait_corde(1.5)
#fait_corde(2)
#fait_corde(2.5)
#fait_corde(3)

L=10

lambda1 = 2*L/(3)
lambda2 = 2*L/(3+0.5)

corde_de_melde('PNG/S03_corde_de_melde_amplif',
               L=L,k=2*np.pi/lambda1,N=1500,ylim=(-1,1),tmax=150)
corde_de_melde('PNG/S03_corde_de_melde_non_amplif',
               L=L,k=2*np.pi/lambda2,N=1500,ylim=(-1,1),tmax=150)



