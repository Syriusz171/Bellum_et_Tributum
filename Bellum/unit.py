import pygame
import random
import copy
from text import Text
from Enums.Direction import Direction
class Unit():
    def __init__(self) -> None:
        super().__init__()
        self.selected = False
        self.banner = None
        self.new_banner = None
        self.type = None
        self.owner = None
        self.on_boat = False
        self.formation = None
        self.base_attack = None
        self.base_defence = None
        self.base_health = None
        self.can_attack = False
        self.village_bonus = None
        self.siege_bonus = None
        self.march = None
        self.anti_cav_bonus = None
        self.anti_infantry_bonus = None
        self.anti_transport_bonus = 0
        self.anti_ram_bonus = 0
        self.units_boat = pygame.sprite.Group()
        self.wall = None
        self.morale = 10
        self.in_village = None
        self.health = 75
        self.is_boat = False
        self.village_defence_bonus = None
        self.moved = False
    """
    def update_color(self):
        if self.owner == 1:
            if self.health == self.base_health:
                self.new_banner.fill((128,0,0),special_flags=pygame.BLEND_ADD)
            elif self.health >0.75*self.base_health:
                self.new_banner.fill((105,0,0))
            elif self.health > 0.50 *self.base_health:
                self.new_banner.fill((80,0,0))
            elif self.health > 0.25 *self.base_health:
                self.new_banner.fill((60,5,5))
            else:
                self.new_banner.fill((55,1,1))
        if self.owner == 2:
            if self.health == self.base_health:
                self.new_banner.fill((0,0,128))
            elif self.health >0.75*self.base_health:
                self.new_banner.fill((0,0,105))
            elif self.health > 0.50 *self.base_health:
                self.new_banner.fill((0,0,80))
            elif self.health > 0.25 *self.base_health:
                self.new_banner.fill((5,5,60))
            else:
                self.new_banner.fill((55,1,1))
        self.new_banner.set_colorkey((255,255,255))
    """
    def update_color(self):
        color_mask = 0
        if self.owner.number == 1:
            color_mask = 0
            if self.health == self.base_health:
                color_mask = (128,0,0)
            elif self.health >0.75*self.base_health:
                color_mask = (105,0,0)
            elif self.health > 0.50 *self.base_health:
                color_mask = (80,0,0)
            elif self.health > 0.25 *self.base_health:
                color_mask = (60,5,5)
            else:
                color_mask = (55,1,1)
        elif self.owner.number == 2:
            color_mask = 0
            if self.health == self.base_health:
                color_mask = (0,0,130)
            elif self.health >0.75*self.base_health:
                color_mask = (0,0,107)
            elif self.health > 0.50 *self.base_health:
                color_mask = (0,0,82)
            elif self.health > 0.25 *self.base_health:
                color_mask = (5,5,62)
            else:
                color_mask = (1,1,56)
        elif self.owner.number == 3:
            color_mask = 0
            if self.health == self.base_health:
                color_mask = (0,130,2)
            elif self.health >0.75*self.base_health:
                color_mask = (0,107,3)
            elif self.health > 0.50 *self.base_health:
                color_mask = (0,82,4)
            elif self.health > 0.25 *self.base_health:
                color_mask = (2,62,6)
            else:
                color_mask = (1,1,56)
        if self.health <= 0:
            color_mask = (60,60,60)
        self.new_banner = copy.copy(self.banner)
        self.new_banner.fill(color_mask,special_flags=pygame.BLEND_RGB_ADD)
        #"""
    def add_group(added,group):
        if added is not None:
            group.add(added)
    def check_if_die(self):
        if self.health <= 0:
            self.kill()
    def just_move(unit,direction,texts):
        unit.direction = direction
        if unit.direction == Direction.UP:
            unit.rect.move_ip(0,-32)
        elif unit.direction == Direction.BOTTOM:
            unit.rect.move_ip(0,32)
        elif unit.direction == Direction.LEFT:
            unit.rect.move_ip(-32,0)
        elif unit.direction == Direction.RIGHT:
            unit.rect.move_ip(32,0)
        else:
            if unit.owner.is_AI != 1:
                Text.add_text(texts,"No direction given! Report it to Syriusz171")