# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




""" 
Suite à une question de Jean-Marie Biansan sur le forum UPS, voici la version 
de la résolution du pont de Wien utilisant sp.integrate.odeint plutôt qu'une 
intégration manuelle comme proposé par Simon Laurette.
"""


from math import *              # Outils mathematiques
import numpy as np              # Outils numeriques
import scipy as sp              # Outils scientifiques
import scipy.integrate          # pour l'integration
import matplotlib.pyplot as plt # Outils graphiques

R=1e3                           # Resistance du Pont de Wien
C=100e-9                        # Capacite du Pont de Wien
K=3.2                           # Gain de l'etage d'amplification
tfin=15e-3                      # instant final de la simulation
dt=0.01e-3                      # pas
vsat=15                         # tension de saturation de l'AO

e0   = 0.01 # entree de l'etage d'amplitication ; 0.01 simule le bruit
dedt0= 0.01 # derivee de e ; 0.01 simule le bruit en entree

def f(y,t):
    e,dedt = y
    if abs(e) < vsat/K:         # Cas non sature
       return [dedt, (K-3)/(R*C)*dedt - e/(R*C)**2]
    else:                       # Cas sature
       return [dedt, ( -3)/(R*C)*dedt - e/(R*C)**2]

# Determination de l'entree de l'etage d'amplification
t   = np.linspace(0,tfin,int(tfin/dt))
sol = sp.integrate.odeint(f,[e0,dedt0],t)
e   = sol[:,0]
dedt= sol[:,1]

# Pour la sortie, on utilise np.where pour ecreter là où e est trop grand
s = np.where(abs(e)>vsat/K,vsat*np.sign(e),e*K)

# Traces des courbes
plt.figure(0,figsize=(14,8))
plt.subplot(2,2,1)     # Figure du haut à gauche
plt.plot(t,s)          # La sortie de l'AO
plt.title("Demarrage des oscillations")
plt.xlabel("$t$ (s)")
plt.ylabel("$s$ (V)")
plt.ylim(-16,16)       # Pour bien voir l'ecretage
plt.subplot(2,2,3)     # Figure du bas à gauche
plt.plot(t,e)          # L'entree
plt.xlabel("$t$ (s)")
plt.ylabel("$e$ (V)")
plt.subplot2grid((2,2),(0,1),rowspan=2) # Figure de droite
plt.plot(e,dedt)       # Le portrait de phase
plt.xlabel("$e$ (V)")
plt.ylabel("d$e$/d$t$ (V/s)")
plt.title('Portrait de phase')
plt.tight_layout()   # Pour ajuster les espaces autour des sous-figures
plt.savefig('PNG/PSI_pont_de_wien_odeint.png')



