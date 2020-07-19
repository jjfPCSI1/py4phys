r"""
Created on Sat Sep 28 23:51:45 2019

@author: Vincent Grenard

Génération automatique de tracés optiques au travers d'un nombre (a priori 
arbitraire) de lentilles consécutives (voir fichier test.pdf pour un exemple).

Pour inclure les fichiers produits, vous pouvez utiliser l'exemple minimal suivant

\documentclass[12pt,a4paper]{article}
\usepackage{pstricks}
\usepackage{pstricks-add}

\begin{document}

\input testXXXXX3.tex

\end{document}

Et compiler (obligatoirement) en passant par la moulinette
latex -> dvips -> ps2pdf
car pstricks ne fonctionne pas directement avec pdflatex

"""

import numpy as np
import matplotlib.pyplot as plt
inf = float("inf")

#####   nom_du_fichier    #####

nom_fichier = "testXXXXX3.tex"

#####   data    #####
#liste_pos_lentilles = [-4, 2.5] #position sur l'axe des abscisses des différentes lentilles
#liste_dists_focales = [3, 2]#distances focales correspondantes
#x_A = -inf #position de l'objet
#AB = -15  #ordonnée/taille de l'objet ; si XA est inf, alors représente l'angle des rayons incidents
#liste_angle = [2, 1, 0.5, 0, -0.5, -1, 2.5]#en degré ; si Xa esdt inf, alors représente la liste des y pour les rayons incidents


#ci-dessous un exemple avec x_A non infini
liste_pos_lentilles = [-4, -2, 3] #position sur l'axe des abscisses des différentes lentilles
liste_dists_focales = [2, -5, 2]#distances focales correspondantes
x_A = -7.5 #position de l'objet
AB = 0.25  #ordonnée/taille de l'objet ; si XA est inf, alors représente l'angle des rayons incidents
liste_angle = [30, 10, 5, 0, -5, -10, -20, -30]#en degré ; si Xa esdt inf, alors représente la liste des y pour les rayons incidents


#ci-dessous un exemple avec x_A infini
#liste_pos_lentilles = [-4, 0,2] #position sur l'axe des abscisses des différentes lentilles
#liste_dists_focales = [5.5, -1.5,4]#distances focales correspondantes
#x_A = -inf #position de l'objet
#AB = -5  #ordonnée/taille de l'objet ; si XA est inf, alors représente l'angle des rayons incidents
#liste_angle = [2,1.5,1,0.5,0,-0.5,-1]#en degré ; si Xa esdt inf, alors représente la liste des y pour les rayons incidents

              
#gestion des objets à l'infini
if abs(x_A) == inf:
    print("objet à l'infini car x_A = inf, la taille de l'objet représente l'angle et la liste des angles représente en fait la liste des y")

#####   limite de l'espace    #####
lim = [-8,8,-2.5,2.5]   # xdeb xfin ydeb yfin
marge = 0.05
x_deb = lim[0]
x_fin = lim[1]
y_deb = lim[2]
y_fin = lim[3]
delta_x = x_fin - x_deb
delta_y = y_fin - y_deb


#liste des couleurs dispo dans pstricks
couleurs_all = "blue","red","green","cyan","magenta","yellow","gray"

#####   calculs    #####
def calcule_liste_pos_et_taille_image():
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
#    print(liste_image)    
#    print(liste_taille_image)
    return liste_image, liste_taille_image
liste_pos_image, liste_taille_image = calcule_liste_pos_et_taille_image()
#print(liste_pos_image)
#print(liste_taille_image)

def traverse_vide(x_old,y_old,theta_old,x_new):
#    print(x_old, y_old, theta_old, x_new)
    return y_old + (x_new-x_old)*theta_old #theta_new = theta_old
def traverse_lentille(y_old,theta_old,fp):
    theta_new = -y_old/fp+theta_old
    return theta_new #y_new = y_old

