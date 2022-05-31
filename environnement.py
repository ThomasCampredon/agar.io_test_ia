import pygame as pg
import random as rd

from nourriture import Nourriture
from bete import Bete
from player import Player


class Environnement:
    LARGEUR = 4000
    HAUTEUR = 2000
    NB_NOURRITURE = 400
    NB_BETE = 5  # joueur inclus
    RATIO_TAILLE_POUR_MANGER = 1.2  # ex : une bête doit être 1.2 fois plus lourde que l'autre pour pouvoir la manger

    def __init__(self, vitesse_basique=3, joueur=False):
        self.vitesse_basique = vitesse_basique

        self.nourritures = pg.sprite.Group()  # todo séparer les points en secteurs
        self.betes = pg.sprite.Group()

        if joueur:
            # on ajoute un joueur
            self.betes.add(Player(0, 0, vitesse_basique))

        self.generer_bete()

    def generer_nourriture(self):
        while len(self.nourritures) < self.NB_NOURRITURE:
            self.nourritures.add(Nourriture(rd.randint(0, self.LARGEUR), rd.randint(0, self.HAUTEUR)))

    def generer_bete(self):
        while len(self.betes) < self.NB_BETE:
            self.ajouter_bete()

    def ajouter_bete(self):
        bete = Bete(rd.randint(0, self.LARGEUR), rd.randint(0, self.HAUTEUR), self.vitesse_basique)
        self.betes.add(bete)

    def afficher_nourritures(self, screen):
        for nourriture in self.nourritures:
            nourriture.draw(screen)

    def afficher_betes(self, screen):
        for bete in self.betes:
            bete.draw(screen)

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

    def update(self):
        # on maintient NB_NOURRITURE de nourriture
        self.generer_nourriture()

        # on gère les collisions
        self.gerer_collisions()

        # on fait bouger les bêtes
        self.betes.update(self.nourritures, self.betes)  # todo voir pour utiliser la librairie multiprocessing

    def draw(self, screen):
        # on affiche les bêtes
        self.afficher_betes(screen)

        # on affiche toutes les nourritures
        self.afficher_nourritures(screen)
