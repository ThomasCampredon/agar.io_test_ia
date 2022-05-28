import pygame as pg

from environnement import Environnement


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
                    print("Spawn 1 bête")

        if not pause:
            # on ajoute l'arrière-plan à la surface
            enviro.screen.fill((0, 0, 0))

            # on calcule les mouvements des bêtes
            enviro.update()

            # on affiche les bêtes et les nourritures
            enviro.draw()

            # on met à jour l'affichage
            pg.display.flip()

            clock.tick(FPS)

    pg.quit()
