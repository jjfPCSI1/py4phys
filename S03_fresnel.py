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
Programme complet permettant la construction de diagrammes de Fresnel pour que 
les élèves puissent s'entraîner. On génère à la fois un énoncé (avec les ondes 
à sommer) et le corrigé correspondant. Le programme a été pensé pour pouvoir 
sommer plus que deux ondes, même si au-delà de trois, cela devient 
difficilement lisible (de plus, comme on ne doit pas dépasser le cadre, la 
génération aléatoire peut prendre du temps avant de converger).

L'idée est de rassembler les divers énoncés sur certaines pages d'un document 
LaTeX avec les corrigés correspondants sur la page suivant pour que les élèves 
aient tout de suite le corrigé en vue.
'''

from  math import *             # Pour sqrt, pi, cos et Cie
from cmath import *             # Pour les complexes, notamment phase()
import random                   # Pour les tirages aléatoires
import matplotlib.pyplot as plt # Pour les dessins

# Décommenter pour débugguer: afin que l'aléatoire soit toujours le même !
#random.seed(20)

# Les angles dont on prendra des multiples
angles_dict = {'\pi/{}'.format(i):pi/i for i in range(2,7)}
angles = list(angles_dict.keys())
# Les tailles de flèches disponibles
tailles= [1,2,3]
max_size = 4 # Taille max pour l'affichage

def new_polar(z):
    '''Bien sûr, il y a incohérence entre le couple (r,theta) renvoyé par les 
    complexes et l'attente de (theta,r) pour les coordonnées polaires de 
    matplotlib...'''
    p = polar(z)
    return tuple(reversed(p))

def ajoute_fleche(couple,ultra=False,origine = 0j,thin=False):
    '''Rajoute une flèche correspond au complexe du couple (module,phase) 
    donné en argument. Paramètres optionnels:
    * origine (complex): pour décaler l'origine ;
    * ultra (bool): pour une trait plus gros.'''
    if ultra : w,hw = 3,10           # Veut-on un trait plus épais ?
    elif thin: w,hw = 0.1,0.1        # ou plus fin ?
    else     : w,hw = 1,7            # sinon une taille normale
    c = rect(*couple)                # Conversion en complexe
    if abs(c) > max_size: raise      # Si on dépasse, c'est la fin !
    plt.annotate('',xytext=new_polar(origine),
                    xy=new_polar(origine+c),
        arrowprops=dict(width=w,facecolor='black',headwidth=hw))

def pointilles(liste_de_couples,reverse=False):
    '''Construit les pointillés pour relier le départ à l'arrivée.'''
    s = ''
    ldc = liste_de_couples[:]
    if reverse: ldc.reverse()
    somme = rect(*ldc[0])
    R,THETA = [ldc[0][0]],[ldc[0][1]]
    for i in range(len(liste_de_couples)-1):
        ajoute_fleche(ldc[i+1],origine=somme,thin=True)
        somme += rect(*ldc[i+1])

def get_one(iterable):
    '''Histoire de pouvoir récupérer un élément au hasard dans une liste.'''
    nb = random.randint(0,len(iterable)-1)
    return iterable[nb]

