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

tmax = 20                        # Temps d'intégration
nb_points = 1000                 # Nombre d'instant échantillonnés
thp0 = np.arange(-8,8.1,0.3)     # Vitesses angulaires initiales
th0  = np.array([0]*len(thp0))   # Positions angulaires initiales
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
    theta = sol[:,0]%(6*np.pi)   # Conditions limites périodiques sur 6pi
    theta[theta > 3*np.pi] = theta[theta > 3*np.pi] - 6*np.pi
    th.append(theta)             # Ajout des positions
    thp.append(sol[:,1])         # et vitesses correspondantes

fig = plt.figure(figsize=(10,10))# Création de la figure

th_lim = (np.min(th),np.max(th)) # Limites en theta
base_name='PNG/M4_pendule_simple_portrait_de_phase_6pi'

for i,ti in enumerate(t):        # Affichage progressif
    print(ti)                    # Un peu de feed back
    thi = [th_p[:i+1] for th_p in th]    # On ne prend que jusqu'à
    thpi= [thp_p[:i+1] for thp_p in thp] # l'instant présent
    plt.suptitle('Pendule simple, $t={}$'.format(round(ti,2)))
    plt.subplot(2,1,1)           # Sous-figure du haut
    portrait_de_phase(thi,thpi,fantome=20,clearfig=False,color=colors,xlim=th_lim)
    plt.xlabel('')
    plt.subplot(2,1,2)           # Sous-figure du bas
    diagramme_energetique(thi,thpi,Em,color=colors,clearfig=False,fantome=20,xlim=th_lim)
    plt.savefig('{}_{:04d}.png'.format(base_name,i))
    plt.clf()                    # Nettoyage

from film import make_film       # Boîte à outil pour faire un film

make_film(base_name)             # et appel effectif





# On peut aussi regarder juste sur juste 2pi d'intervalle, avec les mêmes 
# résultats

for theta in th: # On sait que theta est déjà entre -3pi et 3pi
    theta[theta> np.pi] = theta[theta> np.pi] - 2*np.pi
    theta[theta<-np.pi] = theta[theta<-np.pi] + 2*np.pi

fig = plt.figure(figsize=(10,10))# Définition de la figure

th_lim = (np.min(th),np.max(th)) # Nouvelles limites en theta
base_name='PNG/M4_pendule_simple_portrait_de_phase_2pi'

for i,ti in enumerate(t):        # On regarde à chaque instant
    print(ti)                    # Un peu de feedback
    thi = [th_p[:i+1] for th_p in th]    # On se concentre uniquement sur les
    thpi= [thp_p[:i+1] for thp_p in thp] # valeurs jusqu'à l'instant choisit
    plt.suptitle('Pendule simple, $t={}$'.format(round(ti,2)))
    plt.subplot(2,1,1)           # Première sous-figure
    portrait_de_phase(thi,thpi,fantome=20,clearfig=False,color=colors,xlim=th_lim)
    plt.xlabel('')
    plt.subplot(2,1,2)           # Deuxième sous-figure
    diagramme_energetique(thi,thpi,Em,color=colors,clearfig=False,fantome=20,xlim=th_lim)
    plt.savefig('{}_{:04d}.png'.format(base_name,i))
    plt.clf()                    # Nettoyage après sauvegarde

make_film(base_name)             # Fabrication du film à partir des png







# Voyons ce qui se passe quand on rajoute un peu d'amortissement

alpha = 0.1                      # Constante de frottement

def pendule(y,t):                # Les nouvelles équations d'évolution
    th,thp = y                   # en rajoutant le terme linéaire 
    return [thp,-g/ell * np.sin(th) - alpha*thp]       # en vitesse

t = np.linspace(0,tmax,nb_points)# Échantillonnage en temps
th,thp = [],[]                   # Initialisation
for thi,thpi in zip(th0,thp0):   # Calculs pour toutes les conditions initiales
    sol = sp.integrate.odeint(pendule,[thi,thpi],t)
    theta = sol[:,0]%(6*np.pi)
    theta[theta > 3*np.pi] = theta[theta > 3*np.pi] - 6*np.pi
    th.append(theta)
    thp.append(sol[:,1])

fig = plt.figure(figsize=(10,10))# Crétion de la figure

th_lim = (np.min(th),np.max(th)) # Limites en theta
base_name='PNG/M4_pendule_simple_portrait_de_phase_6pi_amorti'

for i,ti in enumerate(t):        # Et c'est reparti pour chaque instant
    print(ti)                    # échantillonné
    thi = [th_p[:i+1] for th_p in th]    # On ne garde que les valeurs
    thpi= [thp_p[:i+1] for thp_p in thp] # jusqu'à l'instant choisi
    plt.suptitle('Pendule simple, $t={}$'.format(round(ti,2)))
    plt.subplot(2,1,1)           # Première sous-figure
    portrait_de_phase(thi,thpi,fantome=20,clearfig=False,color=colors,xlim=th_lim)
    plt.xlabel('')
    plt.subplot(2,1,2)           # Seconde sous-figure
    diagramme_energetique(thi,thpi,Em,color=colors,clearfig=False,fantome=20,xlim=th_lim)
    plt.savefig('{}_{:04d}.png'.format(base_name,i))
    plt.clf()                    # Nettoyage après sauvegarde

make_film(base_name)             # Fabrication du fil correspondant



