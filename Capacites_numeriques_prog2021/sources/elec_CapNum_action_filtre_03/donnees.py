import numpy as np

t = np.linspace(0, 10, 300)
signal = np.array([(-1)**(int(ti)) for ti in t])
t = t / 1e3

def H(f):
    f0 = 100
    return 1 / (1 + 1j * f / f0)
