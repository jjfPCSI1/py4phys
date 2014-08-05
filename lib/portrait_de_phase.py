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

def portrait_de_phase(x,vx,titre='Portrait de phase',
    xlabel='$x$',ylabel='$v_x$',file=None,position=True,xlim=None,ylim=None):
    """
    Représentation de vx en fonction de x pour les différentes trajectoires 
    données en entrée (x et vx sont des tableaux de tableaux).
    Si 'file' est précisé, on enregistre dans le fichier correspond, sinon on 
    affiche à l'écran.
    Si 'position' est True, on affiche sous forme de rond le dernier point de 
    la trajectoire.
    Si 'xlim' ou 'ylim' sont spécifiés, ils définissent les bords du graphe. 
    Sinon, c'est matplotlib qui choisit tout seul.
    """



