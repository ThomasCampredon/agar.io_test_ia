import math

from bete import Bete
import pygame as pg
import numpy as np


class Player(Bete):
    def __init__(self, x, y, vitesse):
        Bete.__init__(self, x, y, vitesse)
        self.color = (200, 128, 10)
        self.origine_repere = None

    def update(self, liste_secteur, liste_bete=None):
        # on récupère la position de la souris dans la fenêtre
        destination = pg.mouse.get_pos()

        destination = np.array(destination)
        # on calcule les coordonnées de la destination dans le repere du canvas
        destination = destination + self.origine_repere

        # si la souris est suffisament éloigner du centre de la bete
        if math.sqrt(pow(destination[0] - self.x(), 2) + pow(destination[1] - self.y(), 2)) > 30:
            # on calcule la direction dans laquelle va avancer le joueur
            self.calculer_direction(destination)

            for partie in self.parties:
                partie.update(self.direction)

