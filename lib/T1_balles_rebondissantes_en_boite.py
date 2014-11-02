# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.



"""

Code servant à simuler un ensemble de balles rebondissantes soumises à la 
gravité. Le code est adapté de celui proposé par le cours de l'ENS Ulm: 
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

N_sur_4 = 100   # On prend un multiple de 4
N = 4*N_sur_4   # pour les couleurs
output_dir = "PNG/T1_balles_rebondissantes_en_boite_movie"
colors = ['r', 'b', 'g', 'orange']*N
sigma = 0.002                      # Rayon des particules
singles = [(i,j) for i in range(N) for j in range(2)]   # L'ensemble des particules (en 2D)
pairs = [(i,j) for i in range(N) for j in range(i+1,N)] # L'ensemble des paires

t = 0.0                            # Temps initial
dt = 0.02                          # dt=0 corresponds to event-to-event animation
n_steps = 1000                     # Nombre d'étapes


def wall_time(pos_a, vel_a, sigma, g):
    """Fonction qui détermine le prochain choc d'une particule avec un mur."""
    del_t = float('inf')
    #print(pos_a,vel_a,g)
    if g == 0: # Cas d'un axe sans gravité
        if vel_a > 0.0:
            del_t = (1.0 - sigma - pos_a) / vel_a
        elif vel_a < 0.0:
            del_t = (pos_a - sigma) / abs(vel_a)
    else: 
        Delta1= vel_a**2 - 2*g*(pos_a - (1-sigma))
        Delta2= vel_a**2 - 2*g*(pos_a - sigma)
        tpossibles = []
        if Delta1 >= 0:
            tpossibles += [1/g*(-vel_a - Delta1**0.5), 1/g*(-vel_a + Delta1**0.5)]
        if Delta2 >= 0: 
            tpossibles += [1/g*(-vel_a - Delta2**0.5), 1/g*(-vel_a + Delta2**0.5)]
        #print(tpossibles)
        tpossibles = [t for t in tpossibles if t > 1e-5] # On ne garde que les positifs
        #print(tpossibles)
        if len(tpossibles)>0: 
            del_t = min(tpossibles)
    #print(del_t)
    return del_t

def pair_time(pos_a, vel_a, pos_b, vel_b, sigma):
    """
    Fonction qui détermine le temps du prochain choc d'une particule avec une 
    autre. Magie de la gravité: les termes quadratiques disparaissent ! On se 
    ramène donc au cas des particules libres.
    """
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

g = np.array([0,-1])

