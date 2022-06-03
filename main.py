import pygame as pg

from environnement import Environnement

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 75

if __name__ == '__main__':
    running = True

    pg.init()
    pg.display.set_caption("Agar pas très io")
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    enviro = Environnement(True, SCREEN_WIDTH, SCREEN_HEIGHT)
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
                if event.key == pg.K_SPACE:
                    enviro.bete_focus.split()

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
