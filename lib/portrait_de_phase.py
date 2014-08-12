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
Module de génération automatique de portrait de phase et d'animations 
correspondantes..
"""

import matplotlib.pyplot as plt

def portrait_de_phase(x,vx,titre='Portrait de phase',
    xlabel='$x$',ylabel='$v_x$',file=None,position=True,
    xlim=None,ylim=None,fantome=None,color='k'):
    """
    Représentation de vx en fonction de x pour les différentes trajectoires 
    données en entrée (x et vx sont des tableaux de tableaux).
    Si 'file' est précisé, on enregistre dans le fichier correspond, sinon on 
    affiche à l'écran.
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
        if fantome and len(x) > fantome:
            plt.plot(xi,vi,color=ci,alpha=0.2)
            plt.plot(xi[-fantome:],vi[-fantome:],color=ci)
        else:
            plt.plot(xi,vi,color=ci)
    if position:
        for xi,vi,ci in zip(x,vx,color):
            plt.plot(xi[-1],vi[-1],'o',color=ci)
    if file: plt.savefig(file)
    else: plt.show()
    plt.clf()



