import numpy as np
import pygame as pg
import random as rd
import pygame.gfxdraw

from nourriture import Nourriture
from bete import Bete
from player import Player


class Environnement:
    LARGEUR = 4000
    HAUTEUR = 2000
    NB_NOURRITURE = LARGEUR * HAUTEUR // 5000
    NB_BETE = 5  # joueur inclus
    RATIO_TAILLE_POUR_MANGER = 1.2  # ex : une bête doit être 1.2 fois plus lourde que l'autre pour pouvoir la manger
    VITESSE_BASIQUE = 3

    def __init__(self, joueur=False, largeur_screen=1920, hauteur_screen=1080):
        self.nourritures = pg.sprite.Group()  # todo séparer les points en secteurs
        self.betes = pg.sprite.Group()
        self.generer_bete()

        self.bete_focus = None

        if joueur:
            joueur = Player(rd.randint(0, self.LARGEUR), rd.randint(0, self.HAUTEUR), self.VITESSE_BASIQUE)

            # on ajoute un joueur
            self.betes.add(joueur)

            # on enregistre le joueur pour qu'il soit au centre de l'écran
            self.bete_focus = joueur

            self.bete_focus.origine_repere = self.pos_repere_screen(largeur_screen, hauteur_screen)
        else:
            bete = self.ajouter_bete()

            # on enregistre la bête pour qu'elle soit au centre de l'écran
            self.bete_focus = bete

    def generer_nourriture(self):
        while len(self.nourritures) < self.NB_NOURRITURE:
            self.nourritures.add(Nourriture(rd.randint(0, self.LARGEUR), rd.randint(0, self.HAUTEUR)))

    def generer_bete(self):
        while len(self.betes) < self.NB_BETE-1:
            self.ajouter_bete()

    def ajouter_bete(self):
        bete = Bete(rd.randint(0, self.LARGEUR), rd.randint(0, self.HAUTEUR), self.VITESSE_BASIQUE)
        self.betes.add(bete)

        return bete

    def afficher_nourritures(self, screen, pos_screen:np.ndarray):
        for nourriture in self.nourritures:
            nourriture.draw(screen, pos_screen)

    def afficher_betes(self, screen, pos_screen:np.ndarray):
        for bete in self.betes:
            bete.draw(screen, pos_screen)

    def gerer_collisions_bete_betes(self, bete: Bete):
        # liste des bêtes qui se sont fait manger par une autre bête
        betes_mangees = []

        # pour les autres bêtes
        for autre_bete in self.betes:
            # si l'autre bête est différente de la bete actuelle
            if autre_bete is not bete:
                # si la bete est RATIO plus lourde que l'autre bete
                if bete.poids > self.RATIO_TAILLE_POUR_MANGER * autre_bete.poids:
                    # voir schemas/bete_mange_bete.png pour les détails
                    if (bete.distance(autre_bete) + autre_bete.radius) - bete.radius < autre_bete.radius / 2:
                        bete.manger(autre_bete)
                        betes_mangees.append(autre_bete)

        # on efface les bêtes qui se sont fait manger
        for dead_bete in betes_mangees:
            self.betes.remove(dead_bete)

    def gerer_collisions_bete_nourritures(self, bete):
        # collision entre la bete et les nourritures
        nourriture_manger = pg.sprite.spritecollide(bete, self.nourritures, True)

        # pour chaque nourriture qu'on touche
        for i in range(0, len(nourriture_manger)):
            # la bête mange la nourriture
            bete.manger(nourriture_manger[i])

    def gerer_collisions(self):
        # pour chaque bête de l'environnement
        for bete in self.betes:
            self.gerer_collisions_bete_nourritures(bete)
            self.gerer_collisions_bete_betes(bete)

    def pos_repere_screen(self, largeur_screen, hauteur_screen):
        """
        coordonnées de l'origine du repère de la fenêtre par rapport à l'origine
        global (voir schemas/affichage_joueur.drawio.png pour plus de détails)
        """
        pos_screen = np.zeros((2,))

        pos_screen[0] = self.bete_focus.x() - largeur_screen // 2
        pos_screen[1] = self.bete_focus.y() - hauteur_screen // 2

        return pos_screen

    def update(self):
        # on maintient NB_NOURRITURE de nourriture
        self.generer_nourriture()

        # on gère les collisions
        self.gerer_collisions()

        # on fait bouger les bêtes
        self.betes.update(self.nourritures, self.betes)  # todo voir pour utiliser la librairie multiprocessing

    def draw(self, screen):
        # coordonnées de l'origine du repère de la fenêtre par rapport à l'origine
        # global (voir schemas/affichage_joueur.drawio.png pour plus de détails)
        pos_screen = self.pos_repere_screen(screen.get_width(), screen.get_height())

        self.bete_focus.origine_repere = pos_screen  # on passe le repère de la fenêtre au joueur

        #print(pos_screen)

        # on affiche la bordure
        # pg.gfxdraw.rectangle(screen, pg.Rect((0, 0), (self.LARGEUR, self.HAUTEUR)), (255, 255, 255)) # todo mettre dans le bon repère

        # on affiche les bêtes
        self.afficher_betes(screen, pos_screen)

        # on affiche toutes les nourritures
        self.afficher_nourritures(screen, pos_screen)
