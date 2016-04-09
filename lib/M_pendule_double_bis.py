# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.





"""
On reprend tout le problème en se basant sur la mécanique analytique pour les équations

"""

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

# Malheureusement, Xkcd ne fonctionne pas sur mon ordi... :o(
#plt.xkcd()  # XKCD-style requires matplotlib 1.3+


# Les constantes du problème

M1 = 1.0
M2 = 2.0
L1 = 0.9
L2 = 1.2
G  = 9.81
tmax = 100
N  = tmax*100

def energie(th1,th1p,th2,th2p):
    """ On commence par les vérifications énergétiques """
    K = 0.5*(M1+M2)*(L1*th1p)**2 + 0.5*M2*(L2*th2p)**2 + M2*L1*L2*th1p*th2p*cos(th1-th2)
    U = -(M1+M2)*G*L1*cos(th1) - M2*G*L2*cos(th2)
    return U + K

def evolution(y,t):
    th1,th1p,th2,th2p = y
    dydt = np.zeros_like(y)
    # Les vitesses sont déjà connues
    dydt[0] = th1p
    dydt[2] = th2p
    # Les équations trouvées sont un système couplé du type
    # a*th1pp + b*th2pp = alpha
    # c*th1pp + d*th2pp = beta
    # qui se résout par formules de Cramer
    # th1pp = (alpha*d - b*beta)/(ad-bc)
    # th2pp = (a*beta - c*alpha)/(ad-bc)
    cos_delta = cos(th1-th2)
    sin_delta = sin(th1-th2)
    a = (M1+M2)*L1**2
    b = M2*L1*L2*cos_delta
    c = M2*L1*L2*cos_delta
    d = M2*L2**2
    # Le plus dur à écrire sont les seconds membres
    alpha = M2*L1*L2*th2p*sin_delta*(th1p-th2p) 		            - (M1+M2)*G*L1*sin(th1)						            - M2*L1*L2*th1p*th2p*sin_delta
    beta  = M2*L1*L2*th1p*sin_delta*(th1p-th2p)			            - M2*G*L2*sin(th2)							            + M2*L1*L2*th1p*th2p*sin_delta
    # Reste à utiliser Cramer
    dydt[1] = (alpha*d-b*beta)/(a*d-b*c)
    dydt[3] = (a*beta-c*alpha)/(a*d-b*c)
    return dydt


# L'intégration proprement dite

t = np.linspace(0,tmax,N)
def integration(y0):
    # Le calcul des coordonnées généralisées
    sol = integrate.odeint(evolution,y0,t)
    th1 = sol[:,0]
    th1p= sol[:,1]
    th2 = sol[:,2]
    th2p= sol[:,3]
    # On renvoie les positions et l'énergie correspondante
    X1 = L1*sin(th1)
    X2 = X1 + L2*sin(th2)
    Y1 = -L1*cos(th1)
    Y2 = Y1 - L2*cos(th2)
    E = energie(th1,th1p,th2,th2p)
    return X1,X2,Y1,Y2,E

y0_1 = np.array([180,0,-20,0]) * np.pi/180
y0_2 = np.array([180,0,-20,0.001]) * np.pi/180
X1_1,X2_1,Y1_1,Y2_1,E_1 = integration(y0_1)
X1_2,X2_2,Y1_2,Y2_2,E_2 = integration(y0_2)

#------------------------------------------------------------
# set up figure and animation

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-2, 2), ylim=(-2, 2))
#ax.grid()

line,  = ax.plot([], [], 'o-', lw=2)
line2, = ax.plot([], [], 'o-', lw=2)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
energy_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
energy2_text= ax.text(0.02, 0.85, '', transform=ax.transAxes)

def init():
    """initialize animation"""
    line.set_data([], [])
    line2.set_data([], [])
    time_text.set_text('')
    energy_text.set_text('')
    energy2_text.set_text('')
    return line, line2, time_text, energy_text, energy2_text

def animate(i):
    """perform animation step"""
    X_1 = [0,X1_1[i],X2_1[i]]
    Y_1 = [0,Y1_1[i],Y2_1[i]]
    line.set_data(X_1,Y_1)
    X_2 = [0,X1_2[i],X2_2[i]]
    Y_2 = [0,Y1_2[i],Y2_2[i]]
    line2.set_data(X_2,Y_2)
    time_text.set_text('time = %.1f' % t[i])
    energy_text.set_text('energie 1 = %.5f J' % E_1[i])
    energy2_text.set_text('energie 2 = %.5f J' % E_2[i])
    return line, line2, time_text, energy_text, energy2_text

dt = t[1]-t[0]

# choose the interval based on dt and the time to animate one step
from time import time
t0 = time()
animate(0)
t1 = time()
interval = 1000 * dt - (t1 - t0)

ani = animation.FuncAnimation(fig, animate, frames=N,
                              interval=interval, blit=False, init_func=init)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
ani.save('double_pendulum_xkcd.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

#plt.show()




