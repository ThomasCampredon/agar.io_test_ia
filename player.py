import math

from bete import Bete
import pygame as pg
import numpy as np


class Player(Bete):
    def __init__(self, x, y, vitesse):
        Bete.__init__(self, x, y, vitesse)
        self.color = (200, 128, 10)
        self.origine_repere = None

    def update(self, liste_nourriture, liste_bete=None):
        destination = pg.mouse.get_pos()

        destination = np.array(destination)
        destination = destination + self.origine_repere

        if math.sqrt(pow(destination[0] - self.x(), 2) + pow(destination[1] - self.y(), 2)) > 30:
            self.move(destination)

            self.update_detection()
