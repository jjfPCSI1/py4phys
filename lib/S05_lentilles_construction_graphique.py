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
Travail proposé par Vincent Grenard (PCSI, Lycée Poincaré, Nancy)

objectif : automatiser le tracé de rayon dans des lentilles
et sortir le code pstricks

je commence par une seule lentille, et on verra plus tard 
si j'en met plusieurs
"""

import numpy as np
import matplotlib.pyplot as plt

#####   data    #####

x_O = 0  # position du centre optique O
x_A = -3 # position de l'objet, < 0 pour réel, >0 pour virtuel
AB  = 1  # taille de l'objet
f_p = 2  # f' : distance focale

#####   limite de l'espace    #####
lim = [-8,8,-3,3]   # xdeb xfin ydeb yfin
x_deb = lim[0]
x_fin = lim[1]
y_deb = lim[2]
y_fin = lim[3]
delta_x = x_fin - x_deb
delta_y = y_fin - y_deb

#####   calculs    #####

###BUG : gérer le cas x_A = - f_p
if x_A == x_O-f_p:
    x_A = x_A*(1+2**-51) #mauvaise triche : trace un rayon mauvais

# relation de conjugaison : p'= pf'/(p+f')
# p = OA = x_A-x_O
x_A_p = x_O + (x_A-x_O) * f_p /( (x_A-x_O) + f_p)
# grandissement : A_pB_p/AB = OA_p/OA = p'/p = f'/(p+f')
A_pB_p = AB *  f_p /( (x_A-x_O) + f_p)


#####   affichage    #####

#axe optique
plt.plot([x_deb,x_fin],[0,0],'-k')#axe optique
deb_fleche = x_fin - 0.025*delta_x
altitude_fleche = delta_y * 0.025
plt.plot( [deb_fleche,x_fin,deb_fleche],[altitude_fleche,0,-altitude_fleche],'-k') # flèche

#lentille
plt.plot([x_O,x_O],[0.95*y_deb,0.95*y_fin],'-k',lw=2)
if f_p<0:
    sg = -1
else:
    sg = 1
lx_fl = 0.05*delta_x
ly_fl = sg * 0.05*delta_y
plt.plot([x_O-lx_fl,x_O,x_O+lx_fl],[0.95*y_fin-ly_fl,0.95*y_fin,0.95*y_fin-ly_fl],'-k',lw=2)
plt.plot([x_O-lx_fl,x_O,x_O+lx_fl],[0.95*y_deb+ly_fl,0.95*y_deb,0.95*y_deb+ly_fl],'-k',lw=2)
#foyers
plt.plot([x_O+f_p]*2,[delta_y*0.01,-delta_y*0.01])
plt.plot([x_O-f_p]*2,[delta_y*0.01,-delta_y*0.01])

#cas objet réel ou virtuel
if(x_A-x_O<0):
    style = '-k'
else:
    style = '--k'
if AB >0:
    sg = 1
else:
    sg = -1
plt.plot([x_A]*2,[0,AB],style)
lx_fl = 0.025*delta_x
ly_fl = sg*0.025*delta_y
plt.plot([x_A-lx_fl,x_A,x_A+lx_fl],[AB-ly_fl,AB,AB-ly_fl],style)

#image, cas image réelle ou virtuelle
if(x_A_p-x_O>0):
    style = '-k'
else:
    style = '--k'
if A_pB_p >0:
    sg = 1
else:
    sg = -1
plt.plot([x_A_p]*2,[0,A_pB_p],style)
lx_fl = 0.025*delta_x
ly_fl = sg*0.025*delta_y
plt.plot([x_A_p-lx_fl,x_A_p,x_A_p+lx_fl],[A_pB_p-ly_fl,A_pB_p,A_pB_p-ly_fl],style)

#premier rayon facile : par le centre et par l'objet
#thalès AB/(xO-xA) = y/(x_O-xdeb)
plt.plot([x_deb,x_fin],[(x_O-x_deb)/(x_O-x_A)*AB,(x_O-x_fin)/(x_O-x_A)*AB],'-r')

#2e rayon facile : parallèle à l'axe optique puis sort en passant par F'
#thalès : AB/f_p = -y/(x_fin-x_O-f_p)
plt.plot([x_deb,x_O,x_fin],[AB,AB,-(x_fin-x_O-f_p)/f_p*AB],'-b')
plt.plot([x_O,x_A],[AB,AB],'--b') #si objet virtuel
plt.plot([x_O,x_A_p],[AB,A_pB_p],'--b')

#3e rayon facile : passe par F 
# seulement si x_A n'est pas en F
if (abs(x_A-x_O+f_p)>2**(-8) * delta_x):
    plt.plot([x_deb,x_O,x_fin],[(x_deb-x_O+f_p)/(f_p)*A_pB_p,A_pB_p,A_pB_p],'-g')
    plt.plot([x_O,x_A],[A_pB_p,AB],'--g')
    plt.plot([x_O,x_A_p],[A_pB_p,A_pB_p],'--g')

#show
plt.axis('off')
plt.axis(lim)
plt.show(False)


#### génération du code pstricks
print(r"egin{pspicture*}(",x_deb-0.1,",",y_deb-0.1,")(",x_fin+0.1,",",y_fin+0.1,")")
## Axe optique
print(r"% axe optique")
print(r"\psline[arrowscale = 3]{->}(",x_deb,",0)(",x_fin,",0)")
print(r"\uput[90](",x_fin-0.1,",0.1){$\Delta$}")
# Lentille convergente ou divergente
if (f_p<0):
    arrow = '>-<'
else:
    arrow = '<->'
print(r"%Lentille")
print(r"\psline[linewidth = 2pt,arrowscale = 2]{",arrow,"}(",x_O,",",y_deb,")(",x_O,",",y_fin,")")
#objet réel ou virtuel
if(x_A-x_O>0):
    style = r',linestyle = dashed]'
else:
    style = ']'
print(r"% objet réel ou virtuel")
print(r"\psline[linewidth = 1.5pt"+style +"{->}(",x_A,",0)(",x_A,",",AB,")")
if AB >0:
    sg = 1
else:
    sg = -1
print(r"\uput[",-sg*90,"](",x_A,",0){$A$}")
print(r"\uput[",sg*90,"](",x_A,",",AB,"){$B$}")
#image réelle ou virtuelle
print(r"% image réelle ou virtuelle")
if(x_A_p-x_O<0):
    style = r',linestyle = dashed]'
else:
    style = ']'
print(r"\psline[linewidth = 1.5pt"+style +"{->}(",x_A_p,",0)(",x_A_p,",",A_pB_p,")")
if A_pB_p >0:
    sg = 1
else:
    sg = -1
print(r"\uput[",-sg*90,"](",x_A_p,",0){$A'$}")
print(r"\uput[",sg*90,"](",x_A_p,",",A_pB_p,"){$B'$}")
#premier rayon facile plt.plot([x_deb,x_fin],[(x_O-x_deb)/(x_O-x_A)*AB,(x_O-x_fin)/(x_O-x_A)*AB],'-r')
print(r"% rayon non dévié, je mets le 0,0 dedans pour les arrow inside")
print(r"\psline[linecolor = red,ArrowInside = ->,arrowscale = 2](",x_deb,",",(x_O-x_deb)/(x_O-x_A)*AB,")(",x_O,",0)(",x_fin,",",(x_O-x_fin)/(x_O-x_A)*AB,")")
#2e rayon facile : parallèle à l'axe optique puis sort en passant par F'
print(r"% rayon indicent parallèle à l'axe optique")
print(r"\psline[linecolor = blue,ArrowInside = ->>,arrowscale = 2,ArrowInsideOffset=-0.3](",
      x_deb,",",AB,")(",x_O,",",AB,")(",x_fin,",",
      -(x_fin-x_O-f_p)/f_p*AB,")")
if x_A-x_O>0:#objet virtuel
    print(r"\psline[linecolor = blue,linestyle = dashed](",
          x_O,",",AB,")(",x_A,",",AB,")")
if x_A_p-x_O<0:#image virtuelle
    print(r"\psline[linecolor = blue,linestyle = dashed](",
          x_O,",",AB,")(",x_A_p,",",A_pB_p,")")
#3e rayon facile : passe par F  ... seulement si x_A n'est pas en F
if (abs(x_A-x_O+f_p)>2**(-8) * delta_x):
    print(r"\psline[linecolor = green,ArrowInside = ->>,nArrows=3,arrowscale = 2,ArrowInsideOffset=0.3](",
        x_deb,",",-(x_deb-x_O+f_p)/(x_O-f_p)*A_pB_p,")(",
        x_O,",",A_pB_p,")(",
        x_fin,",",A_pB_p,")")
    if x_A-x_O>0:#objet virtuel
        print(r"\psline[linecolor = green,linestyle = dashed](",
              x_O,",",A_pB_p,")(",x_A,",",AB,")")
    if x_A_p-x_O<0:#image virtuelle
        print(r"\psline[linecolor = green,linestyle = dashed](",
              x_O,",",A_pB_p,")(",x_A_p,",",A_pB_p,")")
print(r"")
print(r"")
print(r"")
print(r"\end{pspicture*}")



plt.show()




