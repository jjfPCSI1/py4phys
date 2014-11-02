# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




''' 
Illustration numérique de la conservation de l'énergie mécanique pour 
une équation d'oscillateur harmonique.
'''

import numpy as np                 # Pour np.linspace
import scipy as sp                 # Simple alias usuel
import scipy.integrate             # Pour l'intégration
import matplotlib.pyplot as plt    # Pour les dessins

m = 1                              # Masse du mobile
k = 1                              # Constante de raideur du ressort
omega0 = (k/m)**0.5                # On définit la pulsation propre

def equadiff(y,t):
    '''Renvoie l'action du système dx/dt = vx et dvx/dt = -omega0**2 * x 
    soit bien l'oscillateur harmonique x'' + omega0**2 * x = 0'''
    x,vx = y                        # y contient position et vitesse
    return [vx,- omega0**2 * x]     # On renvoie un doublet pour [dx/dt,dvx/dt]

nb_CI = 2 # Nombre de conditions initiales explorées

t = np.linspace(0,10,1000)          # Le temps total d'intégration
x0= np.linspace(5,1,nb_CI)          # Les positions initiales choisies
v0= np.linspace(0,3,nb_CI)          # Les vitesses  initiales choisies
    
for i in range(nb_CI):              # Pour chaque condition initiale
    # L'intégration proprement dite
    sol = sp.integrate.odeint(equadiff,[x0[i],v0[i]],t)
    x = sol[:,0]                    # Récupération de la position
    v = sol[:,1]                    # et de la vitesse
    Ec = 0.5*m*v**2                 # Energie cinétique
    Ep = 0.5*k*x**2                 # Energie potentielle
    Em = Ec + Ep                    # Energie mécanique
    lab = ' pour x0={} et v0={}'.format(round(x0[i],1),round(v0[i],1))
    plt.plot(t,Ec,label='$E_c$'+lab)# Affichage Ec
    plt.plot(t,Ep,label='$E_p$'+lab)# Affichage Ep
    plt.plot(t,Em,label='$E_m$'+lab)# Affichage Em

# Il ne reste que le traitement cosmétique

plt.title('Oscillateur harmonique pour differentes amplitudes initiales')
plt.ylabel('Energie (unite arbitraire)')
plt.xlabel('Temps (unite arbitraire)')
plt.legend()
plt.savefig('PNG/S01_oscillateur_harmonique_energie.png')



