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

Travail réalisé par Pierre Chary (PCSI, Lycée Buffon, Paris) pour illustrer le 
traitement d'image par strioscopie au programme de Physique en PC mais qui 
peut aussi servir comme projet d'informatique commune en seconde année.

Le script fait usage du module "requests" qui peut ne pas être installé sur 
toutes les distributions (WinPython par exemple) afin de charger des images 
depuis internet, mais il n'est pas nécessaire à son bon fonctionnement: vous 
pouvez aussi simplement lire les images sur votre disque que nous supposerons 
installées dans un dossier SampleImages/ dans le même répertoire où est appelé 
le script.

"""

# Pour manipuler l'image = tableau 2D de nombres
import numpy as np
# Pour les traces
import matplotlib.pyplot as plt
# Pour charger l'image de lena :)
from scipy import misc
# Pour recuperer des images sur le net (.png en noir et blanc)
try:
    import requests
    from io import BytesIO  # Utiliser StringIO au lieu de BytesIO pour Python 2.x
except:
    print(""" 
    Attention, votre distribution ne semble pas inclure le module 'requets'
    Par conséquent, installez-le ou commentez la ligne 'import requests' et
    modifiez les exemples pour qu'il ne fassent pas usage de requests.
    """)


def TF(img):
     """ Calcul de la transforme de Fourier de l'image img"""
     spectre = np.fft.fft2(img)            
     # Il faut decaler le spectre, sinon les basses frequences
     # sont dans les coins et non au centre...
     sp_shifte = np.fft.fftshift(spectre)
     return sp_shifte


def strioscopie(spectre, type="passe haut", proportion = 0.03):
     """ Application d'un filtre passe haut ou passe bas,
     de forme carree sur un pourcentage "proportion" du spectre de Fourier
     2D de l'image"""
     # Nombre de lignes et de colonnes de l'image
     nblig, nbcol = spectre.shape
     # Coordonnees du centre
     clig, ccol = nblig // 2, nbcol // 2
     # On applique un masque de 0 et de 1 au spectre pour le filtrer
     masque = np.zeros((nblig, nbcol))
     taille = int(proportion * (nblig + nbcol) / 2.0)
     masque[clig-taille:clig+taille, ccol-taille:ccol+taille] = 1
     if type == "passe haut":
          masque = 1 - masque
     sp_filtre = spectre * masque
     return sp_filtre
    
def detramage(spectre, type="horizontale", proportion = 0.03):
     """ Application d'une fente verticale ou horizontale, de largeur proportionnellement a l'image "proportion", sur le spectre de Fourier 2D de l'image"""
     # nombre de lignes et de colonnes de l'image
     nblig, nbcol = spectre.shape         
     # CoordonnÃ©es du centre
     clig,ccol = nblig//2 , nbcol//2         
     # On applique un masque de 0 et de 1 au spectre pour le filtrer
     taille = int(proportion * (nblig + nbcol) / 2.0)
     masque = np.zeros((nblig,nbcol))    
     if type == "verticale":
          masque[:,ccol-taille:ccol+taille] = 1
     elif type == "horizontale":
          masque[clig-taille:clig+taille,:] = 1
     sp_filtre = spectre*masque 
     return sp_filtre

def TF_inv(sp_filtre):
     """ Calcul de la transformee de Fourier inverse du spectre filtree """
     # On redecale le spectre pour remettre les basses frequences
     # dans les coins afin que la TF inverse fonctionne correctement.
     sp_filtre_shifte = np.fft.ifftshift(sp_filtre)
     # TF inverse
     img_filtree = np.fft.ifft2(sp_filtre_shifte)
     return np.abs(img_filtree)
     
