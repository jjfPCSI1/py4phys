# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.



"""
Le but de ce script est la résolution d'un exercice concernant un cycle Diesel 
à double combustion (cf fichier py4phys.pdf pour le détail de l'exercice)
"""

import numpy as np               # Les outils mathématiques
import CoolProp.CoolProp as CP   # Les outils thermodynamiques
import matplotlib.pyplot as plt  # Les outils graphiques

P,T,s,v = {},{},{},{}

# Les données de l'énoncé 
R   = 8.314   # Constante des gaz parfaits
gaz = 'Air'   # Type de gaz
T[1]= 293
P[1]= 1e5
P[3]= 65e5
P[4]= P[3]
T[4]= 2173
a   = 19

# Calcul du coefficient de Laplace (en le supposant inchangé sur tout le cycle)
cP  = CP.PropsSI('C','T',T[1],'P',P[1],gaz)
cV  = CP.PropsSI('O','T',T[1],'P',P[1],gaz)
gamma = cP/cV
# et de la masse molaire (NB: pour eux le "SI" de M, c'est le kg/kmol...)
M   = CP.PropsSI(gaz,'molemass')*1e-3  

# Un peu de feedback pour l'utilisateur:
print('Gaz choisi:',gaz)
print('Masse molaire:',M,'kg/mol')
print('gamma:',gamma)

# Fonction dichotomique utile
def find_P_from_v_s(v,s,Pstart,Pstop,eps=1e-6):
    """ Retrouver P par dichotomie à partir du volume massique et de 
    l'entropie massique. """
    v1 = 1/CP.PropsSI('D','P',Pstart,'S',s,gaz)
    v2 = 1/CP.PropsSI('D','P',Pstop,'S',s,gaz)
    while abs(v2-v1)/v > eps:
        Pm = (Pstart+Pstop)/2.0
        vm = 1/CP.PropsSI('D','P',Pm,'S',s,gaz)
        if (vm-v)*(v2-v) < 0: Pstart,v1 = Pm,vm
        else: Pstop,v2 = Pm,vm
    return Pm
    


# Calculs des points intermédiaires
v[1]= 1/CP.PropsSI('D','P',P[1],'T',T[1],gaz) # Inverse de densité
v[2]= v[1]/a                                  # Facteur de compression
s[1]= CP.PropsSI('S','T',T[1],'P',P[1],gaz)   # Entropie correspondante
s[2]= s[1]                                    # Isentropique
P[2]= find_P_from_v_s(v[2],s[2],P[1],P[3])    # Récupération pression (faut ruser)
T[2]= CP.PropsSI('T','P',P[2],'S',s[2],gaz)   # Température correspondante
v[3]= v[2]                                    # Isochore
T[3]= CP.PropsSI('T','P',P[3],'D',1/v[3],gaz) # dont on connaît la pression finale
v[4]= 1/CP.PropsSI('D','P',P[4],'T',T[4],gaz) # Isobare à T connue
s[4]= CP.PropsSI('S','P',P[4],'T',T[4],gaz)   # et calcul de l'entropie correspondante
s[5]= s[4]                                    # Isentropique
v[5]= v[1]                                    # Dernière isochore
P[5]= find_P_from_v_s(v[5],s[5],P[1],P[3])    # Ruse sioux pour la pression
T[5]= CP.PropsSI('T','P',P[5],'D',1/v[5],gaz) # et obtention de la T correspondante


# On échantillonne à présent les pressions sur les différents chemins...
nb_points = 100
P12 = np.linspace(P[1],P[2],nb_points)
P23 = np.array([P[2],P[3]])
P34 = np.array([P[3],P[4]])
P45 = np.linspace(P[4],P[5],nb_points)
P51 = np.array([P[5],P[1]])

# ...pour calculer les volumes massiques correspondants (comme d'habitude,
# CoolProp fournit la masse volumique (densité "D") et non le volume massique
# donc il faut passer à l'inverse).
v12 = 1/CP.PropsSI('D','P',P12,'S',s[1],gaz)   # Compression isentropique
v23 = [v[2],v[3]]                              # Compression isochore
v34 = [v[3],v[4]]                              # Détente isobare
v45 = 1/CP.PropsSI('D','P',P45,'S',s[4],gaz)   # Détente isentropique
v51 = [v[5],v[1]]                              # Détente isochore

def infos_point(nb,P,T,v):
   print('Infos pour le point {0}: T={1} K, v={3} m^3/kg, P={2} bar'.format(nb,round(T,1),round(P/1e5,1),round(v,4)))

