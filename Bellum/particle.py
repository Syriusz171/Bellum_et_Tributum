import pygame
import random
class Particle(pygame.sprite.Sprite):
    def __init__(self,position,ID,half_life,vector=None,rotate=None):
        super().__init__()
        self.vector = vector #TO DO
        self.angle = 0
        self.ID = ID
        self.rotation=rotate
        number = random.randint(-5,5)
        self.time_to_decay = half_life + number
        if self.ID == "sword":
            self.picture = pygame.image.load("images/sword.png")
        self.rect = self.picture.get_rect(center=position)
        self.og_picture = self.picture
    def starting_menu_particles(particles):
        part = Particle((700,750),"sword",-1,rotate=1)
        particles.add(part)
    def rotate_them(particles):
        for part in particles:
            if part.rotation is not None:
                part.angle += part.rotation
                if part.angle - 360 >0:
                    part.angle = part.angle - 360
                part.picture = pygame.transform.rotate(part.og_picture,part.angle)
    def decay(particles):
        for part in particles:
            if part.time_to_decay != -1:
                part.time_to_decay -= 1
                if part.time_to_decay == 0:
                    part.kill()
    def render_particles(particles,screen):
        for a in particles:
            screen.blit(a.picture,a.rect)
        
        