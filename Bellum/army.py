import pygame
from unit import Unit
from Direction import Direction
from player import Player
from text import Text
class Army(Unit,pygame.sprite.Sprite):
    def __init__(self,formation,owner,starting_rect,x=None,y=None) -> None:
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
            self.base_march = 3
            self.base_attack = 20.5
            self.base_defence = 25
            self.base_health = 100
            self.village_bonus = 2
            self.siege_bonus = 0
            self.anti_infantry_bonus = 0
            self.anti_cav_bonus = 2
            self.movement_type = 1
            self.banner = pygame.image.load("images/Spear.png")
        elif self.formation == 0:
            self.base_march = 3
            self.base_attack = 22
            self.base_defence = 26
            self.base_health = 110
            self.village_bonus = 2
            self.siege_bonus = -1
            self.anti_infantry_bonus = 2
            self.anti_cav_bonus = 0
            self.movement_type = 1
            self.banner = pygame.image.load("images/guard.png")
        elif self.formation == 2:
            self.base_march = 3
            self.base_attack = 19
            self.base_defence = 27
            self.base_health = 78
            self.village_bonus = 5
            self.siege_bonus = -3
            self.anti_infantry_bonus = 2
            self.anti_cav_bonus = -3
            self.movement_type = 1
            self.banner = pygame.image.load("images/Bow.png")
        elif self.formation == 4:
            self.base_march = 2.5
            self.base_attack = 25
            self.base_defence = 20
            self.base_health = 80
            self.village_bonus = 3
            self.siege_bonus = 20
            self.anti_infantry_bonus = -7
            self.anti_cav_bonus = -11
            self.movement_type = 1
            self.banner = pygame.image.load("images/catapult.png")
        elif self.formation == 3:
            self.base_march = 4
            self.base_attack = 22
            self.base_defence = 22
            self.base_health = 100
            self.village_bonus = 1
            self.siege_bonus = 3
            self.anti_infantry_bonus = 4
            self.anti_cav_bonus = 0
            self.movement_type = 1
            self.banner = pygame.image.load("images/Horse.png")
        elif self.formation == 100:
            self.base_march = 3
            self.base_attack = 5
            self.base_defence = 10
            self.base_health = 50
            self.village_bonus = 1
            self.siege_bonus = -3
            self.anti_infantry_bonus = 1
            self.anti_cav_bonus = -2
            self.movement_type = 1
            self.banner = pygame.image.load("images/Settler.png")
        elif self.formation == 201:
            self.base_march = 3.5
            self.base_attack = 5.5
            self.base_defence = 15.5
            self.base_health = 55
            self.village_bonus = 1
            self.siege_bonus = -3
            self.anti_infantry_bonus = 0
            self.anti_cav_bonus = -0
            self.anti_transport_bonus = 0
            self.anti_ram_bonus = -3
            self.movement_type = 2
            self.banner = pygame.image.load("images/Transport_boat.png")
        elif self.formation == 202:
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
            self.movement_type = 2
            self.banner = pygame.image.load("images/Ram_boat.png")
        elif self.formation == 400:
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
            self.movement_type = 1
            self.banner = pygame.image.load("images/Alpinist.png")
        self.health = self.base_health
        self.hurt = 0
        self.rect = self.banner.get_rect(bottomleft=starting_rect)
        self.x = starting_rect[0]
        self.y = starting_rect[1]
        self.march = self.base_march
        self.last_rect = self.rect
        self.new_banner = self.banner
        if self.formation > 200 and self.formation < 300:
            self.is_boat = True
    def move_self(direction,armies,terrains,all_armies,texts,villages,debug=False):
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
                for army in armies_testing: 
                    collision1 = army.rect.collidepoint(x+16,y-16)
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
                                    can_move = True
                            else:
                                can_move = False
                                Text.add_text(texts,"Cannot move: Wrong terrain type!")
                    else:
                        if arm.is_boat == False:
                            if arm.march >= 1:
                                cost = 1
                                can_move = True
                            else:
                                Text.add_text(texts,"Cannot move: Not enough movement!")
                                can_move = False
                        else:
                            Text.add_text(texts,"Cannot drive using boat!")
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
                            if collider.is_boat == False and arm.is_boat == False:
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
                        Text.add_text(texts,"Cannot move: Wrong terrain type!")
                if collision_terrain and arm.is_boat:
                    if collider_terrain.move_type != 2:
                        can_move = False
                        Text.add_text(texts,"Cannot move: Wrong terrain type!")
                        continue
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
                    arm.march -= cost
                    arm.x = x
                    arm.y = y
                    Text.add_text(texts,f"Movement left: {arm.march}")
                    armies_testing.empty()
                    if arm.is_boat:
                        for boat in arm.units_boat:
                            boat.march = arm.march
                if_on_boat = pygame.sprite.spritecollide(arm,armies,False)
                for me in if_on_boat:
                    if me.is_boat:
                        me.on_boat = True
                    else:
                        me.on_boat = False
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
    def conscript(type,owner,starting_rect,normal_hire,texts=None):
        player = owner
        constription_possible = None
        if normal_hire == True: #Normal hire is units that cost, if False units will be free
            if type == 1:
                if player.gold >= 3 and player.food >= 7 and player.spear >= 4:
                    player.gold -= 3
                    player.food -= 7
                    player.spear -= 4
                    constription_possible = True
                else:
                    constription_possible = False
            elif type == 2:
                if player.gold >= 5 and player.food >= 7 and player.bow >= 4 and player.lumber >= 1:
                    player.gold -= 5
                    player.food -= 7
                    player.bow -= 4
                    player.lumber -= 1
                    constription_possible = True
                else:
                    constription_possible = False
            elif type == 3:
                if player.gold >= 10 and player.food >= 10 and player.spear >= 3:
                    player.gold -= 10
                    player.food -= 10
                    player.spear -= 3
                    constription_possible = True
                else:
                    constription_possible = False
            elif type == 4:
                if player.gold >= 15 and player.food >= 3 and player.lumber >= 10:
                    player.gold -= 15
                    player.food -= 3
                    player.lumber -= 10
                    constription_possible = True
                else:
                    constription_possible = False
            elif type == 100:
                if player.gold >= 10:
                    player.gold -= 10
                    constription_possible = True
                    Text.add_text(texts,constription_possible)
                else:
                    constription_possible = False
            elif type == 400:
                if player.gold >= 40 and player.food >= 15 and player.lumber >= 5:
                    player.gold -= 40
                    player.food -= 15
                    player.lumber -= 5
                    constription_possible = True
        else:
            constription_possible = True
        if constription_possible:
            new_army = Army(type,owner,starting_rect)
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