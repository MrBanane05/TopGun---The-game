import math
import Tools
import pygame as pg

map = pg.Rect(0, 0, 1023, 712)

#définition des paramètre commun entre missile et avion (vélocité, localisation, accélération...)
class Entity():

    def __init__(self, x, y, img, priority):
        self.location = [x, y]
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0
        self.turn_velocity = 0
        self.turn_acceleration = 0
        self.img = img
        self.bufimg = self.img
        if self.bufimg != None: self.bufrect = self.bufimg.get_rect()
        self.map_rect = map
        self.priority = priority

    def set_angle(self, angle):
        self.angle = angle
        if self.bufimg != None:
            self.bufimg, self.bufrect = Tools.rot_center(self.img, self.img.get_rect(), self.angle * 180 / math.pi)

    def tick(self):
        self.location[0] -= math.sin(self.angle) * self.velocity
        self.location[1] -= math.cos(self.angle) * self.velocity
        return self.alive()

    def render(self, screem):
        screem.blit(self.bufimg, [self.location[i] - self.bufrect[i + 2] / 2 for i in [0, 1]])

    def get_radius(self):
        return (self.img.get_rect()[2] + self.img.get_rect()[3]) / 2

    def collide(self, x, y):
        return self.get_radius() ** 2 > (self.location[0] - x) ** 2 + (self.location[1] - y) ** 2

    def collide_entities(self, other):
        return 0.3 * (self.get_radius() + other.get_radius()) ** 2 > (self.location[0] - other.location[0]) ** 2 + (
                    self.location[1] - other.location[1]) ** 2

    def alive(self):
        return True

