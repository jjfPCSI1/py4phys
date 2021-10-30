import numpy as np
G = 1
M = 1
R0 = [1, 2, 3, 4, 5, 6, 0.5]
R0 = R0 + R0
V0 = [1] * 6 + [0.5] * 7 + [0.25]
temps = np.linspace(0, 10 * np.pi, 1000)