def compute_next_event(pos, vel):
    """ Détermination du prochain "évènement", c'est-à-dire l'instant de ce 
    choc et la particule (ou la paire) correspondante. À noter que l'on stocke 
    toutes ces infos dans un seul indice (cf disjonction de cas dans 
    compute_new_velocities)."""
    #print('-'*70)
    wall_times = [wall_time(pos[k][l], vel[k][l], sigma, g[l]) for k, l in singles]
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
    nbmax   = 80   # Limite verticale des histogrammes
    nb_bins = 20   # Nombre de bins pour les histogrammes
    # Quelques déclarations de tailles
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
    # La dernière particule a droit à son vecteur vitesse
    dx,dy = vel[-1] * arrow_scale 
    pylab.arrow( x, y, dx, dy, fc="k", ec="k", head_width=0.05, head_length=0.05 )
    pylab.text(.5, 1.03, 't = %.2f' % t, ha='center')

    # Second sous-plot: histogramme de la projection suivant x des vitesses
    ax2 = pylab.subplot2grid((2,3),(0,2),colspan=1,rowspan=1)
        
    # Récupération des vitesses et des positions pour les particules encore 
    # dans le champ d'étude (au cas où certaines se seraient échappées [bug à 
    # corriger, mais on fait avec...])
    vitesses = np.array([vel[k] for k in range(N) if 0 <= pos[k][1] <=1 and 0 <= pos[k][0] <= 1])
    positions= np.array([pos[k] for k in range(N) if 0 <= pos[k][1] <=1 and 0 <= pos[k][0] <= 1])
    nb_part  = vitesses.shape[0]               # Nombre de particules encore dans le champ
    r = (-2,2)                                 # Intervalle de vitesses regardé
    pylab.hist(vitesses[:,0],bins=nb_bins,range=r)  # Dessin de l'histogramme
    # Récupération des centres de positionnement des histogrammes
    hist_data,bin_edges = np.histogram(vitesses[:,0],bins=nb_bins,range=r)
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2
    pylab.xlim(r)                              # On impose l'abscisse
    pylab.ylim((0,nbmax))                      # et l'ordonnée
    pylab.ylabel("Nombre de particules")       # Légende verticale
    pylab.xlabel("$v_x$")                      # et horizontale
    pylab.title('Distribution de vitesse suivant $x$')
    # La distribution est sensée être gaussienne
    v = np.linspace(r[0],r[1],100)             # Échantillonnage en vitesses
    #Dv= bin_centers[1] - bin_centers[0]       
    #dispx = np.sum(vel[:,0]**2)/N
    disp2 = np.sum(vitesses**2)/(2*N)          # Dispersion (carrée) des vitesses (avec le 2 en plus)
    A = N / (sum(np.exp(-(bin_centers)**2/disp2))) # Normalisation de la gaussienne
    # Représentation graphique de la gaussienne en pointillés
    pylab.plot(v,A*np.exp(-v**2/disp2),'--k',linewidth=3.0)  

    # Troisième sous-plot: histogramme de répartition des particules selon l'altitude
    ax3 = pylab.subplot2grid((2,3),(1,2),colspan=1,rowspan=1)
    r = (0,1)                                  # Intervalle de hauteurs regardé
    pylab.hist(positions[:,1],bins=nb_bins,range=r)  # Dessin de l'histogramme
    pylab.xlim(r)                              # On impose l'abscisse
    pylab.ylim((0,nbmax))                      # et l'ordonnée
    pylab.ylabel("Nombre de particules")       # Légende verticale
    pylab.xlabel("Altitude $z$")               # et horizontale
    pylab.title("Distribution verticale des particules")
    # Récupération des centres de positionnement des histogrammes
    hist_data,bin_edges = np.histogram(positions[:,1],bins=nb_bins,range=r)
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2
    A = N/(sum(np.exp(g[1]*bin_centers/disp2)))# Calcul de la normalisation
    z = np.linspace(r[0],r[1],100)             # Échantillonage des z
    # Affichage de la courbe exponentielle théorique
    pylab.plot(z, A * np.exp(g[1]*z/disp2),'--k',linewidth=3.0)
    pylab.tight_layout() # Pour ajuster un peu les bords
    
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

# Le début du programme proprement dit

pos = check_position()             # Sélection des positions
vel = 0.5*(np.random.random((N,2))*2 - 1)# et des vitesses
X,Y = [pos[-1][0]],[pos[-1][1]]    # La dernière particule va être suivie à la loupe
next_event, next_event_arg = compute_next_event(pos, vel) # On calcule la première étape
snapshot(t, pos, vel, colors, X, Y)# et on prend une première photo.
for step in range(n_steps):        # On boucle
    if dt:                         # Cas normal,
        next_t = t + dt            # on avance de dt
    else:                          # Sinon,
        next_t = t + next_event    # c'est qu'on veut regarder choc après choc
    while t + next_event <= next_t:# Début des calculs jusqu'à la prochaine sortie
        t += next_event            # On avance
        # On met à jour les position
        pos += [vel[k] * next_event + g/2 * next_event**2 for k in range(N)]    
        # Et les vitesses
        vel += [g * next_event for k in range(N)]
        # Ainsi que les vitesses des particules ayant été "choquées"
        compute_new_velocities(pos, vel, next_event_arg)
        # On calcule le prochain évènement.
        next_event, next_event_arg = compute_next_event(pos, vel)
    remain_t = next_t - t          # S'il est après la mise à jour, 
    # On met à jour les position pour le snapshot
    pos += [vel[k] * remain_t + g/2 * remain_t**2 for k in range(N)]    
    # Et les vitesses
    vel += [g * remain_t for k in range(N)]
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
    




