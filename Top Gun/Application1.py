import pygame as pg
from Game import Game
import Tools
import time
from pygamepopup.components import Button, InfoBox
from pygamepopup.menu_manager import MenuManager

horloge_musique = pg.time.Clock()


#Menu d'accueil JOUER et QUITTER
class Menu1:

    def __init__(self, application, *groupes):
        self.couleurs = dict(
            normal=(0, 200, 0),
            survol=(0, 200, 200),
        )
        font = pg.font.SysFont('Helvetica', 24, bold=True)
        # noms des menus et commandes associées
        items = (
            ('JOUER', application.menu2),
            ('QUITTER', application.quitter)
        )
        x = 1023/2
        y = 400
        self._boutons = []
        for texte, cmd in items:
            mb = MenuBouton(
                texte,
                self.couleurs['normal'],
                font,
                x,
                y,
                200,
                50,
                cmd
            )
            self._boutons.append(mb)
            y += 120
            for groupe in groupes:
                groupe.add(mb)

    def update(self, events):
        clicGauche, *_ = pg.mouse.get_pressed()
        posPointeur = pg.mouse.get_pos()
        for bouton in self._boutons:
            # Si le pointeur souris est au-dessus d'un bouton
            if bouton.rect.collidepoint(*posPointeur):
                # Changement du curseur par un quelconque
                pg.mouse.set_cursor(*pg.cursors.tri_left)
                # Changement de la couleur du bouton
                bouton.dessiner(self.couleurs['survol'])
                # Si le clic gauche a été pressé
                if clicGauche:
                    # Appel de la fonction du bouton
                    bouton.executerCommande()
                break
            else:
                # Le pointeur n'est pas au-dessus du bouton
                bouton.dessiner(self.couleurs['normal'])
        else:
            # Le pointeur n'est pas au-dessus d'un des boutons
            # initialisation au pointeur par défaut
            pg.mouse.set_cursor(*pg.cursors.arrow)

    def detruire(self):
        pg.mouse.set_cursor(*pg.cursors.arrow)  # initialisation du pointeur

#Menu de choix du nom des joueurs + skin
class Menu2:

    _textboxs = []
    isPopupActive = False
    menu_manager = None
    pressedTime = time.time()

    def __init__(self, application, *groupes):
        self.couleurs = dict(
            normal=(0, 200, 0),
            survol=(0, 200, 200),
            black=(0, 0, 0)
        )
        font = pg.font.SysFont('Helvetica', 24, bold=True)

        self.menu_manager = MenuManager(application.fenetre)

        Player1 = Text('Player 1', 22, self.couleurs['normal'], 275 , 480, 70, 45)
        Player2 = Text('Player 2', 22, self.couleurs['normal'], 750, 480, 70, 45)

        P1 = InputBox(240, 500, 70, 45, '')
        P2 = InputBox(715, 500, 70, 45, '')

        self._textboxs.append(P1)
        self._textboxs.append(P2)

        x = 1023/2
        y = 400

        #ajout des boutons sur le menu dans une liste permettant de les adfficher
        self._boutons = []
        mb = MenuBouton('JOUER',self.couleurs['normal'],font,x,y,200,50,application.jeu)
        self._boutons.append(mb)
        mb2 = MenuBouton('QUITTER',self.couleurs['normal'],font,925,680,100,25,application.quitter)
        self._boutons.append(mb2)
        mb3 = MenuBouton('APPARENCE',self.couleurs['normal'],font,x,500,125,30,self.set_ispopupactive)
        self._boutons.append(mb3)
        self.exit_request = False
        self.create_main_menu_interface(application)

        for groupe in groupes:
            groupe.add(mb)
            groupe.add(mb2)
            groupe.add(mb3)
            groupe.add(Player1)
            groupe.add(Player2)
            groupe.add(P1)
            groupe.add(P2)

    def create_main_menu_interface(self, application):                                      #méthode qui créer un menu popup
        main_menu = InfoBox(                                                                #définition de ce qu'il y a dans le menu popup (bibliothèque gère apparence de l'infobox)
            "Apparence",
            [
                [
                    #création de boutons apparaissant dans l'infobox
                    Button(
                        title="WW1",     #Appliquation de l'époque voulu       #ferme le popup
                        callback=lambda: (application.set_epoque('WW1'), self.set_ispopupactive(False)),
                    )
                ],
                [
                    Button(
                        title="WW2",     #Appliquation de l'époque voulu        #ferme le popup
                        callback=lambda: (application.set_epoque('WW2'), self.set_ispopupactive(False)),
                    )
                ],
                [
                    Button(
                        title="Moderne",   #Appliquation de l'époque voulu     #ferme le popup
                        callback=lambda: (application.set_epoque('Moderne'), self.set_ispopupactive(False)),
                    )
                ],
                [
                    Button(
                        title="Quitter",        #ferme le popup
                        callback=lambda: self.set_ispopupactive(False),
                    )
                ],
            ],
            has_close_button=False,
        )
        self.menu_manager.open_menu(main_menu)


    def set_ispopupactive(self, isActive=True):
        self.isPopupActive = isActive
        self.pressedTime = time.time()                                                  #Lance un timer


    def update(self, events):
        if self.isPopupActive:
            self.menu_manager.display()                                                 #affiche le popup si la variable isPopupActive est vraie

            if time.time() < self.pressedTime + 0.35:                                   #Utilise le timer précedant pour pas que le popup ne se ferme instantanément
                return

            for event in events:
                if event.type == pg.MOUSEMOTION:
                    self.menu_manager.motion(event.pos)                                 #permet de traquer la position de la souris sur l'ecran et lorsqu'elle passe au dessus d'un bouton du popu
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1 or event.button == 3:
                        self.menu_manager.click(event.button, event.pos)                #permet de savoir si l'on clique sur un boutton dans le popup
            return

        clicGauche, *_ = pg.mouse.get_pressed()
        posPointeur = pg.mouse.get_pos()
        for bouton in self._boutons:
            if bouton.rect.collidepoint(*posPointeur):                                   # Si le pointeur souris est au-dessus d'un bouton
                pg.mouse.set_cursor(*pg.cursors.tri_left)                                # Changement du curseur par un autre
                bouton.dessiner(self.couleurs['survol'])                                 # Changement de la couleur du bouton
                if clicGauche:                                                           # Si le clic gauche a été pressé
                    bouton.executerCommande()                                            # Appel de la fonction du bouton
                    time.sleep(0.3)                                                      # Attendre pour éviter que ca n'appuie sur un bouton dans l'écran suivant
                break
            else:                                                                        # Le pointeur n'est pas au-dessus du bouton
                bouton.dessiner(self.couleurs['normal'])                                 # Grader la couleur du boutton normal

    def detruire(self):
        pg.mouse.set_cursor(*pg.cursors.arrow)                                           # initialisation du pointeur

