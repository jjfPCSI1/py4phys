# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.



"""
Ce programme est proposé par Vincent Grenard (PCSI, Lycée Poincaré, Nancy).

Il permet de visualiser la rotation du champ magnétique total lors de la
superposition de trois champs en mode triphasé.

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

##############################
###    True pour sauver    ###
###      False sinon       ###
##############################
save=True

w=1
fleche_x=np.array([0,1,0.90,1,0.90,1])
fleche_y=np.array([0,0,0.1,0,-0.1,0])
fleche=np.zeros((2,len(fleche_x)))
fleche[0,:]=fleche_x
fleche[1,:]=fleche_y
#fleche[:,i]=les coordonnées du point i en colonne

N=2000
phi=2*np.pi/3
#test et initialisation
t=0#np.linspace(0,10,N)
theta=w*t#rotation 
fleche_rot_x=(fleche_x*np.cos(theta)-fleche_y*np.sin(theta))
fleche_rot_y=(fleche_x*np.sin(theta)+fleche_y*np.cos(theta))


#on sauve tous les calculs dans un tableau pour que l'animation soit plus rapide
#juste un accès mémoire et pas de calcul, pas de boucle
Fleche_x,osef=np.meshgrid(fleche_rot_x,np.ones(N))
Fleche_y,osef=np.meshgrid(fleche_rot_y,np.ones(N))
t=np.linspace(0,6*np.pi/w,N)
osef,coswt=np.meshgrid(np.ones(len(fleche_x)),np.cos(w*t))
osef,sinwt=np.meshgrid(np.ones(len(fleche_x)),np.sin(w*t))

DataB1x = Fleche_x*coswt
DataB1y = Fleche_y*coswt
#fleche_rot_x=0.35*(fleche_x*np.cos(theta)-fleche_y*np.sin(theta))
#fleche_rot_y=0.35*(fleche_x*np.sin(theta)+fleche_y*np.cos(theta))
#on tourne de 2pi/3 et de 4pi/3
osef,coswt=np.meshgrid(np.ones(len(fleche_x)),np.cos(w*t+2*phi))
osef,sinwt=np.meshgrid(np.ones(len(fleche_x)),np.sin(w*t+2*phi))
DataB2x = (Fleche_x*np.cos(phi)-Fleche_y*np.sin(phi))*coswt
DataB2y = (Fleche_x*np.sin(phi)+Fleche_y*np.cos(phi))*coswt
osef,coswt=np.meshgrid(np.ones(len(fleche_x)),np.cos(w*t+phi))
osef,sinwt=np.meshgrid(np.ones(len(fleche_x)),np.sin(w*t+phi))
DataB3x = (Fleche_x*np.cos(2*phi)-Fleche_y*np.sin(2*phi))*coswt
DataB3y = (Fleche_x*np.sin(2*phi)+Fleche_y*np.cos(2*phi))*coswt

#la résultante
osef,coswt=np.meshgrid(np.ones(len(fleche_x)),np.cos(w*t))
osef,sinwt=np.meshgrid(np.ones(len(fleche_x)),np.sin(w*t))
DataBx = 1.5*( Fleche_x*coswt-Fleche_y*sinwt)
DataBy = 1.5*( Fleche_x*sinwt+Fleche_y*coswt)

wid=2.5
fig = plt.figure(facecolor='w',figsize=[8,8])
B1, = plt.plot(fleche_x,fleche_y,'-b',linewidth=wid)
B2, = plt.plot(fleche_y,fleche_x,'-r',linewidth=wid)
B3, = plt.plot(fleche_y,fleche_x,'-g',linewidth=wid)
B,  = plt.plot(fleche_x+fleche_y,fleche_x+fleche_y,'-k',linewidth=wid)
pointille1, = plt.plot(fleche_x[1],[0],'--r',linewidth=wid+1)
pointille2, = plt.plot(fleche_x[1],[0],'--g',linewidth=wid+1)
plt.plot(1.5*np.cos(np.linspace(0,7,1000)),1.5*np.sin(np.linspace(0,7,1000)),'-k',linewidth=wid)

plt.axis('off')
#plt.axis('equal')
plt.axis([-1.7,1.7,-1.7,1.7])
fig.gca().set_position([0,0,1,1])




def init():
    B.set_xdata([])
    B.set_ydata([])
    B1.set_xdata([])
    B1.set_ydata([])
    B2.set_xdata([])
    B2.set_ydata([])
    B3.set_xdata([])
    B3.set_ydata([])
    pointille1.set_xdata([])
    pointille1.set_ydata([])
    pointille2.set_xdata([])
    pointille2.set_ydata([])
    return (B,B1,B2,B3,pointille1,pointille2)
    
def animate(i):
    i=i%N
    B.set_xdata(DataBx[i,:])
    B.set_ydata(DataBy[i,:])
    B1.set_xdata(DataB1x[i,:])
    B1.set_ydata(DataB1y[i,:])
    B2.set_xdata(DataB2x[i,:])
    B2.set_ydata(DataB2y[i,:])
    B3.set_xdata(DataB3x[i,:])
    B3.set_ydata(DataB3y[i,:])
    
    #on fait fin B1+flèche b2 , fin B1+finB2 
    pointille1.set_xdata(DataB1x[i,1]+DataB2x[i,:])
    pointille1.set_ydata(DataB1y[i,1]+DataB2y[i,:])
    pointille2.set_xdata(DataB1x[i,1]+DataB2x[i,1]+DataB3x[i,:])
    pointille2.set_ydata(DataB1y[i,1]+DataB2y[i,1]+DataB3y[i,:])
    

    return (B,B1,B2,B3,pointille1,pointille2)
    
    

anim = animation.FuncAnimation(fig,animate,N,interval=20,init_func=init,blit=False)
if save:
    anim.save('PNG/I2_champ_tournant_triphase.mp4', fps=30,bitrate=800)
plt.show()