def enonce_et_corrige(nb_ondes=2,num_fichier = 1):
    '''Tirage au sort de valeurs et construction d'un énoncé et du corrigé 
    correspondant. Renvoie un couple de nom des fichiers (énoncé,corrigé).'''
    # Initialisation
    ondes_enonce = [] # liste de strings
    ondes_corrige= [] # liste de couples (norme,argument)
    # Quelques tableaux utiles
    sin_cos = [r'\cos',r'\sin']
    signes  = [' ','+','-']   # 1 -> +, -1 -> -
    # Et c'est parti pour la sélection !
    for i in range(nb_ondes): # Tirage des ondes
        nb_phi = random.randint(0,10)# Le nombre multipliant l'angle
        sincos = random.randint(0,1) # Tirage à pile ou phase pour sinus ou cosinus
        signeA = (-1)**random.randint(0,1) # Signe aléatoire pour l'amplitude
        signeP = (-1)**random.randint(0,1) # et pour la phase
        A = signeA * get_one(tailles)
        phi = get_one(angles)
        # Le cas particulier où l'amplitude est unitaire
        if   A ==  1: Astring = ''
        elif A == -1: Astring = '-'
        else :        Astring = str(A)
        # Et si le facteur multiplicatif est nul ou unitaire
        if   nb_phi == 0: phi_string = ''
        elif nb_phi == 1: phi_string = '{}{}'.format(signes[signeP],phi)
        else :            phi_string = '{}{}{}'.format(signes[signeP],nb_phi,phi)
        # Construction de la chaîne de l'énoncé
        enonce = "{}{}(\omega t{})".format(Astring,sin_cos[sincos],phi_string)
        ondes_enonce.append(enonce)
        # Maintenant on calcule module et argument
        module = A
        # sin(x) = cos(x *-* pi/2)
        argument = angles_dict[phi]*nb_phi*signeP - sincos*pi/2
        ondes_corrige.append((module,argument))
    # Reste à faire le corrigé et l'énoncé
    enonce  = fabrique_enonce_fresnel(ondes_enonce,num_fichier)
    try:    # Cas où cela dépasse du cadre
        corrige=fabrique_corrige_fresnel(ondes_corrige,ondes_enonce,num_fichier)
    except: # Et on reessaie un coup ! 
        return enonce_et_corrige(nb_ondes)
    # Sinon c'est bon.
    return enonce,corrige

def initialisation_graphe(ondes,enonce=True):
    plt.clf()            # Nettoyage, on commence un nouveau graphe
    plt.axes(polar=True) # On initie un graphe en polaires
    # Puis on définit le titre
    if enonce: titre = 'Enonce: Sommer '
    else     : titre = 'Corrige: Sommer '
    titre += ", ".join(['${}$'.format(o) for o in ondes[:-1]])
    titre += " et ${}$.".format(ondes[-1])
    plt.title(titre)
    # et finalement les grilles en distances
    plt.rgrids([i+1 for i in range(max_size)])
    plt.thetagrids([i*15 for i in range(360//15)]) # et en angles

                                            
def fabrique_enonce_fresnel(ondes,num_fichier):
    '''À partir d'une série d'ondes sous forme de chaînes de caractère, 
    construit l'énoncé de la résolution avec Fresnel. Renvoie le nom du 
    fichier sauvegardé'''
    initialisation_graphe(ondes)
    fichier = 'PNG/{}ondes_enonce_{:03d}'.format(len(ondes),num_fichier)
    plt.savefig(fichier)
    return fichier

def fabrique_corrige_fresnel(liste_des_couples,ondes_enonces,num_fichier):
    '''Fabrication du corrigé pour les diagrammes de Fresnel correspondant à 
    une somme d'au moins deux ondes (mais potentiellement plus). La liste des 
    ondes se présente sous forme d'une liste de couples (norme,argument) à 
    chaque fois. Renvoie une chaîne correspondant au dessin TikZ final, ainsi 
    que l'amplitude et la phase (en degrés) pour possible affichage.'''
    # Première étape: initialisation
    initialisation_graphe(ondes_enonces,enonce=False) 
    # Puis, on ordonne par angle croissant
    ldc = sorted(liste_des_couples, key=lambda c: (c[1]-pi)%(2*pi) )
    point_final = 0
    for c in ldc:
        ajoute_fleche(c)         # Les flèches individuelles
        point_final += rect(*c)  # On ajoute au total (en complexe)
    ajoute_fleche(polar(point_final),ultra=True) # La flèche finale
    # On rajoute aussi la construction en pointillés
    pointilles(ldc)              # dans un sens
    pointilles(ldc,reverse=True) # et dans l'autre
    fichier = 'PNG/{}ondes_corrige_{:03d}'.format(len(ondes_enonces),num_fichier)
    plt.savefig(fichier)
    return fichier

# Exemple d'utilisation de tout ceci:
for i in range(5):
    fichier_enonce,fichier_corrige = enonce_et_corrige(2,i)
    # Ne reste plus qu'à faire quelque chose de ces noms de fichier, par 
    # exemple écrire un fichier .tex au vol...


