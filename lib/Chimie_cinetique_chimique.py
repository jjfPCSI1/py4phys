# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




"""
Created on Tue Dec  9 14:22:09 2014

@author: Vincent GRENARD : vincent.grenard@gmail.com
Adaptation à Qt5 : Eric Bachard
Merci de me contacter pour toute suggestion d'amélioration

Modélise la cinétique de la réaction
A <=> B + C
B  => D
Pour montrer que la variation concentration d'un intermédiaire
réactionnel est négligeable par rapport aux autres dérivées temporelles

Les constantes de réactions peuvent être modifiées en direct
Elles sont prises initialement à des valeurs égales, et on peut fortement
diminuer k_1 par rapport aux deux autres pour transformer B en intermédiaire
réactionnel
"""

#chimie

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.widgets import Slider, Button

#réaction chimique :
# A => B + C (k1)
# B + C => A (k_moins1)
# B => D (k2)

#equation :
# dA/dt = -k1 A + k_moins1 B * C
# dB/dt =  k1 A - k_moins1 B * C - k2 B
# dC/dt =  k1 A - k_moins1 B * C
# dD/dt =  k2 B

k1 = 5
k2 = 5
kmoins1 = 5
tmaxNormalise = 5
Npoints = 50000
tmax = tmaxNormalise/min([k1,k2,kmoins1])


def f(X,t):
    Y = [0]*len(X)
    Y[0] = -k1 * X[0] + kmoins1 * X[1]*X[2]
    Y[1] =  k1 * X[0] - kmoins1 * X[1]*X[2] - k2*X[1]
    Y[2] =  k1 * X[0] - kmoins1 * X[1]*X[2]
    Y[3] =  k2 * X[1]
    return Y
    

X0 = [1,0,0,0]
t,dt = np.linspace(0,tmax,Npoints,retstep = True)
X = odeint(f,X0,t)
A = X[:,0]
B = X[:,1]
C = X[:,2]
D = X[:,3]

fig = plt.figure(figsize = [14,10])
plt.figtext(0.5,0.00,
r"""
$A\longleftrightarrow B + C  \quad  (k_1 \, ; \, k_{-1})$
$B\longrightarrow D  \quad  (k_2)$
""",
    fontsize = 18,horizontalalignment ='center')
ax1 = fig.add_axes([0.05,0.3,0.425,0.68])
lA, = plt.plot(t,A,'-b',lw = 2,label = r'$[A]$')
lB, = plt.plot(t,B,'-g',lw = 2,label = r'$[B]$')
lD, = plt.plot(t,D,'-r',lw = 2,label = r'$[D]$')
plt.legend()
plt.xlabel(r'$t$ (u.a.)',fontsize = 16)
plt.ylabel(r'$[A],[B],[D]$ (u.a.)',fontsize = 16)
plt.ylim(0,1)
ax2 = fig.add_axes([0.55,0.3,0.425,0.3])
lBzoom, = plt.plot(t,B,'-g',lw = 2,label = r'$[B]$')
plt.xlabel(r'$t$ (u.a.)',fontsize = 16)
plt.ylabel(r'$[B]$ (u.a.)',fontsize = 16)
axcolor = 'lightgoldenrodyellow'

ax3 = fig.add_axes([0.55,0.68,0.425,0.3])
t2 = 0.5 * (t[1:]+t[:-1])
dAdt = (A[1:]-A[:-1])/dt
dBdt = (B[1:]-B[:-1])/dt
dDdt = (D[1:]-D[:-1])/dt
ldAdt, = plt.plot(t2,dAdt,'-b',lw=2,label = r'$\frac{d[A]}{dt}$')
ldBdt, = plt.plot(t2,dBdt,'-g',lw=2,label = r'$\frac{d[B]}{dt}$')
ldDdt, = plt.plot(t2,dDdt,'-r',lw=2,label = r'$\frac{d[D]}{dt}$')
plt.legend()
#plt.xlabel('t (u.a.)',fontsize = 16) #axe partagé avec la courbe du dessus
plt.ylabel('$d/dt$ (u.a.)',fontsize = 16)

axk1  = plt.axes([0.15, 0.2, 0.8, 0.03], facecolor=axcolor)
axkmoins1  = plt.axes([0.15, 0.15, 0.8, 0.03], facecolor=axcolor)
axk2  = plt.axes([0.15, 0.1, 0.8, 0.03], facecolor=axcolor)

slider_k1 = Slider(axk1, '$k_1$', 0.001, 10.0, valinit=5)
slider_kmoins1 = Slider(axkmoins1, '$k_{-1}$', 0, 50, valinit=5)
slider_k2 = Slider(axk2, '$k_2$', 0, 50, valinit=5)


def update(val):
    global k1, k2, kmoins1,lA,lB,lD,lBzoom
    k1 = slider_k1.val
    kmoins1 = slider_kmoins1.val
    k2 = slider_k2.val
    X0 = [1,0,0,0]
    
    tmax = tmaxNormalise/min([k1,k2,kmoins1])
    t,dt = np.linspace(0,tmax,Npoints,retstep = True)
    X = odeint(f,X0,t)
    A = X[:,0]
    B = X[:,1]
    C = X[:,2]
    D = X[:,3]
    
    t2 = 0.5 * (t[1:]+t[:-1])
    dAdt = (A[1:]-A[:-1])/dt
    dBdt = (B[1:]-B[:-1])/dt
    dDdt = (D[1:]-D[:-1])/dt



    lA.set_xdata(t)
    lB.set_xdata(t)
    lD.set_xdata(t)
    lBzoom.set_xdata(t)
    lA.set_ydata(A)
    lB.set_ydata(B)
    lD.set_ydata(D)
    lBzoom.set_ydata(B)
    ax1.set_xlim([0,tmax])
    ax2.set_xlim([0,tmax])
    ax2.set_ylim([0,max(B)*1.1])
    
    
    ldAdt.set_xdata(t2)
    ldBdt.set_xdata(t2)
    ldDdt.set_xdata(t2)
    ldAdt.set_ydata(dAdt)
    ldBdt.set_ydata(dBdt)
    ldDdt.set_ydata(dDdt)
    tout = np.hstack((dAdt,dBdt,dDdt))
    ax3.set_ylim([tout.min(),tout.max()])
    ax3.set_xlim([0,tmax])
    
    plt.draw()
slider_k1.on_changed(update)
slider_kmoins1.on_changed(update)
slider_k2.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
def reset(event):
    slider_k1.reset()
    slider_kmoins1.reset()
    slider_k2.reset()
button.on_clicked(reset)

plt.show()



