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
Ce programme est proposé par Vincent Grenard (PCSI, Lycée Poincaré, Nancy).

L'idée est de visualiser l'aspect transverse de la propagation d'une onde 
électromagnétique pour introduire le cours d'optique et suite au cours sur la 
propagation d'un signal.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

w=2*np.pi
t=0
k=2

fleche_x=np.array([0,1,0.95,1,0.95,1])
fleche_y=np.array([0,0,0.05,0,-0.05,0])
fleche=np.zeros((2,len(fleche_x)))
fleche[0,:]=fleche_x
fleche[1,:]=fleche_y
#fleche[:,i]=les coordonnées du point i en colonne
theta=np.pi/6+np.pi#rotation pour donner une impression de projection 3D
fleche_rot_x=0.65*(fleche_x*np.cos(theta)-fleche_y*np.sin(theta))
fleche_rot_y=0.65*(fleche_x*np.sin(theta)+fleche_y*np.cos(theta))

fig=plt.figure(facecolor='w',figsize=[12,6])
plt.plot(fleche_x,fleche_y,lw=2)
#plt.plot(fleche_y,fleche_x,'-r',lw=2)
X=np.linspace(0,4,20)
plt.plot(X,0*X,'-b')
plt.plot([0,0],[-2,2],'-r')
plt.plot([2*fleche_rot_x[1],-2*fleche_rot_x[1]],[2*fleche_rot_y[1],-2*fleche_rot_y[1]],'-c')
l1=[]
l2=[]
plt.annotate('$\overrightarrow{E}$',(0,0),xytext=(-0.3,0.4),fontsize=20,color='r')
plt.annotate('$\overrightarrow{B}$',(0,0),xytext=(-0.6,-0.3),fontsize=20,color='c')
plt.annotate('$\overrightarrow{k}$',(0,0),xytext=(0.9,0.05),fontsize=20,color='b')
for (j,x) in enumerate(X):
    amp=np.cos(w*t-k*x)
    tmp,=plt.plot(fleche_y*amp+x,fleche_x*amp,'-r',lw=2)
    l1.append(tmp)
    tmp,=plt.plot(fleche_rot_x*amp+x,fleche_rot_y*amp,'-c',lw=2)
    l2.append(tmp)
XX=np.linspace(X.min(),X.max(),100)
YY=np.cos(w*t-k*XX)
enveloppe_1,=plt.plot(XX,YY,'-r')
enveloppe_2,=plt.plot(YY*fleche_rot_x[1]+XX,YY*fleche_rot_y[1],'-c')
#plt.plot()

#plt.plot(fleche_rot_x,fleche_rot_y,lw=2)
plt.axis('off')
plt.axis([X.min()-1,X.max()+1,-1.2,1.2])

def init():
    for (j,x) in enumerate(X):
        l1[j].set_xdata([])
        l1[j].set_ydata([])
        l2[j].set_xdata([])
        l2[j].set_ydata([])
    enveloppe_1.set_xdata([])
    enveloppe_1.set_ydata([])
    enveloppe_2.set_xdata([])
    enveloppe_2.set_ydata([])
    return tuple(l1+l2+[enveloppe_1]+[enveloppe_2])
    
def animate(i):
    t=0.002*i
    for (j,x) in enumerate(X):
        amp=np.cos(w*t-k*x)
        l1[j].set_xdata(fleche_y*amp+x)
        l1[j].set_ydata(fleche_x*amp)
        l2[j].set_xdata(fleche_rot_x*amp+x)
        l2[j].set_ydata(fleche_rot_y*amp)
    YY=np.cos(w*t-k*XX)
    enveloppe_1.set_xdata(XX)
    enveloppe_1.set_ydata(YY)
    enveloppe_2.set_xdata(YY*fleche_rot_x[1]+XX)
    enveloppe_2.set_ydata(YY*fleche_rot_y[1])
    return tuple(l1+l2+[enveloppe_1]+[enveloppe_2])
    
anim = animation.FuncAnimation(fig,animate,2000,interval=20,init_func=init,blit=False)
#anim.save('onde_EM.mp4', fps=30,bitrate=50)
plt.show()