# Menu d'annonce du gagnant
class Menufin:
    def __init__(self, application, *groupes, winner_name):
        self.app = application
        self.winner_name = winner_name

        self.couleurs = dict(                                                            # Définition des couleur utilisés
            normal=(0, 200, 0),
            survol=(0, 200, 200),
            black=(0, 0, 0)
        )
        font = pg.font.SysFont('Helvetica', 24, bold=True)

        self._boutons = []
        mb2 = MenuBouton('QUITTER',self.couleurs['normal'],font,925,680,100,30,application.quitter)
        self._boutons.append(mb2)
        mb3 = MenuBouton('REJOUER',self.couleurs['normal'],font,100,680,100,30,application.menu2)
        self._boutons.append(mb3)
        for groupe in groupes:
            groupe.add(mb2)
            groupe.add(mb3)
        print(winner_name + " a gagné !")


    def update(self, events):
        clicGauche, *_ = pg.mouse.get_pressed()
        posPointeur = pg.mouse.get_pos()
        for bouton in self._boutons:
            # Si le pointeur souris est au-dessus d'un bouton
            if bouton.rect.collidepoint(*posPointeur):
                # Changement du curseur par un quelconque
                pg.mouse.set_cursor(*pg.cursors.tri_left)
                # Changement de la couleur du bouton
                bouton.dessiner(self.couleurs['survol'])
                # Si le clic gauche a été pressé
                if clicGauche:
                    # Appel de la fonction du bouton
                    bouton.executerCommande()
                break
            else:
                # Le pointeur n'est pas au-dessus du bouton
                bouton.dessiner(self.couleurs['normal'])
        else:
            # Le pointeur n'est pas au-dessus d'un des boutons
            # initialisation au pointeur par défaut
            pg.mouse.set_cursor(*pg.cursors.arrow)

        txt_player = pg.font.SysFont(None, 100)
        text_surf1 = txt_player.render(self.winner_name + " a gagné ! Bravo !", True, (0, 0, 0))
        text_surf1.set_alpha(255)
        self.app.fenetre.blit(text_surf1, (100, 400))


    def detruire(self):
        pg.mouse.set_cursor(*pg.cursors.arrow)

