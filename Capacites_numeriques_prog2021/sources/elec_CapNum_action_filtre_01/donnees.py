import numpy as np

freqs, FFT = np.loadtxt('donnees.txt', unpack = True)

FFT = FFT[freqs < 1000]
freqs = freqs[freqs < 1000]

def H(f):
    """
    Fonction de transfert à valeur complexe qui prend une fréquence en argument
    """
    f0 = 0.5e3
    return (1j * f / f0) / ( 1 + 1j * f / f0)
