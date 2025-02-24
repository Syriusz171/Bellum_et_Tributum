import pygame
#from config import Config
class Player(pygame.sprite.Sprite):
    def __init__(self,number,name,AI=0):
        super(Player,self).__init__()
        self.number = number
        self.defeted = False
        self.name = name
        self.lumber = 50
        self.food = 50
        self.spear = 0
        self.bow = 0
        self.gold = 0
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
        self.is_AI = AI
    def check_production(villages,players):
        Player.reset_production(players)
        for vil in villages:
            if vil.health <= 0:
                vil.owner.p_food -= vil.food_usage
            else:
                if vil.owner.food < vil.food_usage:
                    efficiency = 0.5
                else:
                    efficiency = 1
                    vil.owner.p_gold += vil.tax
                vil.owner.p_gold += vil.p_gold * efficiency
                vil.owner.p_lumber += vil.p_lumber * efficiency
                vil.owner.p_food += vil.p_food * efficiency
                vil.owner.p_spear += vil.p_spear * efficiency
                vil.owner.p_bow += vil.p_bow * efficiency
                if vil.vill_type in [60,3]:
                    vil.owner.p_lumber -= vil.lumber_usage_for_spear
                if vil.vill_type in [4]:
                    vil.owner.p_lumber -= vil.lumber_usage_for_bow
                if vil.vill_type in [5,6]:
                    vil.owner.p_lumber -= vil.lumber_usage_for_mining
                vil.owner.p_food -= vil.food_usage
    def collect_global(players): #Derelict!
        for self in players:
            if self.lumber + self.p_lumber < (self.p_bow * 1.05 + self.p_spear):
                self.lumber += self.absolute_p_lumber
            else:
                self.lumber += self.p_lumber
                self.spear += self.p_spear
                self.bow += self.p_bow
            self.food += self.p_food
            self.gold += self.p_gold
            if self.food < 0:
                self.food = 0
    def mk2_collect_global(players):
        for self in players:
            if self.is_AI != 1:
                for vil in self.villages:
                    if vil.health > 0:
                        if self.food > 0:
                            efficiency = 1
                            self.gold += vil.tax
                        else:
                            efficiency = 0.5
                            if vil.vill_type == 60:
                                self.gold += 3
                        if vil.p_spear > 0:
                            if vil.lumber_usage_for_spear * efficiency <= self.lumber:
                                self.spear += vil.p_spear * efficiency
                                self.lumber -= vil.lumber_usage_for_spear * efficiency
                        if vil.p_bow > 0:
                            if vil.lumber_usage_for_bow * efficiency <= self.lumber:
                                self.bow += vil.p_bow * efficiency
                                self.lumber -= vil.lumber_usage_for_bow * efficiency
                        if vil.p_food > 0:
                            self.food += vil.p_food * efficiency
                        if vil.p_lumber > 0:
                            self.lumber += vil.p_lumber * efficiency
                        if vil.p_gold > 0:
                            if self.lumber >= vil.lumber_usage_for_mining * efficiency:
                                self.lumber -= vil.lumber_usage_for_mining * efficiency
                                self.gold += vil.p_gold *efficiency
                        self.food -= vil.food_usage
                            
                    else:
                        self.food -= vil.food_usage * 0.9
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

                
