import pygame, math
import random

#Système de particule aléatoire lorsqu'un avion est touché par un missile
class ParticleSystem:
    
    def __init__(self):
        self.particles = []
        self.random = random.Random()
    
    def add_particle(self, particle):
        self.particles.append(particle)
    
    def render(self, screen):
        for particle in self.particles:
            particle.render(screen)
    
    def tick(self):
        for particle in self.particles:
            if not particle.move():
                self.particles.remove(particle)
    
    def explosion(self, x, y, particle_count):
        for i in range(particle_count):
            self.add_particle(Particle(self.random.gauss(x, 5),\
                                       self.random.gauss(y, 5),\
                                       0.5*self.random.gauss(20, 5),\
                                       self.random.random()*math.pi*2,\
                                       0.5*self.random.gauss(30, 5)))

class Particle():
    
    def __init__(self, x, y, v, r, ttl):
        self.velocity = v
        self.angle = r
        self.ttl = ttl
        self.location = [x, y]
    
    def alive(self):
        return (self.ttl > 0)
    
    def move(self):
        self.location[0] -= math.sin(self.angle) * self.velocity
        self.location[1] -= math.cos(self.angle) * self.velocity
        self.ttl -= 1
        return self.alive()
        
    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color(0x44, 0x44, 0x44), (self.location[0]-1, self.location[1]-1, 3, 3))