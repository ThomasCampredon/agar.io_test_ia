import pygame as pg
import numpy as np

from environnement import Environnement


if __name__ == '__main__':
    running = True

    pg.init()

    clock = pg.time.Clock()

    enviro = Environnement()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                print("ARRET")

        enviro.update()
        enviro.draw()
        clock.tick(144)

    pg.quit()
