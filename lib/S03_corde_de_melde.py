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
successives se superposent.
"""

import numpy as np
import matplotlib.pyplot as plt
import film 

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
    plt.plot(x,corde(x,t,w,k,L,A))
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
    Écriture récursive de l'état de la corde
    """
    c = w/k
    u = w*t - k*x
    #print(u)
    gauche = A*np.sin(w*t)
    droite = 0.0
    resultat = A*f(u)
    for i in range(1,int(c*t/L)+1):
        if i%2 == 0: 
            resultat += gauche - A*f(u)
        else:        
            resultat += list(reversed(droite - A*f(u)))
        u -= k*L
    return resultat
    

def f(u): 
    res = np.sin(u)
    res[u<0] = 0.0
    return res    

#fait_corde(0)
#fait_corde(1)
#fait_corde(1.2)
#fait_corde(1.5)
#fait_corde(2)
#fait_corde(2.5)
#fait_corde(3)

corde_de_melde('PNG/S03_corde_de_melde_essai',L=np.pi,N=300,ylim=(-1,1),tmax=30)



