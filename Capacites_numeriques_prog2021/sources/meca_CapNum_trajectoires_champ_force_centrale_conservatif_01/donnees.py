import numpy as np
G = 1
M = 4
R0 = [1, 2, 3, 4, 5, 6, 0.5]
V0 = np.array([(G * M / R0[i])**0.5 for i in range(len(R0)) ])
R0 = np.array(R0 + R0)
V0 = np.array(list(V0 / 2**0.5) + list(V0 * 1.2))
temps = np.linspace(0, 20 * np.pi, 10000)
