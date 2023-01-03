import pygame as pg
from math import fabs

#Fonction permettant de fermer la fenêtre
def quitter(self):
    self.statut = False
    print("Vous avez fermé le jeux")

#Fonction permettant de tourner une image sans changer son centre
def rot_center(image, rect, angle):
    rot_image = pg.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect

def sign(x):
    if x == 0:
        return 0
    return x / fabs(x)
