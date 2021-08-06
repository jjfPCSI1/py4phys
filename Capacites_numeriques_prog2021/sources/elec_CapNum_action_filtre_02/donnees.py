import numpy as np

freqs, FFT = np.loadtxt('donnees.txt', unpack = True)

FFT = FFT[freqs < 1000]
freqs = freqs[freqs < 1000]

def H_PBas(f, Q=10):
    """
    Fonction de transfert de passe-bas
    à valeur complexe qui prend une fréquence en argument
    """
    f0 = 0.25e3
    return 1 / ( 1 + 1j * f / (Q * f0) - (f / f0)**2)

def H_PBande(f, Q=30):
    """
    Fonction de transfert de passe-bande à amplification 
    à valeur complexe qui prend une fréquence en argument
    """
    f0 = 0.45e3
    return (1j * f / f0) / ( 1 + 1j * f / (Q * f0) - (f / f0)**2)

liste_H = [H_PBas, H_PBande]

