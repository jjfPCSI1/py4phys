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




""" Implémentation proposée par Miriam Heckmann, PCSI3, Lycée Kléber """

import numpy as np               # Pour la fonction linspace, zeros et la trigo
import matplotlib.pyplot as plt  # Boîte à outils graphiques

def paquet_d_onde(N):
    """Construction d'un paquet d'onde à N ondes"""
    nb_points=1000                   # Le nombre de points d'échantillonage
    x=np.linspace(-100,100,nb_points)# Échantillonnage en position
    y=np.zeros(nb_points)            # Création d'une liste de zéros 

    for i in range(N):
        y += (1-i/N)*np.sin(np.pi*x/(2+i/100))+(1-i/N)*np.sin(np.pi*x/(2-i/100))
    plt.plot(x,y)
    plt.title("Paquet d'onde pour $N={}$".format(N))
    plt.savefig('PNG/S06_paquet_d_ondes_MQ_N{:03d}.png'.format(N))
    plt.clf()

paquet_d_onde(10)
paquet_d_onde(50)



