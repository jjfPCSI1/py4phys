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
Module pour générer simplement un petit film à partir d'une série de fichiers 
png et éviter de recopier le même code de script en script pour ce faire...
"""

def make_film(base_name,out_file=None,resize="600x600",PNM='PNM'):
    """ 
    Fabrique un film automatiquement à partir des fichiers png commençant pas 
    'base_name' à l'aide de convert puis de ppmtoy4m et mpeg2enc (paquet 
    mjpegtools à installer sur la machine). Si 'out_file' n'est pas renseigné, 
    le film sera écrit dans le fichier base_name+'_film.mpeg'. Enfin, il peut 
    arriver que convert se plaigne d'histoires de taille: il faut alors 
    simplement jouer sur le 'resize' jusqu'à trouver une combinaison qui lui 
    plaise (a priori dans les mêmes proportions que la figure initiale).
    Pour le cas des figures monochromes, il faut visiblement spécifier 
    PNM='PPM' pour que cela fonctionne correctement.
    """
    if not(out_file): out_file = base_name + '_film.mpeg'
    
    import os
    
    cmd = '(for f in ' + base_name + '*png ; '
    cmd+= 'do convert -density 100x100 $f -depth 8 -resize {} {}:- ; done)'.format(resize,PNM)
    cmd+= ' | ppmtoy4m -S 420mpeg2'
    cmd+= ' |  mpeg2enc -f1 -b 12000 -q7 -G 30 -o {}'.format(out_file)
    
    print("Execution de la commande de conversion")
    print(cmd)
    os.system(cmd)
    print("Fin de la commande de conversion")



