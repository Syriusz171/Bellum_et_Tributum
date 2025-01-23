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
        self.morale = 10
        self.in_village = None
        self.health = 75
        self.village_defence_bonus = None
    def attack(self,enemy1,is_enemy_army,texts,town=None): # First unit killed 17XII Anno Domini 2024
        enemy = enemy1
        kill_self = False
        if self.can_attack and self.march > 0:
            self.attack = self.base_attack
            if enemy.formation == 1 or enemy.formation == 2 or enemy.formation == 0 or enemy.formation == 100:
                self.attack += self.anti_infantry_bonus
            elif enemy.formation == 3:
                self.attack += self.anti_cav_bonus
            enemy.defence = enemy.base_defence
            if self.owner.food == 0:
                self.attack -= 3
            if enemy.owner.food == 0:
                enemy.defence -= 3
                #Morale
            if enemy.morale >= 12 and enemy.morale <20:
                enemy.defence += 1
            elif enemy.morale > 20:
                enemy.defence += 2
            elif enemy.morale <= 8 and enemy.morale > 0:
                enemy.defence -= 1
            elif enemy.morale < 0:
                enemy.defence -= 2
            if self.morale >= 12 and self.morale <20:
                self.attack += 1
            elif self.morale > 20:
                self.attack += 2
            elif self.morale <= 8 and self.morale > 0:
                self.attack -= 1
            elif self.morale < 0:
                self.attack -= 2
            
            if town is not None:
                self.attack += self.siege_bonus
                if town.health > 0:
                    enemy.defence += enemy.village_bonus
                enemy.defence += town.base_defence*0.5
            if  self.health *2 < self.base_health:
                self.attack -= 1
            if  enemy.health *2 < enemy.base_health:
                enemy.defence -= 1
            self.attack += random.randint(-2,2)
            if self.formation == 1 or self.formation == 2 or self.formation == 0 or self.formation == 100:
                enemy.defence += enemy.anti_infantry_bonus
            if self.formation == 3:
                enemy.defence += enemy.anti_cav_bonus
            enemy.defence += random.randint(-2,2)
            damage_self = (1.5*((enemy.defence*1.1+1)-self.attack*0.60))+4
            damage_enemy = (1.5*((self.attack*1.1+1)-enemy.defence*0.60))
            if damage_self < 4:
                damage_self = 4
            if damage_enemy < 4:
                damage_enemy = 4
            self.health -= damage_self
            enemy.health -= damage_enemy
            if town is not None:
                town.health -= damage_enemy * 0.5
                Text.add_text(texts,f"Village health is {town.health}")
            Text.add_text(texts,f"Attacker health is {self.health}")
            Text.add_text(texts,f"Defender health is {enemy.health}")
            self.march = 0
            if self.health > 0:
                pass
            else:
                kill_self = True
                Unit.morale_change(enemy.owner.armies,self.owner.armies,self.rect.bottomleft)
                enemy.morale += 1
            if enemy.health > 0:
                if town is not None:
                    if town.health < -10:
                        town.health = -10
                if kill_self:
                    self.kill()
                return False
            else:
                Unit.morale_change(self.owner.armies,enemy.owner.armies,enemy.rect.bottomleft)
                self.morale += 1
                if is_enemy_army:
                    enemy.kill()
                    if town is not None:
                        if town.health <= 0:
                            town.change_owner(self.owner,texts)
                            if kill_self:
                                self.kill()
                            return True
                        else:
                            if kill_self:
                                self.kill()
                            return False
                    if kill_self:
                        self.kill()
                elif town is None: # Territory of Player2 conquered 12I2025
                    enemy.change_owner(self.owner,texts)
                    if kill_self:
                        self.kill()
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
        if self.health <= 0:
            color_mask = (60,60,60)
        self.new_banner = copy.copy(self.banner)
        self.new_banner.fill(color_mask,special_flags=pygame.BLEND_RGB_ADD)
        #"""
    def add_group(added,group):
        if added is not None:
            group.add(added)
    def morale_change(army,enemy,location):
        x = location[0]
        y = location[1]
        for me in army:
            if me.rect.colliderect((x-64,y-64,x+64,y+64)):
                me.morale += 1
        for me in enemy:
            if me.rect.colliderect((x-64,y-64,x+64,y+64)):
                me.morale -= 1