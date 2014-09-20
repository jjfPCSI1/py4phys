# coding: latin1

# Sauf mention explicite du contraire par la suite, ce travail a �t� fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lyc�e Kl�ber. 
# Vous �tes libres de le r�utiliser et de le modifier selon vos besoins.
# 
# Si l'encodage vous pose probl�me, vous pouvez r�encoder le fichier � l'aide 
# de la commande
# 
# recode l1..utf8 monfichier.py
# 
# Il faudra alors modifier la premi�re ligne en # coding: utf8
# pour que Python s'y retrouve.




"""
Ce programme est propos� par Vincent Grenard (PCSI, Lyc�e Poincar�, Nancy).
Il a �t� adapt� par JJ Fleck pour les cas d'amplitudes non �gales.

Il s'agit de visualiser la construction de battements tout en regardant 
l'�volution du diagramme de Fresnel correspondant.

"""


import numpy as np                # Bo�te � outils num�riques
import matplotlib.pyplot as plt   # Bo�te � outils graphique
from matplotlib import animation  # Pour les animations "au vol"
from cmath import *               # Pour les complexes, notamment phase()

omega=0.5                         # Pulsation principale
delta_omega=0.045                 # Ecart de pulsation
delta_t=0.09                      # Intervale de temps entre deux points
N=3000                            # Nombre total de points
A = 1.5                           # Amplitude du deuxi�me signal

# D�finition des fl�ches "� la main"
fleche_x=np.array([0,1,0.95,1,0.95,1])  # Dessin suivant x
fleche_y=np.array([0,0,0.05,0,-0.05,0]) # Dessin suivant y

def rotation_fleche(theta): 
    """ Rotation du dessin de base d'une fl�che """
    fleche_rot_x=0.65*(fleche_x*np.cos(theta)-fleche_y*np.sin(theta))
    fleche_rot_y=0.65*(fleche_x*np.sin(theta)+fleche_y*np.cos(theta))
    return fleche_rot_x,fleche_rot_y

# On d�marre le dessin proprement dit.
fig=plt.figure(figsize=(16,10),facecolor='w') # D�finition de la figure
fig.add_axes([0.1,0.4,0.8,0.5])               # Partie sup�rieure
# Les fl�ches de bases
F1, =plt.plot(fleche_x,fleche_y,'g',lw=2)
F2, =plt.plot(A*fleche_x,A*fleche_y,'b',lw=2)
# Les fl�ches pour compl�ter les parall�logrammes
F21,=plt.plot(fleche_x+fleche_x[1],fleche_y+fleche_y[1],'--b',lw=2)
F12,=plt.plot(fleche_x+fleche_x[1],fleche_y+fleche_y[1],'--g',lw=2)
# La fl�che totale
Ft ,=plt.plot((1+A)*fleche_x,(1+A)*fleche_y,'r',lw=2)
plt.axis('equal')                   # Aspect carr�
plt.axis([-4.2,4.2,-2.2,2.2])       # Centrage de la figure
plt.axis('off')                     # On enl�ve les num�ros
fig.add_axes([0.1,0.05,0.8,0.34])   # Partie inf�rieure
temps=np.arange(0,N*delta_t,delta_t)# Le temps et la somme des cosinus
somme=A*np.cos((omega+delta_omega)*temps)+np.cos(omega*temps)
S,=plt.plot(temps,somme)            # Le graphique correspondant

def init(): # On initialise tout avec des donn�es vides
    F1.set_xdata([])
    F1.set_ydata([])
    F2.set_xdata([])
    F2.set_ydata([])
    F21.set_xdata([])
    F21.set_ydata([])
    F12.set_xdata([])
    F12.set_ydata([])
    Ft.set_xdata([])
    Ft.set_ydata([])
    S.set_xdata([])
    S.set_ydata([])
    return F1,F2,F12,F21,Ft,S


def animate(i):               # Fonction qui met � jour les donn�es
    t=delta_t*i               # Le temps
    # On utilise les complexes pour trouver le r�sultat final.
    c1 = rect(1,omega*t)
    c2 = rect(A,(omega+delta_omega)*t)
    c3 = c1 + c2
    # On effectue les trois rotations de la fl�che de base
    fx,fy=rotation_fleche(omega*t)
    fx2,fy2=rotation_fleche((omega+delta_omega)*t)
    fx3,fy3=rotation_fleche(phase(c3))
    F1.set_xdata(fx)          # Mise � jour de la fl�che 1
    F1.set_ydata(fy)
    F2.set_xdata(A*fx2)       # Mise � jour de la flc�eh 2
    F2.set_ydata(A*fy2)
    F21.set_xdata(A*fx2+fx[1])# Premier parall�logramme
    F21.set_ydata(A*fy2+fy[1])
    F12.set_xdata(fx+A*fx2[1])# Second parall�logramme
    F12.set_ydata(fy+A*fy2[1])
    Ft.set_xdata(abs(c3)*fx3)
    Ft.set_ydata(abs(c3)*fy3)
    S.set_xdata(temps[0:i])   # Mise � jour du graphique
    S.set_ydata(somme[0:i])
    return F1,F2,F12,F21,Ft,S

# Fabrication de l'animation
anim = animation.FuncAnimation(fig,animate,N,interval=20,init_func=init,
       blit=False,repeat=False)
# D�commenter la ligne suivante pour convertir l'animation en film .mp4
#anim.save('PNG/S03_battements_fresnel.mp4', fps=30,bitrate=50)

# Sinon on affiche l'animation � l'�cran
plt.show()


