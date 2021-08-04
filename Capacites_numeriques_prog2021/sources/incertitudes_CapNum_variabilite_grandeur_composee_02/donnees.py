import numpy as np
import numpy.random as rd

rd.seed(1)

p  = -0.225   # position de l'objet en m
pp = 1.356    # position de l'image en m

u_p  = 0.002  # Incertitude-type sur la position de l'objet en m
u_pp = 0.1    # Incertitude-type sur la position de l'image en m 

N = 10**6

