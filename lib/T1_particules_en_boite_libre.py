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

Code servant à simuler un gaz parfait soumis uniquement aux chocs entre
molécules. Le code est adapté de celui proposé par le cours de l'ENS Ulm:
"Statistical Mechanics: Algorithms and Computations" sur le site coursera.org.
cf https://class.coursera.org/smac-001

L'idée est de faire une simulation "event-driven", c'est-à-dire que les
équations du mouvement sont connues entre deux chocs, il suffit donc de
déterminer la date du prochain choc et d'utiliser les positions et vitesses
connues après un choc pour calculer facilement les positions entre deux chocs.

Attention, comme on ne sait pas à l'avance qui va rencontrer qui, l'algorithme
est quadratique avec le nombre de particules considérées.

"""


import os, math, pylab
import numpy as np
import numpy.random

N_sur_4 = 20   # On prend un multiple de 4
N = 4*N_sur_4  # pour les couleurs
output_dir = "PNG/T1_particules_en_boite_libre_movie"
colors = ['r', 'b', 'g', 'orange']*N

def wall_time(pos_a, vel_a, sigma):
    """Fonction qui détermine le prochain choc d'une particule avec un mur."""
    if vel_a > 0.0:
        del_t = (1.0 - sigma - pos_a) / vel_a
    elif vel_a < 0.0:
        del_t = (pos_a - sigma) / abs(vel_a)
    else:
        del_t = float('inf')
    return del_t

def pair_time(pos_a, vel_a, pos_b, vel_b, sigma):
    """Fonction qui détermine le temps du prochain choc d'une particule avec une autre."""
    del_x = [pos_b[0] - pos_a[0], pos_b[1] - pos_a[1]]
    del_x_sq = del_x[0] ** 2 + del_x[1] ** 2
    del_v = [vel_b[0] - vel_a[0], vel_b[1] - vel_a[1]]
    del_v_sq = del_v[0] ** 2 + del_v[1] ** 2
    scal = del_v[0] * del_x[0] + del_v[1] * del_x[1]
    Upsilon = scal ** 2 - del_v_sq * (del_x_sq - 4.0 * sigma ** 2)
    if Upsilon > 0.0 and scal < 0.0:
        del_t = - (scal + math.sqrt(Upsilon)) / del_v_sq
    else:
        del_t = float('inf')
    return del_t

def min_arg(l):
    """Récupère à la fois le minimum d'une liste et l'indice correspondant à ce minimum."""
    return min(zip(l, range(len(l))))

def compute_next_event(pos, vel):
    """ Détermination du prochain "évènement", c'est-à-dire l'instant de ce 
    choc et la particule (ou la paire) correspondante. À noter que l'on stocke 
    toutes ces infos dans un seul indice (cf disjonction de cas dans 
    compute_new_velocities)."""
    wall_times = [wall_time(pos[k][l], vel[k][l], sigma) for k, l in singles]
    pair_times = [pair_time(pos[k], vel[k], pos[l], vel[l], sigma) for k, l in pairs]
    return min_arg(wall_times + pair_times)

def compute_new_velocities(pos, vel, next_event_arg):
    """Calcul des nouvelles vitesses"""
    if next_event_arg < len(singles): # Cas d'un choc avec le mur
        collision_disk, direction = singles[next_event_arg]
        vel[collision_disk][direction] *= -1.0 # seule la vitesse sur cet axe est modifiée
    else:                             # Cas d'un choc entre deux particules de même masse
        a, b = pairs[next_event_arg - len(singles)]
        del_x = [pos[b][0] - pos[a][0], pos[b][1] - pos[a][1]]
        abs_x = math.sqrt(del_x[0] ** 2 + del_x[1] ** 2)
        e_perp = [c / abs_x for c in del_x]
        del_v = [vel[b][0] - vel[a][0], vel[b][1] - vel[a][1]]
        scal = del_v[0] * e_perp[0] + del_v[1] * e_perp[1]
        for k in range(2):
            vel[a][k] += e_perp[k] * scal
            vel[b][k] -= e_perp[k] * scal

img = 0
if not os.path.exists(output_dir): os.makedirs(output_dir)

