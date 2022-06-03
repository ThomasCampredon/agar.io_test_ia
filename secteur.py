import pygame as pg
import numpy as np
from pygame.sprite import AbstractGroup
from nourriture import Nourriture


def pos_point_relatif(x_global, y_global, pos_screen):
    pos_relative = np.zeros((2,))

    pos_relative[0] = x_global - pos_screen[0]
    pos_relative[1] = y_global - pos_screen[1]

    return pos_relative


def draw_rectangle_vide(screen, couleur_ligne: tuple, haut_gauche, haut_droite, bas_gauche, bas_droite, largeur_ligne):
    # ligne haute
    pg.draw.line(screen, couleur_ligne, haut_gauche, haut_droite, largeur_ligne)

    # ligne basse
    pg.draw.line(screen, couleur_ligne, bas_gauche, bas_droite, largeur_ligne)

    # ligne droite
    pg.draw.line(screen, couleur_ligne, haut_droite, bas_droite, largeur_ligne)

    # ligne gauche
    pg.draw.line(screen, couleur_ligne, haut_gauche, bas_gauche, largeur_ligne)


class Secteur(pg.sprite.Sprite):
    def __init__(self, x_min, x_max, y_min, y_max, num_horizontal, num_vertical, *groups: AbstractGroup):
        pg.sprite.Sprite.__init__(self, *groups)

        # position dans le canvas
        self.num_horizontal = num_horizontal
        self.num_vertical = num_vertical

        # délimitations du secteur
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        # rectangle pour la collision
        self.rect = pg.Rect(x_min, y_min, x_max - x_min, y_max - y_min)

        # groupe pour enregistrer les nourritures présentes dans le vecteur
        self.nourritures = pg.sprite.Group()

    def ajouter_nourriture(self, nourriture: Nourriture):
        self.nourritures.add(nourriture)

    def draw(self, screen, pos_screen: np.ndarray):
        haut_gauche = pos_point_relatif(self.x_min, self.y_min, pos_screen)
        haut_droite = pos_point_relatif(self.x_max, self.y_min, pos_screen)
        bas_gauche = pos_point_relatif(self.x_min, self.y_max, pos_screen)
        bas_droite = pos_point_relatif(self.x_max, self.y_max, pos_screen)

        couleur_ligne = (255, 255, 255)
        largeur_ligne = 1

        draw_rectangle_vide(screen, couleur_ligne, haut_gauche, haut_droite, bas_gauche, bas_droite, largeur_ligne)
