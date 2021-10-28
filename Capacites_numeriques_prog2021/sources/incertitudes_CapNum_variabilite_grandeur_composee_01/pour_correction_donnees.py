import numpy as np
import numpy.random as rd

rd.seed(1)

x = 134.56
ux = 20
y = 10.765
uy = 1

N = 10**6

def grandeur(x, y):
    """
    Fonction prenant en argument
    """
    return np.sqrt(x**2 + y**2) / (x - 5 * y) / 100


