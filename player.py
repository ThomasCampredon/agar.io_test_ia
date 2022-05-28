from bete import Bete
import pygame as pg
import numpy as np


class Player(Bete):
    def __init__(self, x, y):
        Bete.__init__(self, x, y)
        self.color = (200, 128, 10)

    def update(self, liste_nourriture, liste_bete=None):
        destination = pg.mouse.get_pos()
        destination = np.array(destination)

        direction = destination - self.pos

        # on transforme le vecteur direction en vecteur unitaire
        direction = direction / np.linalg.norm(direction)

        # on modifie la position avec la direction et la vitesse
        self.pos += direction * self.vitesse

        self.update_detection()
