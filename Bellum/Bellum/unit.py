import pygame
import random
import copy
from text import Text
class Unit():
    def __init__(self) -> None:
        super().__init__()
        self.selected = False
        self.banner = None
        self.new_banner = None
        self.type = None
        self.owner = None
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
        self.wall = None
        self.morale = None
        self.in_village = None
        self.health = 75
        self.village_defence_bonus = None
    def attack(self,enemy1,texts): # First unit killed 17XII Anno Domini 2024
        enemy = enemy1
        if self.can_attack and self.march > 0:
            self.attack = self.base_attack
            if enemy.formation == 1:
                self.attack += self.anti_infantry_bonus
            if enemy.formation == 2:
                self.attack += self.anti_infantry_bonus
            if enemy.formation == 3:
                self.attack += self.anti_cav_bonus
            enemy.defence = enemy.base_defence
            if enemy.in_village:
                self.attack += self.siege_bonus
                enemy.attack += enemy.village_bonus
            self.attack += random.randint(-2,2)
            if self.formation == 1 or self.formation == 2:
                enemy.defence += enemy.anti_infantry_bonus
            if self.formation == 3:
                enemy.defence += enemy.anti_cav_bonus
            enemy.defence += random.randint(-2,2)
            damage_self = ((enemy.defence+1)-self.attack*0.60)+1
            damage_enemy = ((self.attack+1)-enemy.defence*0.60)+1
            self.health -= damage_self
            enemy.health -= damage_enemy
            Text.add_text(texts,f"Attacker health is {self.health}")
            Text.add_text(texts,f"Defender health is {enemy.health}")
            self.march = 0
            if self.health > 0:
                pass
            else:
                self.kill()
            if enemy.health > 0:
                return False
            else:
                enemy.kill()
                return True

        else:
            pass
    def heal(armies,villages):
        entities = armies.copy()
        for v in villages:
            entities.add(v)
        for e in entities:
            e.health += 2
            if e.health > e.base_health:
                e.health = e.base_health
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
        if self.owner == 1:
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
        if self.owner == 2:
            color_mask = 0
            if self.health == self.base_health:
                color_mask = (0,0,128)
            elif self.health >0.75*self.base_health:
                color_mask = (0,0,105)
            elif self.health > 0.50 *self.base_health:
                color_mask = (0,0,80)
            elif self.health > 0.25 *self.base_health:
                color_mask = (5,5,60)
            else:
                color_mask = (1,1,55)
        self.new_banner = copy.copy(self.banner)
        self.new_banner.fill(color_mask,special_flags=pygame.BLEND_ADD)
        #"""
    def add_group(added,group):
        if added is not None:
            group.add(added)