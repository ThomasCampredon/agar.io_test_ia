import numpy as np
import math


class Objet_basique:
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

    def distance(self, objet):
        return math.sqrt(pow(objet.x() - self.x(), 2) + pow(objet.y() - self.y(), 2))
