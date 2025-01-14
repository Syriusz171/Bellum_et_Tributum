import pygame
class Button(pygame.sprite.Sprite):
    def __init__(self,type,center,active=False):
        super().__init__()
        self.active = active
        self.checked = None
        self.type = type
        self.center = center
        if type == 1 or type == 4: # 1 is quick start
            self.picture = pygame.image.load("images/generic_button.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 2:
            self.picture = pygame.image.load("images/show_production.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 3:
            self.picture = pygame.image.load("images/key.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 6 or type == 5:
            self.picture = pygame.image.load("images/gold_handicap_button.png")
            self.rect = self.picture.get_rect(center=center)
            self.checked = False
        elif type == 11:
            self.picture = pygame.image.load("images/track_map_icon.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 12:
            self.picture = pygame.image.load("images/flats_map_icon.png")
            self.rect = self.picture.get_rect(center=center)
    def update_button(self):
        if self.type == 6 or self.type == 5:
            if self.checked == False:
                self.checked = True
                self.picture = pygame.image.load("images/gold_handicap_button_on.png")
                self.rect = self.picture.get_rect(center=self.center)
                return True
            else:
                self.checked = False
                self.picture = pygame.image.load("images/gold_handicap_button.png")
                self.rect = self.picture.get_rect(center=self.center)
                return False
    def activate_button(self,activator):
        self.active = activator
        