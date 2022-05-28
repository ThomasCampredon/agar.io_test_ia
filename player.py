from bete import Bete
import pygame as pg
import numpy as np
import math


class Player(Bete):
    def __init__(self, x, y, vitesse):
        Bete.__init__(self, x, y, vitesse)
        self.color = (200, 128, 10)

    def update(self, liste_nourriture, liste_bete=None):
        destination = pg.mouse.get_pos()
        destination = np.array(destination)

        self.move(destination)

        self.update_detection()
