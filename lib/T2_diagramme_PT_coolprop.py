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
Fabrication simple d'un diagramme PT avec CoolProp. Malheureusement, on n'a 
accès qu'à la partie "fluide" du diagramme donc l'équilibre liquide/vapeur, 
mais c'est déjà pas mal.
"""

import matplotlib.pyplot as plt
from CoolProp.Plots import PropsPlot

fluid = 'Water'                  # Le fluide choisi (plus dans CoolProp.CoolProp.FluidsList())
pt_plot = PropsPlot(fluid, 'PT') # Le type de diagramme
plt.yscale('log')                # Échelle logarithmique en pression
pt_plot._draw_graph()            # Dessin du graphe obligatoire avant sauvegarde
plt.savefig('PNG/T2_diagramme_PT_coolprop_{}.png'.format(fluid))



