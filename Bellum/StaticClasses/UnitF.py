import pygame
import random
import copy
import army
from village import Village
from unit import Unit
from text import Text
from Enums.Direction import Direction

class UnitF:
    def attack(attacker,enemy,is_enemy_army,texts,town=None,boat=None,enemy_boat=None): # First unit killed 17XII Anno Domini 2024
        kill_attacker = False
        there_attacker_units = False
        there_enemy_units = False
        if attacker.can_attack and attacker.march > 0:
            attacker.attack = attacker.base_attack
            if enemy.formation == 1 or enemy.formation == 2 or enemy.formation == 0 or enemy.formation == 100:
                attacker.attack += attacker.anti_infantry_bonus
            elif enemy.formation == 3:
                attacker.attack += attacker.anti_cav_bonus
            enemy.defence = enemy.base_defence
            if attacker.owner.food == 0:
                attacker.attack -= 3
            if enemy.owner.food == 0:
                enemy.defence -= 3
                #=====Morale=====#
            UnitF.morale_combat(attacker,enemy)
            if attacker.is_boat:
                if enemy.formation in [202]:
                    attacker.attack += attacker.anti_ram_bonus
                if enemy.formation in [201]:
                    attacker.attack += attacker.anti_transport_bonus
            if enemy.is_boat:
                if attacker.formation in [202]:
                    enemy.defence += enemy.anti_ram_bonus
                if attacker.formation in [201]:
                    enemy.defence += enemy.anti_transport_bonus
                pass
                #Finish here!
            if town is not None:
                attacker.attack += attacker.siege_bonus
                if town.health > 0:
                    enemy.defence += enemy.village_bonus
                enemy.defence += town.base_defence*0.5
            #===== BOAT =====#
            if attacker.is_boat:
                if len(attacker.units_boat) > 0:
                    there_attacker_units = True
                    for unit in attacker.units_boat:
                        if unit.is_boat != True:
                            attacker.attack += unit.base_attack * 0.50
            if enemy.is_boat:
                if len(enemy.units_boat) > 0:
                    there_enemy_units = True
                    for unit in enemy.units_boat:
                        if unit.is_boat != True:
                            enemy.defence += unit.base_defence * 0.50
            #-----HEALTH
            if attacker.health < attacker.base_health * 0.8:
                attacker.attack -= attacker.base_attack * (attacker.health/attacker.base_health*0.9)
            if enemy.health < enemy.base_health * 0.8:
                enemy.defence -= enemy.base_defence * (enemy.health/enemy.base_health*0.9)
            attacker.attack += random.randint(-2,2)
            if attacker.formation == 1 or attacker.formation == 2 or attacker.formation == 0 or attacker.formation == 100:
                enemy.defence += enemy.anti_infantry_bonus
            if attacker.formation == 3:
                enemy.defence += enemy.anti_cav_bonus
            enemy.defence += random.randint(-2,2)
            damage_attacker = (1.5*((enemy.defence*1.1+1)-attacker.attack*0.60))+4
            damage_enemy = (1.5*((attacker.attack*1.1+1)-enemy.defence*0.60))
            if damage_attacker < 4:
                damage_attacker = 4
            if damage_enemy < 4:
                damage_enemy = 4
            attacker.health -= damage_attacker
            enemy.health -= damage_enemy
            if town is not None:
                town.health -= damage_enemy * 0.5
                Text.add_text(texts,f"Village health is {town.health}")
            if there_attacker_units:
                for unit in attacker.units_boat:
                    damage_unit = damage_attacker
                    if enemy.anti_transport_bonus > 0:
                        damage_unit = enemy.anti_transport_bonus * (random.randint(0,4) *0.30 + 1)
                    unit.health -= damage_unit
                    Text.add_text(texts,f"Attacker passager health is {unit.health}!")
                    unit.check_if_die()
                    break
            if there_enemy_units:
                for unit in enemy.units_boat:
                    damage_unit = damage_enemy
                    if attacker.anti_transport_bonus > 0:
                        damage_unit = attacker.anti_transport_bonus * random.randint(0,4) *0.30 + 1
                    print(damage_unit)
                    unit.health -= damage_unit
                    Text.add_text(texts,f"Defender passager health is {unit.health}!")
                    unit.check_if_die()
                    break
            Text.add_text(texts,f"Attacker health is {attacker.health}")
            Text.add_text(texts,f"Defender health is {enemy.health}")
            attacker.march = 0
            attacking_player = attacker.owner
            if attacker.health > 0:
                pass
            else:
                kill_attacker = True
                UnitF.morale_change(enemy.owner.armies,attacker.owner.armies,attacker.rect.bottomleft)
                enemy.morale += 1
            if enemy.health > 0:
                if town is not None:
                    if town.health < -10:
                        town.health = -10
                if kill_attacker:
                    attacker.kill()
                return False
            else:
                UnitF.morale_change(attacker.owner.armies,enemy.owner.armies,enemy.rect.bottomleft)
                attacker.morale += 1
                if isinstance(enemy, army.Army):
                    enemy.kill()
                    if town is not None:
                        if town.health <= 0:
                            if town.vill_type != 30:
                                town.change_owner(attacker.owner,texts)
                            else:
                                UnitF.bandit_get_killed(enemy,attacking_player)
                            if kill_attacker:
                                attacker.kill()
                            return True
                        else:
                            if kill_attacker:
                                attacker.kill()
                            return False
                    if kill_attacker:
                        attacker.kill()
                #elif town is None: # Territory of Player2 conquered 12I2025
                elif isinstance(enemy, Village):
                    if enemy.vill_type != 30:
                        enemy.change_owner(attacker.owner,texts)
                    else:
                        UnitF.bandit_get_killed(enemy,attacking_player)
                    if kill_attacker:
                        attacker.kill()
                    return True
                else:
                    Text.add_text(texts,"Error: Defender is not an army or a village: Report it on Github.")

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
    def update_color(attacker):
        if attacker.owner == 1:
            if attacker.health == attacker.base_health:
                attacker.new_banner.fill((128,0,0),special_flags=pygame.BLEND_ADD)
            elif attacker.health >0.75*attacker.base_health:
                attacker.new_banner.fill((105,0,0))
            elif attacker.health > 0.50 *attacker.base_health:
                attacker.new_banner.fill((80,0,0))
            elif attacker.health > 0.25 *attacker.base_health:
                attacker.new_banner.fill((60,5,5))
            else:
                attacker.new_banner.fill((55,1,1))
        if attacker.owner == 2:
            if attacker.health == attacker.base_health:
                attacker.new_banner.fill((0,0,128))
            elif attacker.health >0.75*attacker.base_health:
                attacker.new_banner.fill((0,0,105))
            elif attacker.health > 0.50 *attacker.base_health:
                attacker.new_banner.fill((0,0,80))
            elif attacker.health > 0.25 *attacker.base_health:
                attacker.new_banner.fill((5,5,60))
            else:
                attacker.new_banner.fill((55,1,1))
        attacker.new_banner.set_colorkey((255,255,255))
    """
    def update_color(attacker):
        color_mask = 0
        if attacker.owner.number == 1:
            color_mask = 0
            if attacker.health == attacker.base_health:
                color_mask = (128,0,0)
            elif attacker.health >0.75*attacker.base_health:
                color_mask = (105,0,0)
            elif attacker.health > 0.50 *attacker.base_health:
                color_mask = (80,0,0)
            elif attacker.health > 0.25 *attacker.base_health:
                color_mask = (60,5,5)
            else:
                color_mask = (55,1,1)
        elif attacker.owner.number == 2:
            color_mask = 0
            if attacker.health == attacker.base_health:
                color_mask = (0,0,130)
            elif attacker.health >0.75*attacker.base_health:
                color_mask = (0,0,107)
            elif attacker.health > 0.50 *attacker.base_health:
                color_mask = (0,0,82)
            elif attacker.health > 0.25 *attacker.base_health:
                color_mask = (5,5,62)
            else:
                color_mask = (1,1,56)
        elif attacker.owner.number == 3:
            color_mask = 0
            if attacker.health == attacker.base_health:
                color_mask = (0,130,2)
            elif attacker.health >0.75*attacker.base_health:
                color_mask = (0,107,3)
            elif attacker.health > 0.50 *attacker.base_health:
                color_mask = (0,82,4)
            elif attacker.health > 0.25 *attacker.base_health:
                color_mask = (2,62,6)
            else:
                color_mask = (1,1,56)
        if attacker.health <= 0:
            color_mask = (60,60,60)
        attacker.new_banner = copy.copy(attacker.banner)
        attacker.new_banner.fill(color_mask,special_flags=pygame.BLEND_RGB_ADD)
        #"""
    def add_group(added,group):
        if added is not None:
            group.add(added)
    #========== MORALE ==========#
    def morale_change(army,enemy,location):
        x = location[0]
        y = location[1]
        for me in army:
            if me.rect.colliderect((x-64,y-64,x+64,y+64)):
                me.morale += 1
        for me in enemy:
            if me.rect.colliderect((x-64,y-64,x+64,y+64)):
                me.morale -= 1
    def morale_combat(attacker,defender):
        if attacker.morale > 12 and attacker.morale <=20:
            attacker.attack += 1
        elif attacker.morale > 20 and attacker.morale <=30:
            attacker.attack += 2
        elif attacker.morale > 30 and attacker.morale <=100:
            attacker.attack += 2.5
        elif attacker.morale > 100:
            attacker.attack += 3.5
        elif attacker.morale < 8 and attacker.morale >= 0:
            attacker.attack -= 1
        elif attacker.morale < 0:
            attacker.attack -= 2

        
        if defender.morale > 12 and defender.morale <=20:
            defender.defence += 1
        elif defender.morale > 20 and defender.morale <=30:
            defender.defence += 2
        elif defender.morale > 30 and defender.morale <=100:
            defender.defence += 2.5
        elif defender.morale > 100:
            defender.defence += 3.5
        elif defender.morale < 8 and defender.morale >=0:
            defender.defence -= 1
        elif defender.morale < 0:
            defender.defence -= 2
    '''def check_if_die(attacker):
        if attacker.health <= 0:
            attacker.kill()
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
                Text.add_text(texts,"No direction given! Report it to Syriusz171")'''
    def buy(costList,player,texts=None):
        '''Takes input of cost list and player. Checks if the player can afford the cost,
        if so, it is taken from the player. Returns True or False values.
        Can output texts.'''
        if costList[0] > player.gold:
            if texts is not None:
                Text.add_text(texts,"Not enough gold!")
            return False
        if costList[1] > player.lumber:
            if texts is not None:
                if random.randint(0,11) == 0:
                    Text.add_text(texts,"More wood is needed!")
                else:
                    Text.add_text(texts,"Not enough lumber!")
            return False
        if costList[2] > player.food:
            if texts is not None:
                Text.add_text(texts,"Not enough food!")
            return False
        if costList[3] > player.spear:
            if texts is not None:
                Text.add_text(texts,"Not enough spears!")
            return False
        if costList[4] > player.bow:
            if texts is not None:
                Text.add_text(texts,"Not enough bows!")
            return False
        player.gold -= costList[0]
        player.lumber -= costList[1]
        player.food -= costList[2]
        player.spear -= costList[3]
        player.bow -= costList[4]
        return True
    def bandit_get_killed(town,killer):
        town.kill()
        killer.gold += random.randint(20,25)
        killer.bow += 1
        killer.spear += random.randint(5,16)
        killer.food += random.randint(5,6)