import numpy as np
import pygame as pg
import random as rd

from nourriture import Nourriture
from bete import Bete
from player import Player
from secteur import Secteur


class Environnement:
    LARGEUR = 4000  # largeur du canvas
    HAUTEUR = 2000  # hauteur du canvas
    NB_SECTEURS_HORIZONTAL = 20
    NB_SECTEURS_VERTICAL = 10
    LARGEUR_SECTEUR = LARGEUR // NB_SECTEURS_HORIZONTAL
    HAUTEUR_SECTEUR = HAUTEUR // NB_SECTEURS_VERTICAL

    NB_NOURRITURE = LARGEUR * HAUTEUR // 5000  # nombre de nourritures présentes sur le canvas
    NB_BETE = 15  # joueur inclus
    RATIO_TAILLE_POUR_MANGER = 1.2  # ex : une bête doit être 1.2 fois plus lourde que l'autre pour pouvoir la manger
    VITESSE_BASIQUE = 3  # vitesse de départ des bêtes
    LIMITE_POIDS_MANGER = 400  # limite de poids à laquelle une bête ne grossit plus en mangeant de la nourriture

    def __init__(self, joueur=False, largeur_screen=1920, hauteur_screen=1080):
        self.largeur_screen = largeur_screen
        self.hauteur_screen = hauteur_screen

        # pour accélérer les calculs, on sépare le canvas en différent secteur
        # on utilise un dictionnaire pour pouvoir retrouver les secteurs en fonction de leur position
        self.secteurs: dict[(int, int)] = dict()
        self.generer_secteur()

        self.generer_nourriture()

        self.betes = pg.sprite.Group()
        self.generer_bete()

        self.bete_focus = None

        if joueur:
            self.ajouter_joueur()
        else:
            bete = self.ajouter_bete_aleatoire()

            # on enregistre la bête pour qu'elle soit au centre de l'écran
            self.bete_focus = bete

    # ================= #
    # ==    FRONT    == # =============================================================================================
    # ================= #

    def afficher_nourritures(self, screen, pos_screen: np.ndarray):
        for secteur in self.secteurs.values():
            for nourriture in secteur.nourritures:
                nourriture.draw(screen, pos_screen)

    def afficher_betes(self, screen, pos_screen: np.ndarray):
        for bete in self.betes:
            bete.draw(screen, pos_screen)

    def afficher_secteurs(self, screen, pos_screen: np.ndarray):
        for secteur in self.secteurs.values():
            secteur.draw(screen, pos_screen)

    def draw(self, screen):
        # coordonnées de l'origine du repère de la fenêtre par rapport à l'origine
        # global (voir schemas/affichage_joueur.drawio.png pour plus de détails)
        pos_screen = self.pos_repere_screen(screen.get_width(), screen.get_height())

        self.bete_focus.origine_repere = pos_screen  # on passe le repère de la fenêtre au joueur

        # on affiche la bordure
        # secteur.draw_rectangle_vide(screen, (255, 255, 255), ) todo à l'occasion mettre dans le bon repère

        # on affiche les délimitations des secteurs
        # self.afficher_secteurs(screen, pos_screen)

        # on affiche les bêtes
        self.afficher_betes(screen, pos_screen)

        # on affiche toutes les nourritures
        self.afficher_nourritures(screen, pos_screen)

    # ================= #
    # ==     BACK    == # =============================================================================================
    # ================= #
    def generer_secteur(self) -> None:
        for x in range(0, self.NB_SECTEURS_HORIZONTAL):
            for y in range(0, self.NB_SECTEURS_VERTICAL):
                self.secteurs[(x, y)] = Secteur(x * self.LARGEUR_SECTEUR,
                                                (x * self.LARGEUR_SECTEUR) + self.LARGEUR_SECTEUR,
                                                y * self.HAUTEUR_SECTEUR,
                                                (y * self.HAUTEUR_SECTEUR) + self.HAUTEUR_SECTEUR,
                                                x, y)

    def generer_nourriture(self) -> None:
        # nombre de nourritures présentes sur le canvas
        nb_nourriture = 0

        # pour chaque secteur
        for secteur in self.secteurs.values():
            # on ajoute le nombre de nourritures du secteur dans le total
            nb_nourriture += len(secteur.nourritures)

        # pour chaque nourriture manquante
        for i in range(0, self.NB_NOURRITURE - nb_nourriture):
            # nourriture aléatoire
            nourriture = Nourriture(rd.randint(1, self.LARGEUR - 1), rd.randint(1, self.HAUTEUR - 1))

            # on trouve les index du secteur auquel la nourriture va appartenir
            index_secteur_x = int(nourriture.x() // self.LARGEUR_SECTEUR)
            index_secteur_y = int(nourriture.y() // self.HAUTEUR_SECTEUR)

            # on ajoute la nourriture au secteur
            self.secteurs[(index_secteur_x, index_secteur_y)].nourritures.add(nourriture)

    def generer_bete(self) -> None:
        while len(self.betes) < self.NB_BETE - 1:
            self.ajouter_bete_aleatoire()

    def ajouter_bete_aleatoire(self) -> Bete:
        r1 = rd.randint(10, 240)  # random 1
        r2 = (r1 + rd.randint(20, 240)) % 240  # random 2
        r3 = (r2 + rd.randint(20, 240)) % 240  # random 3

        couleur = (r1, r2, r3)

        bete = Bete(rd.randint(0, self.LARGEUR), rd.randint(0, self.HAUTEUR), couleur=couleur,
                    vitesse=self.VITESSE_BASIQUE)
        self.betes.add(bete)

        return bete

    def ajouter_joueur(self):
        # on crée un joueur
        joueur = Player(rd.randint(0, self.LARGEUR), rd.randint(0, self.HAUTEUR), self.VITESSE_BASIQUE)

        # on suit ce joueur
        self.bete_focus = joueur

        # on l'ajoute à la liste de bête de l'environnement
        self.betes.add(joueur)

        self.bete_focus.origine_repere = self.pos_repere_screen(self.largeur_screen, self.hauteur_screen)

    def gerer_collisions_bete_betes(self, bete: Bete) -> None:
        # liste des bêtes qui se sont fait manger par une autre bête
        betes_mangees = []

        # pour les autres bêtes
        for autre_bete in self.betes:
            # si l'autre bête est différente de la bete actuelle
            if autre_bete is not bete:
                # pour chaque partie de la bete
                for partie in bete.parties:
                    # pour chaque partie de l'autre bête
                    for autre_bete_partie in autre_bete.parties:
                        # si la bete est RATIO plus lourde que l'autre bete
                        if partie.poids > self.RATIO_TAILLE_POUR_MANGER * autre_bete_partie.poids:
                            # voir schemas/bete_mange_bete.png pour les détails
                            if (partie.distance(
                                    autre_bete_partie) + autre_bete_partie.radius) - partie.radius < autre_bete_partie.radius / 2:
                                # la partie de la bête 1 mange la partie de l'autre bête
                                partie.manger(autre_bete_partie)

                                # l'autre bête perd sa partie
                                autre_bete.parties.remove(autre_bete_partie)

                                # on enregistre la bête qui s'est fait grignoter
                                betes_mangees.append(autre_bete)

                                # si la bete qui se fait manger est la bête qu'on suit (ou le joueur)
                                if autre_bete is self.bete_focus:
                                    # si la bête qu'on suit n'a plus de partie
                                    if len(self.bete_focus.parties) < 1:
                                        # on change la bete qu'on suit par la bête qui l'a mangé
                                        self.bete_focus = bete

        # on efface les bêtes qui se sont fait manger si elles n'ont plus de parties
        for dead_bete in betes_mangees:
            if len(dead_bete.parties) < 1:
                self.betes.remove(dead_bete)

    def gerer_collisions_bete_nourritures(self, bete: Bete) -> None:
        liste_collision = bete.liste_secteur_collision(self.secteurs)

        for secteur in liste_collision:
            for partie in bete.parties:
                # collision entre la bete et les nourritures (on supprime les nourritures en collisions)
                nourriture_manger = pg.sprite.spritecollide(partie, secteur.nourritures, True)

                # pour chaque nourriture qu'on touche
                for i in range(0, len(nourriture_manger)):
                    # si la bete peut encore grossir en mangeant de la nourriture
                    if bete.poids < self.LIMITE_POIDS_MANGER:  # todo voir pour désactiver les collisions quand poids >
                        # la bête mange la nourriture
                        partie.manger(nourriture_manger[i])

    def gerer_collisions_bete_bordures(self, bete: Bete) -> None:
        # pour chaque partie de la bête
        for partie in bete.parties:
            # collision top
            if partie.y() - partie.radius < 0:
                partie.pos[1] = partie.radius
            # collision bottom
            elif partie.y() + partie.radius > self.HAUTEUR:
                partie.pos[1] = self.HAUTEUR - partie.radius

            # collision gauche
            if partie.x() - partie.radius < 0:
                partie.pos[0] = partie.radius
            # collision droite
            elif partie.x() + partie.radius > self.LARGEUR:
                partie.pos[0] = self.LARGEUR - partie.radius

    def gerer_collisions(self) -> None:
        # pour chaque bête de l'environnement
        for bete in self.betes:
            self.gerer_collisions_bete_bordures(bete)
            self.gerer_collisions_bete_nourritures(bete)
            self.gerer_collisions_bete_betes(bete)

    def pos_repere_screen(self, largeur_screen, hauteur_screen) -> np.ndarray:
        """
        Coordonnées de l'origine du repère de la fenêtre par rapport à l'origine
        global (voir schemas/affichage_joueur.drawio.png pour plus de détails)
        """
        pos_screen = np.zeros((2,))

        centre_focus = self.bete_focus.centre()

        pos_screen[0] = centre_focus[0] - largeur_screen // 2
        pos_screen[1] = centre_focus[1] - hauteur_screen // 2

        return pos_screen

    def update(self):
        # on maintient NB_NOURRITURE de nourriture
        self.generer_nourriture()

        # on gère les collisions
        self.gerer_collisions()

        # on fait bouger les bêtes
        self.betes.update(self.secteurs, self.betes)  # todo voir pour utiliser la librairie multiprocessing

        # todo pour la version finale ajouter
        # self.generer_bete()
