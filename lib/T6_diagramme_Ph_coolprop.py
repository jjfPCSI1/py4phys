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
Fabrication d'un diagramme (P,h) avec les iso-choses adéquates.
"""

import numpy as np               # Les outils mathématiques
import CoolProp.CoolProp as CP   # Les outils thermodynamiques
import CoolProp.Plots as CPP     # Les outils thermographiques
import matplotlib.pyplot as plt  # Les outils graphiques


print(CP.FluidsList())           # Pour regarder les fluides disponibles
fluide= 'Water'                  # Le choix du fluide
Plogscale = True                 # Axe en pression logarithmique ?
iso_T = True                     # Veut-on des isothermes ?
iso_x = True                     # et les isotitres ?
iso_s = True                     # et les isentropiques ?
iso_v = True                     # et les isochores ?

# Données pour les isothermes
dT = 20                                 # Incrément de températures
Ttriple = CP.PropsSI(fluide,'Ttriple')  # Valeur de la température au point triple
Tcrit = CP.PropsSI(fluide,'Tcrit')      # et au point critique
Tmin = int(Ttriple/10)*10 + 10          # Par défaut, on par près du point triple
val_T = np.arange(Tmin,1.5*Tcrit,dT)    # et on dépasse un peu le point critique
T_to_show = list(range(2,len(val_T),2)) # Sélection des T à afficher (mettre None pour toutes)

# Données pour les isotitres
val_x = np.linspace(0.1,0.9,9)          # Les valeurs des isotitres

# Données pour les isentropiques
ds = 0.5e3
striple_x0 = CP.PropsSI('S','Q',0,'T',Ttriple,fluide) # Entropie triple à gauche
striple_x1 = CP.PropsSI('S','Q',1,'T',Ttriple,fluide) # Entropie triple à droite
val_s = np.arange(striple_x0,striple_x1*1.2,ds)       # Valeurs à tracer
s_to_show = list(range(2,len(val_s),2))               # et à afficher

# Données pour les isochores (réparties de manière logarithmique par défaut)
vcrit = 1/CP.PropsSI(fluide,'rhocrit')                 # Volume massique critique
exp_min = int(np.floor(np.log10(vcrit)))+1             # Puissance de 10 proche
vtriple_x1 = 1/CP.PropsSI('D','Q',1,'T',Ttriple,fluide)# Point triple à droite
exp_max = int(np.ceil(np.log10(vtriple_x1)))-1         # Puissance de 10 proche
# Les valeurs à prendre
val_v = [a * 10**b for a in [1,2,5] for b in range(exp_min,exp_max+1)]
v_to_show = None                                       # On les affiche toutes.

# Quelques constantes
UNITS = {'T': 'K', 'Q': '', 'S': 'kJ/K/kg', 'V': 'm$^3$/kg'}
LABEL = {'T': 'T', 'Q': 'x','S': 's', 'V': 'v'}
COLOR_MAP = {'T': 'Darkred',
             'P': 'DarkCyan',
             'H': 'DarkGreen',
             'V': 'DarkBlue',
             'S': 'DarkOrange',   
             'Q': 'black'}

# On prépare un format pour impression sur A3 ou presque (dimensions en pouces)
plt.figure(figsize=(30,21))

def place_label(x,y,label,indice=None,cotan=False,color='k'):
    """ Routine qui se débrouille pour mettre un label semi-transparent au 
    niveau de la courbe données par ses coordonnées x et y. Si on sait que le 
    label sera presque vertical avec possibilité de dépasser 90°, on peut 
    utiliser cotan=True pour corriger (considération purement esthétique). 
    'indice' correspond à la position dans les tableaux x et y où devra 
    s'afficher le label demandé. """
    print(x[0],y[0],label) # un peu de feedback pour savoir ce qu'on calcule
    N = len(x)//2          # Emplacement par défaut
    if indice: N=indice    # sauf si l'utilisateur impose la valeur
    xi,xf = plt.xlim()     # Les limites en x du graphe
    yi,yf = plt.ylim()     # Pareil en y
    Xsize = xf - xi        # La largeur
    # Pour la hauteur et la pente, cela dépend si les ordonnées sont en repère 
    # logarithmique ou non.
    if Plogscale:
        Ysize = np.log10(yf) - np.log10(yi)
        a = (np.log10(y[N+1])-np.log10(y[N-1]))/(x[N+1]-x[N-1]) * Xsize/Ysize
    else:
        Ysize = yf - yi
        a = (y[N+1]-y[N-1])/(x[N+1]-x[N-1]) * Xsize/Ysize
    bbox = plt.gca().get_window_extent() # Récupération de la taille de la figure
    a *= bbox.height / bbox.width        # Correction de la pente avec la taille 
    rot = np.degrees(np.arctan(a))       # Calcul de l'angle de rotation
    if cotan: rot = 90 - rot             # Si on dépasse la verticale
    t = plt.text(x[N],y[N],label,        # On met le texte au bon endroit
    ha='center',va='center',color=color,rotation = rot) # Avec la bonne rotation
    # On se débrouille pour que la "boîte" d'écriture soit semi-transparente
    t.set_bbox(dict(facecolor='w',edgecolor='None',alpha=0.8))