#Permet de créer des boutons rectengulaire
class MenuBouton(pg.sprite.Sprite):

    def __init__(self, texte, couleur, font, x, y, largeur, hauteur, commande):
        super().__init__()
        self._commande = commande

        self.image = pg.Surface((largeur, hauteur))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.texte = font.render(texte, True, (0, 0, 0))
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (largeur / 2, hauteur / 2)
        self.dessiner(couleur)

    def dessiner(self, couleur):
        self.image.fill(couleur)
        self.image.blit(self.texte, self.rectTexte)

    def executerCommande(self):                                             # Appel de la commande du bouton
        self._commande()

#Permet d'afficher du texte sur l'écran
class Text(pg.sprite.Sprite):
    def __init__(self, text, size, color, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, 1, color)
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')
        self.rect.center = (x, y)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width / 2 - W / 2, height / 2 - H / 2])
        self.position = (x, y)

#Permet d'afficher les cellules où l'ont met les noms des joueurs
class InputBox(pg.sprite.Sprite):
    pg.init()
    my_font = pg.font.Font(None, 32)

    def __init__(self, x, y, w, h, text=''):
        super().__init__()

        self.couleur = dict(
            normal = (0, 200, 0),
            clique = (0, 200, 200)
        )
        self.color = self.couleur["normal"]
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = self.my_font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):                                                          # Gère l'apparence du bouton (couleur/forme)
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pg.Surface((max(self.width, t_surf.get_width() + 10), t_surf.get_height() + 10),
                                    pg.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pg.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:                                        # Si le boutton est utilisé
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = 'survol' if self.active else 'normal'                      # Change la couleur du boutton
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.my_font.render(self.text, True, self.color)


    def update(self, event_list):                                               #boucle principale permettant d'afficher les boutons
        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pg.KEYDOWN and self.active:
                if event.key == pg.K_RETURN:
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))                           # affiche le bouton sur l'ecran
        pg.draw.rect(screen, self.color, self.rect, 2)                                          # Dessine le bouton à l'ecran

#Classe maîtresse gérant les différentes interfaces du jeu
class Application1:

    background = pg.image.load('images\Home.jpg')
    fenetre = pg.display.set_mode((1023, 712))
    epoque = 'WW1'                                                                      #Apparence de base

    def __init__(self):
        pg.init()
        pg.font.init()
        pg.display.set_caption("TOP GUN the game")

        self.fond = pg.image.load('images\Home.jpg')

        self.fenetre = pg.display.set_mode((1023, 712))
        # Groupe de sprites utilisé pour l'affichage
        self.groupeGlobal = pg.sprite.Group()
        self.statut = True
        self.musique = time.process_time()

    def _initialiser(self):                                                                                             # enlever tout les sprites de l'ecran
        try:
            self.ecran.detruire()
            self.groupeGlobal.empty()                                                                                   # suppression des sprites du groupe
        except AttributeError:
            pass

    def menu(self):                                                                                                     # Affichage 1er menu
        self._initialiser()
        self.ecran = Menu1(self, self.groupeGlobal)
        pg.mixer.music.load("musiques/topgun.mp3")
        pg.mixer.music.play(-1, self.musique, 6000)

    def menu2(self):                                                                                                    #affichage menu choix des nom et apparences
        self.ecran.detruire()
        self._initialiser()
        self.ecran = Menu2(self, self.groupeGlobal)
        time.sleep(0.30)

    def jeu(self):                                                                                                      # Affichage du jeu
        self.player1Name = self.ecran._textboxs[0].text if self.ecran._textboxs[0].text != '' else 'Player1'
        self.player2Name = self.ecran._textboxs[1].text if self.ecran._textboxs[1].text != '' else 'Player2'
        self._initialiser()
        self.ecran = Game(self, self.groupeGlobal)

    def quitter(self):
        Tools.quitter(self)

    def menu_fin(self, winner_name):                                            # afficher menu du gagnant
        self._initialiser()
        self.ecran = Menufin(self, self.groupeGlobal, winner_name=winner_name)

    def set_epoque(self, epoque):                                               # appliquer l'époque des apparences
        self.epoque = epoque

    def update1(self):                                                          # boucle principal permettant l'affichage de la fenêtre
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                Tools.quitter(self)
                return

        self.fenetre.blit(self.fond,(0,0))
        self.groupeGlobal.update(events)
        self.groupeGlobal.draw(self.fenetre)
        self.ecran.update(events)
        pg.display.update()