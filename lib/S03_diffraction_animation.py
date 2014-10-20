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
Simulation d'un phénomène de diffraction par une ouverture rectangulaire après 
arrivée d'une onde plane inclinée d'un certain angle theta0 par rapport à la 
normale.

Le graphe du bas représente la coupe en intensité (amplitude au carré) sur un 
écran situé à y fixé.

Version avec animation pour montrer l'effet de modifications de paramètres 
comme la largeur de la fente ou la longueur d'onde.

En touchant à dtrou_dt, on peut modifier la largeur du trou et voir l'effet 
instantané sur l'onde diffracté (pas d'effet retard) [NB: si la largeur du 
trou essaie de devenir inférieure à 2*dx, alors on repart dans l'autre sens]

NB: plus le trou est large, plus c'est lent car on rajoute des sources 
secondaires à sommer sur l'ensemble de l'image.

NB2: la normalisation de l'onde diffractée est encore à revoir. Pour le 
moment, j'ai mis un facteur 2 pour mettre en avant le phénomène, mais il 
faudrait réfléchir pour savoir parfaitement quoi mettre pour que ce soit 
cohérent.

"""

import numpy as np               # Pour les facilités de calcul
import matplotlib.pyplot as plt  # Pour les dessins
from matplotlib.colors import LightSource # Pour l'aspect en relief
from matplotlib import animation # Pour l'animation progressive

shading = False                   # Pour un "effet 3D"
k,w,epsilon = 5,1,1              # Quelques constantes 
c = w/k                          # La vitesse des ondes
tmin,tmax = 50,250                # L'intervalle de temps d'étude
dt = 0.4                         # Le pas de temps
ycut = 19                         # Le plan de coupe en y
vmin,vmax=-1,1                   # Les valeurs extrêmes de l'amplitude
trou = 8                         # La taille du trou
dtrou_dt = -0.1
theta= 0.0                       # L'angle d'incidence (en radians)
ext = 25.0                       # Les limites de la fenêtre d'étude    
dx,dy = 0.1,0.1                  # Resolution
x = np.arange(-ext,ext,dx)       # Axe en x
y = np.arange(ext,-4,-dy)        # et  en y (à l'envers du fait de imshow)
X,Y = np.meshgrid(x,y)           # pour produire la grille

# Pour définir correctement les limites de la fenêtre.
xmin, xmax, ymin, ymax = np.amin(x), np.amax(x), np.amin(y), np.amax(y)
extent = xmin, xmax, ymin, ymax    

base_name = 'PNG/S03_diffraction_' # Le nom par défaut

def point_source(x,y,t,x0=0,y0=0,theta=0):
    '''La fonction représentant une source située en (x0,y0) produite par un 
    front d'onde incliné de theta.'''
    u0= front(x0,y0,t,theta)         # Le front au niveau de la source secondaire
    r = np.sqrt((x-x0)**2+(y-y0)**2) # La distance à la source
    u = u0 + k*r 	                 # La variable de déplacement
                                     # (w*t est déjà dans le u0)
    res =  np.sin(u)                 # Simple sinus
    res[u > 0] = 0.0                 # Le facteur n'est pas passé...
    return 2*res # Facteur multiplicatif pour voir clairement quelque chose...

def front(x,y,t,theta=0):
    '''Définition de la ligne du front d'onde plane. 
    À t=0, le front d'onde passe au point (0,ymin).'''
    return k*(np.sin(theta)*x + np.cos(theta)*(y-ymin)) - w*t
    

def onde_plane(x,y,t,theta=0):
    '''Fonction représentative d'une onde plane faisant un angle theta avec 
    la normale. À t=0, le front d'onde passe au point (0,ymin).'''
    u = front(x,y,t,theta)
    res =  np.sin(u)                 # Simple sinus
    res[u > 0] = 0.0                 # Pour s'assurer qu'à t<0, il n'y a pas d'onde
    return res

def superposition(x,y,t,largeur_trou,theta=0):
    '''Fonction calculant automatiquement la superposition des ondes après 
    passage pour l'ouverture de largeur 'largeur_trou'.'''
    # On commence par mettre l'onde plane partout.
    res = onde_plane(x,y,t,theta)
    # Ensuite, on réfléchit et on corrige pour le valeurs de y > 0
    x_trou = np.arange(-largeur_trou/2,largeur_trou/2,dx)
    S = sum([point_source(x,y,t,xt,0,theta) for xt in x_trou])/len(x_trou)
    res[y > 0] = S[y > 0]
    print(t)    # Un tout petit peu de feedback
    return res  # et on renvoie le résultat à afficher

#for t in np.arange(tmin,tmax,dt):  # On boucle sur le temps
if True:
    t = 0
    Z = superposition(X,Y,t,trou,theta)

    # Calcul à part pour la section de coupe.
    x_trou = np.arange(-trou/2,trou/2,dx)
    Zcut = (sum([point_source(x,ycut,t,xt,0,theta) for xt in x_trou])/len(x_trou))**2

    # Ouverture de la figure et définition des sous-figures
    fig = plt.figure(figsize=(14,10)) 
    ax1= plt.subplot2grid((3,2),(0,0),colspan=2,rowspan=2)
    titre = plt.title('Diffraction par une ouverture plane, $t={}$'.format(round(t,1)))
    plt.ylabel('$y$')
    plt.xlim((xmin,xmax))
    plt.ylim((ymin,ymax))
    if shading:
        ls = LightSource(azdeg=20,altdeg=65) # create light source object.
        rgb = ls.shade(Z,plt.cm.copper)      # shade data, creating an rgb array.
        image = plt.imshow(rgb,extent=extent)
    else:
        image = plt.imshow(Z,interpolation='bilinear',extent=extent,cmap='jet',vmin=vmin,vmax=vmax)
    
    # On rajoute deux barres pour les murs
    murg = plt.annotate('',xytext=(-ext,0),xy=(-trou/2,0),
                 arrowprops=dict(facecolor='black',width=2,frac=0,headwidth=2))
    murd = plt.annotate('',xytext=( ext,0),xy=( trou/2,0),
                 arrowprops=dict(facecolor='black',width=2,headwidth=2,frac=0))
    
    plt.plot([-ext,ext],[ycut,ycut],'--k') # et l'endroit de la section.

    # La figure du bas
    ax2= plt.subplot2grid((3,2),(2,0),colspan=2,sharex=ax1)
    plt.xlabel('$x$')
    plt.ylabel('Intensite\nSection $y={}$'.format(ycut))
    plt.ylim((0,vmax**2))
    section, = plt.plot(x,Zcut**2)

    #plt.savefig(base_name + '{:04d}.png'.format(i))
    #plt.close()

def init():
    section.set_ydata([])

def animate(i):
    global trou, dtrou_dt
    t = i*dt + tmin
    Z = superposition(X,Y,t,trou,theta)
    trou += dtrou_dt * dt
    if trou < 2*dx: 
         dtrou_dt = - dtrou_dt
         trou = 2*dx
    x_trou = np.arange(-trou/2,trou/2,dx)
    murg.xy = (-trou/2,0)
    murd.xy = ( trou/2,0)
    Zcut = (sum([point_source(x,ycut,t,xt,0,theta) for xt in x_trou])/len(x_trou))**2
    titre.set_text('Diffraction par une ouverture plane, $t={}$'.format(round(t,1)))
    if shading: 
        rgb = ls.shade(Z,plt.cm.copper)      # shade data, creating an rgb array.
        image.set_data(rgb)
    else:
        image.set_data(Z)
    section.set_ydata(Zcut**2)
    
# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=int((tmax-tmin)/dt),interval=20)


# Sinon, on montre en direct
plt.show()
    


