# Capacité numériques en Physique, CPGE, pour le lycée Kléber

## Présentation

Le présent dépôt vise à rassembler, sous forme de Notebook Jupyter, les 
capacités numériques du programme de CPGE. L'idée est de fournir un Notebook à 
compléter aux élèves et de les laisser explorer. Bien sûr, pour qu'il y ait 
une certaine «motivation», il faudra associer cela à une note et don trouver 
un moyen de quantifier le travail, c'est pourquoi chaque notebook démarre par 
l'importation de valeurs numériques stockées dans un fichier externe (que le 
professeur peut donc changer lors de l'évaluation) et doit terminer par le 
stockage dans la variable `reponse` du résultat demandé (sous la forme 
demandée, qui peut-être une valeur simple ou une liste de valeurs)

Les «vraies» capacités numériques du programme contiennent `_CapNum_` dans 
leur nom alors que les autres sont simplement préfixées par le domaine de la 
physique (`meca_`, `elec_`, `thermo_`, etc.) qu'elles concernent.

## Recensement

Voici les capacités numériques recensées dans les différents programmes:

### Physique, commun MPSI/PCSI/MP2I et chimie PCSI

* [X] `incertitudes_CapNum_variabilite_grandeur_composee`: simuler un processus aléatoire permettant de caractériser la variabilité de la valeur d'une grandeur composée
* [X] `incertitudes_CapNum_regression_lineaire`: simuler un processus aléatoire de variation des valeurs expérimentales de l'une des grandeurs -- simulation Monte-Carlo -- pour évaluer l'incertitude sur les paramètres du modèle.

### Physique, commun MPSI/PCSI/MP2I

* [ ] `elec_CapNum_euler_reponse_premier_ordre`: mettre en œuvre la méthode d'Euler pour simuler la réponse d'un système linéaire du premier ordre à une excitation de forme quelconque.
* [ ] `elec_CapNum_action_filtre`: simuler l'action d'un filtre sur un signal périodique dont le spectre est fourni. Mettre en évidence l'influence des caractéristiques du filtre sur l'opération de filtrage.
* [ ] `meca_CapNum_effets_non_lineaires`: résoudre numériquement une équation différentielle du deuxième ordre non-linéaire et faire apparaître l'effet des termes non-linéaires.
* [ ] `meca_CapNum_trajectoires_champ_force_centrale_conservatif`: obtenir des trajectoires d'un point matériel soumis à un champ de force centrale conservatif.
* [ ] `meca_CapNum_pendule_pesant`: Mettre en évidence le non isocrhonisme des oscillations.

### Physique PCSI only

* [ ] `thermo_CapNum_temperature_pression_atmosphere`: Étudier les variations de température et de pression dans l'atmosphère.

### Chimie MPSI only

* [ ] `chimie_CapNum_etat_final_une_reaction`: Déterminer l'état final d'un système siège d'une transformation, modélisée par une réaction à partir des conditions initiales et valeur de la constante d'équilibre.

### Physique MP2I only

* [ ] `optique_CapNum_stigmatisme_demi_boule`: tester le stigmatisme approché d'une lentille demi-boule pour les rayons proches de l'axe optique.
* [ ] `elec_CapNum_systeme_lineaire_deuxieme_ordre`: Simuler la réponse d'un système linéaire du deuxième ordre à une excitation de forme quelconque.

### Chimie PCSI only

* [ ] `chimie_CapNum_etat_final_une_reaction`: Déterminer l'état final d'un système siège d'une transformation, modélisée par une réaction à partir des conditions initiales et valeur de la constante d'équilibre.
* [ ] `chimie_CapNum_etat_final_deux_reactions`: Déterminer l'état final d'un système siège d'une transformation, modélisée par deux réactions à partir des conditions initiales et valeurs des constantes d'équilibre.
* [ ] `chimie_CapNum_trace_evolution_temporelle`: À partir de données expérimentales, tracer l'évolution temporelle d'une concentration, d'une vitesse volumique de formation ou de consommation, d'une vitesse de réaction et tester une loi de vitesse donnée

### Chimie PCSI-PC, only

* [ ] `chimie_CapNum_cinetique_concentrations`: Établir un système d’équations différentielles et le résoudre numériquement afin de visualiser l’évolution temporelle des concentrations et de leurs dérivées dans le cas d’un mécanisme à deux actes élémentaires successifs. Mettre en évidence l’étape cinétiquement déterminante ou l’approximation de l’état quasi-stationnaire d’un intermédiaire réactionnel.
* [ ] `chimie_CapNum_controle_thermo_ou_cinetique`: Établir un système d’équations différentielles et le résoudre numériquement, avec un langage de programmation, afin de visualiser l’évolution des concentrations au cours du temps pour mettre en évidence les situations de contrôle cinétique ou thermodynamique.

### Chimie PCSI-PC et PCSI-PSI

* [ ] `chimie_CapNum_diagramme_distribution`: Tracer le diagramme de distribution des espèces d’un ou plusieurs couple(s) acide-base, ou d’espèces impliquées dans une réaction de précipitation.
