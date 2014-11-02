# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




import numpy as np               # Boîtes
import scipy as sp               # à outils
import scipy.integrate           # numériques
import matplotlib.pyplot as plt  # Boîte à outil graphique
# Pour le tracé des portraits de phase et les diagrammes énergétiques
from portrait_de_phase import portrait_de_phase,diagramme_energetique

tmax = 10                        # Temps d'intégration
nb_points = 500                  # Nombre d'instant échantillonnés
th0  = np.arange(-0.15,0.151,0.01)# Positions angulaires initiales
thp0 = np.array([0]*len(th0))    # Vitesses angulaires initiales
g,m,ell = 9.81,1,1               # Quelques constantes

# Pour avoir des couleurs qui changent et se correspondent
colors = ["blue","red","green","magenta","cyan","yellow",
          "darkblue","darkred","darkgreen","darkmagenta","darkcyan"]*10

def Em(th,thp):                  # Energie mécanique du pendule simple
    return m*g*ell*(1-np.cos(th)) +  0.5*m*(ell*thp)**2

def pendule(y,t):                # Equations d'évolution du pendule simple
    th,thp = y
    return [thp,-g/ell * np.sin(th)]

t = np.linspace(0,tmax,nb_points)# Echantillonnage en temps
th,thp = [],[]                   # Initialisation
for thi,thpi in zip(th0,thp0):   # On itère sur les conditions initiales
    sol = sp.integrate.odeint(pendule,[thi,thpi],t) # Intégration
    th.append(sol[:,0])          # Ajout des positions
    thp.append(sol[:,1])         # et vitesses correspondantes

fig = plt.figure(figsize=(10,10))# Création de la figure

th_lim = (np.min(th),np.max(th)) # Limites en theta
thp_lim=(np.min(thp),np.max(thp))# Limites en theta point
base_name='PNG/M4_pendule_simple_portrait_de_phase_zoom'

for i,ti in enumerate(t):        # Affichage progressif
    print(ti)                    # Un peu de feed back
    thi = [th_p[:i+1] for th_p in th]    # On ne prend que jusqu'à
    thpi= [thp_p[:i+1] for thp_p in thp] # l'instant présent
    plt.suptitle('Pendule simple, $t={}$'.format(round(ti,2)))
    plt.subplot(2,1,1)           # Sous-figure du haut
    portrait_de_phase(thi,thpi,fantome=20,clearfig=False,
                      color=colors,xlim=th_lim,ylim=thp_lim)
    plt.xlabel('')
    plt.subplot(2,1,2)           # Sous-figure du bas
    diagramme_energetique(thi,thpi,Em,color=colors,clearfig=False,fantome=20,xlim=th_lim)
    plt.savefig('{}_{:04d}.png'.format(base_name,i))
    plt.clf()                    # Nettoyage

from film import make_film       # Boîte à outil pour faire un film

make_film(base_name)             # et appel effectif



