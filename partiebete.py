import pygame as pg
import numpy as np
import math
import pygame.gfxdraw

from objetbasique import ObjetBasique
from mangeable import Mangeable
from secteur import Secteur

from pygame.sprite import AbstractGroup


class PartieBete(pg.sprite.Sprite, ObjetBasique, Mangeable):
    RAYON_INITIAL = 15

    def __init__(self, x, y, vitesse, poids, couleur: tuple, *groups: AbstractGroup):
        ObjetBasique.__init__(self, x, y)
        pg.sprite.Sprite.__init__(self, *groups)
        Mangeable.__init__(self, poids)

        # vitesse de la partie
        self.vitesse = vitesse

        # acceleration
        self.acceleration = np.zeros((2,))

        self.radius = 2 * math.sqrt(self.poids) + self.RAYON_INITIAL

        # booléen pour savoir si on peut re fusionner la partie avec les autres parties
        self.fusionnable = False

        self.image = pg.Surface([self.radius, self.radius])
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.height = self.radius * 2
        self.rect.width = self.radius * 2

        self.color = couleur

    def update_radius(self):
        """
        Mise à jour du rayon en fonction du poids
        """
        self.radius = 2 * math.sqrt(self.poids) + self.RAYON_INITIAL

    def liste_secteur_collision(self, liste_secteur: dict[(int, int)]) -> set[Secteur]:
        """
        Donne la liste des secteurs en collision avec la partie

        :return: un set de secteur
        """
        set_collision = set()  # set des secteurs en collision avec la bête

        for secteur in liste_secteur.values():
            # si on a collision
            if pg.sprite.collide_rect(self, secteur):
                set_collision.add(secteur)  # on ajoute le secteur à la liste

        # set des secteurs autour de ceux en collisions
        set_autour = set()

        # pour chaque secteur en collision
        for secteur in set_collision:
            # couple (x, y) de coordonnées du secteur
            index_x = secteur.num_horizontal
            index_y = secteur.num_vertical

            # pour les abscisses des secteurs à côté (+2, car on exclut la valeur de fin dans le for)
            for i in range(max(0, index_x - 1), index_x + 2):
                # pour les ordonnés des secteurs à côté
                for j in range(max(0, index_y - 1), index_y + 2):
                    try:
                        # on rajoute les secteurs autour du secteur
                        set_autour.add(liste_secteur[(i, j)])
                    except KeyError:
                        pass

        # on ajoute les secteurs autours dans la liste des collisions
        for secteur_autour in set_autour:
            set_collision.add(secteur_autour)

        return set_collision

    def manger(self, mangeable: Mangeable) -> None:
        # on prend le poids du mangeable
        self.poids += mangeable.poids

        # on met à jour le rayon du cercle en fonction du poids
        self.update_radius()

    def move(self, direction: np.ndarray) -> None:
        # on modifie la position avec la direction et la vitesse en prenant en compte la taille
        self.pos += direction * (self.vitesse - (math.sqrt(self.radius) * 0.08)) + self.acceleration   # todo voir si
        # possible d'avoir mieux

    def update_hitbox(self) -> None:
        """
        On met à jour la position et la taille de la hitbox
        """
        self.rect.center = (self.x(), self.y())

        # on met à jour la taille du carré pour la détection de collision
        self.rect.height = self.radius * 2
        self.rect.width = self.radius * 2

    def collide(self, partie) -> bool:
        """
        Retourne vrai s'il y a collision entre la partie et la partie en paramètre

        :return: bool
        """
        return self.distance(partie) < self.radius + partie.radius

    def distance_contacte(self, partie) -> float:
        """
        Donne la distance entre les borts des deux cercles des parties
        """
        return self.distance(partie) - (self.radius + partie.radius)

    def update(self, direction: np.ndarray) -> None:
        try:
            # se déplacer vers la destination
            self.move(direction)
        except AttributeError:
            pass

        # on met à jour la position du carré pour la détection de collision
        self.update_hitbox()

    def draw(self, screen, pos_screen: np.ndarray) -> None:
        pos_relative = self.position_relative(pos_screen)

        try:
            # contour du cercle
            pg.gfxdraw.aacircle(screen, int(pos_relative[0]), int(pos_relative[1]), int(self.radius), self.color)

            # intérieur du cercle
            pg.gfxdraw.filled_circle(screen, int(pos_relative[0]), int(pos_relative[1]), int(self.radius), self.color)
        except ValueError:
            pass

        # on met le poids en texte
        font_obj = pg.font.Font('freesansbold.ttf', 16)
        text_surface_obj = font_obj.render(str(self.poids), True, "white")
        text_rect_obj = text_surface_obj.get_rect(center=(pos_relative[0], pos_relative[1]))

        # on donne les modifications au screen
        screen.blit(text_surface_obj, text_rect_obj)
