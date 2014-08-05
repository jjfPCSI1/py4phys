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



'''
Un filtre "bizarre" dont il faut trouver la fonction de transfert sachant 
qu'il est du premier ordre.
'''

from scipy import signal # Pour lti et bode
import numpy as np       # Pour l'échantillonnage

num = [0.001,10.1]       # Numérateur   (-> 0.001*jw + 10.1)
den = [0.0101,1]         # Dénominateur (-> 0.0101*jw + 1  )


# Extraction des données
f = np.logspace(0,6,num=200)
s1 = signal.lti(num,den)
f, GdB, phase = signal.bode(s1,f)

# Et préparation du diagramme
from bode import diag_bode
diag_bode(f,GdB,phase,'PNG/S11_filtre_bizarre.png')


