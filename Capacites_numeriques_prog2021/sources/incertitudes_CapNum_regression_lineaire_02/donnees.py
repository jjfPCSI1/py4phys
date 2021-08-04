import numpy as np
import numpy.random as rd

rd.seed(1)

N = 10**4

# Lecture des données

t, x = np.loadtxt('donnees.txt', unpack = True)

u_t = 1 # en s
u_x = 1 # en micromol/L

