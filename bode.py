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



'''
Petit module pour rassembler la procédure de tracé de diagramme de Bode pour 
pouvoir se concentrer uniquement sur ce qu'il y a autour.
'''

import matplotlib.pyplot as plt  # Pour les dessins

def diag_bode(f,GdB,phase,out_file,titre=None):
    '''Dessine un diagramme de bode quand on donne la fréquence, le gain et la 
    phase correspondants. Le résultat est écrit dans le fichier 'out_file'.'''
    plt.figure()                 # Ouverture de la figure
    plt.subplot(211)             # La première sous-figure
    if titre: plt.title(titre)   # Rajout du titre si demandé
    plt.semilogx(f, GdB)         # Graphique semi-log en x pour le gain
    plt.grid(which='both')       # On rajoute la grille
    plt.ylabel(r'Gain (dB)')     # Label vertical
    plt.subplot(212)             # La seconde sous-figure
    plt.semilogx(f, phase)       # Graphique semi-log en x pour la phase
    plt.ylabel(r'Phase (deg)')   # Label en y
    plt.xlabel(r'Frequence (Hz)')# et label en x commun
    plt.grid(which='both')       # On rajoute la grille
    plt.savefig(out_file)        # Sauvegarde du fichier
    plt.close()                  # et fermeture de la figure

# Le module signal possède une fonction "bode" dédiée que l'on va utiliser
from scipy import signal

def second_ordre(f0,Q,filename='defaut.png',type='PBs',f=None):
    '''Petite fonction pour faciliter l'utilisation de la fonction "bode" du 
    module "signal" quand on s'intéresse à des filtres du 2e ordre. Il suffit 
    de donner la fréquence propre f0 et le facteur de qualité Q pour obtenir 
    ce que l'on veut. Autres paramètres:
    * filename: le nom du fichier ('defaut.png' par défaut)
    * type: le type du filtre, à choisir parmi 'PBs' (passe-bas), 
    'PBd' (passe-bande) et 'PHt' (passe-haut). On peut aussi définir soi-même 
    le numérateur sous forme d'une liste de plusieurs éléments, le degré le 
    plus haut donné en premier. NB: le '1.01' des définitions est juste là 
    pour améliorer sans effort le rendu graphique.
    * f: les fréquences à échantillonner (si None, la fonction choisit 
    d'elle-même un intervalle adéquat).
    '''
    den = [1./f0**2,1./(Q*f0),1]              # Le dénominateur de la fonction de transfert
    if   type == 'PBs': num = [1.01]          # Le numérateur pour un passe-bas
    elif type == 'PBd': num = [1.01/(Q*f0),0] # pour un passe-bande
    elif type == 'PHt': num = [1.01/f0**2,0,0]# pour un passe-haut
    else: num = type                          # sinon, c'est l'utilisateur qui le définit.
    s1 = signal.lti(num,den)                  # Définition de la fonction de transfert
    f, GdB, phase = signal.bode(s1,f)         # Obtention des valeurs adéquates
    diag_bode(f,GdB,phase,filename)           # Dessin du diagramme proprement dit



