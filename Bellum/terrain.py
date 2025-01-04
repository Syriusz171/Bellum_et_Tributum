import pygame
import random
class Terrain(pygame.sprite.Sprite):
    def __init__(self,form,starting_rect) -> None:
        super().__init__()
        self.form = form
        self.rect = ((starting_rect),(32,31))
        #Move type 0 = impassable, 1 = land unit passable, 2 = water, 5 = mountain
        if self.form == 1: #Woods, good for lumberjacks
            self.movement_cost = 1.5
            self.move_type = 1
            self.look = pygame.image.load("images/woods.png")
        elif self.form == 2: # Fertile land, good for farms
            self.movement_cost = 1
            self.move_type = 1
            if random.randint(0,3) == 0:
                self.look = pygame.image.load("images/fertile_land.png")
            else:
                self.look = pygame.image.load("images/fertile_land2.png")
        elif self.form == 3: # Gold deposit, there is a lot of gold here
            self.movement_cost = 1
            self.move_type = 1
            self.look = pygame.image.load("images/gold_deposit.png")
        elif self.form == 4: # Mountain
            self.move_type = 5
            self.movement_cost = 2
            if random.randint(0,1) == 0:
                self.look = pygame.image.load("images/mountain1.png")
            else:
                self.look = pygame.image.load("images/mountain2.png")
        elif self.form == 20: #Road, player builded construction that allows you and your enemy to march faster
            self.movement_cost = 0.5
            self.move_type = 1
            random_a = random.randint(0,2)
            if random_a == 0:
                self.look = pygame.image.load("images/track_SN2.png")
            elif random_a == 1:
                self.look = pygame.image.load("images/track_SN.png")
            else:
                self.look = pygame.image.load("images/track_SN3.png")
    def generate(type):
        terrain_list = pygame.sprite.Group()
        if type == "flats":
            for i in range(25):
                for j in range(25):
                    location = (i*32,j*32+2)
                    number = random.randint(1,100)
                    if j == 12 and i == 12:
                        new_terrain = Terrain(4,location)
                    else:
                        if number < 30:
                            new_terrain = None
                        elif number < 65:
                            new_terrain = Terrain(1,location)
                        elif number < 95:
                            new_terrain = Terrain(2,location)
                        elif number >= 95:
                            new_terrain = Terrain(3,location)
                    if new_terrain is not None:
                        terrain_list.add(new_terrain)
        elif type == "track":
            for i in range(25):
                for j in range(25):
                    location = (i*32,j*32+2)
                    number = random.randint(1,100)
                    if i == 12:
                        new_terrain = Terrain(20,location)
                    else:
                        if number < 20:
                            new_terrain = None
                        elif number < 29:
                            new_terrain = Terrain(4,location)
                        elif number < 64:
                            new_terrain = Terrain(1,location)
                        elif number < 94:
                            new_terrain = Terrain(2,location)
                        elif number >= 94:
                            new_terrain = Terrain(3,location)
                    if new_terrain is not None:
                        terrain_list.add(new_terrain)
        elif type == "Start_menu":
            for i in range(6):
                for j in range(6):
                    location = (i*32,j*32+2)
                    number = random.randint(1,100)
                    if number < 20:
                        new_terrain = None
                    elif number < 29:
                        new_terrain = Terrain(4,location)
                    elif number < 64:
                        new_terrain = Terrain(1,location)
                    elif number < 94:
                        new_terrain = Terrain(2,location)
                    elif number >= 94:
                        new_terrain = Terrain(3,location)
                    if new_terrain is not None:
                        terrain_list.add(new_terrain)
        elif type=="deserted":
            for i in range(25):
                for j in range(25):
                    location = (i*32,j*32+2)
                    number = random.randint(1,100)
                    if number < 43:
                        new_terrain = None
                    elif number < 53:
                        new_terrain = Terrain(4,location)
                    elif number < 73:
                        new_terrain = Terrain(1,location)
                    elif number < 84:
                        new_terrain = Terrain(2,location)
                    elif number >= 84:
                        new_terrain = Terrain(3,location)
                    if new_terrain is not None:
                        terrain_list.add(new_terrain)
        return terrain_list
                        
