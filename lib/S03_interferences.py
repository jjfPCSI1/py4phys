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
Simulation d'un phénomène d'interférences à deux ondes circulaires (comme 
des ronds dans l'eau). Les graphes du bas et de la droite représentent des 
coupes respectivement à x et à y fixé.

On peut simuler une décroissance de l'onde en 1/r (sauf au centre pour éviter 
toute divergence) ou simplement avoir une fonction sinusoïdale en jouant sur 
la fonction 'source'. En cas de changement, il faut penser à modifier les 
valeurs vmin,vmax qui définissent les extrêmes du code couleur adopté.
'''

import numpy as np               # Pour les facilités de calcul
import matplotlib.pyplot as plt  # Pour les dessins
from matplotlib.colors import LightSource # Pour l'aspect en relief

def source(x,y,t,x0=0,y0=0,phi=0):
    '''La fonction représentant notre source située en (x0,y0)'''
    k,w,epsilon = 5,1,1              # Quelques constantes 
    r = np.sqrt((x-x0)**2+(y-y0)**2) # La distance à la source
    u = k*r - w*t + phi              # La variable de déplacement
    #res =  np.sin(u)                # Simple sinus
    res = np.sin(u)/(r+epsilon)      # ou décroissance de l'amplitude...
    res[u > 0] = 0.0                 # Pour s'assurer qu'à t<0, il n'y a pas d'onde
    return res

shading = True             # Si on veut un "effet 3D"
ext = 6.0                  # Les limites de la fenêtre d'étude    
pos = 3.5                  # Positions des sources symétriquement selon x
phi = np.pi/2              # Déphasage de la deuxième source
tmin,tmax = 0,60           # L'intervalle de temps d'étude
dt = 0.1                   # et le pas 
xcut = 1                   # Les plans de coupe en x
ycut = 2                   # et en y
vmin,vmax=-0.5,0.5         # Les valeurs extrêmes de l'amplitude
dx,dy = 0.05,0.05          # Resolution
x = np.arange(-ext,ext, dx)# Axe en x
y = np.arange(ext,-ext,-dy)# et  en y
X,Y = np.meshgrid(x,y)     # pour produire la grille

# Pour définir correctement les limites de la fenêtre.
xmin, xmax, ymin, ymax = np.amin(x), np.amax(x), np.amin(y), np.amax(y)
extent = xmin, xmax, ymin, ymax    

base_name = 'PNG/S03_interferences_' # Le nom par défaut

i = 0                              # Initialisation du compteur
for t in np.arange(tmin,tmax,dt):  # On boucle sur le temps
    i += 1                         # Incrémentation du compteur
    print(t)                       # Un peu de feedback
    Z1 = source(X,Y,t,-pos,0)      # La première source
    Z2 = source(X,Y,t, pos,0,phi)  # et la seconde

    # Ouverture de la figure et définition des sous-figures
    plt.figure(figsize=(8,7.76)) 
    ax1= plt.subplot2grid((3,3),(0,0),colspan=2,rowspan=2)
    plt.title('Interferences a deux sources, $t={}$'.format(round(t,1)))
    plt.ylabel('$y$')
    if shading:
        ls = LightSource(azdeg=20,altdeg=65) # create light source object.
        rgb = ls.shade(Z1+Z2,plt.cm.copper)  # shade data, creating an rgb array.
        plt.imshow(rgb,extent=extent)
    else:
        plt.imshow(Z1+Z2,interpolation='bilinear',extent=extent,cmap='jet',vmin=vmin,vmax=vmax)

    # Pour visualiser les deux plans de coupes
    plt.plot([-ext,ext],[ycut,ycut],'--k') 
    plt.plot([xcut,xcut],[-ext,ext],'--k')    

    # La figure du bas
    ax2= plt.subplot2grid((3,3),(2,0),colspan=2,sharex=ax1)
    plt.xlabel('$x$')
    plt.ylabel('Intensite\nSection $y={}$'.format(ycut))
    plt.ylim((0,vmax**2))
    plt.plot(x,(source(x,ycut,t,-pos,0)+source(x,ycut,t,pos,0,phi))**2)

    # et celle de la droite
    ax3= plt.subplot2grid((3,3),(0,2),rowspan=2,sharey=ax1)
    plt.xlabel('Intensite')
    plt.xlim((0,vmax**2))
    plt.title('Section $x={}$'.format(xcut))
    plt.plot((source(xcut,y,t,-pos,0)+source(xcut,y,t,pos,0,phi))**2,y)
    plt.savefig(base_name + '{:04d}.png'.format(i))
    plt.close()

# Ne reste plus qu'à rassembler en un fichier mpeg à l'aide de convert puis de 
# ppmtoy4m et mpeg2enc (paquet mjpegtools à installer sur la machine)

from film import make_film

make_film(base_name,resize="700x500")

#import os
#
#cmd = '(for f in ' + base_name + '*png ; '
#cmd+= 'do convert -density 100x100 $f -depth 8 -resize 700x500 PNM:- ; done)'
#cmd+= ' | ppmtoy4m -S 420mpeg2'
#cmd+= ' |  mpeg2enc -f1 -b 12000 -q7 -G 30 -o {}film.mpeg'.format(base_name)
#
#print("Execution de la commande de conversion")
#print(cmd)
#os.system(cmd)
#print("Fin de la commande de conversion")



