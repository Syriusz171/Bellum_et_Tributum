import pygame
from unit import Unit
#from copy import deepcopy
from player import Player
from text import Text
import army
import random
class Village(Unit,pygame.sprite.Sprite):
    def __init__(self,owner1,vill_type,starting_rect) -> None:   #if type is 60 village is a city, owner 0 is no one's villge
        super(Village,self).__init__()
        self.owner = owner1
        self.vill_type = vill_type
        self.selected = False
        self.can_conscript_turns = 4
        
        self.is_village = True

        self.tax = 0
        self.p_gold = 0
        self.p_spear = 0
        self.p_food = 0
        self.food_usage = 0
        self.p_bow = 0
        self.p_lumber = 0
        self.lumber_usage_for_spear = 0
        self.lumber_usage_for_bow = 0
        self.lumber_usage_for_mining = 0
        self.gold_usage = 0
        #self.rect = starting_rect.copy()
        if vill_type == 60:
            self.base_health = 225
            self.base_defence = 30
            self.tax = 5
            self.p_spear = 10
            self.food_usage = 3
            self.p_bow = 0
            self.lumber_usage_for_spear = 2
            self.banner = pygame.image.load("images/city.png")
        elif vill_type == 20:
            self.base_health = 60
            self.base_defence = 13.5
        elif vill_type == 30:
            self.base_health = 62
            self.base_defence = 15.5
            self.banner = pygame.image.load("images/bandit_camp.png")
        else:
            self.base_health = 33
            self.base_defence = 6
        if vill_type == 1:
            self.p_lumber = 5
            self.food_usage = 1
            self.tax = 0.1
            self.banner = pygame.image.load("images/village_lumber.png")
        if vill_type == 2:
            self.p_food = 6
            self.food_usage = 1
            self.tax = 0.1
            self.banner = pygame.image.load("images/village_food.png")
        if vill_type == 3:
            self.lumber_usage_for_spear = 1
            self.food_usage = 1
            self.tax = 0.15
            self.p_spear = 5
            self.banner = pygame.image.load("images/village_spear.png")
        elif vill_type == 4:
            self.lumber_usage_for_bow = 1.05
            self.food_usage = 1
            self.p_bow = 1
            self.tax = 0.15
            self.banner = pygame.image.load("images/village_bow.png")
        elif vill_type == 5:
            self.lumber_usage_for_mining = 1
            self.food_usage = 2
            self.p_gold = 10
            self.tax = 0.2
            self.banner = pygame.image.load("images/village_gold.png")
        elif vill_type == 6:
            self.lumber_usage_for_mining = 0.75
            self.food_usage = 1.15
            self.p_gold = 6
            self.tax = 0.15
            self.banner = pygame.image.load("images/village_salt.png")
        elif vill_type == 20:
            self.lumber_usage_for_bow = 0.525
            self.p_bow = 0.5
            self.lumber_usage_for_spear = 0.2
            self.p_spear = 1
            self.tax = 2.9
            self.food_usage = 2
            self.banner = pygame.image.load("images/port_town.png")
        self.health = self.base_health
        self.rect = self.banner.get_rect(bottomleft=starting_rect)
        self.x = starting_rect[0]
        self.y = starting_rect[1]
        self.new_banner = self.banner
        #TEMPORARY!
        self.anti_infantry_bonus = 0
        self.anti_cav_bonus = 0
        #===== AI =====#
        if self.owner.is_AI == 1 and self.vill_type != 60:
            self.base_health += 4
            self.base_defence += 2
            print(self.base_defence)
    def select_village(self,villages,texts):
        for vil in villages:
            vil.selected = False
        if self.selected:
            self.selected = False
            Text.add_text(texts,"Village unselected!")
        else:
            self.selected = True
            Text.add_text(texts,"Village selected!")
    def unselect_villages(villages,texts):
        Text.add_text(texts,"All villages unselected!")
        for vil in villages:
            vil.selected = False
        
    def locate_village(type,owner,starting_rect,free_location=False,texts=None):
        player = owner
        location_possible = False
        new_village = None
        if free_location == False:
            if type in [2,3,4]:
                if player.gold >= 2 and player.lumber >= 5:
                    location_possible = True
                    player.gold -= 2
                    player.lumber -= 5
                else:
                    if texts is not None:
                        Text.add_text(texts,"Our stocks are too low!")
            elif type == 1:
                if player.gold >= 3:
                    location_possible = True
                    player.gold -= 3
                else:
                    if texts is not None:
                        Text.add_text(texts,"Our stocks are too low!")
            elif type == 5:
                if player.gold >= 10 and player.lumber >= 8 and player.food >= 1:
                    player.gold -= 10
                    player.lumber -= 8
                    player.food -= 1
                    location_possible = True
                else:
                    if texts is not None:
                        Text.add_text(texts,"Our stocks are too low!")
            elif type == 6:
                if player.gold >= 4 and player.lumber >= 6 and player.food >= 1:
                    player.gold -= 4
                    player.lumber -= 6
                    player.food -= 1
                    location_possible = True
                else:
                    if texts is not None:
                        Text.add_text(texts,"Our stocks are too low!")
            elif type == 20:
                if player.gold >= 40 and player.lumber >= 22 and player.food >= 10:
                    player.gold -= 40
                    player.lumber -= 22
                    player.food -= 10
                    location_possible = True
                else:
                    if texts is not None:
                        Text.add_text(texts,"Our stocks are too low!")
        else:
            location_possible = True
        if location_possible:
            if texts is not None:
                Text.add_text(texts,"Village_founded!")
            new_village = Village(owner,type,starting_rect)
            return new_village
                
    """
    def check_production_global(villages,players):
        for p in players:
            p.reset_production
        for vil in villages:
            vil.owner.p_gold += vil.p_gold
            vil.owner.p_lumber += vil.p_lumber
            vil.owner.p_food += vil.p_food
            vil.owner.p_spear += vil.p_spear
            vil.owner.p_bow += vil.p_bow"""
    def turns_left_change(villages):
        for vil in villages:
            if vil.can_conscript_turns > 0:
                vil.can_conscript_turns -= 1
    def change_owner(self,new_owner,texts):
        self.owner.villages.remove(self)
        self.owner = new_owner
        new_owner.get_villaged(self)
        Text.add_text(texts,f"Village conquered by {new_owner.name}!")
                                