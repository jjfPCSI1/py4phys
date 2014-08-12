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
Animation montrant l'apparition de l'attracteur étrange dit du "papillon 
de Lorenz" (NB: ce n'est pas le Lorentz des transformations relativistes: il 
n'a pas de 't'), qui correspond à la solution du système différentiel
	dx/dt = a*(y-x)
	dy/dt = b*x - y - x*z
	dz/dt =-c*z + x*y
Les valeurs "simple" de (a,b,c) qui mènent au chaos sont (10,28,8/3).
On va essayer d'illustrer deux phénomènes différents: la sensibilité aux 
conditions initiales et le fait qu'un certain ordre se cache tout de même dans 
le chaos (voir Ian Stewart, Dieu joue-t-il aux dés, p196 et suivantes pour 
plus de détails)
"""

import numpy as np
import scipy as sp
import scipy.integrate
import matplotlib.pyplot as plt

# Nécessaire pour la 3D, même si cela n'apparaît pas explicitement
from mpl_toolkits.mplot3d import Axes3D 

tmax = 100
nb_points = 10000
yvect0 = np.array([1.0,1.0,1.0])
ecart_relatif = 0.01

def systeme_de_Lorenz(yvect,t):
    a,b,c = 10,28,8/3.0
    x,y,z = yvect
    return [a*(y-x),b*x-y-x*z,-c*z+x*y]

t = np.linspace(0,tmax,nb_points)
sol1 = sp.integrate.odeint(systeme_de_Lorenz,yvect0,t)
sol2 = sp.integrate.odeint(systeme_de_Lorenz,yvect0*(1+ecart_relatif),t)

X1,Y1,Z1 = sol1[:,0],sol1[:,1],sol1[:,2]
X2,Y2,Z2 = sol2[:,0],sol2[:,1],sol2[:,2]

def trouve_positions_maximums(X):
    """ Renvoie la liste des indices correspondant aux maximums de la liste X 
    fournie en paramètre. """
    positions = []
    for i in range(1,len(X)-1):
        if X[i] > X[i-1] and X[i] > X[i+1]:
            positions.append(i)
    return positions



def both_plot(ax,X1,Y1,X2,Y2):
    ax.plot(X1,Y1,'b',X2,Y2,'r')
    ax.plot(X1[-1],Y1[-1],'o',color='cyan')
    ax.plot(X2[-1],Y2[-1],'o',color='magenta')
    

def fait_plot(X,Y,Z,Xp,Yp,Zp,t,i):
    ax1 = fig.add_subplot(2,4,1)
    both_plot(ax1,X,Z,Xp,Zp)
    plt.xlabel('X')
    plt.ylabel('Z')
    ax2 = fig.add_subplot(2,4,2)
    both_plot(ax2,Y,Z,Yp,Zp)
    plt.xlabel('Y')
    plt.ylabel('Z')
    ax3 = fig.add_subplot(2,4,6)
    both_plot(ax3,Y,X,Yp,Xp)
    plt.xlabel('Y')
    plt.ylabel('X')
    ax4 = fig.add_subplot(2,4,5)
    pos = trouve_positions_maximums(Z)
    ax4.plot(Z[pos[:-1]], Z[pos[1:]], 'b.')
    ax4.plot(Z[pos[-1]] , Z[-1], 'o', color='cyan')
    pos = trouve_positions_maximums(Zp)
    ax4.plot(Zp[pos[:-1]],Zp[pos[1:]],'r.')
    ax4.plot(Zp[pos[-1]] ,Zp[-1], 'o', color='magenta')
    plt.xlabel('Z$_k$')
    plt.ylabel('Z$_{k+1}$')
    plt.ylim(25,50)
    ax5 = plt.subplot2grid((2,4),(0,2),colspan=2,rowspan=2,projection='3d')
    ax5.set_xlabel('X')
    ax5.set_ylabel('Y')
    ax5.set_zlabel('Z')
    ax5.plot(X,Y,Z,'b')
    ax5.plot([X[-1]],[Y[-1]],[Z[-1]],'o', color='cyan')
    ax5.plot(Xp,Yp,Zp,'r')
    ax5.plot([Xp[-1]],[Yp[-1]],[Zp[-1]],'o', color='magenta')
    ax5.view_init(elev=10,azim=i%360)
    plt.suptitle('Papillon de Lorenz, $t={}$'.format(t))
    plt.savefig('{}{:05d}.png'.format(base_name,i))
    plt.clf()

base_name = 'PNG/M_papillon_de_lorenz_'

fig = plt.figure(figsize=(16,8))

i = 1000
fait_plot(X1[:i],Y1[:i],Z1[:i],X2[:i],Y2[:i],Z2[:i],round(t[i],3),i)


#for i in range(5,len(t)):
#    fait_plot(X1[:i],Y1[:i],Z1[:i],X2[:i],Y2[:i],Z2[:i],round(t[i],3),i)

# Ne reste plus qu'à rassembler en un fichier mpeg à l'aide de convert puis de
# ppmtoy4m et mpeg2enc (paquet mjpegtools à installer sur la machine)
    
import os

cmd = '(for f in ' + base_name + '*png ; '
cmd+= 'do convert -density 100x100 $f -depth 8 -resize 1200x600 PNM:- ; done)'
cmd+= ' | ppmtoy4m -S 420mpeg2'
cmd+= ' |  mpeg2enc -f1 -b 12000 -q7 -G 30 -o {}film.mpeg'.format(base_name)

print("Execution de la commande de conversion")
print(cmd)
os.system(cmd)
print("Fin de la commande de conversion")



