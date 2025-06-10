import pygame
import copy
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
        elif type == 13:
            self.picture = pygame.image.load("images/rich_center_icon.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 14:
            self.picture = pygame.image.load("images/test_map_icon.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 15:
            self.picture = pygame.image.load("images/yorktown_icon.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 16:
            self.picture = pygame.image.load("images/bastion_icon.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 20:
            self.picture = pygame.image.load("images/stone_button.png")
            self.rect = self.picture.get_rect(center=center)
        elif type == 400:
            self.picture = pygame.image.load("images/alpinist_off.png")
            self.rect = self.picture.get_rect(center=center)
            self.checked = True
        self.og_picture = self.picture
        if type == 400:
            self.mask_self()
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
        else:
            if self.type == 400:
                if self.checked:
                    self.checked = False
                    self.mask_self()
                    return False
                else:
                    self.checked = True
                    self.mask_self()
                    return True
    def activate_button(self,activator):
        self.active = activator
    def activate_group(buttons,state):
        for button in buttons:
            button.active = state
    def mask_self(self):
        if self.checked:
            color_mask = (5,79,20)
        else:
            color_mask = (79,5,20)
        self.picture = copy.copy(self.og_picture)
        self.picture.fill(color_mask,special_flags=pygame.BLEND_RGB_ADD)
        