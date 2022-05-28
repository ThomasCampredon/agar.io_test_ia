import pygame as pg

from environnement import Environnement
from player import Player

if __name__ == '__main__':
    running = True

    pg.init()

    clock = pg.time.Clock()

    enviro = Environnement(joueur=True)
    pause = False
    FPS = 75

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

        clock.tick(FPS)

    pg.quit()
