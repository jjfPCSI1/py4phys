import numpy as np
import numpy.random as rd

rd.seed(1)

x = 34.56
ux = 2
y = 0.765
uy = 3e-1

N = 10**6

def grandeur(x, y):
    """
    Fonction prenant en argument
    """
    return x / (x - 10 * y)


