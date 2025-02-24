import pygame
import random
class Particle(pygame.sprite.Sprite):
    def __init__(self,position,ID,half_life,vector=None):
        super().__init__()
        self.vector = vector #TO DO
        self.ID = ID
        number = random.randint(-5,5)
        self.time_to_decay = half_life + number
        if self.ID == "sword":
            self.picture = pygame.image.load("images/sword.png")
        self.rect = self.picture.get_rect(center=position)
    def decay(particles):
        for part in particles:
            part.time_to_decay -= 1
            if part.time_to_decay <= 0:
                part.kill()
    def render_particles(particles,screen):
        for a in particles:
            screen.blit(a.picture,a.rect)
        
        