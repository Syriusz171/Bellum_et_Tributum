import pygame
from unit import Unit
from Direction import Direction
from player import Player
from text import Text
import copy
from particle import Particle
from random import choice
from village import Village
import random
import currect_language
import config
#Rip army1.py 15.06.2025
class Army(Unit,pygame.sprite.Sprite):
    def __init__(self,formation,owner,starting_rect,x=None,y=None,is_defending=False) -> None:
        super(Army,self).__init__()
        self.formation = formation
        self.owner = owner
        self.armies = []
        self.can_attack = True
        self.morale = 10
        self.selected = False
        self.direction = Direction.UP
        self.starting_rect = starting_rect
        self.in_village = None
        self.target_location = [0,0]
        self.distance = 9000000
        self.is_defending = is_defending

        self.is_village = False
        """
        Formations:
        0 - elite
        1 - spearman
        2 - archer
        3 - horseman
        4 - catapult
        100 - settler
        
        """
        if self.formation == 1:
            self.name = currect_language.spearman
            self.base_march = 3
            self.base_attack = 20.5
            self.base_defence = 25
            self.base_health = 100
            self.village_bonus = 2
            self.siege_bonus = 0
            self.anti_infantry_bonus = 0
            self.anti_cav_bonus = 2
            self.movement_type = [1]
            self.banner = pygame.image.load("images/Spear.png")
        elif self.formation == 0:
            self.name = "Guard"
            self.base_march = 3
            self.base_attack = 22
            self.base_defence = 26
            self.base_health = 110
            self.village_bonus = 2
            self.siege_bonus = -1
            self.anti_infantry_bonus = 2
            self.anti_cav_bonus = 0
            self.movement_type = [1]
            self.banner = pygame.image.load("images/guard.png")
        elif self.formation == 2:
            self.name = "Archers"
            self.base_march = 3
            self.base_attack = 19
            self.base_defence = 27
            self.base_health = 78
            self.village_bonus = 5
            self.siege_bonus = -3
            self.anti_infantry_bonus = 2
            self.anti_cav_bonus = -3
            self.movement_type = [1]
            self.banner = pygame.image.load("images/Bow.png")
        elif self.formation == 4:
            self.name = "Catapult"
            self.base_march = 2.5
            self.base_attack = 25
            self.base_defence = 20
            self.base_health = 80
            self.village_bonus = 3
            self.siege_bonus = 20
            self.anti_infantry_bonus = -7
            self.anti_cav_bonus = -11
            self.movement_type = [1]
            self.banner = pygame.image.load("images/catapult.png")
        elif self.formation == 3:
            self.name = "Light cavalry"
            self.base_march = 4
            self.base_attack = 22.5
            self.base_defence = 22
            self.base_health = 100
            self.village_bonus = 1
            self.siege_bonus = 3
            self.anti_infantry_bonus = 4
            self.anti_cav_bonus = 0
            self.movement_type = [1]
            self.banner = pygame.image.load("images/Horse.png")
        elif self.formation == 7:
            self.name = "Militia"
            self.base_march = 3.5
            self.base_attack = 16.5
            self.base_defence = 13
            self.base_health = 52
            self.village_bonus = 1
            self.siege_bonus = -3
            self.anti_infantry_bonus = 0
            self.anti_cav_bonus = -3
            self.movement_type = [1]
            self.banner = pygame.image.load("images/Militia.png")
        elif self.formation == 100:
            self.name = "Settlers"
            self.base_march = 4
            self.base_attack = 5
            self.base_defence = 10
            self.base_health = 50
            self.village_bonus = 1
            self.siege_bonus = -3
            self.anti_infantry_bonus = 1
            self.anti_cav_bonus = -2
            self.movement_type = [1]
            self.banner = pygame.image.load("images/Settler.png")
        elif self.formation == 201:
            self.name = "Hulk"
            self.base_march = 4
            self.base_attack = 8.5
            self.base_defence = 15.5
            self.base_health = 60
            self.village_bonus = 1
            self.siege_bonus = -3
            self.anti_infantry_bonus = 0
            self.anti_cav_bonus = -0
            self.anti_transport_bonus = 0
            self.anti_ram_bonus = -3
            self.movement_type = [2]
            self.banner = pygame.image.load("images/Transport_boat.png")
        elif self.formation == 202:
            self.name = "Ramming Ship"
            self.base_march = 3.5
            self.base_attack = 20
            self.base_defence = 15
            self.base_health = 80
            self.village_bonus = 1
            self.siege_bonus = -3
            self.anti_infantry_bonus = 0
            self.anti_cav_bonus = -0
            self.anti_ram_bonus = 3
            self.anti_transport_bonus = 4
            self.movement_type = [2]
            self.banner = pygame.image.load("images/Ram_boat.png")
        elif self.formation == 400:
            self.name = "Alpinist unit"
            self.base_march = 3.5
            self.base_attack = 20
            self.base_defence = 15
            self.base_health = 46
            self.village_bonus = 1
            self.siege_bonus = -3
            self.anti_infantry_bonus = -1
            self.anti_cav_bonus = -3
            self.anti_ram_bonus = 0
            self.anti_transport_bonus = 0
            self.movement_type = [1,5]
            self.banner = pygame.image.load("images/Alpinist.png")
        self.health = self.base_health
        self.hurt = 0
        self.rect = self.banner.get_rect(bottomleft=starting_rect)
        self.x = starting_rect[0]
        self.y = starting_rect[1]
        self.march = self.base_march
        self.last_rect = self.rect
        self.new_banner = self.banner
        self.def_x = self.x
        self.def_y = self.y
        if self.formation >= 200 and self.formation < 300:
            self.is_boat = True
    def move_self(direction,armies,terrains,all_armies,texts,villages,debug=False):
        not_boated = all_armies.copy()
        for arm in all_armies:
            if arm.is_boat:
                not_boated.remove(arm)
                arm.units_boat.empty()
                to_boat = pygame.sprite.spritecollide(arm,armies,False)
                for boat in to_boat:
                    arm.units_boat.add(boat)
                    not_boated.remove(boat)
        for not_boat in not_boated:
            not_boat.on_boat = False
        enemy_armies = all_armies.copy()
        villages1 = villages.copy()
        iterated = False
        for arm in armies:
            enemy_armies.remove(arm)
        for arm in armies:
            if iterated == False:
                for vil in villages:
                    if vil.owner == arm.owner:
                        villages1.remove(vil)
                iterated = True
            print(arm.selected)
            arm.direction = direction
            armies_testing = armies.copy()
            armies_testing.remove(arm)
            can_move = True
            terrain_exception = False
            x = None
            y = None
            if arm.march >= 0.5 and arm.selected:
                if arm.direction == Direction.UP:
                    x = arm.x
                    y = arm.y - 32
                elif arm.direction == Direction.BOTTOM:
                    x = arm.x
                    y = arm.y + 32
                elif arm.direction == Direction.LEFT:
                    x = arm.x -32
                    y = arm.y
                elif arm.direction == Direction.RIGHT:
                    x = arm.x+32
                    y = arm.y
                colliders = pygame.sprite.Group()
                collision = False
                collision1 = False
                cost = 0
                collider_enemy = False
                collider_terrain = None
                collision_enemy = False
                collision_enemy = False
                collision_terrain = None
                collider_village = None
                collision_village = False
                collision1_village = False
                boat_enemy = None
                """if_on_boat = pygame.sprite.spritecollide(arm,armies,False)
                if len(if_on_boat) == 0:
                    arm.on_boat = False
                for me in if_on_boat:
                    if arm.is_boat != True:
                     me.units_boat.add(arm)
                     arm.on_boat = True"""
                # TEST
                if arm.on_boat and arm.is_boat == False:
                    continue
                for army in armies_testing: 
                    collision1 = army.rect.collidepoint(x+16,y-16)
                    if army != arm:
                        if collision1:
                            collision = True
                            colliders.add(army)
                for army in enemy_armies: 
                    collision1_enemy = army.rect.collidepoint(x+20,y-16)
                    if collision1_enemy:
                        collision_enemy = True
                        collider_enemy = army
                        if collider_enemy.is_boat:
                            boat_enemy = army
                            break
                for ter in terrains: 
                    collision_terrain = ter.rect.collidepoint(x+16,y-16)
                    if collision_terrain:
                        collider_terrain = ter
                        if debug:
                            Text.add_text(texts,collider_terrain.form)
                        break
                for vil in villages1: 
                    collision1_village = vil.rect.collidepoint(x+16,y-16)
                    if collision1_village:
                        collision_village = True
                        collider_village = vil
                        break
                if collision == False:
                    if collision_terrain:
                        if collider_terrain.move_type == 5 and arm.formation == 400:
                            terrain_exception = True
                            cost = 3.5
                            left = arm.march - cost
                            if left < 0:
                                can_move = False
                                Text.add_text(texts,"Not enough movement!")
                            else:
                                can_move = True
                        else:
                            if collider_terrain.move_type == arm.movement_type:
                                left = arm.march - collider_terrain.movement_cost
                                cost = collider_terrain.movement_cost
                                if left < 0:
                                    can_move = False
                                    Text.add_text(texts,"Not enough movement!")
                                else:
                                    #can_move = True
                                    pass
                            else:
                                if arm.owner.is_AI != True:
                                    Text.add_text(texts,"Cannot move: Wrong terrain type1!")
                                can_move = False
                    else:
                        if arm.is_boat == False:
                            if arm.march >= 1:
                                cost = 1
                                #can_move = True
                            else:
                                Text.add_text(texts,"Cannot move: Not enough movement!")
                                can_move = False
                        else:
                            Text.add_text(texts,"Cannot use boat as car!")
                            can_move = False
                            #"""
                else:
                    for collider in colliders:
                        if len(colliders) > 1:
                            Text.add_text(texts,"Cannot stack armies on boats!")
                            terrain_exception = True
                            can_move = False
                            break
                        else:
                            if collider.is_boat == False and arm.is_boat == False and collider != arm:
                                Text.add_text(texts,"Cannot move: other unit already there!")
                                can_move = False
                            else:
                                if arm.is_boat:
                                    cost = 2
                                else:
                                    terrain_exception = True
                            if collider.is_boat and arm.is_boat:
                                can_move = False
                                Text.add_text(texts,"Cannot stack boats!")
                if arm.is_boat:
                    terrain_exception = False
                if collision_terrain == False and arm.movement_type != 1:
                    if terrain_exception == False or arm.on_boat == False or arm.is_boat == False:
                        can_move = False
                        Text.add_text(texts,"Cannot move: Wrong terrain type2!")
                if collision_terrain and arm.is_boat:
                    if collider_terrain.move_type != 2:
                        can_move = False
                        Text.add_text(texts,"Cannot move2: Wrong terrain type3!")
                if collision_enemy:
                    if boat_enemy is not None:
                        collider_enemy = boat_enemy
                if collision_enemy and can_move and collision_village == False:
                    battle = Unit.attack(arm,collider_enemy,True,texts)
                    if battle == False:
                        can_move = False
                elif collision_enemy == False and can_move and collision_village:
                    battle = Unit.attack(arm,collider_village,False,texts)
                    if battle == False:
                        can_move = False
                elif collision_enemy and can_move and collision_village:
                    battle = Unit.attack(arm,collider_enemy,True,texts,collider_village)
                    if battle == False:
                        can_move = False
                        #"""
                if arm.on_boat and arm.is_boat == False:
                    cost = 0
                if x >= 800 or y > 800 or x <0 or y<=0:
                    can_move = False
                    Text.add_text(texts,"You cannot leave the map!")
                if can_move:
                    if arm.direction == Direction.UP:
                        arm.rect.move_ip(0,-32)
                    elif arm.direction == Direction.BOTTOM:
                        arm.rect.move_ip(0,32)
                    elif arm.direction == Direction.LEFT:
                        arm.rect.move_ip(-32,0)
                    elif arm.direction == Direction.RIGHT:
                        arm.rect.move_ip(32,0)
                    if arm.is_boat:
                         for army in arm.units_boat:
                            if army != arm:
                                #Army.move_only_self(army,arm.direction,arm.owner.armies,terrains,all_armies,texts,villages)
                                Unit.just_move(army,direction,texts)
                    arm.march -= cost
                    arm.x = x
                    arm.y = y
                    Text.add_text(texts,f"Movement left: {arm.march}")
                    armies_testing.empty()
                    if arm.is_boat:
                        for boat in arm.units_boat:
                            boat.march = arm.march
                else:
                    if arm.is_boat:
                        for army in arm.units_boat:
                            if collision_terrain:
                                if collider_terrain.move_type == 2:
                                    break
                            if army != arm:
                                Army.move_only_self(army,arm.direction,arm.owner.armies,terrains,all_armies,texts,villages)
    def selection(self,texts):
        if self.selected:
            self.selected = False
            Text.add_text(texts,"Army unselected!")
        else:
            self.selected = True
            Text.add_text(texts,"Army is selected!")
    def unselect_me(self,texts):
        self.selected = False
    def unselect(armies,texts):#Unselects all armies of player
        first = True
        for arm in armies:
            if first:
                name = arm.owner.name
            arm.selected = False
        Text.add_text(texts,f"Unselected all armies of {name}")
        
    def reset_march(armies):
        for army in armies:
            army.march = army.base_march
    def conscript(type,owner,starting_rect,normal_hire,texts=None,is_defending=False):
        player = owner
        constription_possible = None
        if normal_hire == True: #Normal hire is units that cost, if False units will be free
            if Unit.buy(Army.conscript_get_cost(type),owner,texts):
                constription_possible = True
            else:
                constription_possible = False
        else:
            constription_possible = True
        if constription_possible:
            new_army = Army(type,owner,starting_rect,is_defending=is_defending)
            if is_defending:
                pass
            #self.armies.append(new_army)
            if normal_hire:
                Text.add_text(texts,"Army conscripted!")
            return new_army
        else:
            Text.add_text(texts,"Army cannot be conscripted!")
            return None

    def draw_armies(self,screen,armies): #DEPRACADED!
        for army in armies:
            screen.blit(self.banner, self.rect)
    def spawn_at_enemy_points(players,armies,terrains,texts):
        for terrain in terrains:
            if terrain.form == 41:
                if random.randint(1,40+config.difficulty) > 20:
                    who_to_select = random.randint(1,100)
                    if who_to_select > 91:
                        new_army = Army.conscript(7,terrain.owner,(terrain.x,terrain.y+32),False,texts)
                    elif who_to_select > 30:
                        new_army = Army.conscript(1,terrain.owner,(terrain.x,terrain.y+32),False,texts)
                    elif who_to_select > 15:
                        new_army = Army.conscript(3,terrain.owner,(terrain.x,terrain.y+32),False,texts)
                    elif who_to_select > 12:
                        new_army = Army.conscript(4,terrain.owner,(terrain.x,terrain.y+32),False,texts)
                    elif who_to_select > 11:
                        new_army = Army.conscript(2,terrain.owner,(terrain.x,terrain.y+32),False,texts)
                    else:
                        new_army = Army.conscript(0,terrain.owner,(terrain.x,terrain.y+32),False,texts)
                    armies.add(new_army)
                    new_army.owner.armies.add(new_army)
    def summon_militia_global(players,armies,texts): #Militia at 14:02 17 II AD 2025
        for player in players:
            if player.is_AI == 1:
                for village in player.villages:
                    if village.can_conscript_turns < 1 and village.health > 0:
                        if_collision = pygame.sprite.spritecollideany(village,armies)
                        if if_collision:
                            continue
                        else:
                            if random.randint(1,8-config.difficulty) == 1:
                                if config.allow_AI_spearman == True and random.randint(1,4) == 1:
                                    new_army = Army.conscript(1,player,(village.x,village.y),False,texts)
                                elif config.allow_AI_units and random.randint(1,10) == 1:
                                    what_unit = random.randint(0,20)
                                    if what_unit in [3,4,5]:
                                        new_army = Army.conscript(4,player,(village.x,village.y),False,texts)
                                    elif what_unit == 2:
                                        new_army = Army.conscript(2,player,(village.x,village.y),False,texts)
                                    elif what_unit == 0:
                                        new_army = Army.conscript(0,player,(village.x,village.y),False,texts)
                                    elif what_unit == 6:
                                        new_army = Army.conscript(400,player,(village.x,village.y),False,texts)
                                    else:
                                        new_army = Army.conscript(3,player,(village.x,village.y),False,texts)
                                elif random.randint(1,4) < 3 and village.vill_type == 20:
                                    new_army = Army.conscript(202,player,(village.x,village.y),False,texts)
                                else:
                                    new_army = Army.conscript(7,player,(village.x,village.y),False,texts)
                                player.get_armied(new_army)
                                armies.add(new_army)
                                if village.vill_type !=60:
                                    village.can_conscript_turns = 4
                                else:
                                    village.can_conscript_turns = 0
                                #Text.add_text(texts,"Militia created!")
    def pathfind(player,armies,villages,terrains,particles):
        t_entities = armies.copy()
        t_villages = villages.copy()
        for vil in t_villages:
            t_entities.add(vil)
        for p in player.armies:
            t_entities.remove(p)
        for py in player.villages:
            t_entities.remove(py)
        for army in player.armies:
            for enti in t_entities:
                distance = abs(army.x - enti.x )+ abs(army.y - enti.y)
                if army.distance > distance:
                    army.target_location = [enti.x,enti.y]
                    army.distance = distance
            particle_new = Particle((army.target_location[0],army.target_location[1]),"sword",10)
            particles.add(particle_new)
    def drunk_move_army(self,terrains,armies,villages):
        can_move_east = True
        can_move_west = True
        can_move_north = True
        can_move_south = True
        x = self.rect.centerx
        y = self.rect.centery
        priorities = []
        if random.randint(1,14) != 1:
            for arm in armies:
                collision1 = arm.rect.collidepoint(x+32,y)
                if collision1:
                    if arm.owner == self.owner:
                        can_move_east = False
                    else:
                        priorities.append(Direction.RIGHT)
                collision2 = arm.rect.collidepoint(x-32,y)
                if collision2:
                    if arm.owner == self.owner:
                        can_move_west = False
                    else:
                        priorities.append(Direction.LEFT)
                collision3 = arm.rect.collidepoint(x,y-32)
                if collision3:
                    if arm.owner == self.owner:
                        can_move_north = False
                    else:
                        priorities.append(Direction.UP)
                collision4 = arm.rect.collidepoint(x,y+32)
                if collision4:
                    if arm.owner == self.owner:
                        can_move_south = False
                    else:
                        priorities.append(Direction.BOTTOM)
            for vill in villages:
                collision1 = vill.rect.collidepoint(x+32,y)
                if collision1:
                    if vill.owner == self.owner:
                        pass
                    else:
                        priorities.append(Direction.RIGHT)
                collision2 = arm.rect.collidepoint(x-32,y)
                if collision2:
                    if arm.owner == self.owner:
                        pass
                    else:
                        priorities.append(Direction.LEFT)
                collision3 = arm.rect.collidepoint(x,y-32)
                if collision3:
                    if arm.owner == self.owner:
                        pass
                    else:
                        priorities.append(Direction.UP)
                collision4 = arm.rect.collidepoint(x,y+32)
                if collision4:
                    if arm.owner == self.owner:
                        pass
                    else:
                        priorities.append(Direction.BOTTOM)
            if x - 32 < 0:
                can_move_west = False
            elif x + 32 > 800:
                can_move_east = False
            if y - 32 < 0:
                can_move_north = False
            elif y + 32<0:
                can_move_south = False
            if self.is_defending:
                if x-self.def_x >=64:
                    can_move_east = False
                elif -x+self.def_x >= 32:
                    can_move_west = False
                if y-self.def_y >=32:
                    can_move_south = False
                elif -y+self.def_y >= 64:
                    can_move_north = False

            if len(priorities) != 0:
                not_attacking_chance_bonus = 0
                if arm.formation == 2:
                    not_attacking_chance_bonus = 1
                if arm.health/arm.base_health < 0.3:
                    not_attacking_chance_bonus += 2
                    if arm.health/arm.base_health < 0.1:
                        not_attacking_chance_bonus += 1
                if random.randint(1,5+not_attacking_chance_bonus) > 4:
                    pass
                else:
                    direction_of_move = choice(priorities)
                    return direction_of_move
            directions = []
            if can_move_east:
                directions.append(Direction.RIGHT)
                if random.randint(1,15) == 1:
                    return Direction.RIGHT
            if can_move_west:
                directions.append(Direction.LEFT)
            if can_move_north:
                directions.append(Direction.UP)
            if can_move_south:
                directions.append(Direction.BOTTOM)
            if len(directions) != 0:
                direction_of_move = choice(directions)
                return direction_of_move
            else:
                if self.is_defending:
                    return Direction.NULL
                else:
                    return Direction.RIGHT
        else:
            return Direction.NULL
    def move_only_self(army,direction,armies,terrains,all_armies,texts,villages,debug=False): #The first multiplayer victory at 23 II AD 2025 18:10.
        enemy_armies = all_armies.copy()
        villages1 = villages.copy()
        #iterated = False
        for arm2 in armies:
            enemy_armies.remove(arm2)
        army.direction = direction
        armies_testing = armies.copy()
        can_move = True
        terrain_exception = False
        x = army.rect.centerx
        y = army.rect.centery
        arm = army
        armies_testing.remove(army)
        if arm.owner.is_AI == False:
            Text.add_text(texts,"Trying to move!")
        for vil in villages:
            if vil.owner == arm.owner:
                villages1.remove(vil)
        if arm.march >= 0.5:
            if arm.direction == Direction.UP:
                x = arm.x
                y = arm.y - 32
            elif arm.direction == Direction.BOTTOM:
                x = arm.x
                y = arm.y + 32
            elif arm.direction == Direction.LEFT:
                x = arm.x -32
                y = arm.y
            elif arm.direction == Direction.RIGHT:
                x = arm.x+32
                y = arm.y
                
            else:
                if arm.owner.is_AI != 1:
                    Text.add_text(texts,"No direction given! Report it to Syriusz171")
            colliders = pygame.sprite.Group()
            collision = False
            collision1 = False
            cost = 0
            collider_enemy = None
            collider_terrain = None
            collision_enemy = False
            collision_enemy = False
            collision_terrain = False
            collider_village = None
            collision_village = False
            collision1_village = False
            boat_enemy = None
            boat_our = None
            for army2 in armies_testing: 
                collision1 = army2.rect.collidepoint(x+5,y)
                if collision1 and army2 != arm:
                    collision = True
                    colliders.add(army)
                    if army2.is_boat:
                        boat_our = army2
            for army2 in enemy_armies: 
                collision1_enemy = army2.rect.collidepoint(x+5,y)
                if collision1_enemy:
                    collision_enemy = True
                    collider_enemy = army2
                    if collider_enemy.is_boat:
                        boat_enemy = army2
                        break
            for ter in terrains: 
                collision_terrain = ter.rect.collidepoint(x+5,y)
                if collision_terrain:
                    collider_terrain = ter
                    if debug:
                        Text.add_text(texts,collider_terrain.form)
                    break
            for vil in villages1: 
                collision1_village = vil.rect.collidepoint(x+5,y)
                if collision1_village:
                    collision_village = True
                    collider_village = vil
                    break
            if collision == False:
                if collision_terrain:
                    if collider_terrain.move_type == 5 and arm.formation == 400:
                        terrain_exception = True
                        cost = 3.5
                        left = arm.march - cost
                        if left < 0:
                            can_move = False
                            if arm.owner.is_AI != True:
                                Text.add_text(texts,"Not enough movement!")
                        else:
                            can_move = True
                    else:
                        if collider_terrain.move_type == arm.movement_type:
                            left = arm.march - collider_terrain.movement_cost
                            cost = collider_terrain.movement_cost
                            if left < 0:
                                can_move = False
                                if arm.owner.is_AI != True:
                                    Text.add_text(texts,"Not enough movement!")
                                #can_move = True
                        else:
                            if arm.owner.is_AI != True:
                                Text.add_text(texts,"Cannot move: Wrong terrain type1!")
                            can_move = False
                else:
                    if arm.is_boat == False:
                        if arm.march >= 1:
                            cost = 1
                            #can_move = True
                        else:
                            if arm.owner.is_AI != True:
                                Text.add_text(texts,"Cannot move: Not enough movement!")
                            can_move = False
                    else:
                        if arm.owner.is_AI != True:
                            Text.add_text(texts,"print(\"Car!=boat!\")!")
                        can_move = False
                        #"""
            else:
                for collider in colliders:
                    if len(colliders) > 1:
                        if arm.owner.is_AI != True:
                            Text.add_text(texts,"Cannot stack armies on boats!")
                        terrain_exception = True
                        can_move = False
                        break
                    else:
                        if collider.is_boat == False and arm.is_boat == False:
                            if collider != arm:
                                can_move = False
                                if arm.owner.is_AI != True:
                                    Text.add_text(texts,"Cannot move: other unit already there!")
                            can_move = False
                        else:
                            if arm.is_boat:
                                cost = 2
                            else:
                                terrain_exception = True
                        if collider.is_boat and arm.is_boat:
                            can_move = False
                            if arm.owner.is_AI != True:
                                Text.add_text(texts,"Cannot stack boats!")
            if arm.is_boat:
                terrain_exception = False
            if collision_terrain == False and arm.movement_type != 1:
                if terrain_exception == False or arm.on_boat == False or arm.is_boat == False:
                    can_move = False
                    if arm.owner.is_AI != True:
                        Text.add_text(texts,"Cannot move: Wrong terrain type2!")
            if collision_terrain and arm.is_boat:
                if collider_terrain.move_type != 2:
                    can_move = False
                    if arm.owner.is_AI != True:
                        Text.add_text(texts,"Cannot move: Wrong terrain type3!")
            if collision_enemy:
                if boat_enemy is not None:
                    collider_enemy = boat_enemy
            if collision_enemy and can_move and collision_village == False:
                battle = Unit.attack(arm,collider_enemy,True,texts)
                if battle == False:
                    can_move = False
            elif collision_enemy == False and can_move and collision_village:
                battle = Unit.attack(arm,collider_village,False,texts)
                if battle == False:
                    can_move = False
            elif collision_enemy and can_move and collision_village:
                battle = Unit.attack(arm,collider_enemy,True,texts,collider_village)
                if battle == False:
                    can_move = False
                    #"""
            if arm.on_boat and arm.is_boat == False:
                cost = 0
            if x >= 800 or y > 800 or x <0 or y<=0:
                can_move = False
                if arm.owner.is_AI != True:
                    Text.add_text(texts,"You cannot leave the map!")
            if can_move:
                if arm.direction == Direction.UP:
                    arm.rect.move_ip(0,-32)
                elif arm.direction == Direction.BOTTOM:
                    arm.rect.move_ip(0,32)
                elif arm.direction == Direction.LEFT:
                    arm.rect.move_ip(-32,0)
                elif arm.direction == Direction.RIGHT:
                    arm.rect.move_ip(32,0)
                else:
                    if arm.owner.is_AI != 1:
                        Text.add_text(texts,"No direction given! Report it to Syriusz171")
                arm.march -= cost
                arm.x = x
                arm.y = y
                if arm.owner.is_AI != 1:
                    Text.add_text(texts,f"Movement left: {arm.march}")
                armies_testing.empty()
                if arm.is_boat:
                    for boat in arm.units_boat:
                        boat.march = arm.march
    def move_all(players,armies,villages,terrains,direction,texts):
        entities = armies.copy()
        for self in armies:
            self.on_boat = False
        for self in armies:
            armies1 = armies.copy()
            armies1.remove(self)
            if self.is_boat:
                self.units_boat.empty()
                unit = pygame.sprite.spritecollideany(self,armies1)
                if unit is not None:
                    if unit != self:
                        self.units_boat.add(unit)
                        unit.on_boat = True
        for vil in villages:
            entities.add(vil)
        for ent in entities:
            ent.moved = False
        for arm in armies:
            entities_false = entities.copy()
            entities_false.remove(arm)
            arm.direction = direction
            if arm.owner.active and arm.selected and arm.march >= 0.5:
                if direction == Direction.UP:
                    x = arm.rect.centerx
                    y = arm.rect.centery -32
                elif direction == Direction.BOTTOM:
                    x = arm.rect.centerx
                    y = arm.rect.centery +32
                elif direction == Direction.RIGHT:
                    x = arm.rect.centerx+32
                    y = arm.rect.centery
                elif direction == Direction.LEFT:
                    x = arm.rect.centerx-32
                    y = arm.rect.centery
                elif arm.direction == Direction.NULL:
                    break
                else:
                    Text.add_text(texts,"ERROR: No direction given! Report it to Syriusz171!")
                    break
                if x >= 800 or y > 800 or x <0 or y<=0:
                    if arm.owner.is_AI != True:
                        Text.add_text(texts,"You cannot leave the map!")
                    break
                x+=1
                y+=1
                colliders = pygame.sprite.Group()
                allies = pygame.sprite.Group()
                allied_boats = pygame.sprite.Group()
                allied_towns = pygame.sprite.Group()
                enemies = pygame.sprite.Group()
                cost = 1
                #===== VILLAGES + ARMIES COLLISIONS
                for ent in entities_false:
                    coll = ent.rect.collidepoint(x,y)
                    if coll:
                        colliders.add(ent)
                        if ent.owner == arm.owner:
                            if ent.is_village:
                                allied_towns.add(ent)
                            elif ent.is_boat == False:
                                allies.add(ent)
                            else:
                                allied_boats.add(ent)
                        else:
                            enemies.add(ent)
                can_move = True
                collided = False
                #===== TERRAIN COLLISION =====#
                for terr in terrains:
                    coll = terr.rect.collidepoint(x,y)
                    if coll:
                        collided = True
                        cost = terr.movement_cost
                        if terr.move_type not in arm.movement_type and arm.movement_type != -1:
                            if len(allied_boats) == 0:
                                if terr.move_type != 2:
                                    if arm.owner.is_AI != True:
                                        Text.add_text(texts,"Cannot move: Wrong terrains type!")
                                        if arm.is_boat:
                                            for army in arm.units_boat:
                                                Army.move_me(army,players,armies,villages,terrains,direction,texts)
                                else:
                                    if arm.owner.is_AI != True:
                                        Text.add_text(texts,"In order to sail you need a few builded boats!")
                                can_move = False
                                continue
                            else: # There is boat!
                                cost = 1
                if 1 not in arm.movement_type and collided == False:
                    if arm.owner.is_AI != True:
                        Text.add_text(texts,"This unit cannot go on land!")
                        can_move = False
                        if arm.is_boat:
                            for army in arm.units_boat:
                                Army.move_me(army,players,armies,villages,terrains,direction,texts)
                        continue
                if can_move == False:
                    continue
                if len(allies) >= 1:
                    for ally in allies:
                        pass
                        #if ally.selected == False:
                        #   ARMY SWAPPING will go here
                    if arm.owner.is_AI != True:
                        Text.add_text(texts,"Cannot increase pressure of armies (stack them)!")
                    continue
                if cost > arm.march:
                    if arm.owner.is_AI != True:
                        Text.add_text(texts,"Cannot move: Not enough movement!")
                    continue
                if len(enemies) >= 1:
                    town = None
                    boat = None
                    land_army = None
                    for enemy in enemies:
                        if enemy.is_boat:
                            boat = enemy
                        elif enemy.is_village:
                            town = enemy
                        else:
                            land_army = enemy
                    if boat is not None:
                        land_army = boat
                    #There is an army:
                    if land_army is not None:
                        battle = Unit.attack(arm,land_army,True,texts,town)
                        if battle == False:
                            continue
                    else:
                        battle = Unit.attack(arm,town,False,texts)
                        if battle == False:
                            continue
                if arm.direction == Direction.UP:
                    arm.rect.move_ip(0,-32)
                elif arm.direction == Direction.BOTTOM:
                    arm.rect.move_ip(0,32)
                elif arm.direction == Direction.LEFT:
                    arm.rect.move_ip(-32,0)
                elif arm.direction == Direction.RIGHT:
                    arm.rect.move_ip(32,0)
                if arm.is_boat:
                    for army in arm.units_boat:
                        Unit.just_move(army,direction,texts)
                        #Army.move_me(army,players,armies,villages,terrains,direction,texts)
                arm.march -= cost
                if arm.owner.is_AI != True:
                    Text.add_text(texts,f"Movement left {arm.march}")

    def move_me(arm,players,armies,villages,terrains,direction,texts,do_check=False):
        entities = armies.copy()
        """
        for self in armies:
            self.on_boat = False
        for self in armies:
            armies1 = armies.copy()
            armies1.remove(self)
            if self.is_boat:
                self.units_boat.empty()
                unit = pygame.sprite.spritecollideany(self,armies1)
                if unit is not None:
                    if unit != self:
                        self.units_boat.add(unit)
                        unit.on_boat = True"""
        for vil in villages:
            entities.add(vil)
        for ent in entities:
            ent.moved = False
        entities_false = entities.copy()
        entities_false.remove(arm)
        arm.direction = direction
        if arm.march >= 0.5:
            if direction == Direction.UP:
                x = arm.rect.centerx
                y = arm.rect.centery -32
            elif direction == Direction.BOTTOM:
                x = arm.rect.centerx
                y = arm.rect.centery +32
            elif direction == Direction.RIGHT:
                x = arm.rect.centerx+32
                y = arm.rect.centery
            elif direction == Direction.LEFT:
                x = arm.rect.centerx-32
                y = arm.rect.centery
            elif arm.direction == Direction.NULL:
                return
            else:
                Text.add_text(texts,"ERROR: No direction given! Report it to Syriusz171!")
                return
            if x >= 800 or y > 800 or x <0 or y<=0:
                if arm.owner.is_AI != True:
                    Text.add_text(texts,"You cannot leave the map!")
                return
            x+=1
            y+=1
            colliders = pygame.sprite.Group()
            allies = pygame.sprite.Group()
            allied_boats = pygame.sprite.Group()
            allied_towns = pygame.sprite.Group()
            enemies = pygame.sprite.Group()
            cost = 1
            #===== VILLAGES + ARMIES COLLISIONS
            for ent in entities_false:
                coll = ent.rect.collidepoint(x,y)
                if coll:
                    colliders.add(ent)
                    if ent.owner == arm.owner:
                        if ent.is_village:
                            allied_towns.add(ent)
                        elif ent.is_boat == False:
                            allies.add(ent)
                        else:
                            allied_boats.add(ent)
                    else:
                        enemies.add(ent)
            can_move = True
            collided = False
            #===== TERRAIN COLLISION =====#
            for terr in terrains:
                coll = terr.rect.collidepoint(x,y)
                if coll:
                    collided = True
                    cost = terr.movement_cost
                    if terr.move_type not in arm.movement_type and arm.movement_type != -1:
                        if len(allied_boats) == 0:
                            if terr.move_type != 2:
                                if arm.owner.is_AI != True:
                                    Text.add_text(texts,"Cannot move: Wrong terrains type!")
                            else:
                                if arm.owner.is_AI != True:
                                    Text.add_text(texts,"In order to sail you need a few builded boats!")
                            can_move = False
                            return
                        else: # There is boat!
                            cost = 1
            if arm.is_boat and collided == False:
                if arm.owner.is_AI != True:
                    Text.add_text(texts,"This unit cannot go on land!")
                can_move = False
                '''if arm.is_boat:
                    for army in arm.units_boat:
                        Army.move_me(army,players,armies,villages,terrains,direction,texts)'''
                return
            if can_move == False:
                return
            if len(allies) >= 1:
                for ally in allies:
                    pass
                    #if ally.selected == False:
                    #   ARMY SWAPPING will go here
                if arm.owner.is_AI != True:
                    Text.add_text(texts,"Cannot increase pressure of armies (stack them)!")
                return
            if len(enemies) >= 1:
                town = None
                boat = None
                land_army = None
                for enemy in enemies:
                    if enemy.is_boat:
                        boat = enemy
                    elif enemy.is_village:
                        town = enemy
                    else:
                        land_army = enemy
                if boat is not None:
                    land_army = boat
                #There is an army:
                if land_army is not None:
                    battle = Unit.attack(arm,land_army,True,texts,town)
                    if battle == False:
                        return
                else:
                    battle = Unit.attack(arm,town,True,texts)
                    if battle == False:
                        return
            if cost > arm.march:
                if arm.owner.is_AI != True:
                    Text.add_text(texts,"Cannot move: Not enough movement!")
                return
            if arm.direction == Direction.UP:
                arm.rect.move_ip(0,-32)
            elif arm.direction == Direction.BOTTOM:
                arm.rect.move_ip(0,32)
            elif arm.direction == Direction.LEFT:
                arm.rect.move_ip(-32,0)
            elif arm.direction == Direction.RIGHT:
                arm.rect.move_ip(32,0)
            arm.march -= cost
            if arm.owner.is_AI != True:
                Text.add_text(texts,f"Movement left {arm.march}")
    def Id_to_name(input_ID):
        IDs = {0:"Guard",1:"Spear infantry",2:"Archers",3:"Light cavalry",4:"Catapult",7:"Militia",100:"Settlers",201:"Hulk",202:"Ramming ship",400:"Alpinistic unit"}
        for ID, name in IDs.items():
            if ID == input_ID:
                return name
    def conscript_get_cost(ID):
        # GOLD, LUMBER, FOOD, SPEARS, BOWS
        if ID == 0:
            return(70,20,25,30,5)
        elif ID == 1:
            return (10,1,7,20,0)
        elif ID == 2:
            return (15,5,5,0,4)
        elif ID == 3:
            return (25,1,15,20,0)
        elif ID == 4:
            return (30,20,8,1,0)
        elif ID == 7:
            return (5,0,15,5,0)
        elif ID == 100:
            return (20,0,0,0,0)
        elif ID == 201:
            return (30,20,2,0,0)
        elif ID == 202:
            return (40,25,10,10,1)
        elif ID == 400:
            return (30,10,10,10,3)
    


