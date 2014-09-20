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

Il produit une boîte de dialogue qui permet un tracé interactif des battements 
en permettant de modifier les divers paramètres pour illustrer la notion de 
battements.

"""
import numpy as np
import pylab as py
from matplotlib.widgets import Slider, Button, RadioButtons

def s(t,w=1,a=1,phi=0):
    return a*np.cos(3*w*t+phi)
    
t=np.linspace(0,100,5000)

fig = py.figure('Battement')
ax = fig.add_subplot(1,1,1)

py.subplots_adjust(left=0.2, bottom=0.35)
py.axis([0,0.8,0,0.8])

l1,l2 =py.plot([],[],'-k',[],[],'-r')

def rebond (event):	
    a1  = amplitude1.val
    a2  = amplitude2.val
    f2  = frequence2.val
    phi = phase.val
    
    t=np.linspace(0,100,1000)
    l1.set_xdata(t)
    y=s(t,a=a1)+s(t,f2,a2,phi)
    l1.set_ydata(y)
    l2.set_xdata(t)
    
    if(a2==a1):
        l2.set_ydata(s(t,(f2-1)/2.0,2*a2,phi/2.0))
    else:
        l2.set_ydata(np.sqrt(a1**2+a2**2+2*a1*a2*s(t,f2-1,1,phi)))
#    elif(a1>a2):
#        l2.set_ydata(np.abs(a1-a2)+np.abs(s(t,(f2-1)/2.0,2*a2,phi/2.0)))
#    else:
#        l2.set_ydata(np.abs(a2-a1)+np.abs(s(t,(f2-1)/2.0,2*a1,phi/2.0)))
    
    ax.axes.axis([0,100,1.1*min(y),1.1*max(y)])
    py.draw()
    
    

    

sld_amplitude1 = py.axes([0.2, 0.1, 0.7, 0.03], axisbg='grey')
sld_amplitude2 = py.axes([0.2, 0.15, 0.7, 0.03], axisbg='grey')
sld_frequence2 = py.axes([0.2, 0.2, 0.7, 0.03], axisbg='grey')
sld_phase2     = py.axes([0.2, 0.25, 0.7, 0.03], axisbg='grey')

amplitude1     = Slider(sld_amplitude1, 'amplitude 1', 0.0, 2.0, valinit=1)
amplitude2     = Slider(sld_amplitude2, 'amplitude 2', 0, 2.0, valinit=1)
frequence2     = Slider(sld_frequence2, r'$f_2/f_1$', 0.9, 1.1, valinit=1)
phase          = Slider(sld_phase2, r'$\varphi_2-\varphi_1$', 1, 5.0, valinit=0)

button_demarre = py.axes([0.7, 0.02, 0.2, 0.05])
button = Button(button_demarre, 'animation', color='grey', hovercolor='white')
button.on_clicked(rebond)

py.show()


