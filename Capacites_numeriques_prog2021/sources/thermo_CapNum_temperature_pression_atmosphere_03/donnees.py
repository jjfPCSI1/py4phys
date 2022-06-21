import numpy as np

M = 28.965e-3 # en kg/mol, donnée wikipédia 
P0= 101325    # en Pa, au niveau du sol

R = 8.314

R_T = 6378e3
g0 = 9.81
alpha = 6.5e-3
T0 = 273.16 + 15


def g(z):
    """Accélération de la pesanteur constante"""
    return g0 * (R_T / (R_T + z))**2

z11 = 11000
z20 = 20000
z32 = 32000
z47 = 47000
z51 = 51000
z71 = 71000
z86 = 86000

z = np.linspace(0, z86-1, 10**3) # 10**3 points en 0 et 44km (cf infra), 

def my_T(z):
    if z <= z11:
       zi = 0
       Ti = T0
       alpha = -6.5e-3
    elif z <= z20:
       zi = z11
       Ti = T(zi)
       alpha = 0
    elif z <= z32:
       zi = z20
       Ti = T(zi)
       alpha = 1e-3
    elif z <= z47:
       zi = z32
       Ti = T(zi)
       alpha = 2.8e-3
    elif z <= z51:
       zi = z47
       Ti = T(zi)
       alpha = 0
    elif z <= z71:
       zi = z51
       Ti = T(zi)
       alpha = -2.8e-3
    elif z <= z86:
       zi = z71
       Ti = T(zi)
       alpha = -2e-3
    else:
       Ti = T(z86)
       alpha = 0
       zi = z86
    return Ti + alpha * (z - zi)

z_standard = np.array([0, z11, z20, z32, z47, z51, z71, z86])
P_standard = np.array([101325, 22632, 5474.9, 868.02, 110.91, 66.939, 3.9564, 0.3734])
T_standard = 273.15 + np.array([15, -56.5, -56.5, -44.5, -2.5, -2.5, -58.5, -86.2])

T = np.vectorize(my_T)

alpha = -np.mean((np.log(P_standard[1:]) - np.log(P0)) / z_standard[1:])
