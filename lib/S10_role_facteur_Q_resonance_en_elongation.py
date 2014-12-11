# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.




import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation # Pour l'animation progressive
import cmath

E0 = 1
Q = 2
xmax = 2

def u_barre(x,Q):
    return E0/(1 - x**2 + 1j*x/Q)

fig = plt.figure(figsize=(10,10))


x = np.linspace(0,xmax,1000)
ub = u_barre(x,Q)

plt.subplot(211)
ax = fig.gca()
plt.title('$Q={:.2f}$'.format(Q))
absu,    = plt.plot(x,np.abs(ub),linewidth=2)
pos_w0, =plt.plot([1,1,0],[0,Q*E0,Q*E0],'k--',linewidth=2)
xres = np.sqrt(1 - 1/(2*Q**2))
pos_res, = plt.plot([xres,xres],[0,abs(u_barre(xres,Q))],'r--',linewidth=2)

plt.ylabel('$u_0$')

plt.subplot(212)
phi = np.array(list(map(cmath.phase,ub)))
lphi,    =plt.plot(x,phi,linewidth=2)
plt.plot([0,1,1],[-np.pi/2,-np.pi/2,0],'k--',linewidth=2)
plt.xlabel('$x$')
plt.ylabel('$\phi$')

def init():
    pass
    
nb_Q = 500
Q = np.logspace(-1,1,nb_Q)

def animate(i):
    if i < nb_Q: q = Q[i]
    else: q = Q[2*nb_Q-i-1]
    ub = u_barre(x,q)
    absu.set_ydata(np.abs(ub))
    pos_w0.set_ydata([0,q*E0,q*E0])
    phi = np.array(list(map(cmath.phase,ub)))
    lphi.set_ydata(phi)
    ax.set_title('$Q={:.2f}$'.format(q))
    xres = np.sqrt(1 - 1/(2*q**2))
    pos_res.set_ydata([abs(u_barre(xres,q)),0])
    pos_res.set_xdata([xres,xres])


# L'animation proprement dite
anim = animation.FuncAnimation(fig,animate,frames=2*nb_Q,interval=20)


plt.show()