def snapshot(t, pos, vel, colors, X, Y, arrow_scale=.2):
    """ La routine qui s'occupe des tracés graphiques."""
    global img
    nbmax = 20
    pylab.subplots_adjust(left=0.10, right=0.90, top=0.90, bottom=0.10)
    pylab.gcf().set_size_inches(12, 12*2/3)
    # Le premier sous-plot: carré de 2x2
    ax1 = pylab.subplot2grid((2,3),(0,0),colspan=2,rowspan=2)
    pylab.setp(pylab.gca(), xticks=[0, 1], yticks=[0, 1])
    pylab.plot(X,Y,'k') # On y met le trajet de la dernière particule
    pylab.xlim((0,1))   # On doit astreindre les côtés horizontaux
    pylab.ylim((0,1))   # et verticaux
    # Boucle sur les points pour rajouter les cercles colorés
    for (x, y), c in zip(pos, colors): 
        circle = pylab.Circle((x, y), radius=sigma, fc=c)
        pylab.gca().add_patch(circle)
    dx,dy = vel[-1] * arrow_scale # La dernière particule a droit à son vecteur vitesse
    pylab.arrow( x, y, dx, dy, fc="k", ec="k", head_width=0.05, head_length=0.05 )
    pylab.text(.5, 1.03, 't = %.2f' % t, ha='center')
    # Second sous-plot: histogramme de la projection suivant x des vitesses
    ax2 = pylab.subplot2grid((2,3),(0,2),colspan=1,rowspan=1)
    r = (-2,2)  # Intervalle de vitesses regardé
    pylab.hist(vel[:,0],bins=20,range=r)
    pylab.xlim(r)
    pylab.ylim((0,nbmax))
    pylab.ylabel("Nombre de particules")
    pylab.xlabel("$v_x$")
    # Troisième sous-plot: histogramme de la norme des vitesses
    ax3 = pylab.subplot2grid((2,3),(1,2),colspan=1,rowspan=1)
    r = (0,2)   # Intervalle de vitesses regardé
    pylab.hist(np.sqrt(np.sum(vel**2,axis=1)),bins=20,range=r)
    pylab.xlim(r)
    pylab.ylim((0,nbmax))
    pylab.ylabel("Nombre de particules")
    pylab.xlabel("$||\\vec{v}||$")
    pylab.savefig(os.path.join(output_dir, '{:04d}.png'.format(img)))
    img += 1

def check_position():
    """ Une routine pour s'assurer que les particules ne se chevauchent pas au 
    départ. Il peut se passer un certain temps avant que l'on trouve une 
    configuration adéquate. """
    continue_condition = True  # Condition de non-arrêt
    c = 0                      # Compteur
    d2= 4*sigma**2             # Distance (carrée) de sécurité
    while continue_condition:
        c += 1
        if c%100 == 0:         # Un peu de feedback
           print(c,'trials to get initial conditions and still trying...')
        pos = np.random.random((N,2))*(1-2*sigma) + sigma
        k = 0
        for (i,j) in pairs:    # Les vérifications sur toutes les paires
            if sum((pos[i]-pos[j])**2) > d2: k+= 1
            else:
                if c%100 == 0: print(i,j)
                break
        if k == len(pairs): continue_condition = False
    print("Let's compute some physics !")
    return pos

sigma = 0.01                       # Rayon des particules
singles = [(i,j) for i in range(N) for j in range(2)]   # L'ensemble des particules (en 2D)
pairs = [(i,j) for i in range(N) for j in range(i+1,N)] # L'ensemble des paires
pos = check_position()             # Sélection des positions
vel = np.random.random((N,2))*2 - 1# et des vitesses
X,Y = [pos[-1][0]],[pos[-1][1]]    # La dernière particule va être suivie à la loupe

t = 0.0                            # Temps initial
dt = 0.02                          # dt=0 corresponds to event-to-event animation
n_steps = 1000                     # Nombre d'étapes
next_event, next_event_arg = compute_next_event(pos, vel) # On calcule la première étape
snapshot(t, pos, vel, colors, X, Y)# et on prend une première photo.
for step in range(n_steps):        # On boucle
    if dt:                         # Cas normal,
        next_t = t + dt            # on avance de dt
    else:                          # Sinon,
        next_t = t + next_event    # c'est qu'on veut regarder choc après choc
    while t + next_event <= next_t:# Début des calculs jusqu'à la prochaine sortie
        t += next_event            # On avance
        pos += vel * next_event    # On met à jour les position
        # Ainsi que les vitesses des particules ayant été "choquées"
        compute_new_velocities(pos, vel, next_event_arg)
        # On calcule le prochain évènement.
        next_event, next_event_arg = compute_next_event(pos, vel)
    remain_t = next_t - t          # S'il est après la mise à jour, 
    pos += vel * next_event        # On met à jour les position pour le snapshot
    t += remain_t                  # On arrive au temps voulu
    next_event -= remain_t         # et on corrige du temps restant
    X.append(pos[-1][0])           # Suivi x de la dernière particule
    Y.append(pos[-1][1])           # Ainsi que Y
    snapshot(t,pos,vel,colors,X,Y) # Souriez pour la photo
    print('time',t)                # et un peu de feedback

# Ne reste plus qu'à rassembler en un fichier mpeg à l'aide de convert puis de
# ppmtoy4m et mpeg2enc (paquet mjpegtools à installer sur la machine)

import os
    
cmd = '(for f in ' + output_dir + '/*png ; '
cmd+= 'do convert -density 100x100 $f -depth 8 -resize 600x600 PNM:- ; done)'
cmd+= ' | ppmtoy4m -S 420mpeg2'
cmd+= ' |  mpeg2enc -f1 -b 12000 -q7 -G 30 -o {}/film.mpeg'.format(output_dir)

print("Execution de la commande de conversion")
print(cmd)
os.system(cmd)
print("Fin de la commande de conversion")
    