def trace_matplotlib():
    """
    Trace à l'aide de matplotlib pour qu'on voit à quoi ça ressemble sans avoir à compiler un fichier latex
    
    """
    #tracé objet + lentilles
    plt.plot([x_A,x_A], [0,AB])
    for i in range(len(liste_pos_lentilles)):
        x = liste_pos_lentilles[i]
        plt.plot([x,x], [-2.25,2.25])
    #fin tracé objet + lentilles
    #axe optique
    plt.plot([x_deb,x_fin],[0,0],'-k')#axe optique
    deb_fleche = x_fin - 0.025*delta_x
    altitude_fleche = delta_y * 0.025
    plt.plot( [deb_fleche,x_fin,deb_fleche],[altitude_fleche,0,-altitude_fleche],'-k') # flèche
    
    #lentille
    for x_O, f_p in zip(liste_pos_lentilles, liste_dists_focales):
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
    #ajoute une lentille virtuelle à la fin pour pas avoir à gérer différemment le dernier espace vide
    if liste_pos_lentilles[-1] != x_fin: #inutile de le faire plusieurs fois
        liste_pos_lentilles.append(x_fin)
        liste_dists_focales.append(float("inf"))
    #tracé de chaque rayon
    for angle_deg in liste_angle:
    
        
        angle = np.deg2rad(angle_deg)    
        liste_x_rayons = [x_deb]
        if abs(x_A) != inf:
            liste_y_rayons = [AB+angle*(x_deb-x_A)]
        else:
            liste_y_rayons = [angle_deg] #l'angle représente un y
            angle = np.deg2rad(AB) #AB représente en fait l'angle à l'infini
        
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
            theta = traverse_lentille(y,theta, liste_dists_focales[ind])
            
            #met à jour le x_old y_old theta_old
            x_old = x
            y_old = y
            theta_old = theta
            
            #met à jour les listes pour tracer les rayons
            liste_x_rayons.append(x)
            liste_y_rayons.append(y)
        
        
            #gérer l'espace vide après la dernière lentille fait en rajoutant une fausse lentille
        
        plt.plot(liste_x_rayons, liste_y_rayons)
    for xap, ApBp in zip(liste_pos_image, liste_taille_image):
        if abs(xap) != inf:
            plt.plot([xap, xap],[0, ApBp])
    plt.axis('off')
    plt.axis(lim)
    plt.show(False)
trace_matplotlib()
#print("fin matplotlib")


