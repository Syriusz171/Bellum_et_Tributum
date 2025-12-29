import pygame
import copy
class Button(pygame.sprite.Sprite):
    def __init__(self,type,center,active=False,image=None,checked=True,tags=None,text=None):
        super().__init__()
        self.active = active
        self.checked = checked
        self.type = type
        self.center = center
        self.tags = tags
        self.text = text
        if image is not None:
            self.picture = pygame.image.load(image)
            self.rect = self.picture.get_rect(center=center)
        else:
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
            elif type == 14:
                self.picture = pygame.image.load("images/lakes_map_icon.png")
            elif type == 15:
                self.picture = pygame.image.load("images/yorktown_icon.png")
            elif type == 16:
                self.picture = pygame.image.load("images/bastion_icon.png")
            elif type == 20:
                self.picture = pygame.image.load("images/stone_button.png")
            elif type == 400:
                self.picture = pygame.image.load("images/alpinist_off.png")
                self.checked = True
        self.rect = self.picture.get_rect(center=center)
        self.og_picture = copy.copy(self.picture)
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
    def action_tag(buttons,tag,action):
        #Action must be: "kill", "off" or "on"!
        for i in buttons:
            if i.tags is not None:
                if tag in i.tags:
                    if action == "off":
                        i.active = False
                    elif action == "on":
                        i.active = True
                    elif action == "kill":
                        i.kill()
    def blit_buttons(buttons,screen):
        for b in buttons:
            if b.active:
                screen.blit(b.picture,b.rect)
                if b.text is not None:
                    screen.blit(b.text[1].render(b.text[0],False,b.text[2]),(b.rect.left+7,b.rect.centery-b.text[1].get_ascent()/2))#-b.text[1].get_ascent()
                    #screen.blit(b.text,(b.rect.left+7,b.rect.centery-10))
        