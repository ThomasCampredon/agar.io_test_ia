import pygame as pg
import pygame.gfxdraw
import numpy as np
import math

from objet_basique import Objet_basique
from mangeable import Mangeable
from pygame.sprite import AbstractGroup


class Bete(pg.sprite.Sprite, Objet_basique, Mangeable):
    """
    Classe pour les bêtes, qui mangent de la nourriture ou d'autre bête
    """

    def __init__(self, x: int, y: int, vitesse=2, detection_range: float = 100, poids: int = 15,
                 *groups: AbstractGroup):

        # todo définir une classe stratégie et ses classes filles pour faire varier le update

        # init superclasses
        pg.sprite.Sprite.__init__(self, *groups)
        Objet_basique.__init__(self, x, y)
        Mangeable.__init__(self, poids)

        # distance de vue de la bête
        self.detection_range = detection_range

        # vitesse de la bête
        self.vitesse = vitesse

        self.radius = math.sqrt(self.poids)

        self.image = pg.Surface([self.radius, self.radius])
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.height = self.radius * 2
        self.rect.width = self.radius * 2

        self.color = (0, 200, 125)

    def nourriture_la_plus_proche(self, liste_nourriture):
        dist_min = 999999  # distance minimal jusqu'à une nourriture
        nourriture_proche = None  # nourriture la plus proche

        # pour chaque nourriture
        for nourriture in liste_nourriture:
            # distance simplifié entre la nourriture et la bête
            dist = self.distance(nourriture)

            # si on a plus proche
            if dist < dist_min:
                dist_min = dist
                nourriture_proche = nourriture

        return nourriture_proche, dist_min

    def manger(self, mangeable: Mangeable):
        # on prend le poids du mangeable
        self.poids += mangeable.poids

        # on met à jour le rayon du cercle en fonction du poids
        self.radius = math.sqrt(self.poids)

        # on met à jour la taille du carré pour la détection de collision
        self.rect.height = self.radius * 2
        self.rect.width = self.radius * 2

    def update(self, liste_nourriture, liste_bete=None):
        # nourriture à atteindre
        destination, distance = self.nourriture_la_plus_proche(liste_nourriture)

        # si on voit la nourriture la plus proche
        if distance < self.detection_range:
            # vecteur direction vers la nourriture
            direction = destination.pos - self.pos

            # on transforme le vecteur direction en vecteur unitaire
            direction = direction / np.linalg.norm(direction)

            # on modifie la position avec la direction et la vitesse
            self.pos += direction * self.vitesse  # todo prendre en compte le poids

            # on met à jour la position du carré pour la détection de collision
            self.rect.center = (self.x(), self.y())

    def draw(self, screen):
        # pg.draw.circle(screen, self.color, (self.x(), self.y()), self.radius)
        pg.gfxdraw.aacircle(screen, int(self.x()), int(self.y()), int(self.radius), self.color)
        pg.gfxdraw.filled_circle(screen, int(self.x()), int(self.y()), int(self.radius), self.color)

        # on met le poids en texte
        font_obj = pygame.font.Font('freesansbold.ttf', 16)
        text_surface_obj = font_obj.render(str(self.poids), True, "white")
        text_rect_obj = text_surface_obj.get_rect(center=(self.x(), self.y()))
        screen.blit(text_surface_obj, text_rect_obj)

    def draw_detection_range(self, screen):
        pg.draw.circle(screen, (125, 125, 125, 120), (self.x(), self.y()), self.detection_range)