def genere_pstricks(nom_fichier):
    ### ouverture du fichier
    
    fichier = open(nom_fichier,'w+')
    #### génération du code pstricks
    print(r"%généré automatiquement par lentilles_matricielles.py",file = fichier)
    print(r"%paramètres : ",file = fichier)
    print(r"%liste_pos_lentilles =",liste_pos_lentilles,file = fichier)
    print(r"%liste_dists_focales =",liste_dists_focales, "   % remarque : si la dernière valeur est inf, c'est une lentille fictive pour faciliter le code",file = fichier)
    print(r"%x_A =",x_A,file = fichier)
    print(r"%AB =",AB,file = fichier)
    print(r"%liste_angle =",liste_angle,file = fichier)
    print(r"% et pour les limites : ",file = fichier)
    print(r"%lim =",lim,file = fichier)
    print(r"%marge =",marge,file = fichier)
    print(r"\begin{pspicture*}(",x_deb-marge,",",y_deb-marge,")(",x_fin+marge,",",y_fin+marge,")",file = fichier)
    ## Axe optique
    print(r"% axe optique",file = fichier)
    print(r"\psline[arrowscale = 3]{->}(",x_deb,",0)(",x_fin,",0)",file = fichier)
    print(r"\uput[90](",x_fin-0.1,",0.1){$\Delta$}",file = fichier)
    # Lentille convergente ou divergente
    print(r"%affichage des lentilles",file = fichier)
    for x_O, f_p in zip(liste_pos_lentilles, liste_dists_focales):
        if x_O >= x_fin:
            break #gère la lentille virtuelle rajoutée à la fin
        if (f_p<0):
            arrow = '>-<'
        else:
            arrow = '<->'
        print(r"    %Lentille en",x_O,"de distance focale",f_p,file = fichier)
        print(r"    \psline[linewidth = 2pt,arrowscale = 2]{",arrow,"}(",x_O,",",y_deb,")(",x_O,",",y_fin,")",file = fichier)
    x_O = liste_pos_lentilles[0]
    f_p = liste_dists_focales[0]
    #objet réel ou virtuel ou à l'infini
    if abs(x_A) != inf: #dessine l'objet seulement s'il n'est pas à l'infini
        if(x_A-x_O>0):
            style = r',linestyle = dashed]'
        else:
            style = ']'
        print(r"% objet réel ou virtuel",file = fichier)
        print(r"\psline[linewidth = 1.5pt"+style +"{->}(",x_A,",0)(",x_A,",",AB,")",file = fichier)
        if AB >0:
            sg = 1
        else:
            sg = -1
        print(r"\uput[",-sg*90,"](",x_A,",0){$A$}",file = fichier)
        print(r"\uput[",sg*90,"](",x_A,",",AB,"){$B$}",file = fichier)
    #trace les images intermédiaires
    print(r"%positionnement des différentes images",file = fichier)
    for i, x_A_p, A_pB_p, f_p in zip(range(1, len(liste_pos_image)+1), liste_pos_image, liste_taille_image,liste_pos_lentilles):
        if abs(x_A_p) == inf or x_A_p < x_deb or x_A_p > x_fin:
            continue #sort de l'image
        elif liste_pos_lentilles[i-1]<x_A_p<liste_pos_lentilles[i]:
            style = ']'#image réelle
        else:
            style = r',linestyle = dashed]' #image virtuelle
        print(r"    %position de l'image",i,file = fichier)
        print(r"    \psline[linewidth = 1.5pt"+style +"{->}(",x_A_p,",0)(",x_A_p,",",A_pB_p,")",file = fichier)
        if A_pB_p >0:
            sg = 1
        else:
            sg = -1
        nom_imageA = "A_"+str(i)
        nom_imageB = "B_"+str(i)
        if i == len(liste_pos_image):
            nom_imageA = "A'"
            nom_imageB = "B'"
        print(r"    \uput[",-sg*90,"](",x_A_p,",0){$",nom_imageA,"$}",file = fichier)
        print(r"    \uput[",sg*90,"](",x_A_p,",",A_pB_p,"){$",nom_imageB,"$}",file = fichier)
    #maintenant il va falloir tracer les rayons (et réfléchir si on trace les pointillés)
    #ajoute une lentille virtuelle à la fin pour pas avoir à gérer différemment le dernier espace vide
    if liste_pos_lentilles[-1] != x_fin: #inutile de le faire plusieurs fois
        liste_pos_lentilles.append(x_fin) 
        liste_dists_focales.append(float("inf"))
    #tracé de chaque rayon
    if abs(x_A) != inf: #dessine l'objet seulement s'il n'est pas à l'infini
        print(r"%tracé des rayons pour les différents angles de",liste_angle,file = fichier)
    else:
        print(r"%tracé des rayons pour les différents y_deb de",liste_angle,file = fichier)
    for ind_angle,angle_deg in enumerate(liste_angle):
        couleur = couleurs_all[ind_angle%len(couleurs_all)]
        
        if abs(x_A) != inf: #dessine l'objet seulement s'il n'est pas à l'infini
            print(r"    %tracé du rayon pour l'angle initial",angle_deg,"° en couleur",couleur,file = fichier)
        else:
            print(r"    %tracé du rayon pour le y initial",angle_deg," en couleur",couleur,file = fichier)
    
        
        
        angle = np.deg2rad(angle_deg)   
        liste_x_rayons = [x_deb]
        if abs(x_A) != inf:
            liste_y_rayons = [AB+angle*(x_deb-x_A)]
        else:
            liste_y_rayons = [angle_deg] #l'angle représente un y
            angle = np.deg2rad(AB) #AB représente en fait l'angle à l'infini
        
        
        x_old = x_deb
        y_old = liste_y_rayons[0]
        theta_old = angle
        
        chaine_position = "("+str(x_old)+","+str(y_old)+")"
        if x_A < liste_pos_lentilles[0] and abs(x_A) != inf:
            #objet réel ; on le rajoute à la liste pour les flèches des arrowinside
            liste_x_rayons.append(x_A)
            liste_y_rayons.append(AB)
            chaine_position += "("+str(x_A)+","+str(AB)+")"
        
        for ind in range(len(liste_pos_lentilles)):
            #pour chaque lentille 
            
            #traverse le vide jusqu'à la lentille
            x = liste_pos_lentilles[ind]
            y = traverse_vide(x_old, y_old, theta_old, x)
            theta = theta_old
            
            #passe la lentille
            theta = traverse_lentille(y,theta, liste_dists_focales[ind])
            
            #met à jour le x_old y_old theta_old
            x_old = x
            y_old = y
            theta_old = theta
            
            #met à jour les listes pour tracer les rayons
            liste_x_rayons.append(x)
            liste_y_rayons.append(y)
            
            chaine_position += "("+str(x_old)+","+str(y_old)+")"
        
        
            #gérer l'espace vide après la dernière lentille fait en rajoutant une fausse lentille
            
            #tracé des pointillés si image virtuelle ?
            if ind < len(liste_pos_image):
                x_A_p = liste_pos_image[ind]
                A_pB_p = liste_taille_image[ind]
                if abs(x_A_p) == inf or x_A_p < x_deb or x_A_p > x_fin or A_pB_p > y_fin or A_pB_p < y_deb:
                    continue #sort de l'image
                elif x_A_p < liste_pos_lentilles[ind] or x_A_p > liste_pos_lentilles[ind+1]:
                    print(r"        %pointillés parce que l'image n'est pas entre les deux lentilles", file = fichier)
                    print(r"        \psline[linecolor = "+couleur+",linewidth = 0.75pt, linestyle = dashed]"+"(%f,%f)(%f,%f)"%(x,y,x_A_p,A_pB_p),file = fichier)
                    
                    
                    
        
        
        print(r"    \psline[linecolor = "+couleur+",ArrowInside = ->,arrowscale = 2]"+chaine_position,file = fichier)
    
    
