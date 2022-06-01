import numpy as np
import pygame as pg
import random as rd
import pygame.gfxdraw

from nourriture import Nourriture
from bete import Bete
from player import Player
from secteur import Secteur


class Environnement:
    LARGEUR = 4000
    HAUTEUR = 2000
    NB_SECTEURS_HORIZONTAL = 20
    NB_SECTEURS_VERTICAL = 10

    NB_NOURRITURE = LARGEUR * HAUTEUR // 5000  # nombre de nourritures présentes sur le canvas
    NB_BETE = 5  # joueur inclus
    RATIO_TAILLE_POUR_MANGER = 1.2  # ex : une bête doit être 1.2 fois plus lourde que l'autre pour pouvoir la manger
    VITESSE_BASIQUE = 3  # vitesse de départ des bêtes
    LIMITE_POIDS_MANGER = 400  # limite de poids à laquelle une bête ne grossit plus en mangeant de la nourriture

    def __init__(self, joueur=False, largeur_screen=1920, hauteur_screen=1080):
        # pour accélérer les calculs, on sépare le canvas en différent secteur
        self.secteurs = list()
        self.generer_secteur()

        self.generer_nourriture()

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

    # ================= #
    # ==    FRONT    == # =============================================================================================
    # ================= #

    def afficher_nourritures(self, screen, pos_screen: np.ndarray):
        for secteur in self.secteurs:
            for nourriture in secteur.nourritures:
                nourriture.draw(screen, pos_screen)

    def afficher_betes(self, screen, pos_screen: np.ndarray):
        for bete in self.betes:
            bete.draw(screen, pos_screen)

    def afficher_secteurs(self, screen, pos_screen: np.ndarray):
        for secteur in self.secteurs:
            secteur.draw(screen, pos_screen)

    def draw(self, screen):
        # coordonnées de l'origine du repère de la fenêtre par rapport à l'origine
        # global (voir schemas/affichage_joueur.drawio.png pour plus de détails)
        pos_screen = self.pos_repere_screen(screen.get_width(), screen.get_height())

        self.bete_focus.origine_repere = pos_screen  # on passe le repère de la fenêtre au joueur

        # on affiche la bordure
        # pg.gfxdraw.rectangle(screen, pg.Rect((0, 0), (self.LARGEUR, self.HAUTEUR)), (255, 255, 255)) # todo mettre dans le bon repère

        # on affiche les délimitations des secteurs
        self.afficher_secteurs(screen, pos_screen)

        # on affiche les bêtes
        self.afficher_betes(screen, pos_screen)

        # on affiche toutes les nourritures
        self.afficher_nourritures(screen, pos_screen)

    # ================= #
    # ==     BACK    == # =============================================================================================
    # ================= #

    def get_largeur_secteur(self):
        return self.LARGEUR // self.NB_SECTEURS_HORIZONTAL

    def get_hauteur_secteur(self):
        return self.HAUTEUR // self.NB_SECTEURS_VERTICAL

    def generer_secteur(self):
        largeur_secteur = self.get_largeur_secteur()
        hauteur_secteur = self.get_hauteur_secteur()

        for x in range(0, self.NB_SECTEURS_HORIZONTAL):
            for y in range(0, self.NB_SECTEURS_VERTICAL):
                self.secteurs.append(Secteur(x * largeur_secteur, (x * largeur_secteur) + largeur_secteur,
                                          y * hauteur_secteur, (y * hauteur_secteur) + hauteur_secteur,
                                          x, y))

    def generer_nourriture(self):
        # todo répartir sur le canvas, pas par secteur
        nb_nourriture_secteur = self.NB_NOURRITURE // (self.NB_SECTEURS_HORIZONTAL * self.NB_SECTEURS_VERTICAL)
        largeur_secteur = self.get_largeur_secteur()
        hauteur_secteur = self.get_hauteur_secteur()

        for secteur in self.secteurs:
            while len(secteur.nourritures) < nb_nourriture_secteur:
                secteur.nourritures.add(Nourriture(rd.randint(secteur.x_min, secteur.x_min + largeur_secteur),
                                                   rd.randint(secteur.y_min, secteur.y_min + hauteur_secteur)))

    def generer_bete(self):
        while len(self.betes) < self.NB_BETE - 1:
            self.ajouter_bete()

    def ajouter_bete(self):
        bete = Bete(rd.randint(0, self.LARGEUR), rd.randint(0, self.HAUTEUR), self.VITESSE_BASIQUE)
        self.betes.add(bete)

        return bete

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

    def gerer_collisions_bete_nourritures(self, bete: Bete):
        liste_collision = bete.liste_secteur_collision(self.secteurs)

        for secteur in liste_collision:
            # collision entre la bete et les nourritures
            nourriture_manger = pg.sprite.spritecollide(bete, secteur.nourritures, True)

            # pour chaque nourriture qu'on touche
            for i in range(0, len(nourriture_manger)):
                # si la bete peut encore grossir en mangeant de la nourriture
                if bete.poids < self.LIMITE_POIDS_MANGER:
                    # la bête mange la nourriture
                    bete.manger(nourriture_manger[i])

    def gerer_collisions_bete_bordures(self, bete):
        # collision top
        if bete.y() - bete.radius < 0:
            bete.pos[1] = bete.radius
        # collision bottom
        elif bete.y() + bete.radius > self.HAUTEUR:
            bete.pos[1] = self.HAUTEUR - bete.radius

        # collision gauche
        if bete.x() - bete.radius < 0:
            bete.pos[0] = bete.radius
        # collision droite
        elif bete.x() + bete.radius > self.LARGEUR:
            bete.pos[0] = self.LARGEUR - bete.radius

    def gerer_collisions(self):
        # pour chaque bête de l'environnement
        for bete in self.betes:
            self.gerer_collisions_bete_bordures(bete)
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
        self.gerer_collisions()  # todo vérifier les collisions avec les bords

        # on fait bouger les bêtes
        self.betes.update(self.secteurs, self.betes)  # todo voir pour utiliser la librairie multiprocessing
