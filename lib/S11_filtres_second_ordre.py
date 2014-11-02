# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




'''
Exemple de génération de filtres du second ordre (ici pour une question de 
cours [QDC pour les intimes]).
'''

import numpy as np                       # Pour np.logspace
from bode import diag_bode, second_ordre # Pour les diagrammes

f100 = np.logspace(1,4,num=1000)         # Echantillonnage en f pour Q=100
f0p1 = np.logspace(0,6,num=200)          # Pareil pour Q=0.1

# Deux passe-bas, puis deux passe-hauts et enfin deux passe-bandes
second_ordre(10**3, 100,'PNG/S11_filtres_QDC_PBs_Q100.png',f=f100)
second_ordre(10**3,1/10,'PNG/S11_filtres_QDC_PBs_Q0_1.png',f=f0p1)
second_ordre(10**3, 100,'PNG/S11_filtres_QDC_PHt_Q100.png',f=f100,type='PHt')
second_ordre(10**3,1/10,'PNG/S11_filtres_QDC_PHt_Q0_1.png',f=f0p1,type='PHt')
second_ordre(10**3, 100,'PNG/S11_filtres_QDC_PBd_Q100.png',f=f100,type='PBd')
second_ordre(10**3,1/10,'PNG/S11_filtres_QDC_PBd_Q0_1.png',f=f0p1,type='PBd')



