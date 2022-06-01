import numpy as np
import math


class ObjetBasique:
    def __init__(self, x: int, y: int):
        self.pos = np.ndarray((2,))
        self.pos[0] = x
        self.pos[1] = y

    def x(self):
        """
        :return: l'index en abscisse
        """
        return self.pos[0]

    def y(self):
        """
        :return: l'index en ordonnée
        """
        return self.pos[1]

    def distance_manhattan(self, objet):
        """
        Donne la distance de manhattan, calculée plus rapidement que la distance exacte
        """
        return abs(objet.x() - self.x()) + abs(objet.y() - self.y())

    def distance(self, objet) -> float:
        return math.sqrt(pow(objet.x() - self.x(), 2) + pow(objet.y() - self.y(), 2))

    def position_relative(self, pos_screen: np.ndarray) -> np.ndarray:
        """
        Retourne les coordonnées de l'objet dans le repère de la fenêtre
        """

        pos_relative = np.zeros((2,))

        pos_relative[0] = self.x() - pos_screen[0]
        pos_relative[1] = self.y() - pos_screen[1]

        return pos_relative
