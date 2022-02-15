import numpy as np

# * `G` contient la valeur choisie pour la constante de gravitation universelle
# * `M0` la masse de l'amas
# * `a` le rayon de Plummer de l'amas
# * `v0` vitesse initiale à «l'infini» (soit 100a vers la gauche)
# * `temps` liste des temps à utiliser pour l'intégration (choisis avec soin pour vous)
# * `liste_b` la liste des paramètres d'impact (positifs) que l'on veut explorer

G = 1
M0= 500
a = 1
v0= 20
temps = np.linspace(0, 20, 100000)
liste_b = [0.1, 1, 2, 5]
