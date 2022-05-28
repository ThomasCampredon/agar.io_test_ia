import pygame as pg
import numpy as np

from environnement import Environnement


if __name__ == '__main__':
    running = True

    pg.init()

    clock = pg.time.Clock()

    enviro = Environnement()
    pause = False

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                print("ARRET")

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    if not pause:
                        pause = True
                        print("Pause")
                    else:
                        pause = False
                        print("Relance")
                if event.key == pg.K_s:
                    enviro.ajouter_bete()

        if not pause:
            enviro.update()
            enviro.draw()
        clock.tick(144)

    pg.quit()
