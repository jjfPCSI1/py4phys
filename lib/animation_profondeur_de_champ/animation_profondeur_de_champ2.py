# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 10:36:53 2019

@author: Vincent Grenard

Programme permettant d'illustrant la notion d'image nette, de profondeur de 
champ et l'évolution de la netteté de l'image dans le cas d'une lentille et 
d'un objet réel avec :
    - la position de l'écran (L)
    - la taille du diaphragme (R)
Montre aussi que la notion de stigmatisme dépend de la résolution du capteur
en utilisant une image fortement pixelisée pour laquelle on peut remarquer que
la profondeur de champ est plus grande.

Nécessite une image de résolution raisonnable pour les démonstrations, le nom 
de l'image se réglant dans la variable "nom_image" au début du programme


On peut en théorie au début du programme faire varier 
    - la distance focale fp
    - la position de l'objet xA
    - la largeur de l'image
Toutefois, certaines dimensions dans matplotlib risquent ensuite de ne plus 
être adaptées.

Remarque, la luminositée est automatiquement adapté, cela cache donc le fait 
que diminuer la taille du diaphragme diminue fortement la luminosité de l'image

Les calculs sont fait dans le cadre de l'approximation des petits angles, ne 
tient pas compte du côté non stigmatique des lentilles, en particulier aux 
grandes ouvertures. Calculs non garantis car fait vite fait sur un brouillon.
(Basé sur le formalisme de l'optique matricielle, plus facile qu'avec les 
relations de conjugaison et de la trigo)

Ne tiens pas compte non plus du phénomène de diffraction qui est le phénomène
(à ma connaissance) qui limite la résolution lorsque les diaphragmes sont très
fermés.

