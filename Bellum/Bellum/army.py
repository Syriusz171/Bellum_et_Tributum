import pygame
from unit import Unit
from Direction import Direction
from player import Player
from text import Text
class Army(Unit,pygame.sprite.Sprite):
    def __init__(self,formation,owner,starting_rect) -> None:
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
            self.base_attack = 20
            self.base_defence = 25
            self.base_health = 100
            self.village_bonus = 2
            self.siege_bonus = 0
            self.anti_infantry_bonus = 0
            self.anti_cav_bonus = 2
            self.movement_type = 1
            self.banner = pygame.image.load("images/Spear.png")
        elif self.formation == 2:
            self.base_march = 3
            self.base_attack = 15
            self.base_defence = 27
            self.base_health = 75
            self.village_bonus = 5
            self.siege_bonus = -3
            self.anti_infantry_bonus = 2
            self.anti_cav_bonus = -3
            self.movement_type = 1
            self.banner = pygame.image.load("images/Bow.png")
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
        self.health = self.base_health
        self.hurt = 0
        self.rect = self.banner.get_rect(center=starting_rect)
        self.march = self.base_march
        self.last_rect = self.rect
        self.new_banner = self.banner
    def move_self(direction,armies,terrains,all_armies,texts):
        enemy_armies = all_armies.copy()
        for arm in armies:
            enemy_armies.remove(arm)
        for arm in armies:
            print(arm.selected)
            arm.direction = direction
            armies_testing = armies.copy()
            armies_testing.remove(arm)
            can_move = None
            if arm.march >= 0.5 and arm.selected:
                if arm.direction == Direction.UP:
                    arm.rect.move_ip(0,-32)
                if arm.direction == Direction.BOTTOM:
                    arm.rect.move_ip(0,32)
                if arm.direction == Direction.LEFT:
                    arm.rect.move_ip(-32,0)
                if arm.direction == Direction.RIGHT:
                    arm.rect.move_ip(32,0)
                collision = pygame.sprite.spritecollideany(arm,armies_testing)
                collision_enemy = pygame.sprite.spritecollideany(arm,enemy_armies)
                collision_terrain = pygame.sprite.spritecollideany(arm,terrains)
                if collision is None:
                    if collision_terrain is not None:
                        if collision_terrain.move_type == arm.movement_type:
                            arm.march -= collision_terrain.movement_cost
                            if arm.march < 0:
                                can_move = False
                                Text.add_text(texts,"Not enough movement")
                            else:
                                can_move = True
                        else:
                            can_move = False
                    else:
                        if arm.march >= 1:
                            arm.march -= 1
                            can_move = True
                        else:
                            can_move = False
                            #"""
                if collision_enemy is not None:
                    battle = Unit.attack(arm,collision_enemy,texts)
                    if battle:
                        can_move = True
                    else:
                        can_move = False
                        #"""
                if arm.rect.top <0 or arm.rect.top >= 800:
                    can_move = False
                if arm.rect.left <0 or arm.rect.left >= 800:
                    can_move = False
                if can_move == False:
                    if arm.direction == Direction.UP:
                        arm.rect.move_ip(0,32)
                    if arm.direction == Direction.BOTTOM:
                        arm.rect.move_ip(0,-32)
                    if arm.direction == Direction.LEFT:
                        arm.rect.move_ip(32,0)
                    if arm.direction == Direction.RIGHT:
                        arm.rect.move_ip(-32,0)
                    if collision_terrain is not None:
                        if collision_terrain.move_type == arm.movement_type:
                            arm.march += collision_terrain.movement_cost
                    else:
                        arm.march += 1
                Text.add_text(texts,f"Movement left: {arm.march}")
                armies_testing.empty()
    def selection(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True
        print(self.selected)
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
    def conscript(type,owner,starting_rect,normal_hire):
        player = owner
        constription_possible = None
        if normal_hire == True: #Normal hire is units that cost, if False units will be free
            if type == 1:
                if player.gold >= 3 and player.food >= 7 and player.spear >= 4:
                    player.gold -= 3
                    player.food -= 7
                    player.spear -= 4
                    constription_possible == True
                else:
                    constription_possible == False
            elif type == 2:
                if player.gold >= 5 and player.food >= 7 and player.bow >= 4 and player.lumber >= 1:
                    player.gold -= 5
                    player.food -= 7
                    player.bow -= 4
                    player.lumber -= 1
                    constription_possible == True
                else:
                    constription_possible == False
            elif type == 3:
                if player.gold >= 10 and player.food >= 10 and player.spear >= 2:
                    player.gold -= 10
                    player.food -= 10
                    player.spear -= 2
                    constription_possible == True
                else:
                    constription_possible == False
            elif type == 4:
                if player.gold >= 15 and player.food >= 3 and player.lumber >= 10:
                    player.gold -= 15
                    player.food -= 3
                    player.lumber -= 10
                    constription_possible == True
                else:
                    constription_possible == False
            elif type == 100:
                if player.gold >= 10 and player.food >= 20 and player.lumber >= 20:
                    player.gold -= 10
                    player.food -= 20
                    player.lumber -= 20
                    constription_possible == True
                else:
                    constription_possible == False
        else:
            constription_possible = True
        if constription_possible:
            new_army = Army(type,owner,starting_rect)
            #self.armies.append(new_army)
            return new_army

    def draw_armies(self,screen,armies): #DEPRACADED!
        for army in armies:
            screen.blit(self.banner, self.rect)