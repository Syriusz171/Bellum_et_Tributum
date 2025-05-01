import pygame
import random
import copy
from text import Text
from Direction import Direction
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
    def attack(self,enemy1,is_enemy_army,texts,town=None,boat=None,enemy_boat=None): # First unit killed 17XII Anno Domini 2024
        enemy = enemy1
        kill_self = False
        there_self_units = False
        there_enemy_units = False
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
            if self.is_boat:
                if enemy.formation in [202]:
                    self.attack += self.anti_ram_bonus
                if enemy.formation in [201]:
                    self.attack += self.anti_transport_bonus
            if enemy.is_boat:
                if self.formation in [202]:
                    enemy.defence += enemy.anti_ram_bonus
                if self.formation in [201]:
                    enemy.defence += enemy.anti_transport_bonus
                pass
                #Finish here!
            if town is not None:
                self.attack += self.siege_bonus
                if town.health > 0:
                    enemy.defence += enemy.village_bonus
                enemy.defence += town.base_defence*0.5
            #===== BOAT =====#
            if self.is_boat:
                if len(self.units_boat) > 0:
                    there_self_units = True
                    for unit in self.units_boat:
                        if unit.is_boat != True:
                            self.attack += unit.base_attack * 0.50
            if enemy.is_boat:
                if len(enemy.units_boat) > 0:
                    there_enemy_units = True
                    for unit in enemy.units_boat:
                        if unit.is_boat != True:
                            enemy.defence += unit.base_defence * 0.50
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
            print(f"{damage_enemy} juj")
            if damage_self < 4:
                damage_self = 4
            if damage_enemy < 4:
                damage_enemy = 4
            self.health -= damage_self
            enemy.health -= damage_enemy
            if town is not None:
                town.health -= damage_enemy * 0.5
                Text.add_text(texts,f"Village health is {town.health}")
            if there_self_units:
                for unit in self.units_boat:
                    damage_unit = damage_self
                    if enemy.anti_transport_bonus > 0:
                        damage_unit = enemy.anti_transport_bonus * (random.randint(0,4) *0.30 + 1)
                    unit.health -= damage_unit
                    Text.add_text(texts,f"Attacker passager health is {unit.health}!")
                    unit.check_if_die()
                    break
            if there_enemy_units:
                for unit in enemy.units_boat:
                    damage_unit = damage_enemy
                    if self.anti_transport_bonus > 0:
                        damage_unit = self.anti_transport_bonus * random.randint(0,4) *0.30 + 1
                    print(damage_unit)
                    unit.health -= damage_unit
                    Text.add_text(texts,f"Defender passager health is {unit.health}!")
                    unit.check_if_die()
                    break
            Text.add_text(texts,f"Attacker health is {self.health}")
            Text.add_text(texts,f"Defender health is {enemy.health}")
            self.march = 0
            attacking_player = self.owner
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
                            if town.vill_type != 30:
                                town.change_owner(self.owner,texts)
                            else:
                               Unit.bandit_get_killed(enemy,attacking_player)
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
                    if enemy.vill_type != 30:
                        enemy.change_owner(self.owner,texts)
                    else:
                        Unit.bandit_get_killed(enemy,attacking_player)
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
            if e.health < -10:
                e.health = -10
            e.health += 2
            if pygame.sprite.spritecollideany(e,villages) is not None:
                e.health += 0.5
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
    def morale_change(army,enemy,location):
        x = location[0]
        y = location[1]
        for me in army:
            if me.rect.colliderect((x-64,y-64,x+64,y+64)):
                me.morale += 1
        for me in enemy:
            if me.rect.colliderect((x-64,y-64,x+64,y+64)):
                me.morale -= 1
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
    def bandit_get_killed(town,killer):
        town.kill()
        killer.gold += random.randint(20,25)
        killer.bow += 1
        killer.spear += random.randint(5,16)
        killer.food += random.randint(5,6)