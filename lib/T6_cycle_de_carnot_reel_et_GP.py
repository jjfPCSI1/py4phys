# coding: utf8

# Sauf mention explicite du contraire par la suite, ce travail a été fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lycée Kléber. 
# Vous êtes libres de le réutiliser et de le modifier selon vos besoins.



"""
Le but de ce script est de tracer un cycle de Carnot (deux isothermes et deux 
isentropiques) pour un gaz (a priori l'air, mais on peut le modifier) à la 
fois à partir de données réelles (via CoolProp) et dans la modélisation d'un 
gaz parfait (le coefficient gamma de Laplace étant aussi obtenu à partir de 
CoolProp). On suppose que le cycle se fait de la manière suivante (on 
numérote les point "à l'informaticienne" de 0 à 3):
* Compression isotherme de (P0,TF) à (P1,TF)
* Compression isentropique de (P1,TF) à (Pmax,TC)
* détente isotherme de (Pmax,TC) à (P3,TC)
* détente isentropique de (P3,TC) à (P0,TF)
À noter que si jamais Pmax est trop faible, commence par une détente isotherme 
à TF et on continuera par une compression isotherme à TC
"""

import numpy as np               # Les outils mathématiques
import CoolProp.CoolProp as CP   # Les outils thermodynamiques
import matplotlib.pyplot as plt  # Les outils graphiques

# Les valeurs réglables
R   = 8.314   # Constante des gaz parfaits
gaz = 'Air'   # Type de gaz
TF  = 300     # Température de l'isotherme "froide"
TC  = 900     # Température de l'isotherme "chaude"
P0  = 1e5     # Pression (a priori) la plus faible (et de départ)
Pmax= 1e8     # Pression (a priori) la plus importante

# Calcul du coefficient de Laplace (en le supposant inchangé sur tout le cycle)
cP  = CP.PropsSI('C','T',TF,'P',P0,gaz)
cV  = CP.PropsSI('O','T',TF,'P',P0,gaz)
gamma = cP/cV
# et de la masse molaire (NB: pour eux le "SI" de M, c'est le kg/kmol...)
M   = CP.PropsSI(gaz,'molemass')*1e-3  

# Un peu de feedback pour l'utilisateur:
print('Gaz choisi:',gaz)
print('Masse molaire:',M,'kg/mol')
print('gamma:',gamma)

# Calcul des positions intermédiaires réelles
S3 = CP.PropsSI('S','T',TF,'P',P0,gaz)    # Entropie de la détente isentropique
S1 = CP.PropsSI('S','T',TC,'P',Pmax,gaz)  # Entropie de la compression isentropique
P1 = CP.PropsSI('P','T',TF,'S',S1,gaz)    # Pression au point 1
P3 = CP.PropsSI('P','T',TC,'S',S3,gaz)    # Pression au point 3

# On échantillonne à présent les pressions sur les différents chemins...
nb_points = 1000
P01 = np.linspace(P0,P1,nb_points)
P12 = np.linspace(P1,Pmax,nb_points)
P23 = np.linspace(Pmax,P3,nb_points)
P30 = np.linspace(P3,P0,nb_points)

# ...pour calculer les volumes massiques correspondants (comme d'habitude,
# CoolProp fournit la masse volumique (densité "D") et non le volume massique 
# donc il faut passer à l'inverse).
v01 = 1/CP.PropsSI('D','P',P01,'T',TF,gaz) # Compression isotherme
v12 = 1/CP.PropsSI('D','P',P12,'S',S1,gaz) # Compression isentropique
v23 = 1/CP.PropsSI('D','P',P23,'T',TC,gaz) # Détente isotherme
v30 = 1/CP.PropsSI('D','P',P30,'S',S3,gaz) # Détente isentropique

def infos_point(nb,P,T,v):
   print('Infos pour le point {0}: T={1}K, v={3} m^3/kg, P={2} bar'.format(nb,T,round(P/1e5,1),round(v,4)))

def travail(L_P,L_v):
    W = 0
    for (P,v) in zip(L_P,L_v):
        W -= np.trapz(P,v)
    return W

# On donne du feedback:
print('Cas réel:')
infos_point(0,P0,TF,v01[0])
infos_point(1,P1,TF,v12[0])
infos_point(2,Pmax,TC,v23[0])
infos_point(3,P3,TC,v30[0])
W = travail([P01,P12,P23,P30],[v01,v12,v23,v30])
print('Travail total sur le cycle:',round(W/1e3,2),'kJ/kg')

# Reste à représenter le tout
plt.plot(v01,P01,label='Compression isoT')
plt.plot(v12,P12,label='Compression isoS')
plt.plot(v23,P23,label='Detente isoT')
plt.plot(v30,P30,label='Detente isoS')
plt.legend()
plt.yscale('log')
plt.xscale('log')
#plt.show()

# Maintenant, faisons quelques calculs théoriques.
# On peut calculer les pressions P1 et P3 grâce aux relations de Laplace sur 
# les deux isentropiques
P3 = P0 * (TF/TC)**(gamma/(1-gamma))
P1 = Pmax*(TC/TF)**(gamma/(1-gamma))

# On échantillonne à présent les pressions sur les différents chemins...
nb_points = 1000
P01 = np.linspace(P0,P1,nb_points)
P12 = np.linspace(P1,Pmax,nb_points)
P23 = np.linspace(Pmax,P3,nb_points)
P30 = np.linspace(P3,P0,nb_points)

# ... pour calculer les volumes massiques à l'aide des lois de Laplace ou des 
# gaz parfaits.
v01 = R*TF/(M*P01)
v12 = v01[-1] * (P1/P12)**(1/gamma)
v23 = R*TC/(M*P23)
v30 = v23[-1] * (P3/P30)**(1/gamma)

# Reste à représenter le tout
plt.plot(v01,P01,label='GP Compression isoT')
plt.plot(v12,P12,label='GP Compression isoS')
plt.plot(v23,P23,label='GP Detente isoT')
plt.plot(v30,P30,label='GP Detente isoS')

plt.title('Cycle de Carnot: comparaison gaz reel et gaz parfait')
plt.xlabel('$v$ en m$^3/$kg')
plt.ylabel('P en Pa')
plt.legend(loc='lower left')
plt.savefig('PNG/T6_cycle_de_carnot_reel_et_GP_{}.png'.format(gaz))

# On donne du feedback:
print('Cas Gaz Parfait:')
infos_point(0,P0,TF,v01[0])
infos_point(1,P1,TF,v12[0])
infos_point(2,Pmax,TC,v23[0])
infos_point(3,P3,TC,v30[0])
W = travail([P01,P12,P23,P30],[v01,v12,v23,v30])
print('Travail total sur le cycle:',round(W/1e3,2),'kJ/kg')




