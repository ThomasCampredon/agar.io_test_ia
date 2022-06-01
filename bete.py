import pygame as pg
import pygame.gfxdraw
import numpy as np
import math

from objetbasique import ObjetBasique
from mangeable import Mangeable
from pygame.sprite import AbstractGroup


class Bete(pg.sprite.Sprite, ObjetBasique, Mangeable):
    """
    Classe pour les bêtes, qui mangent de la nourriture ou d'autre bête
    """

    RAYON_INITIAL = 15

    def __init__(self, x: int, y: int, vitesse=2, poids: int = 15, *groups: AbstractGroup):

        # todo définir une classe stratégie et ses classes filles pour faire varier le update

        # init superclasses
        pg.sprite.Sprite.__init__(self, *groups)
        ObjetBasique.__init__(self, x, y)
        Mangeable.__init__(self, poids)

        # vitesse de la bête
        self.vitesse = vitesse

        self.radius = 2 * math.sqrt(self.poids) + self.RAYON_INITIAL

        self.image = pg.Surface([self.radius, self.radius])
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.height = self.radius * 2
        self.rect.width = self.radius * 2

        self.color = (0, 200, 125)

    def update_radius(self):
        self.radius = 2 * math.sqrt(self.poids) + self.RAYON_INITIAL

    def nourriture_la_plus_proche(self, liste_secteur):
        dist_min = 999999  # distance minimal jusqu'à une nourriture
        nourriture_proche = None  # nourriture la plus proche

        for secteur in liste_secteur:
            # pour chaque nourriture
            for nourriture in secteur.nourritures:
                # distance simplifié entre la nourriture et la bête
                dist = self.distance_manhattan(nourriture)

                # si on a plus proche
                if dist < dist_min:
                    dist_min = dist
                    nourriture_proche = nourriture

        return nourriture_proche, dist_min

    def liste_secteur_collision(self, liste_secteur):
        # todo faire en sorte de prendre les secteurs autours de ceux qu'on collisionne
        liste_collision = []  # liste des secteurs en collision avec la bête

        for secteur in liste_secteur:
            # si on a collision
            if pg.sprite.collide_rect(self, secteur):
                liste_collision.append(secteur)  # on ajoute le secteur à la liste

        return liste_collision

    def manger(self, mangeable: Mangeable):
        # on prend le poids du mangeable
        self.poids += mangeable.poids

        # on met à jour le rayon du cercle en fonction du poids
        self.update_radius()

        # on met à jour la taille du carré pour la détection de collision
        self.rect.height = self.radius * 2
        self.rect.width = self.radius * 2

    def move(self, destination: np.ndarray):
        # vecteur direction vers la destination
        direction = destination - self.pos

        # on transforme le vecteur direction en vecteur unitaire
        direction = direction / np.linalg.norm(direction)

        # on modifie la position avec la direction et la vitesse en prenant en compte la taille
        self.pos += direction * (self.vitesse - (math.sqrt(self.radius) * 0.05))  # todo voir si possible d'avoir mieux

    # todo essayer de faire le split()

    def update_detection(self):
        """
        On met à jour la position de la hitbox
        """
        self.rect.center = (self.x(), self.y())

    def update(self, liste_secteur, liste_bete=None):  # todo en cours
        # nourriture à atteindre
        destination, distance = self.nourriture_la_plus_proche(self.liste_secteur_collision(liste_secteur))

        try:
            # se déplacer vers la destination
            self.move(destination.pos)
        except AttributeError:
            pass

        # on met à jour la position du carré pour la détection de collision
        self.update_detection()

    def draw(self, screen, pos_screen: np.ndarray):
        pos_relative = self.position_relative(pos_screen)

        pg.gfxdraw.aacircle(screen, int(pos_relative[0]), int(pos_relative[1]), int(self.radius), self.color)
        pg.gfxdraw.filled_circle(screen, int(pos_relative[0]), int(pos_relative[1]), int(self.radius), self.color)

        # on met le poids en texte
        font_obj = pygame.font.Font('freesansbold.ttf', 16)
        text_surface_obj = font_obj.render(str(self.poids), True, "white")
        text_rect_obj = text_surface_obj.get_rect(center=(pos_relative[0], pos_relative[1]))
        screen.blit(text_surface_obj, text_rect_obj)
