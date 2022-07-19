import pygame as pg
import pygame.gfxdraw
import numpy as np

from pygame.sprite import AbstractGroup
from objetbasique import ObjetBasique
from mangeable import Mangeable


class Nourriture(pg.sprite.Sprite, ObjetBasique, Mangeable):
    """
    Classe pour gérer la nourriture qui apparaitra aléatoirement sur le canvas
    """

    def __init__(self, x: int, y: int, poids=1, *groups: AbstractGroup):
        pg.sprite.Sprite.__init__(self, *groups)
        ObjetBasique.__init__(self, x, y)
        Mangeable.__init__(self, poids)

        self.radius = 3
        self.image = pg.Surface([self.radius, self.radius])
        self.rect = self.image.get_rect(center=(x, y))
        self.color = (125, 25, 125)

    def draw(self, screen, pos_screen: np.ndarray):
        pos_relative = self.position_relative(pos_screen)

        try:
            pg.gfxdraw.aacircle(screen, int(pos_relative[0]), int(pos_relative[1]), self.radius, self.color)
            pg.gfxdraw.filled_circle(screen, int(pos_relative[0]), int(pos_relative[1]), self.radius, self.color)
        except ValueError:
            pass
