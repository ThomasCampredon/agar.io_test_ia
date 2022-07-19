import numpy as np


def vecteur_unitaire(vecteur: np.ndarray) -> np.ndarray:
    """
    Retourne le vecteur unitaire du vecteur en paramètre

    :return: np.ndarray
    """
    if vecteur is not None:
        return vecteur / np.linalg.norm(vecteur)
    else:
        return np.zeros((2,))


