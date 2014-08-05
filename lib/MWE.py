
import numpy as np               
import CoolProp.CoolProp as CP   # Les outils thermodynamiques
import matplotlib.pyplot as plt  # Les outils graphiques

#Infos pour le point 4: T=2173.0 K, v=0.097 m^3/kg, P=65.0 bar
#Infos pour le point 5: T=1110.2 K, v=0.8407 m^3/kg, P=3.8 bar

fluid = 'Air'
T1 = 2173
P1 = 65e5
S1 = CP.PropsSI('S','P',P1,'T',T1,fluid)
P2 = 3.8e5
P_lin = np.linspace(P1,P2,1000)
D_lin = CP.PropsSI('D','P',P_lin,'S',S1,fluid)

plt.plot(D_lin,P_lin)

plt.savefig('MWE.png')

import CoolProp
print(CoolProp.__version__)
