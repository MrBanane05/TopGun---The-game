import pygame as pg
from entities import Avion, Missile
from particlesys import ParticleSystem

#Assignation des touches de controle et du système de particule
KEY_BINDINGS_1 = {pg.K_LEFT: "left",
                pg.K_RIGHT: "right",
                pg.K_UP: "up",
                pg.K_DOWN: "down",
                pg.K_m: "gun_fire"}
KEY_BINDINGS_2 = {pg.K_q: "left",
                pg.K_d: "right",
                pg.K_z: "up",
                pg.K_s: "down",
                pg.K_SPACE: "gun_fire"}
psys = ParticleSystem()

#Classe maitresse du Jeu
class Game:
    input_listener = []
    keys_pressed = []
    world = []
    starttime = 0
    avionimg = {                                                                                # Dictionnaire des apparences d'avion en fonction de l'époque
        "WW1": ["images/WW1_bleu.png", "images/WW1_rouge.png"],                                 # Apparence avions WW1
        "WW2": ["images/WW2_bleu.png", "images/WW2_rouge.png"],                                 # Apparence avions WW2
        "Moderne" : ["images/Moderne_bleu.png", "images/Moderne_rouge.png"]                     # Apparence avions Modernes
    }

    def __init__(self, application, *groupes):
        self.app = application

        #Définition des avions du Player 1 et du Player 2
        self.Avion1 = Avion(100, 500, pg.image.load(self.avionimg[application.epoque][0]), pg.image.load("images/transparant.png"), KEY_BINDINGS_2, self.app.player1Name)
        self.Avion2 = Avion(900, 500, pg.image.load(self.avionimg[application.epoque][1]), pg.image.load("images/transparant.png"), KEY_BINDINGS_1, self.app.player2Name)

        img = pg.image.load('images/ciel.jpg')                                                 # Images de fond du jeu
        self.img = pg.transform.scale(img, (1023, 712))

        self.input_listener.append(self.Avion1)
        self.input_listener.append(self.Avion2)

        self.world.append(self.Avion1)
        self.world.append(self.Avion2)
        self.world = [[e.priority, e] for e in self.world]
        self.Avion1.set_world(self.world)
        self.Avion2.set_world(self.world)

    #Boucle principale du jeux
    def update(self, events):
        self.starttime = pg.time.get_ticks()

        #Vérifie si l'avion 1 a atteint le score gagnant
        if self.Avion1.score >= 5:
            self.app.menu_fin(self.Avion1.name)

        #Vérifie si l'avion 2 a atteint le score gagnant
        if self.Avion2.score >= 5:
            self.app.menu_fin(self.Avion2.name)

        #boucle principal du fonctionnement du jeux
        for event in events:
            if event.type == pg.KEYDOWN:
                self.keys_pressed.append(event.key)
            elif event.type == pg.KEYUP:
                self.keys_pressed.remove(event.key)
        for l in self.input_listener:
            l.on_input(self.keys_pressed)

        #affiche la fenêtre du jeux
        self.app.fenetre.fill((255, 255, 255))
        self.app.fenetre.blit(self.img, self.img.get_rect())

        #permet de reset lorsqu'un avion est touché
        to_reset = False
        for [p, entity] in self.world:
            if not entity.tick():
                self.world.remove([entity.priority, entity])
                if isinstance(entity, Avion):
                    to_reset = True
                    break
            else:
                self.check_collisions(self.world, entity)
                entity.render(self.app.fenetre)

        if to_reset:
            self.reset_game()

        psys.tick()
        psys.render(self.app.fenetre)

        self.render_gui(self.app.fenetre)

        pg.display.flip()
        span = pg.time.get_ticks() - self.starttime
        while (span < 20):
            pg.time.wait(1)
            print
            'wait for %d seconds ' % span
            span = pg.time.get_ticks() - self.starttime

    #Vérifie si le joueur rentre en colision avec la bordure l'autre avion ou un missile
    def check_collisions(self, world, entity):
        for p, e1 in world:
            if e1 != entity and e1.collide_entities(entity):
                if isinstance(e1, Avion):
                    if isinstance(entity, Missile):
                        e1.damage(entity)
                        psys.explosion(entity.location[0], entity.location[1], 200)
                    if isinstance(entity, Avion):
                        entity.step_back()
                        e1.step_back()

    #Permet d'afficher barre de munition et nom des joueurs en jeux
    def render_gui(self, screen):

        pg.draw.rect(screen, pg.Color(0, 128, 0), (10, 10, 200, 10), 2)                                                 #affichage barre rechargement joueur 1
        pg.draw.rect(screen, pg.Color(0, 128, 0), (10, 10, self.Avion2.shoot_reload * 200 / Avion.RELOAD_TIME, 10))

        pg.draw.rect(screen, pg.Color(0, 128, 0), (810, 10, 200, 10), 2)                                                #affichage barre rechargement joueur 2
        pg.draw.rect(screen, pg.Color(0, 128, 0), (810, 10, self.Avion1.shoot_reload * 200 / Avion.RELOAD_TIME, 10))

        txt_player = pg.font.SysFont(None, 30)
        text_surf1 = txt_player.render(self.Avion1.name + ":    " + str(self.Avion1.score), True, (0, 0, 0))            # affichage nom joueur 1
        text_surf1.set_alpha(255)
        self.app.fenetre.blit(text_surf1, (10, 20))

        text_surf2 = txt_player.render(self.Avion2.name + ":    " + str(self.Avion2.score), True, (0, 0, 0))            # affichage nom joueur 2
        text_surf2.set_alpha(255)
        self.app.fenetre.blit(text_surf2, (810, 20))

    #Permet de remettre les avions a 0 lorsque un avion est touché
    def reset_game(self):
        self.world = []
        self.Avion1.reset( 100, 500)
        self.Avion2.reset(900, 500)
        self.world.append(self.Avion1)
        self.world.append(self.Avion2)
        self.world = [[e.priority, e] for e in self.world]
        self.Avion1.set_world(self.world)
        self.Avion2.set_world(self.world)