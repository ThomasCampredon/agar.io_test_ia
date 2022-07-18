import pygame as pg
import pygame.gfxdraw
import numpy as np
import math
import utilitaires as uti

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
        self.direction = uti.vecteur_unitaire(self.direction)

    def update_poids(self) -> None:
        # on reset le poids
        self.poids = 0

        # pour chaque partie
        for partie in self.parties:
            # on ajoute le poids de la partie au poids total
            self.poids += partie.poids

    def split(self) -> None:
        """
        Sépare la bête en partie égale (ex : 1 partie de 50 → 2 parties de 25)
        """

        nombre_partie = len(self.parties)

        # on limite le nombre de parties maximum à 4
        if nombre_partie <= 2:
            # pour chaque partie de la bête
            for i in range(0, nombre_partie):
                # on divise le poids de la partie par 2
                self.parties[i].poids //= 2

                # partie en cours
                p1 = self.parties[i]

                # on cherche la position de la nouvelle partie
                p2_pos = p1.pos + (self.direction * (p1.radius*2))

                # on ajoute une nouvelle partie à la bête
                self.parties.append(PartieBete(p2_pos[0], p2_pos[1], p1.vitesse, p1.poids, p1.color))

        # TODO essayer de faire le split()

    def reforme(self):
        pass  # todo gérer la fusion des parties splitées

    def gerer_collisions_parties(self) -> None:
        """
        Fait en sorte que les parties d'une bête ne se superposent pas
        voir schemas/collision_parties.drawio.png pour plus de détails
        """

        # pour chaque partie
        for i in range(0, len(self.parties) - 1):
            # pour les autres parties
            for j in range(i + 1, i + len(self.parties)):

                # partie 1
                p1 = self.parties[i]

                # partie 2
                p2 = self.parties[j % len(self.parties)]

                # si la partie 1 se superpose à la partie p2
                if p1.collide(p2):
                    # vecteur entre les centres des parties
                    vect = p2.pos - p1.pos

                    # nouveau centre de p2
                    self.parties[j % len(self.parties)].pos = p1.pos + (uti.vecteur_unitaire(vect) * (p1.radius + p2.radius))

    def update(self, liste_secteur: dict[(int, int)], liste_bete=None) -> None:
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

        # on regarde si on peut refusioner des parties qui ont été splitées
        self.reforme()

    def draw(self, screen, pos_screen: np.ndarray) -> None:
        # on dessine chaque partie
        for partie in self.parties:
            partie.draw(screen, pos_screen)
