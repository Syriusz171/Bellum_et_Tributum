import pygame
import random
class Terrain(pygame.sprite.Sprite):
    def __init__(self,form,starting_rect,generation=7) -> None:
        super().__init__()
        self.form = form
        self.generation = generation
        self.do_gen = True
        self.x = starting_rect[0]
        self.y = starting_rect[1]
        self.rect = pygame.Rect(starting_rect[0]+1,starting_rect[1],30,30)
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
        """
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
            return terrain_list"""
        if False:
            pass
        elif type=="flats":
            change_needed = True
            terrain_list = pygame.sprite.Group()
            for i in range(25):
                for j in range(25):
                    location = (i*32,j*32+2)
                    number = random.randint(1,100)
                    if j == 12 and i == 12:
                        new_terrain = Terrain(4,location)
                        terrain_list.add(new_terrain)
                    else:
                        if number < 62:
                            new_terrain = None
                        elif number < 76:
                            new_terrain = Terrain(1,location,5)
                        elif number < 89:
                            new_terrain = Terrain(2,location,5)
                        elif number >= 93:
                            new_terrain = Terrain(3,location,5)
                        if new_terrain is not None:
                            terrain_list.add(new_terrain)
            terrain_list_neo = terrain_list.copy()
            while change_needed:
                if len(terrain_list_neo) == 0:
                    change_needed = False
                for ter in terrain_list_neo:
                    if ter.do_gen and ter.form != 3 and ter.form != 20 and ter.form != 4:
                        neo_terrain = None
                        #Check
                        if ter.check_gen(terrain_list,0,32):
                            neo_terrain = Terrain(ter.form,(ter.x,ter.rect.y+32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,-32,0):
                            neo_terrain = Terrain(ter.form,(ter.x-32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,32,0):
                            neo_terrain = Terrain(ter.form,(ter.x+32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,0,-32):
                            neo_terrain = Terrain(ter.form,(ter.x,ter.y-32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                    ter.gen = False
                    terrain_list_neo.remove(ter)
            return terrain_list
        elif type=="track":
            change_needed = True
            terrain_list = pygame.sprite.Group()
            for i in range(25):
                for j in range(25):
                    location = (i*32-1,j*32+2)
                    number = random.randint(1,100)
                    if i == 12:
                        new_terrain = Terrain(20,location)
                        terrain_list.add(new_terrain)
                    else:
                        if number < 62:
                            new_terrain = None
                        elif number < 69:
                            new_terrain = Terrain(4,location,3)
                        elif number < 79:
                            new_terrain = Terrain(1,location,3)
                        elif number < 90:
                            new_terrain = Terrain(2,location,3)
                        elif number >= 90:
                            new_terrain = Terrain(3,location,3)
                        if new_terrain is not None:
                            terrain_list.add(new_terrain)
            terrain_list_neo = terrain_list.copy()
            while change_needed:
                if len(terrain_list_neo) == 0:
                    change_needed = False
                for ter in terrain_list_neo:
                    if ter.do_gen and ter.form != 3 and ter.form != 20:
                        neo_terrain = None
                        #Check
                        if ter.check_gen(terrain_list,0,32):
                            neo_terrain = Terrain(ter.form,(ter.x,ter.rect.y+32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,-32,0):
                            neo_terrain = Terrain(ter.form,(ter.x-32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,32,0):
                            neo_terrain = Terrain(ter.form,(ter.x+32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,0,-32):
                            neo_terrain = Terrain(ter.form,(ter.x,ter.y-32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                    ter.gen = False
                    terrain_list_neo.remove(ter)
            return terrain_list
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
            return terrain_list
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
        elif type=="better_gen": #Mk2 generation 8I2025
            change_needed = True
            for i in range(25):
                for j in range(25):
                    location = (i*32-1,j*32+2)
                    number = random.randint(1,100)
                    if number < 70:
                        new_terrain = None
                    elif number < 76:
                        new_terrain = Terrain(4,location,3)
                    elif number < 84:
                        new_terrain = Terrain(1,location,3)
                    elif number < 93:
                        new_terrain = Terrain(2,location,3)
                    elif number >= 93:
                        new_terrain = Terrain(3,location,3)
                    if new_terrain is not None:
                        terrain_list.add(new_terrain)
            terrain_list_neo = terrain_list.copy()
            while change_needed:
                if len(terrain_list_neo) == 0:
                    change_needed = False
                for ter in terrain_list_neo:
                    if ter.do_gen and ter.form != 3 and ter.form != 20:
                        neo_terrain = None
                        #Check
                        if ter.check_gen(terrain_list,0,32):
                            neo_terrain = Terrain(ter.form,(ter.x,ter.rect.y+32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,-32,0):
                            neo_terrain = Terrain(ter.form,(ter.x-32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,32,0):
                            neo_terrain = Terrain(ter.form,(ter.x+32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,0,-32):
                            neo_terrain = Terrain(ter.form,(ter.x,ter.y-32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                    ter.gen = False
                    terrain_list_neo.remove(ter)
            return terrain_list
        elif type=="test":
            change_needed = True
            new_terrain = Terrain(4,(12*32-2,12*32),-1.2)
            if new_terrain is not None:
                terrain_list.add(new_terrain)
            terrain_list_neo = terrain_list.copy()
            while change_needed:
                if len(terrain_list_neo) == 0:
                    change_needed = False
                for ter in terrain_list_neo:
                    if ter.do_gen and ter.form != 3 and ter.form != 20:
                        neo_terrain = None
                        #Check
                        if ter.check_gen(terrain_list,0,32):
                            neo_terrain = Terrain(ter.form,(ter.x,ter.rect.y+32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,-32,0):
                            neo_terrain = Terrain(ter.form,(ter.x-32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,32,0):
                            neo_terrain = Terrain(ter.form,(ter.x+32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,0,-32):
                            neo_terrain = Terrain(ter.form,(ter.x,ter.y-32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        #Generation
                    ter.gen = False
                    terrain_list_neo.remove(ter)
            return terrain_list
    def check_gen(self,terrains,x_change,y_change):
        if (0 > self.x+x_change or self.x+x_change > 780 or 0 > self.y+y_change or self.y+y_change > 800):
            return False
        for j in terrains:
            if j.rect.colliderect((self.x+x_change,self.y+y_change+3,16,16)):
                return False
        if random.randint(1,100+self.generation*60) <= 100:
            return True
        else:
            return False
