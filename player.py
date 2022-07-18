import math

from bete import Bete
import pygame as pg
import numpy as np

from partiebete import PartieBete


class Player(Bete):
    def __init__(self, x, y, vitesse):
        Bete.__init__(self, x, y, (200, 128, 10), vitesse)
        self.origine_repere = None

        # todo retirer après les tests
        self.parties.append(PartieBete(x+30, y+30, vitesse, self.poids, (255, 50, 126)))
        self.parties.append(PartieBete(x - 30, y - 30, vitesse, self.poids, (126, 50, 255)))

    def update(self, liste_secteur, liste_bete=None):
        # on récupère la position de la souris dans la fenêtre
        destination = pg.mouse.get_pos()

        destination = np.array(destination)
        # on calcule les coordonnées de la destination dans le repere du canvas
        destination = destination + self.origine_repere

        centre_joueur = self.centre()

        # si la souris est suffisament éloigner du centre de la bete
        if math.sqrt(pow(destination[0] - centre_joueur[0], 2) + pow(destination[1] - centre_joueur[1], 2)) > 30:
            # on calcule la direction dans laquelle va avancer le joueur
            self.calculer_direction(destination)

            for partie in self.parties:
                partie.update(self.direction)

        # on gère les collisions entre les parties
        self.gerer_collisions_parties()

        # on met à jour le poids de la bête
        self.update_poids()

        # on regarde si on peut refusioner des parties qui ont été splitées
        self.reforme()