"""

import numpy as np #testé avec np.__version__ 1.16.1
import matplotlib.pyplot as plt #testé avec matplotlib.__version__ 2.0.0
import PIL.Image as im#attention à la majuscule ; testé avec PIL.__version__ '5.4.1'
from matplotlib.widgets import Slider, Button#, RadioButtons
from scipy.signal import fftconvolve #testé avec scipy.__version__ 1.2.1


####### définition des constante et valeurs initiales
nom_image = "cachotier.png" #nom de l'image si dans le même dossier, nom avec le chemin relatif ou absolu si dans un autre dossier
#l'image avec laquelle j'ai fait les tests était de taille 665 x 1000 x 3 ; je ne gère pas le canal alpha s'il y en a un


fp = 1 #distance focale de la lentille
xA = -2 #position algébrique de l'objet
#yB déterminé par la position du pixel sur l'image comme étant l'écart à l'axe optique
largeur_image = 1# ne sert pas forcément à grand chose vu que tout est "relatif"


inf = float("inf")
#####   limite de l'espace  pour matplotlib  #####
xAp = 1/(1/fp+1/xA) #position de l'image
lim = [xA,xAp*2,-4,4]   # xdeb xfin ydeb yfin
marge = 0.05
x_deb = lim[0]
x_fin = lim[1]
y_deb = lim[2]
y_fin = lim[3]
delta_x = x_fin - x_deb
delta_y = y_fin - y_deb
###### fin de déf des constantes

###### chargement de l'image + conversion numpy
objet = np.array(im.open(nom_image))*1.0/255#PIL=> Numpy (float entre 0 et 1)




#création d'une image perso avec quelques points bleu rouge etc...
test = np.zeros((2**10,4*2**10,3)) #on va downsample après pour faire apparaitre les pixels volontairement
x_test = np.linspace(-4,4,4*2**10)
y_test = np.linspace(-1,1,2**10)
X_test, Y_test = np.meshgrid(x_test, y_test)
liste_cercle = [(-2+0.5,-0.25,0.45,[1,0,0]), #(position_centre_x, position_y, rayon, couleur)
                (-1+0.5,-0.25,0.45,[0,1,0]),
                (-1.5+0.5,-0.25+2**-0.5,0.45,[0,0,1]),
                (2+0.5,0.25,0.65,[1,1,0]), 
                (1+0.5,0.25,0.65,[0,1,1]),
                (1.5+0.5,+0.25-2**-0.5,0.65,[1,0,1]),]

for xc, yc, rc, coul in liste_cercle:
    indices = (X_test-xc)**2+(Y_test-yc)**2 <= rc**2
    test[indices] += coul
    indices = test>1
    test[indices] = 1

#downsample
def divise_par_deux_taille_image(im):
    """
    Fonction qui divise par 2 la taille d'une image en x et en y en lissant 
    (moyenne sur 4 pixels => 1 pixel)
    """
    if im.shape[0]%2==1: #gestion des tailles d'image impaires
        im = im[:-1]
    if im.shape[1]%2==1: #idem
        im = im[:,:-1]
    im = (im[::2,::2]+im[1::2,::2]+im[::2,1::2]+im[1::2,1::2])*0.25
    return im
for i in range(3): #utilise l'oversampling pour avoir un cercle aliasé "correctement"
    test = divise_par_deux_taille_image(divise_par_deux_taille_image(test))
test[1:-1,0:4] = [0,0,1] #drapeau bleu
test[1:-1,4:8] = [1,1,1] #blanc
test[1:-1,8:12] = [1,0,0]#rouge
objet_perso = test #objet fortement pixelisé


fig = plt.figure(figsize = [10,6])

###### création des sliders
#([0.58,0.35,0.4,0.65]) pour les tracé de rayon
axcolor = 'lightgoldenrodyellow'
ax_R = plt.axes([0.58, 0.1, 0.37, 0.1], facecolor=axcolor)
ax_L = plt.axes([0.58, 0.225, 0.37, 0.1], facecolor=axcolor)

slider_R = Slider(ax_R, 'R', 0.001,0.8*y_fin, valinit=1)#, valstep=1)
slider_L = Slider(ax_L, 'L', xAp/2, xAp*2, valinit=xAp)
R = slider_R.val #pour les initialisations




axe_tout_noir = plt.axes([0.00,0.18,0.575,0.99]) ## pour mettre l'image sur un fond noir, mais pas toute la figure
plt.axis("off")
plt.imshow(np.zeros(objet.shape))

axe_image = plt.axes([0.035,0.2,0.5,0.95])
plt.axis("off")

image_plot = plt.imshow(objet)

axe_image2 = plt.axes([0,0,0.55,0.2])
image_perso_plot = plt.imshow(objet_perso)
plt.axis("off")



###############################################################################
###############################################################################
#                                                                             #
#                   gestion du floutage de l'image                            #
#                                                                             #
###############################################################################
###############################################################################



def pos_image(xA, yB, xE):
    """ 
    fonction qui détermine la position de l'image sur l'écran (écart à l'axe 
    optique, il faudra aussi trouver les indices correspondant à un moment !)
    Arguments :
        - xA la position algébrique de l'objet sur l'axe optique ; un nombre
        - fp la distance focale de la lentille ; un nombre
        - yB l'écart de l'objet à l'axe optique ; matrice ou nombre
        - xE la position algébrique de l'écran sur lequel on visualise sur l'axe optique ; un nombre
        - R le rayon du diaphragme supposé collé à la lentille ; un nombre
    Hypothèse :
        - position de la lentille : origine des positions
        - xA < 0 et xE > 0
    Renvoie : y_im
        - y_im l'écart de l'image à l'axe optique ; matrice ou nombre (comme yB)
    """
    y_im = yB/xA*xE    #position de l'image sur l'écran, thalès
    return y_im
def rayon_image(xA, fp, xE, R):
    """ 
    fonction qui détermine le rayon des taches créées par des objets ponctuel
    ramené à la taille de l'objet ; but : ne pas se casser la tête si possible 
    pour recréer l'image en reprennant simplement l'objet
    Arguments :
        - xA la position algébrique de l'objet sur l'axe optique
        - fp la distance focale de la lentille
        - xE la position algébrique de l'écran sur lequel on visualise sur l'axe optique
        - R le rayon du diaphragme supposé collé à la lentille
    Hypothèse :
        - position de la lentille : origine des positions
        - xA < 0 et xE > 0
    Renvoie : r_im
        - r_im le rayon occupé par l'image sur l'écran ; un nombre
    """
    r_im = R*xE*(1/xE-1/xA-1/fp) #la parenthèse vaut 0 si la relation de conjugaison est vérifiée
    return abs(r_im)
#idée : normaliser le rayon sur l'image par la taille de l'image pour pouvoir afficher objet et image avec la même taille
#et au passage ne pas se casser la tête à retourner l'image

def rayon_image_normalise(xA, fp, xE, R):
    """ 
    fonction qui détermine le rayon des taches créées par des objets ponctuel 
    optique, il faudra aussi trouver les indices correspondant à un moment !)
    
    la dimension du rayon des tache est normalisée pour correspondre à la 
    taille de l'objet et non à celle de l'image.
        
    Arguments :
        - xA la position algébrique de l'objet sur l'axe optique
        - fp la distance focale de la lentille
        - xE la position algébrique de l'écran sur lequel on visualise sur l'axe optique
        - R le rayon du diaphragme supposé collé à la lentille
    Hypothèse :
        - position de la lentille : origine des positions
        - xA < 0 et xE > 0
    Renvoie : r_im
        - r_im le rayon occupé par l'image sur l'écran ; un nombre
    """
    r_im = R*xE*(1/xE-1/xA-1/fp) #la parenthèse vaut 0 si la relation de conjugaison est vérifiée
    return abs(r_im*xA/xE)

def floute_image(xA, fp, xE, R, objet):
    """ 
    fonnction qui détermine le rayon des taches créées par des objets ponctuel 
    optique, il faudra aussi trouver les indices correspondant à un moment !)
    Arguments :
        - xA la position algébrique de l'objet sur l'axe optique
        - fp la distance focale de la lentille
        - xE la position algébrique de l'écran sur lequel on visualise sur l'axe optique
        - R le rayon du diaphragme supposé collé à la lentille
        - objet l'image que l'on va flouter
    Hypothèse :
        - position de la lentille : origine des positions
        - xA < 0 et xE > 0
    Renvoie : resultat l'image floutée
    """
    dim_objet = objet.shape[:2]#nb_ligne et col
    rayon = rayon_image_normalise(xA, fp, xE, R) #rayon de la tache (cercle de confusion ?)
    
    ########## suggestion JB Caussin : faire des conv2D a l'aide d'une bibliothèque
    ##créer la matrice qui va bien
    #conversion rayon/indices dim_image[1] correspond à 2*largeur image
    
    rayon_indices = rayon*dim_objet[1]/(2*largeur_image) #non entier
    #print(rayon_indices)
    ###### Mauvaise solution pour éviter les bugs lorsque l'image est trop floues : limiter artificiellement le rayon du cercle de confusion vu qu'on voit déjà plus rien de toutes façons
    if rayon_indices > 650:
        rayon_indices = 650
        print("attention, saturation du floutage pour éviter de 'planter' l'ordinateur")
    elif rayon_indices == 0:
        mat_convol = np.zeros((3,3))
        mat_convol[1,1] = 1
    elif rayon_indices <= 1e-3:#problème lors que le rayon est tellement faible que même avec oversampling y'a aucun point d'allumé dans la matrice
        mat_convol = np.zeros((3,3))
        mat_convol[1,1] = 1
    else:
        dim_convol = 3*int(np.ceil(rayon_indices)) #3 pour avoir gauche, milieu, droite
        #sinon des problèmes quand faible rayon : matrice 2x2 avec 4 fois 0.25 alors qu'au final on s'attend à peu de flou
        
        #Oversampling : L'oversampling est une méthode simple mais extrêmement coûteuse en performance. Il s'agit de calculer une image deux ou quatre fois plus grande que la résolution souhaitée, puis de la réduire jusqu'à cette dernière. L'interpolation de la grande image en petite image élimine d'elle-même toute trace d'aliasing.
        
        N_fact = int(np.log2(1024/dim_convol))
        facteur = 2**N_fact
        mat_convol_oversampling = np.zeros((facteur*dim_convol, facteur*dim_convol))
        x_oversampling = np.linspace(-0.5*facteur*dim_convol, 0.5*facteur*dim_convol,facteur*dim_convol)
        X_over, Y_over = np.meshgrid(x_oversampling, x_oversampling)
        mat_convol_oversampling[X_over**2+Y_over**2<=(rayon_indices*facteur)**2] = 1
        mat_convol = mat_convol_oversampling
        for i in range(N_fact):
            mat_convol = divise_par_deux_taille_image(mat_convol)
        if np.sum(mat_convol) == 0:
            mat_convol[1,1] = 1
        mat_convol = mat_convol/np.sum(mat_convol) #normalisation pour l'intensité lumineuse
    
    mode = "same" #full ou valid ou same ; détermine la taille de l'image après convolution
    
    resultatr = fftconvolve(objet[:,:,0], mat_convol, mode)
    resultatv = fftconvolve(objet[:,:,1], mat_convol, mode)
    resultatb = fftconvolve(objet[:,:,2], mat_convol, mode)
    
    dim_convol = resultatr.shape
    resultat = np.zeros((dim_convol[0],dim_convol[1],3))
    resultat[:,:,0] = resultatr
    resultat[:,:,1] = resultatv
    resultat[:,:,2] = resultatb
        
    return resultat

###############################################################################
###############################################################################
#                                                                             #
#              fin de la gestion du floutage de l'image                       #
#                                                                             #
###############################################################################
###############################################################################




###############################################################################
###############################################################################
#                                                                             #
#                     gestion du tracé des rayons                             #
#                                                                             #
###############################################################################
###############################################################################

liste_pos_lentilles = [0] #position sur l'axe des abscisses des différentes lentilles
liste_dists_focales = [fp]#distances focales correspondantes
x_A = xA #position de l'objet
AB = largeur_image  #ordonnée/taille de l'objet ; si XA est inf, alors représente l'angle des rayons incidents
#liste_angle = np.arange(-150,150,5)#en degré ; si Xa esdt inf, alors représente la liste des y pour les rayons incidents
def calcule_liste_angle(R):
    """ calcule la liste des angles que l'on va tracer de façon à avoir
    10 rayons qui heurte le diaphragme en haut, 10 en bas, et 10 qui "passent"    
    """
    angle_diaphg_haut = (R - AB)/(-xA)*0.995
    angle_diaphg_bas = (-R - AB)/(-xA)*0.995
    angle_ext_haut = (y_fin - AB)/(-xA)
    angle_ext_bas = (y_deb - AB)/(-xA)
    liste_angle = np.hstack((np.linspace(angle_ext_bas,angle_diaphg_bas,10),
                             np.linspace(angle_diaphg_bas,angle_diaphg_haut,10),
                             np.linspace(angle_diaphg_haut,angle_ext_haut,10)))
    return liste_angle
liste_angle = calcule_liste_angle(R)#en degré ; si Xa esdt inf, alors représente la liste des y pour les rayons incidents
#en fait, ne pas se limiter à 90 car approx petits angles pourries et que c'est plutôt la liste des tangentes

              

#liste des couleurs dispo dans pstricks
couleurs_all = "blue","red","green","cyan","magenta","yellow","gray"

#####   calculs    #####
def calcule_liste_pos_et_taille_image():
    """ fonction qui calcule une liste d'image et de position compte tenu d'un
    objet et d'une liste de lentille,
    franchement pas très pertinent ici car une seule lentille, mais programme
    repris par paresse en faisant une liste d'une seule lentille ...    
    
    """
    ###BUG : gérer le cas x_A = - f_p
    ###à améliorer en prennant en compte les angles
    liste_image = [] #on ne les mettra pas si image à l'infini
    liste_taille_image = [] #on ne les mettra pas si image à l'infini, mais je gère mal la taille du coup
    x_A_temp = x_A #variable qui va changer, on sépare de xA pour pas modifier les paramètres
    AB_temp = AB
    if abs(x_A) == inf:
        angle = np.deg2rad(AB)
    for x_O, f_p in zip(liste_pos_lentilles, liste_dists_focales):
        if x_O >= x_fin:
            break # pour gérer le cas où on a rajouté la lentille virtuelle à la fin
        if x_A_temp == x_O-f_p:
            x_A_p = inf
            angle = (0 - AB_temp)/(x_O-x_A_temp)
            A_pB_p = inf
        elif abs(x_A_temp) == inf:
            x_A_p = x_O + f_p
            A_pB_p = angle * f_p 
        else:
            # relation de conjugaison : p'= pf'/(p+f')
            # p = OA = x_A-x_O
            x_A_p = x_O + (x_A_temp-x_O) * f_p /( (x_A_temp-x_O) + f_p)
            # grandissement : A_pB_p/AB = OA_p/OA = p'/p = f'/(p+f')
            A_pB_p = AB_temp *  f_p /( (x_A_temp-x_O) + f_p)
        liste_image.append(x_A_p)
        liste_taille_image.append(A_pB_p)
        x_A_temp = x_A_p
        AB_temp = A_pB_p
    return liste_image, liste_taille_image
liste_pos_image, liste_taille_image = calcule_liste_pos_et_taille_image()

def traverse_vide(x_old,y_old,theta_old,x_new):
    """ optique matricielle 
        traversé du vide : theta inchangé, y change : ynew = yold + theta*dist
    """
    return y_old + (x_new-x_old)*theta_old #theta_new = theta_old
def traverse_lentille(y_old,theta_old,fp):
    """ optique matricielle 
        traversé d'une lentille : y inchangé, theta_new = theta_old - y/f'
    """
    theta_new = -y_old/fp + theta_old
    return theta_new #y_new = y_old


liste_trace_matplotlib = [] #liste qui contient les lignes pour les tracés de rayons à l'aide de matplotlib, permettra la mise à jour lorsqu'on bouge les sliders avec des set_data

def trace_matplotlib_initial():
    """
    Tracé à l'aide de matplotlib ; initialisation
    
    """
        
    #ajoute une lentille virtuelle à la fin pour pas avoir à gérer différemment le dernier espace vide
    if liste_pos_lentilles[-1] != x_fin: #inutile de le faire plusieurs fois
        liste_pos_lentilles.append(x_fin)
        liste_dists_focales.append(float("inf"))
        
    #tracé de chaque rayon
    for angle in liste_angle:
        #angle = np.deg2rad(angle_deg)    #déjà en rad maintenant
        liste_x_rayons = [x_deb]
        liste_y_rayons = [AB+angle*(x_deb-x_A)]
        x_old = x_deb
        y_old = liste_y_rayons[0]
        theta_old = angle
        
        for ind in range(len(liste_pos_lentilles)): #ridicule ici car une seule lentille, mais repris par paresse
            #pour chaque lentille 
            
            #traverse le vide jusqu'à la lentille
            x = liste_pos_lentilles[ind]
            y = traverse_vide(x_old, y_old, theta_old, x)
            theta = theta_old
            
            #passe la lentille
            if ind == 0 or abs(y_old) < R: #diaphragme
                #ind == 0 pour avoir le tracé jusqu'à la lentille
                #y_old car dernière lentille virtuel => il faut avoir passé le diaphragme au niveau de la lentille précédente
                
                theta = traverse_lentille(y,theta, liste_dists_focales[ind])
                
                #met à jour le x_old y_old theta_old
                x_old = x
                y_old = y
                theta_old = theta
                
                #met à jour les listes pour tracer les rayons
                liste_x_rayons.append(x)
                liste_y_rayons.append(y)
        
        
            #gérer l'espace vide après la dernière lentille fait en rajoutant une fausse lentille
        
        trace, = plt.plot(liste_x_rayons, liste_y_rayons) # attention à la p*** de virgule à cause de ce que renvoie matplotlib : PLUSIEURS tracé
        
        liste_trace_matplotlib.append(trace)

    #tracé du diaphragme
    global diaphragme_bas, diaphragme_haut
    diaphragme_bas, = plt.plot([-0.075,-0.075],[0.9*y_deb, -R],'-',lw = 5, color = [0.5,0.5,0.5])
    diaphragme_haut, =plt.plot([-0.075,-0.075],[0.9*y_fin, R],'-',lw = 5, color = [0.5,0.5,0.5])
    
    #tracé écran
    global trace_ecran
    trace_ecran, = plt.plot([xAp]*2,[y_deb, y_fin], "--k")
    
    #tracé objet +lentilles
    plt.plot([x_A,x_A], [0,AB])
    
    #axe optique
    plt.plot([x_deb,x_fin],[0,0],'-k')#axe optique
    deb_fleche = x_fin - 0.025*delta_x
    altitude_fleche = delta_y * 0.025
    plt.plot( [deb_fleche,x_fin,deb_fleche],[altitude_fleche,0,-altitude_fleche],'-k') # flèche
    
    #lentille
    x_O, f_p = liste_pos_lentilles[0], liste_dists_focales[0] #une seule lentille ici en fait
    plt.plot([x_O,x_O],[0.995*y_deb,0.995*y_fin],'-k',lw=2)
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
    plt.axis('off')
    plt.axis(lim)

diaphragme_bas = 0
diaphragme_haut = 0
trace_ecran = 0
def update_trace_rayon(R,L):
    """
    Met à jour le tracé des rayons en fonction de la taille du diaphragme R et 
    de la distance L entre la lentille et l'écran
    
    """
    liste_angle = calcule_liste_angle(R)#en degré ; si Xa esdt inf, alors représente la liste des y pour les rayons incidents

    
    #diaphragme
    diaphragme_bas.set_ydata([0.9*y_deb, -R])
    diaphragme_haut.set_ydata([0.9*y_fin, R])
    #ecran
    trace_ecran.set_xdata([L]*2)
    #tracé de chaque rayon
    for ind_angle,angle_deg in enumerate(liste_angle):
        angle = angle_deg
        liste_x_rayons = [x_deb]   
        liste_y_rayons = [AB+angle*(x_deb-x_A)]     
        x_old = x_deb
        y_old = liste_y_rayons[0]
        theta_old = angle
        for ind in range(len(liste_pos_lentilles)):
            #pour chaque lentille 
            
            #traverse le vide jusqu'à la lentille
            x = liste_pos_lentilles[ind]
            y = traverse_vide(x_old, y_old, theta_old, x)
            theta = theta_old
            
            #passe la lentille
            if ind == 0 or abs(y_old) < R: #diaphragme
                #ind == 0 pour avoir le tracé jusqu'à la lentille
                #y_old car dernière lentille virtuel => il faut avoir passé le diaphragme au niveau de la lentille précédente
                
                theta = traverse_lentille(y,theta, liste_dists_focales[ind])
                
                #met à jour le x_old y_old theta_old
                x_old = x
                y_old = y
                theta_old = theta
                
                #met à jour les listes pour tracer les rayons
                liste_x_rayons.append(x)
                liste_y_rayons.append(y)
        
        
            #gérer l'espace vide après la dernière lentille fait en rajoutant une fausse lentille
        
        liste_trace_matplotlib[ind_angle].set_data(liste_x_rayons, liste_y_rayons)


axe_trace_rayon = plt.axes([0.58,0.35,0.4,0.65])
plt.axis("off")
trace_matplotlib_initial()

###############################################################################
###############################################################################
#                                                                             #
#               fin de la gestion du tracé des rayons                         #
#                                                                             #
###############################################################################
###############################################################################


#Le "gros" morceau : qu'est-ce qu'on fait lorsqu'un slider change
#assez facile car les fonctions ont été programmées avant
def update(osef):
    R = slider_R.val
    xE = slider_L.val
    resultat =  floute_image(xA, fp, xE, R, objet)
    update_trace_rayon(R,xE)
    
    image_plot.set_data(resultat)
    resultat2 = floute_image(xA, fp, xE, R, objet_perso)
    image_perso_plot.set_data(resultat2)
    fig.canvas.draw_idle()

slider_R.on_changed(update) #connection signal/slot
slider_L.on_changed(update)


resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')    

def reset(event):
    slider_R.reset()
    slider_L.reset()
button.on_clicked(reset)


plus_L = plt.axes([0.53, 0.275, 0.0225, 0.045])
button_plus_L = Button(plus_L, '+', color=axcolor, hovercolor='0.975')   
moins_L = plt.axes([0.53, 0.225, 0.0225, 0.045])
button_moins_L = Button(moins_L, '-', color=axcolor, hovercolor='0.975')   

def f_plus_L(event):
    slider_L.set_val(slider_L.val + 0.005)
button_plus_L.on_clicked(f_plus_L)
def f_moins_L(event):
    slider_L.set_val(slider_L.val - 0.005)
button_moins_L.on_clicked(f_moins_L)


plus_R = plt.axes([0.53, 0.15, 0.0225, 0.045])
button_plus_R = Button(plus_R, '+', color=axcolor, hovercolor='0.975')   
moins_R = plt.axes([0.53, 0.1, 0.0225, 0.045])
button_moins_R = Button(moins_R, '-', color=axcolor, hovercolor='0.975')    

def f_plus_R(event):
    slider_R.set_val(slider_R.val + 0.005)
button_plus_R.on_clicked(f_plus_R)
def f_moins_R(event):
    slider_R.set_val(slider_R.val - 0.005)
button_moins_R.on_clicked(f_moins_R)


   
update(0)
plt.show()
#image_plot.set_data(test2)