def execute(img, type, proportion=0.03,save=None):
     """ Programme principal      
     Donner une valeur à save (par exemple save='mon_fichier.png') permet de 
     sauvegarder la figure produite.
     """
     sp_shifte = TF(img)
     if type == "verticale" or type == "horizontale":
          sp_filtre = detramage(sp_shifte, type, proportion)
     else:
          sp_filtre = strioscopie(sp_shifte, type, proportion)
     img_filtree = TF_inv(sp_filtre)
     # Echelle logarithmique pour bien voir toutes les composantes spectrales
     # d'amplitudes tres differentes, le +1 est pour eviter les valeurs nulles
     # dans le log.
     sp_shifte_module = 20*np.log(1+np.abs(sp_shifte))
     sp_filtre_module = 20*np.log(1+np.abs(sp_filtre))
     
     # Traces
     plt.figure()
     plt.subplot(221), plt.imshow(img, cmap='gray')
     plt.title('Image de depart'), plt.xticks([]), plt.yticks([])
     plt.subplot(222), plt.imshow(sp_shifte_module, cmap='gray')
     plt.title('Spectre (TF)'), plt.xticks([]), plt.yticks([])
     plt.subplot(223), plt.imshow(img_filtree, cmap='gray')
     plt.title('Image filtree ' + type), plt.xticks([]), plt.yticks([])
     plt.subplot(224), plt.imshow(sp_filtre_module, cmap='gray')
     plt.title('Spectre filtre ' + type), plt.xticks([]), plt.yticks([])
     if save:  plt.savefig(save)
     else:     plt.show()

if __name__ == '__main__':
    # Les images doivent etre en .PNG et en noir et blanc, sinon les convertir 
    # ou utiliser Image de la bibliothèque PIL au lieu de imread
    
    # Strioscopie sur Lena 
    img = misc.lena()
    execute(img, "passe haut", 0.06)
    execute(img, "passe bas", 0.06)
    
    # Suppression du bruit HF sur une image prise sur le net
    url = "https://raw.githubusercontent.com/scipy-lectures/scipy-lecture-notes/master/data/moonlanding.png"
    response = requests.get(url)
    img = plt.imread(BytesIO(response.content))
    # Si jamais requests n'est pas installé, commentez les trois lignes 
    # précédentes et décommentez la ligne suivante
    #img = plt.imread('SampleImages/moonlanding.png')
    execute(img, "passe bas", 0.08)
    
    # Detramage sur une grille
    url = "https://raw.githubusercontent.com/pchary/Image/master/SampleImages/grille.png"
    response = requests.get(url)
    img = plt.imread(BytesIO(response.content))
    # Si jamais requests n'est pas installé, commentez les trois lignes 
    # précédentes et décommentez la ligne suivante
    #img = plt.imread('SampleImages/grille.png')
    execute(img, "verticale")
    execute(img, "horizontale")
    
    # Pour une image sur le disque utiliser la ligne suivante (ex de chemin complet)
    #img = plt.imread(r"E:\Prepa\Informatique\Python\moonlanding.png") 
    
    # Strioscopie sur la Nebuleuse: c'est bluffant !
    img =  plt.imread('SampleImages/Nebuleuse.png')
    execute(img, "passe haut", 0.06)
    execute(img, "passe bas", 0.06)
    execute(img, "passe haut", 0.06, save='PNG/PC_strioscopie_Nebuleuse_PH.png')
    execute(img, "passe bas", 0.06,  save='PNG/PC_strioscopie_Nebuleuse_PB.png')
    
    
# On observe des alias ("ringing artifact") sur l'image filtree par le passe 
# bas. Ceci est du a la forme discontinue du masque applique qui est une porte.
# Un masque plus lisse (gaussien) permettrait de s'en affranchir 
# (https://fr.wikipedia.org/wiki/Masque_flou). Cela peut donner l'occasion de 
# faire le lien avec le cours sur l'echantillonnage, le phenomene de Gibbs...

# On peut melanger l'image filtree passe haut avec l'image originale 
# (alpha*img+(1-alpha)img_filtree) pour obtenir une image plus piquee,

# Bien entendu, il y a des modules qui font cela tout seul: scipy.ndimage 
# (https://scipy-lectures.github.io/advanced/image_processing/), scikit-image 
# (https://scipy-lectures.github.io/packages/scikit-image/index.html#scikit-image), 
# PIL etc.

    


