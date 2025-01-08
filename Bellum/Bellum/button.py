import pygame
class Button(pygame.sprite.Sprite):
    def __init__(self,type,center,active=False):
        super().__init__()
        self.active = active
        self.type = type
        if type == 1 or type == 4: # 1 is quick start
            self.picture = pygame.image.load("images/generic_button.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 2:
            self.picture = pygame.image.load("images/show_production.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 3:
            self.picture = pygame.image.load("images/key.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 11:
            self.picture = pygame.image.load("images/track_map_icon.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 12:
            self.picture = pygame.image.load("images/flats_map_icon.png")
            self.rect = self.picture.get_rect(center=center)
    def activate_button(self,activator):
        self.active = activator
        