def fait_isolignes(type,valeurs,position=None,nb_points=1000,to_show=None,round_nb = 0 ):
    """ S'occupe du calcul et du tracé des isolignes. """
    if not(to_show):                        # Valeurs par défauts:
        to_show = list(range(len(valeurs))) # toutes !
    Pmin,Pmax = plt.ylim()                  # On regarde les 
    Hmin,Hmax = plt.xlim()                  # limites du graphique
    # Il y a un bug au niveau des unités du graphe et des points de 
    # représentation, d'où les 1e3 qui trainent un peu partout
    # Par défaut, l'échantillonnage en P est linéaire
    val_P = np.linspace(Pmin*1e3,Pmax*1e3,nb_points) 
    # Sinon, on se met en échelle log. (1e3 -> 3)
    if Plogscale: val_P = 3+np.logspace(np.log10(Pmin),np.log10(Pmax),nb_points)
    # Cas où les lignes ne vont pas sur tout l'éventail des pression, on 
    # échantillonne en températures (car on ne peut pas directement 
    # échantillonner en enthalpie h)
    Tmin = Ttriple
    Tmax = CP.PropsSI('T','P',Pmax,'H',Hmax,fluide)
    val_T = np.linspace(Tmin,Tmax,nb_points)
    # Pour chacune des valeurs demandées, 
    for val,i in zip(valeurs,range(len(valeurs))):
        if type == 'V':  # Cas particulier des volumes massiques: échantillonnage
            val_P = CP.PropsSI('P','T',val_T,'D',1/val,fluide)  # en température
            val_H = CP.PropsSI('H','T',val_T,'D',1/val,fluide)  # et non en P
        else:            # Sinon, on utilise l'éventail des pression
            val_H = CP.PropsSI('H','P',val_P,type,val,fluide)
        if type == 'S': val /= 1e3 # Pour mettre en kJ/K/kg
        if round_nb >0 : val = str(round(val,round_nb)) # Pour faire joli
        else: val = str(int(round(val)))                # là aussi...
        label = '${}={}$ {}'.format(LABEL[type],val,UNITS[type])
        plt.plot(val_H,val_P,color=COLOR_MAP[type])     # Affichage courbe
        if i in to_show: # Ainsi que du label s'il fait partie de la liste
            place_label(val_H,val_P,label,int(position*nb_points))

# Le programme proprement dit commence ici.

ph_plot = CPP.PropsPlot(fluide,'Ph')   # On demande gentiment le plot de base
if Plogscale: plt.yscale('log')        # Passage en log(P)

if iso_x: # Les lignes isotitres sont un peu spéciales, donc ont leur code propre
    ph_plot.draw_isolines('Q',val_x)   # Tracé des lignes isotitres
    # Récupération de la liste des isotitres.
    isoQ = CPP.Plots.IsoLines(fluide,'Ph','Q').get_isolines(val_x)
    for line in isoQ:                  # Rajout des label
        label = line['label'] + line['unit']
        x,y = line['x'],line['y']
        place_label(x,y,label,indice=len(x)//20)

# Ici, on fait toutes les autres isolignes (le boulot a été fait plus haut)
if iso_T: fait_isolignes('T',val_T,position=0.8,to_show=T_to_show)
if iso_s: fait_isolignes('S',val_s,position=0.3,to_show=s_to_show,round_nb=3)
if iso_v: fait_isolignes('V',val_v,position=0.25,to_show=v_to_show,round_nb=3)

plt.grid(which='both') # Rajout de la grille
ph_plot._draw_graph()  # On oblige le dessin avant la sauvegarde
plt.savefig('PNG/T6_diagramme_Ph_coolprop_{}.png'.format(fluide))