#définition de l'avion
class Avion(Entity):
    MAX_SPEED = 5
    MAX_TURN_SPEED = 0.025 * math.pi
    MAX_AMMO = 10000000000
    MAX_HEALTH = 1
    RELOAD_TIME = 10
    DCL_AIM = 0.005 * math.pi
    DCL_TURN = 0.001 * math.pi
    DCL_MOVE = 0.3

    def __init__(self, x, y, img, top_img, key_binding, name):
        Entity.__init__(self, x, y, img, 10)
        self.aim_direction = 0
        self.top_img = top_img
        self.top_bufimg = top_img
        if self.top_bufimg != None: self.top_bufrect = top_img.get_rect()
        self.aim_velocity = 0
        self.aim_acceleration = 0
        self.old_location = self.location
        self.shoot_reload = 0
        self.key_binding = key_binding
        self.ammo = Avion.MAX_AMMO
        self.health = Avion.MAX_HEALTH
        self.last_action = [0, 0, 0]
        self.base = None
        self.score = 0
        self.name = name

    def reset(self, x , y):
        self.location = [x, y]
        self.angle = 0
        self.velocity = 0
        self.acceleration = 0
        self.turn_velocity = 0
        self.turn_acceleration = 0
        self.health = Avion.MAX_HEALTH
        self.ammo = Avion.MAX_AMMO
        self.old_location = self.location
        self.last_action = [0, 0, 0]

    def set_base(self, base):
        self.base = base

    def ready_to_shoot(self):
        return self.shoot_reload == Avion.RELOAD_TIME and self.ammo > 0

    def step_back(self):
        self.location = self.old_location[:]

    def to_base(self, base):
        if base.owner == self:
            self.ammo = Avion.MAX_AMMO

    def decelerate(self, acc, vel, dec, limit, mult=1):
        if acc != 0:
            vel = max(min(vel + acc * dec * mult, limit), -limit)
        elif vel > 0:
            vel = max(vel - dec, 0)
        elif vel < 0:
            vel = min(vel + dec, 0)
        return vel

    def tick(self):
        # Garde en mémoire la position a chaque instant
        self.old_location = self.location[:]

        # met a la vitesse de l'avion
        self.aim_velocity = self.decelerate(self.aim_acceleration, self.aim_velocity, Avion.DCL_AIM, Avion.MAX_TURN_SPEED)
        self.turn_velocity = self.decelerate(self.turn_acceleration, self.turn_velocity, Avion.DCL_TURN,
                                             Avion.MAX_TURN_SPEED)
        mult = 0.25 if self.velocity * self.acceleration > 0 else 1
        self.velocity = self.decelerate(self.acceleration, self.velocity, Avion.DCL_MOVE, Avion.MAX_SPEED, mult)

        # met a jour la position de l'avion
        self.rotate_gun_to(self.aim_direction + self.aim_velocity)
        self.set_angle(self.angle + self.turn_velocity)
        Entity.tick(self)

        # vérifie si l'avion est entre les bordures de l'ecran
        self.check_borders()

        # recharge les missiles
        self.shoot_reload = min(self.shoot_reload + 1, Avion.RELOAD_TIME)

        return self.alive()

    def move_copy(self, action):
        avion = Avion(self.location[0], self.location[1], self.img, self.top_img, None)
        avion.aim_direction = self.aim_direction
        avion.aim_velocity = self.aim_velocity
        avion.aim_acceleration = self.aim_acceleration
        avion.old_location = self.old_location[:]
        avion.shoot_reload = self.shoot_reload
        avion.ammo = self.ammo
        avion.health = self.health
        avion.last_action = action
        avion.perform_action(action)
        avion.tick()
        return avion

    def check_borders(self):
        for i in [0, 1]:
            if self.location[i] - self.bufrect[i + 2] / 2 < self.map_rect[i]:
                self.location[i] = self.map_rect[i] + self.bufrect[i + 2] / 2
            if self.location[i] + self.bufrect[i + 2] / 2 > self.map_rect[i] + self.map_rect[i + 2]:
                self.location[i] = self.map_rect[i] + self.map_rect[i + 2] - self.bufrect[i + 2] / 2

    def rotate_gun_to(self, angle):
        self.aim_direction = self.angle + self.turn_velocity
        if self.top_bufimg != None:
            self.top_bufimg, self.top_bufrect = Tools.rot_center(self.top_img, self.top_img.get_rect(),
                                                                 self.aim_direction * 180 / math.pi)

    def render(self, screen):
        Entity.render(self, screen)
        rect = self.top_bufrect
        screen.blit(self.top_bufimg, [self.location[i] - rect[i + 2] / 2 for i in [0, 1]])

    def damage(self, missile):
        if missile.owner != self:
            self.health -= missile.damage
            missile.destroy()
            missile.owner.gain_point()

    def alive(self):
        return self.health > 0

    def shoot(self):
        if self.ready_to_shoot():
            x, y = (self.location[0] - 1.5 * math.sin(self.aim_direction) * 40), \
                   (self.location[1] - 1.5 * math.cos(self.aim_direction ) * 40)
            missile = Missile(x, y, pg.image.load("images/balle.gif"), self)
            self.ammo -= 1
            self.shoot_reload = 0
            self.world.append([missile.priority, missile])

    def set_world(self, world):
        self.world = world

    def on_input(self, keys):
        actions = []
        for key in keys:
            if key in self.key_binding.keys():
                actions.append(self.key_binding[key])
        #

        self.last_action = [int("up" in actions),
                            int("down" in actions),
                            int("left" in actions),
                            int("right" in actions),
                            int("gun_left" in actions),
                            int("gun_right" in actions),
                            int("gun_fire" in actions)]
        self.perform_action(self.last_action)

    def perform_action(self, actions):
        if actions == None:
            return
        move = actions[0] - actions[1]
        turn = actions[2] - actions[3]
        aim = actions[4] - actions[5]
        self.last_action = actions[:]
        self.perform_action_move(move, turn, aim)
        if actions[6]: self.shoot()

    def perform_action_move(self, move=0, turn=0, aim=0):
        self.acceleration = int(move)
        self.turn_acceleration = int(turn)
        self.aim_acceleration = int(aim)

    def get_repr(self):
        return [self.location[0] / self.map_rect.width,
                self.location[1] / self.map_rect.height,
                self.angle / (math.pi * 2.),
                self.velocity / Avion.MAX_SPEED,
                self.aim_direction / (math.pi * 2),
                self.aim_velocity / Avion.MAX_TURN_SPEED,
                self.turn_velocity / Avion.MAX_TURN_SPEED,
                self.ammo / float(Avion.MAX_AMMO),
                self.health / float(Avion.MAX_HEALTH)]

    def gain_point(self):
        self.score += 1

#définition des missiles
class Missile(Entity):

    def __init__(self, x, y, img, owner):
        Entity.__init__(self, x, y, img, 5)
        self.velocity = 15                            # vitesse du missile
        self.owner = owner                            # propriétaire du missile (avion1 ou avion2)
        self.set_angle(owner.aim_direction)           # Lance le missile dans la direction dans laquelle l'avion regarde
        self.ttl = 200
        self.damage = 1                               # Degat du missile

    def destroy(self):
        self.ttl = 0

    def alive(self):
        return (self.ttl > 0) and (self.velocity > 2)

    def tick(self):
        Entity.tick(self)
        self.ttl -= 1
        if self.location[0] < 0 or self.location[0] > self.map_rect.width or \
                self.location[1] < 0 or self.location[1] > self.map_rect.height:
            self.destroy()

        return self.alive()