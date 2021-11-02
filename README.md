Py4Phys
-------

Projet pour rassembler l'ensemble des programmes Python qui peuvent être 
utiles pour illustrer le cours de physique de CPGE.

## Nouveauté

Des notebook Jupyter permettant d'illustrer les différentes capacités 
numériques du programme de PCSI/MPSI/MP2I apparaissent petite à petit dans le 
dossier `Capacites_numeriques_prog2021/`. N'hésitez pas à y jeter un œil. 
L'idée est de proposer aux étudiants des Notebooks à compléter avec plusieurs 
niveaux d'autonomie:
* le niveau 1 fait une explication détaillée et propose un exemple avant de demander une application aux étudiants ;
* le niveau 2 revient à faire la même chose que le niveau 1 (ou presque) mais sans rappel ;
* le niveau 3 se veut plus ambitieux avec plusieurs outils à utiliser avant d'arriver au résultat demandé.

## Organisation

* Le fichier py4phys.pdf rassemble les codes et les graphiques qui en sont issus. 
* Le répertoire lib/ rassemble les fichiers .py prêts à être utilisés.
* Vous trouverez aussi quelques animations sur la page 
http://pcsi.kleber.free.fr/IPT/py4phys.html

## Roadmap

Pour le moment, j'essaie de rassembler toutes les idées concernant le cours de 
physique de PCSI, plus quelques illustrations annexes que j'ai toujours voulu 
mettre en oeuvre (comme l'exploration des zones chaotiques de la rotation 
d'Hypérion autour de Saturne).

## Description succincte des fichiers

### Bloc Induction
* I1_lignes_champ_magnetique.py: Code écrit par Sylvain Condamin (adapté 
d'un code de Thierry Pré) pour simuler les lignes de champ magnétique autour de 
divers objets (fil infini, dipôle magnétique ou spire)

### Bloc Mécanique
* M4_oscillateur_de_landau_portrait_de_phase.py: Portrait de 
phase pour un oscillateur de Landau
* M4_pendule_simple_portrait_de_phase.py: fabrication du 
portrait de phase d'un pendule simple. 
* M_hyperion.py: Étude d'une section de Poincaré pour la rotation propre 
d'Hypérion (satellite de Saturne) qui mette en avant le caractère chaotique 
d'une telle rotation (cf Ian Stewart, "Dieu joue-t-il aux dés" pour une 
introduction à cette problématique).
* M_papillon_de_lorentz.py: Illustration du concept 
d'attracteur étrange à l'aide du papillon de Lorenz (cf encore Ian Stewart 
dans le même livre)
* portrait_de_phase.py: Module générique pour produire un 
portrait de phase

### Bloc Signal
* S01_oscillateur_harmonique_energie.py: Illustration de la conservation de 
l'énergie pour un oscillateur harmonique.
* S01_oscillateur_harmonique_periode.py: Illustration de l'isochronisme des 
oscillations pour un oscillateur harmonique.
* S02_onde_progressive.py: Illustration de la notion d'onde progressive
* S02_onde_progressive_animation_superposition.py: Petite animation sur 
l'exemple précédent en superposant plusieurs ondes se déplaçant à diverses 
vitesses.
* S03_battements.py: Illustration de la notion de battements lors de la 
superposition de deux ondes de fréquences voisines.
* S03_diffraction.py: Diffraction (2D) d'une onde plane après passage d'une 
ouverture plane. On peut jouer sur l'angle d'incidence sur l'ouverture.
* S03_fresnel.py: Fabrication d'énoncés et de corrigés pour entraîner les 
élèves sur les constructions de Fresnel.
* S03_interferences.py: Animation montrant la mise en place d'interférences 
lors de la superposition des signaux en provenance de deux points sources.
* S04_arc_en_ciel_turtle.py: Programme 'turtle' écrit par Tom Morel pour 
expliquer la réfraction à l'intérieur d'une goutte d'eau.
* S05_distortion_chromatique.py: Programme 'turtle' écrit par Tom Morel pour 
mettre en avant la dépendance de la distance focale avec la couleur des rayons 
incidents
* S05_gauss_4P.py: Programme 'turtle' écrit par Tom Morel pour illustrer la 
règle des "4P" (Plus Plat, Plus Près)
* S05_lentilles_construction_graphique.py (non encore fait): Illustration des 
construction graphique pour les lentilles
* S06_paquet_d_ondes_MQ.py: Programme écrit par Miriam Heckmann pour simuler 
un paquet d'ondes en mécanique quantique
* S11_filtre_bizarre.py: Dessine le diagramme de Bode d'un filtre du type 
(A+jw/w1)/(1+jw/w2)
* S11_filtre_derivateur.py: Diagramme de Bode pour deux filtres où il faut 
déterminer la zone qui se comporte comme un dérivateur
* S11_filtre_diagrammes_en_amplitudes.py: Diagrammes de Bode en amplitude pour 
détermination graphique de w0 et Q.
* S11_filtre_integrateur.py: Diagramme de Bode pour deux filtres où il faut 
déterminer la zone qui se comporte comme un intégrateur
* S11_filtres_second_ordre.py: Exemples de génération de diagramme de Bode 
pour des filtre du second ordre en utilisant le module 'bode.py'
* bode.py: Module de génération de diagrammes de Bode.

### Bloc Thermodynamique
* T1_balles_rebondissantes_en_boite.py: Simulation des billes à 2D coincées 
dans une boite et soumises à la gravité ainsi qu'aux chocs pour montrer la loi 
de répartition de Boltzmann de la densité de balles en fonction de l'altitude.
* T1_particules_en_boite_libre.py: Simulation d'un gaz parfaits avec chocs 
pour appréhender les notions de libre parcours moyen et de marche aléatoire.
* T1_particules_en_boite_mouvement_brownien.py (non encore fait): Comme la 
simulation précédente mais en rajoutant une "grosse" particule au milieu qui 
serait, sur certains intervalles de temps, la seule visible pour appréhender 
la notion de mouvement Brownien découvert en observant des grains de pollens 
dans une solution aqueuse.
* T2_diagramme_PT_coolprop.py: génération d'un diagramme PT 
pour un fluide donné à partir du module CoolProp
* T2_diagramme_Pv_coolprop.py: génération d'un diagramme Pv 
pour un fluide donné à partir du module CoolProp
* T2_reseau_d_isothermes_coolprop.py: génération d'un réseau d'isothermes 
d'Andrews pour montrer comment on peut déterminer "à la main" la courbe de 
saturation dans un diagramme (P,v)
* T5_isentropique_GP_vs_gaz_reel_coolprop.py (non encore fait): Comparaison 
des isentropiques prédites par le modèle du gaz parfait à celles données par 
le module CoolProp.
* T6_cycle_de_carnot_reel_et_GP.py: Comparaison des prédictions d'un modèle de 
gaz parfait à celle du module CoolProp pour un cycle de Carnot (deux 
isentropiques et deux isothermes).
* T6_diagramme_Ph_coolprop.py: génération d'un diagramme 
enthalpique complet à l'aide du module CoolProp.
* T6_diagramme_Ts_coolprop.py: génération d'un diagramme 
entropique complet à l'aide du module CoolProp.
* T6_resolution_cycle_diesel.py: résolution d'un exercice classique sur un 
cycle Diesel à double combustion à l'aide du module CoolProp et de manière 
théorique avec le modèle du gaz parfait.


## TODO
### Bloc Induction
* I2_champ_tournant_diphase.py (non encore écrit): Fabrique une petite 
animation pour illustrer la notion de champ tournant à partir de deux bobines 
en quadrature de phase.
* I2_champ_tournant_triphase.py (non encore écrit): Comme le précédent, mais 
en triphasé.
* I4_couplage_de_deux_circuits.py: résolution numérique d'un couplage de 
circuits oscillants pour illustrer notamment la notion de battements en cas de 
couplage faible.

### Bloc Mécanique
* M2_trainee.py (non encore fait): illustration de l'influence de la traînée 
sur un tir d'obus.
* M2_trainee_portrait_de_phase.py (non encore fait): pareil via un portrait de 
phase.
* M4_oscillateur_de_landau_effets_non_lineaires.py (non encore fait): Non 
isochronisme des oscillations dans le cas d'un oscillateur de Landau.
* M4_pendule_simple_non_isochronisme.py (non encore fait): Non isochronisme 
des oscillations pour un pendule simple.
* M4_pendule_simple_oscillations_amorties.py (non encore fait): Oscillations 
amorties dans le cadre du pendule simple.
* M5_mouvement_dans_champ_E_et_B.py (non encore fait): calcul de la 
trajectoire d'une particule chargée soumise à la fois à un champ E et un champ 
B.
* M5_mouvement_helicoidal.py (non encore fait): Trajectoire d'une particule 
chargée soumise uniquement à un champ magnétique.
* M_pendule_double.py (non encore fait): Illustration de la dépendance aux 
conditions initiales pour les mouvements chaotiques sur l'exemple du pendule 
double rigide.

### Bloc Signal

* S03_ondes_stationnaires.py (non encore fait): Illustration de la notion 
d'onde stationnaire lors de la superposition d'ondes progressives de sens 
opposés
* S04_lois_de_descartes.py (non encore fait): Illustration de la loi de 
Descartes via une animation de réfraction pour de multiples incidences.
* S07_elec_resolution_pivot_de_gauss.py (non encore fait): Résolution d'un 
système électrique linéaire sans dérivées temporelles à l'aide d'un pivot de 
Gauss
* S08_circuit_premier_ordre_complexe.py (non encore fait): Résolution d'un 
système électrique complexe en se contentant d'écrire les lois des mailles, 
des noeuds et relations électriques de chaque dipôle.
* S08_circuit_premier_ordre_simple.py (non encore fait): Résolution d'un    
système électrique simple en se contentant d'écrire les lois des mailles,   
des noeuds et relations électriques de chaque dipôle.
* S09_oscillateur_amorti_libre.py (non encore fait): 
* S10_oscillateur_amorti_force.py (non encore fait):

### Bloc Thermodynamique
* T1_particules_en_boite_mouvement_brownien.py (non encore fait): Comme la 
simulation précédente mais en rajoutant une "grosse" particule au milieu qui 
serait, sur certains intervalles de temps, la seule visible pour appréhender 
la notion de mouvement Brownien découvert en observant des grains de pollens 
dans une solution aqueuse.
* T5_isentropique_GP_vs_gaz_reel_coolprop.py (non encore fait): Comparaison 
des isentropiques prédites par le modèle du gaz parfait à celles données par 
le module CoolProp.


### Divers
* Regarder le potentiel de "latexification" des figures et écrire un module 
dédié.
