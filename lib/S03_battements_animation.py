# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




'''
Simple illustration de la notion de battements par superposition de deux ondes 
sinusoïdales de pulsation proches.

Version avec animation de ce que propose le fichier S03_battements.py
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation # Pour l'animation progressive

t  = np.linspace(0,10,1000)    # Echantillonnage en temps
w1 = 25                        # La pulsation du premier signal
w2 = w1*1.07                   # La pulsation du second  signal
S1 = 1.0*np.cos(w1*t)          # Le premier signal proprement dit
S2 = np.cos(w2*t)              # Le second  signal proprement dit
S3 = S1+S2                     # La somme des deux

oscillateurs = [S1,S2,S3]

fig = plt.figure(figsize=(18,8)) 

plt.subplot(211)                   # La figure du dessus contient
plt.title('Illustration de la notion de battements')
l1,=plt.plot(t,S1)                 # le premier signal et
l2,=plt.plot(t,S2)                 # le second  signal.
plt.ylabel('Deux cosinus')
plt.subplot(212)                   # La figure du dessous
l3,=plt.plot(t,S3)                 # contient leur somme
plt.ylabel('et leur somme')
plt.xlabel('Temps')            


lignes = [l1,l2,l3]

def init():
    for l in lignes:
        l.set_xdata([])
        l.set_ydata([])
    
def animate(i):
    for l,x in zip(lignes,oscillateurs):
        l.set_ydata(x[:i])
        l.set_xdata(t[:i])

anim = animation.FuncAnimation(fig,animate,len(t),interval=20,init_func=init,blit=False)

plt.show()

#plt.savefig('PNG/S03_battements.png')