def travail(L_P,L_v):
    W = 0
    for (P,v) in zip(L_P,L_v):
        W -= np.trapz(P,v)
    return W

def calcule_Delta(f,i,j):
    """ Calcule la variation de la fonction d'état f (à choisir entre 'U', 
    'H', 'S' ou 'G') entre les points i et j à partir des valeurs (supposées 
    connues) de température et de pression. """
    fi = CP.PropsSI(f,'P',P[i],'T',T[i],gaz)
    fj = CP.PropsSI(f,'P',P[j],'T',T[j],gaz)
    return fj-fi


# On donne du feedback:
print('Cas réel:')
for i in range(1,6):         
    infos_point(i,P[i],T[i],v[i])
L_P = [P12,P23,P34,P45,P51]
L_v = [v12,v23,v34,v45,v51]
W = travail(L_P,L_v)              # Calcul du travail sur tout le cycle
print('Travail total sur le cycle:',round(W/1e3,2),'kJ/kg')
Q23 = calcule_Delta('U',2,3)      # Q pour une isochore
Q34 = calcule_Delta('H',3,4)      # Q pour une isobare
print('Transfert thermique reçu sur 2->3:',round(Q23/1e3,2),'kJ/kg')
print('Transfert thermique reçu sur 3->4:',round(Q34/1e3,2),'kJ/kg')
# Calcul du rendement
print('Rendement total: r=',-W/(Q23+Q34))

# Reste à représenter le tout
for i in range(len(L_v)):
    plt.plot(L_v[i],L_P[i]/1e5,label='{}$\\to${}, reel'.format(i+1,(i+1)%5+1))


# Maintenant, faisons quelques calculs théoriques.
# D'abord les volumes massiques des deux premiers points:
v[1] = R*T[1]/(M*P[1])                
v[2] = v[1]/a
# Pressions et Température en 2 s'obtiennent via la loi de Laplace
P[2] = P[1] * (v[1]/v[2])**gamma
T[2] = T[1] * (v[1]/v[2])**(gamma-1)
# Ensuite, on fait une isochore dont on connaît la pression d'arrivée
v[3] = v[2]
T[3] = M*P[3]*v[3]/R
# Après, c'est au tour de l'isobare dont on connait la température finale
v[4] = R*T[4]/(M*P[4])
# Finalement, on refait  une isentropique jusqu'à atteindre v[1]
v[5] = v[1]
P[5] = P[4] * (v[4]/v[5])**gamma
T[5] = T[4] * (v[4]/v[5])**(gamma-1)

# On échantillonne à présent les pressions sur les différents chemins...
nb_points = 100
P12 = np.linspace(P[1],P[2],nb_points)
P23 = np.array([P[2],P[3]])
P34 = np.array([P[3],P[4]])
P45 = np.linspace(P[4],P[5],nb_points)
P51 = np.array([P[5],P[1]])

# ...pour calculer les volumes massiques correspondants 
v12 = v[1]*(P[1]/P12)**(1/gamma)               # Compression isentropique
v23 = [v[2],v[3]]                              # Compression isochore
v34 = [v[3],v[4]]                              # Détente isobare
v45 = v[4]*(P[4]/P45)**(1/gamma)               # Détente isentropique
v51 = [v[5],v[1]]                              # Détente isochore

# On donne du feedback:
print('Cas Gaz parfait:')
for i in range(1,6):
    infos_point(i,P[i],T[i],v[i])
L_P = [P12,P23,P34,P45,P51]
L_v = [v12,v23,v34,v45,v51]
W = travail(L_P,L_v)        # Calcul du travail total
print('Travail total sur le cycle:',round(W/1e3,2),'kJ/kg')
Q23 = cV*(T[3]-T[2])        # Q sur une isochore
Q34 = cP*(T[4]-T[3])        # Q sur une isobare
print('Transfert thermique reçu sur 2->3:',round(Q23/1e3,2),'kJ/kg')
print('Transfert thermique reçu sur 3->4:',round(Q34/1e3,2),'kJ/kg')

print('Rendement total: r=',-W/(Q23+Q34))

# Reste à représenter le tout
for i in range(len(L_v)):
    plt.plot(L_v[i],L_P[i]/1e5,label='{}$\\to${}, GP'.format(i+1,(i+1)%5+1))
plt.legend()
plt.xlabel('$v$ en m$^3/$kg')
plt.ylabel('P en bar')
plt.title("""Cycle Diesel double combustion
Comparaison du gaz reel et du gaz parfait""")

plt.savefig('PNG/T6_resolution_cycle_diesel.png')



