import pygame as pg

from environnement import Environnement

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 75


if __name__ == '__main__':
    running = True

    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    enviro = Environnement(joueur=True)
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
                    print("Spawn 1 bête")

        if not pause:
            # on ajoute l'arrière-plan à la surface
            screen.fill((0, 0, 0))

            # on calcule les mouvements des bêtes
            enviro.update()

            # on affiche les bêtes et les nourritures
            enviro.draw(screen)

            # on met à jour l'affichage
            pg.display.flip()

            clock.tick(FPS)

    pg.quit()
