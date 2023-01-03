import Application1
import pygame as pg
import pygamepopup as pgp
import time

pg.init()
pgp.init()

# Permet de charger les menu ou le jeu
app1 = Application1.Application1()
app1.menu()

# Permet de charger une horloge virtuelle
clock = pg.time.Clock()

while app1.statut:
    app1.update1()
    clock.tick(30)

pg.quit()