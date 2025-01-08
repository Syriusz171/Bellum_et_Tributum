import pygame
class Kliczek():
    def __init__(self) -> None:
        self.image = pygame.image.load("images/kliczek.png") #Kliczek is an entity that is always in position of mouse
        self.rect = self.image.get_rect(center=(13*32+16,13*32+16))
    def move_kliczek(self,location):
        self.rect = self.image.get_rect(center=location)
    def draw_kliczek(self,screen):
        screen.blit(self.image,self.rect)