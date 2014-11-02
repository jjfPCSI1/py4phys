# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.



import numpy as np               # Les outils mathématiques
import CoolProp.CoolProp as CP   # Les outils thermodynamiques
import matplotlib.pyplot as plt  # Les outils graphiques

""" 
Fabrication d'un diagramme (P,v) avec CoolProp, ce qui n'est pas possible 
en natif car ils travaillent en masse volumique et non en volume massique par 
défaut.
"""

def diagramme_Pv(fluide,dico={}):
    """ Dessine le diagramme Pv pour le fluide demandé avec des 
    choix par défaut qui peuvent être "overridden" en spécifiant ceux à 
    changer dans le dictionnaire 'dico'. Les options disponibles sont:
    * 'vmin' et 'vmax' pour définir les limites des échantillonnages en volume 
    massique. Par défaut vtripleL et vtripleG * 10
    * 'Prange' pour l'intervalle de pression affiché
    * 'T': une liste des températures pour lesquelles il faut tracer 
    l'isotherme. (défaut à None)
    * 'x': une liste des titres en vapeur pour lesquels il faut tracer la 
    courbe isotitre (défaut à np.linspace(0,1,11))
    * 'titre': le titre (textuel, hein...) à donner au graphique.
    * 'fichier': le nom du fichier dans lequel enregistrer la figure.
    * 'logx': Booléen indiquant si on veut un axe logarithmique en abscisse
    * 'logy': Booléen indiquant si on veut un axe logarithmique en ordonnée
    * 'legend': Booléen indiquant si on veut rajouter les légendes
    * 'saturation': Booléen indiquant si on veut rajouter la courbe de 
    saturation au tracé (défaut à True)
    """
    Pcritique = CP.PropsSI(fluide,'pcrit')  # Pression
    Tcritique = CP.PropsSI(fluide,'Tcrit')  # et température critique
    Ptriple = CP.PropsSI(fluide,'ptriple')  # Pression 
    Ttriple = CP.PropsSI(fluide,'Ttriple')  # et température au point triple
    # On récupère les volumes massiques via les 'densités' (ie masses 
    # volumiques) données par CoolProp
    vtripleL = 1/CP.PropsSI('D','P',Ptriple,'Q',0,fluide)
    vtripleG = 1/CP.PropsSI('D','P',Ptriple,'Q',1,fluide)
    vcritique= 1/CP.PropsSI('D','P',Pcritique,'T',Tcritique,fluide)
    P_sat= np.linspace(Ptriple,Pcritique,1000)
    # L'ensemble des valeurs par défaut.
    DEFAUTS = {'vmin':vtripleL, 'vmax':vtripleG*10, 
       'Prange': None, 
       'T': None, 'x': np.linspace(0,1,11),
       'titre': "Diagramme $(P,v)$ pour le fluide {}".format(fluide),
       'fichier': 'PNG/T2_diagramme_Pv_coolprop_{}.png'.format(fluide),
       'logx': True, 'logy': True, 'legend': False,
       'saturation': False}
    DEFAUTS.update(dico)      # Mise à jour des valeurs par défaut via 'dico' 
    # L'échantillonnage sera différent
    if DEFAUTS['logx']:       # si l'axe est logarithmique
       v=np.logspace(np.log10(DEFAUTS['vmin']),np.log10(DEFAUTS['vmax']),1000)
    else:                     # ou simplement linéaire
       v=np.linspace(DEFAUTS['vmin'],DEFAUTS['vmax'],1000)
    if DEFAUTS['T'] != None:
        for Ti in DEFAUTS['T']:   # Tracé des différentes isothermes
            P = CP.PropsSI('P','T',Ti,'D',1/v,fluide)
            plt.plot(v,P,label='$T={}$'.format(Ti))
    if DEFAUTS['x'] != None:
        for xi in DEFAUTS['x']:   # Tracé des courbes isotitre
            vxi = 1/CP.PropsSI('D','P',P_sat,'Q',xi,fluide)
            plt.plot(vxi,P_sat,'k',label='$x={}$'.format(xi))
    if DEFAUTS['saturation']: # Tracé de la courbe de saturation
        v_eb   = 1/CP.PropsSI('D','P',P_sat,'Q',0,fluide)
        v_rosee= 1/CP.PropsSI('D','P',P_sat,'Q',1,fluide)
        plt.plot(v_eb,P_sat,'k',linewidth=4.0)
        plt.plot(v_rosee,P_sat,'k',linewidth=4.0)
    if DEFAUTS['Prange']: plt.ylim(DEFAUTS['Prange']) # Intervalle vertical
    plt.xlim((DEFAUTS['vmin'],DEFAUTS['vmax']))       # Intervalle horizontal
    if DEFAUTS['logx']: plt.xscale('log')             # Echelle log en x
    if DEFAUTS['logy']: plt.yscale('log')             # Echelle log en y
    if DEFAUTS['legend']: plt.legend()                # Rajout des légendes
    plt.xlabel('Volume massique $v$ en m$^3/$kg')     # Légende en abscisse
    plt.ylabel('Pression en Pa')                      # Légende en ordonnée
    plt.title(DEFAUTS['titre'])                       # Titre
    plt.savefig(DEFAUTS['fichier'])                   # Enregistrement
    plt.clf()                                         # Nettoyage

# Le fluide à étudier (à choisir parmi ceux donnés par CP.FluidsList())
fluide = 'Water'

# Le diagramme "par défaut"
diagramme_Pv(fluide)

# Les valeurs suivantes ont été choisies suite à l'observation du diagramme 
# par défaut. Il faudra certainement changer les valeurs si vous modifiez le 
# fluide
dico = {'Prange':(1e7,3e7),
        'fichier':'PNG/T2_diagramme_Pv_coolprop_{}_lin.png'.format(fluide),
        'logx':False, 'logy': False,
        'vmin': 1e-3, 'vmax':1e-2}
diagramme_Pv(fluide,dico)



