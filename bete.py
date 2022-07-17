import pygame as pg
import pygame.gfxdraw
import numpy as np
import math

from nourriture import Nourriture
from objetbasique import ObjetBasique
from mangeable import Mangeable
from partiebete import PartieBete
from secteur import Secteur

from pygame.sprite import AbstractGroup


class Bete(pg.sprite.Sprite, Mangeable):
    """
    Classe pour les bêtes, qui mangent de la nourriture ou d'autre bête
    """

    def __init__(self, x: int, y: int, couleur: tuple = (0, 200, 125), vitesse=2, poids: int = 15,
                 *groups: AbstractGroup):

        # todo définir une classe stratégie et ses classes filles pour faire varier le update

        # init superclasses
        pg.sprite.Sprite.__init__(self, *groups)
        Mangeable.__init__(self, poids)

        # vitesse de la bête
        self.vitesse = vitesse

        # liste des parties de la bête
        self.parties: list[PartieBete] = list()
        self.parties.append(PartieBete(x, y, vitesse, poids, couleur))  # on ajoute une partie

        # direction dans laquelle va la bete
        self.direction = np.zeros((2,))

        self.color = couleur

    def centre(self) -> np.ndarray:
        """
        Retourne les cordonnées du point au centre des parties de la bête
        :return: np.array
        """
        centre = np.zeros((2,))  # coordonnées du centre

        # pour chaque partie
        for partie in self.parties:
            centre += partie.pos  # on additionne la position de la partie

        # on fait la moyenne des coordonnées
        centre /= len(self.parties)

        return centre

    def nourriture_la_plus_proche(self, liste_secteur) -> Nourriture:
        nourriture_proche = None  # nourriture la plus proche
        dist_min = 999999  # distance minimale jusqu'à une nourriture

        # pour chaque partie de la bête
        for partie in self.parties:
            for secteur in liste_secteur:
                # pour chaque nourriture
                for nourriture in secteur.nourritures:
                    # distance simplifié entre la nourriture et la bête
                    dist = partie.distance_manhattan(nourriture)

                    # si on a plus proche
                    if dist < dist_min:
                        dist_min = dist
                        nourriture_proche = nourriture

        return nourriture_proche

    def liste_secteur_collision(self, liste_secteur: dict[(int, int)]) -> set[Secteur]:
        liste_collision = set()  # set des secteurs en collision avec les parties de la bête

        # pour chaque partie de la bête
        for partie in self.parties:
            # on ajoute les secteurs en collision avec la partie dans la liste des collisions
            liste_collision = liste_collision.union(partie.liste_secteur_collision(liste_secteur))

        return liste_collision

    def calculer_direction(self, destination: np.ndarray) -> None:
        # vecteur direction vers la destination
        self.direction = destination - self.centre()

        # on transforme le vecteur direction en vecteur unitaire
        self.direction = self.direction / np.linalg.norm(self.direction)

    def update_poids(self):
        self.poids = 0

        for partie in self.parties:
            self.poids += partie.poids

    def split(self) -> None:
        print("split")
        pass
        # TODO essayer de faire le split()

    # todo gérer_collision entre les parties
    def gerer_collisions_parties(self):
        pass

    def update(self, liste_secteur: dict[(int, int)], liste_bete=None):
        # <<<<<<<<<<<<<<<<  todo mettre en place la stratégie
        # nourriture à atteindre
        destination = self.nourriture_la_plus_proche(self.liste_secteur_collision(liste_secteur))

        # si on a trouvé une destination
        if destination is not None:
            # on calcule la direction que la bête doit prendre pour atteindre la nourriture
            self.calculer_direction(destination.pos)

        # >>>>>>>>>>>>>>>>>

        try:
            # on met à jour les parties
            for partie in self.parties:
                partie.update(self.direction)
        except AttributeError:
            pass

        # on gère les collisions entre les parties
        self.gerer_collisions_parties()

        # on met à jour le poids de la bête
        self.update_poids()

    def draw(self, screen, pos_screen: np.ndarray):
        # on dessine chaque partie
        for partie in self.parties:
            partie.draw(screen, pos_screen)
