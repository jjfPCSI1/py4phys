# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.



"""
Module de génération automatique de portrait de phase et d'animations 
correspondantes..
"""

import numpy as np
import matplotlib.pyplot as plt

def portrait_de_phase(x,vx,titre='Portrait de phase',
    xlabel='$x$',ylabel='$v_x$',file=None,position=True,
    xlim=None,ylim=None,fantome=None,color='k',clearfig=True):
    """
    Représentation de vx en fonction de x pour les différentes trajectoires 
    données en entrée (x et vx sont des tableaux de tableaux).
    Si 'file' est précisé, on enregistre dans le fichier correspond, sinon on 
    affiche à l'écran.
    Si 'clearfig' est à False et que 'file' n'est pas précisé, il n'y aura ni 
    savefig, ni show, ni clf, donc la routine pourra servir pour écrire dans 
    des sous-figures définies à l'extérieur de la routine.
    Si 'position' est True, on affiche sous forme de rond le dernier point de 
    la trajectoire.
    Si 'xlim' ou 'ylim' sont spécifiés, ils définissent les bords du graphe. 
    Sinon, c'est matplotlib qui choisit tout seul.
    On peut actionner le mode "fantome" qui laisse en traits pleins le nombre 
    de points signalés (par exemple fantome=10 laissera 10 points) et mettra 
    en "grisé" les points précédents.
    'color' peut être soit directement une chaîne décrivant la couleur, soit 
    une liste de couleurs de la même taille que x et vx (chaque trajectoire 
    étant bien sûr associée à la couleur correspondante).
    """
    plt.title(titre)
    if xlim: plt.xlim(xlim)
    if ylim: plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if list(color) != color: color = [color]*len(x)
    for xi,vi,ci in zip(x,vx,color):
        if fantome and len(xi) > fantome:
            plot_avec_discontinuite(xi,vi,color=ci,alpha=0.2)
            plot_avec_discontinuite(xi[-fantome:],vi[-fantome:],color=ci)
        else:
            plot_avec_discontinuite(xi,vi,color=ci)
    if position:
        for xi,vi,ci in zip(x,vx,color):
            plt.plot(xi[-1],vi[-1],'o',color=ci)
    if file or clearfig: 
        if file: plt.savefig(file)
        else: plt.show()
        plt.clf()

def plot_avec_discontinuite(x,v,**kargs):
    disc = cherche_discontinuite(x)
    for i in range(len(disc)-1):
        plt.plot(x[disc[i]:disc[i+1]],v[disc[i]:disc[i+1]],**kargs)

def cherche_discontinuite(x,limite=2):
    disc = [0]
    for i in range(1,len(x)):
        if abs(x[i]-x[i-1]) > limite: disc.append(i)
    disc.append(len(x))
    return disc

def diagramme_energetique(x,vx,Ep,titre='Diagramme energetique',
    xlabel='$x$',ylabel='$E_p$',file=None,position=True,
    xlim=None,ylim=None,fantome=None,color='k',clearfig=True):
    """
    Représentation de l'énergie potentielle en fonction de x pour les 
    différentes trajectoires données en entrée (x et vx sont des tableaux de 
    tableaux). Ep doit être une fonction de variables x,vx et qui gère 
    correctement les appels sur des np.array.
    Si 'file' est précisé, on enregistre dans le fichier correspond, sinon on 
    affiche à l'écran.
    Si 'clearfig' est à False et que 'file' n'est pas précisé, il n'y aura ni 
    savefig, ni show, ni clf, donc la routine pourra servir pour écrire dans 
    des sous-figures définies à l'extérieur de la routine.
    Si 'position' est True, on affiche sous forme de rond le dernier point de 
    la trajectoire.
    Si 'xlim' ou 'ylim' sont spécifiés, ils définissent les bords du graphe. 
    Sinon, c'est matplotlib qui choisit tout seul.
    On peut actionner le mode "fantome" qui laisse en traits pleins le nombre 
    de points signalés (par exemple fantome=10 laissera 10 points) et mettra 
    en "grisé" les points précédents.
    'color' peut être soit directement une chaîne décrivant la couleur, soit 
    une liste de couleurs de la même taille que x et vx (chaque trajectoire 
    étant bien sûr associée à la couleur correspondante).
    """
    plt.title(titre)
    if xlim: plt.xlim(xlim)
    if ylim: plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if list(color) != color: color = [color]*len(x)
    if xlim: 
        xmin,xmax = xlim
    else:
        xmin = np.min(x)
        xmax = np.max(x)
    X = np.linspace(xmin,xmax,500)
    plt.plot(X,Ep(X,0),'k',linewidth=2)
    for xi,vi,ci in zip(x,vx,color):
        Epi = Ep(xi,vi)
        if fantome and len(xi) > fantome:
            plot_avec_discontinuite(xi,Epi,color=ci,alpha=0.2)
            plot_avec_discontinuite(xi[-fantome:],Epi[-fantome:],color=ci)
        else:
            plot_avec_discontinuite(xi,Epi,color=ci)
    if position:
        for xi,vi,ci in zip(x,vx,color):
            Epi = Ep(xi,vi)
            plt.plot(xi[-1],Epi[-1],'o',color=ci)
    if file or clearfig: 
        if file: plt.savefig(file)
        else: plt.show()
        plt.clf()
    