#    #si image en haut, je mets le foyer en bas et réciproquement
#if A_pB_p<0: signe = -1
#else: signe = 1
#print(r"\uput[", -signe * 90,"](",x_O+f_p,",",-signe * delta,r"){$F'$}",file = fichier)
#if AB<0: signe = -1
#else: signe = 1
#print(r"\uput[", -signe * 90,"](",x_O-f_p,",",-signe * delta,r"){$F$}",file = fichier)
    
    print(r"%affichage des foyers des lentilles ; à retoucher à la main si besoin",file = fichier)
    for i,x_O, f_p in zip(range(1,len(liste_pos_lentilles)+1),liste_pos_lentilles, liste_dists_focales):
        if x_O >= x_fin:
            break #gère la lentille virtuelle rajoutée à la fin
        print(r"    %Lentille en",x_O,"de distance focale",f_p,file = fichier)
        delta = 0.085
        print(r"    \psline(",x_O+f_p,",",delta,")(",x_O+f_p,",",-delta,")",file = fichier)
        print(r"    \psline(",x_O-f_p,",",delta,")(",x_O-f_p,",",-delta,")",file = fichier)
        nom = "F'_" +str(i)
        texte = r"    \uput[-90]("+"%f,%f"%(x_O-f_p,0)+r"){\psframebox[linewidth=0.1pt,linecolor=white,fillstyle=solid,opacity=0.8,framearc=0.3,framesep=0.5pt]{$"+nom+"$}}"
        print(texte,file = fichier)
        nom = "F_" +str(i)
        texte = r"    \uput[-90]("+"%f,%f"%(x_O+f_p,0)+r"){\psframebox[linewidth=0.1pt,linecolor=white,fillstyle=solid,opacity=0.8,framearc=0.3,framesep=0.5pt]{$"+nom+"$}}"
        print(texte,file = fichier)

    ### fermeture du fichier
    print(r"\end{pspicture*}",file = fichier)
    print(r"",file = fichier)
    print(r"",file = fichier)
    print(r"",file = fichier)
    
    fichier.close()
genere_pstricks(nom_fichier)
