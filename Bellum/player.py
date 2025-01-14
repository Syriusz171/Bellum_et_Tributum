import pygame
#from config import Config
class Player(pygame.sprite.Sprite):
    def __init__(self,number,name):
        super(Player,self).__init__()
        self.number = number
        self.name = name
        self.lumber = 50
        self.food = 50
        self.spear = 0
        self.bow = 0
        self.gold = 5
        self.gold_handicap = 0
        self.absolute_p_lumber = 0
        self.p_lumber = 0
        self.p_food = 0
        self.p_spear = 0
        self.p_bow = 0
        self.p_gold = 0
        self.active = False
        self.armies = pygame.sprite.Group()
        self.villages = pygame.sprite.Group()
    def check_production(villages,players):
        Player.reset_production(players)
        for vil in villages:
            if vil.health < 0:
                if vil.p_food <0:
                    vil.owner.p_food += vil.p_food
            else:
                vil.owner.p_gold += vil.p_gold
                vil.owner.absolute_p_lumber += vil.p_lumber
                vil.owner.p_lumber += vil.p_lumber
                vil.owner.p_food += vil.p_food
                vil.owner.p_spear += vil.p_spear
                vil.owner.p_bow += vil.p_bow
    def collect_global(players):
        for self in players:
            if (self.lumber + self.p_lumber) < (self.p_bow * 1.05 + self.p_spear):
                self.lumber += self.absolute_p_lumber
            else:
             self.lumber += self.p_lumber
             self.spear += self.p_spear
             self.bow += self.p_bow
            self.food += self.p_food
            self.gold += self.p_gold
            if self.food < 0:
                self.food = 0
    def reset_production(players):
        for self in players:
            self.p_lumber = 0
            self.p_food = 0
            self.p_spear = 0
            self.p_bow = 0
            self.p_gold = 0
            self.absolute_p_lumber = 0
            self.p_gold += self.gold_handicap
    def get_armied(self,army):
        self.armies.add(army)
    def get_villaged(self,village):
        self.villages.add(village)
    def activate(self):
        if self.active:
            self.active = False
        else:
            self.active = True

                
