import numpy as np


def vecteur_unitaire(vecteur: np.ndarray) -> np.ndarray:
    """
    Retourne le vecteur unitaire du vecteur en paramètre

    :return: np.ndarray
    """
    return vecteur / np.linalg.norm(vecteur)


