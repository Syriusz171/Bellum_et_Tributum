import pygame
import random
from maps import yorktown, bastion
class Terrain(pygame.sprite.Sprite):
    def __init__(self,form,starting_rect,generation=7,fixed_texture=None,owner=None) -> None:
        super().__init__()
        self.form = form
        self.generation = generation
        self.do_gen = True
        self.x = starting_rect[0]
        self.y = starting_rect[1]
        self.rect = pygame.Rect(starting_rect[0]+1,starting_rect[1],30,30)
        
        self.owner = owner
        #Move type 0 = impassable, 1 = land unit passable, 2 = water, 5 = mountain
        if self.form == 1: #Woods, good for lumberjacks
            self.movement_cost = 1.5
            self.move_type = 1
            self.look = pygame.image.load("images/woods.png")
        elif self.form == 2: # Fertile land, good for farms
            self.movement_cost = 1
            self.move_type = 1
            if fixed_texture is None:
                if random.randint(0,3) == 0:
                    self.look = pygame.image.load("images/fertile_land.png")
                else:
                    self.look = pygame.image.load("images/fertile_land2.png")
            elif fixed_texture == 2.5:
                self.look = pygame.image.load("images/fertile_land2.png")
            else:
                self.look = pygame.image.load("images/fertile_land.png")
        elif self.form == 3: # Gold deposit, there is a lot of gold here
            self.movement_cost = 1
            self.move_type = 1
            self.look = pygame.image.load("images/gold_deposit.png")
        elif self.form == 4: # Mountain
            self.move_type = 5
            self.movement_cost = 3.5
            if random.randint(0,1) == 0:
                self.look = pygame.image.load("images/mountain1.png")
            else:
                self.look = pygame.image.load("images/mountain2.png")
        elif self.form == 5:
            self.movement_cost = 1
            self.move_type = 1
            self.look = pygame.image.load("images/salt_deposit.png")
        elif self.form == 10:
            self.movement_cost = 1
            self.move_type = 2
            random_int = random.randint(0,1)
            if random_int == 0:
                self.look1 = pygame.image.load("images/water1.png")
            elif random_int == 1:
                self.look1 = pygame.image.load("images/water2.png")
            random_int = random.randint(0,1)
            if random_int != 1:
                self.look = pygame.transform.rotate(self.look1,90)
            else:
                self.look = self.look1
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
        elif self.form == 40:
            self.movement_cost = 5
            self.move_type = 6
            self.look = pygame.image.load("images/mountain_high.png")
        elif self.form == 41:
            self.movement_cost = 4
            self.move_type = 6
            self.look = pygame.image.load("images/enemy_spawn_tile.png")
        elif self.form == 101:
            self.movement_cost = 1.5
            self.move_type = 2
            self.look = pygame.image.load("images/water_rocks1.png")
        elif self.form == 190:
            self.movement_cost = 1
            self.move_type = 1
            self.look = pygame.image.load("images/island_sand1.png")
        #self.rect = self.look.get_rect(bottomleft=starting_rect)
    def generate(type,map_name = None):
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
            new_terrain = None
            for i in range(25):
                for j in range(25):
                    location = (i*32,j*32+2)
                    number = random.randint(1,100)
                    if j == 12 and i == 12:
                        new_terrain = Terrain(4,location)
                        terrain_list.add(new_terrain)
                    else:
                        if number < 60:
                            new_terrain = None
                        elif number < 74:
                            new_terrain = Terrain(1,location,5)
                        elif number < 87:
                            new_terrain = Terrain(2,location,5)
                        else:
                            if random.randint(1,13) <= 2:
                                new_terrain = Terrain(3,location,5)
                            else:
                                new_terrain = Terrain(5,location,5)
                        if new_terrain is not None:
                            terrain_list.add(new_terrain)
            terrain_list_neo = terrain_list.copy()
            while change_needed:
                if len(terrain_list_neo) == 0:
                    change_needed = False
                for ter in terrain_list_neo:
                    if ter.do_gen and ter.form != 3 and ter.form != 20 and ter.form != 4 and ter.form != 5:
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
                            if random.randint(1,13) <= 2:
                                new_terrain = Terrain(3,location,3)
                            else:
                             new_terrain = Terrain(5,location,3)
                        if new_terrain is not None:
                            terrain_list.add(new_terrain)
            terrain_list_neo = terrain_list.copy()
            while change_needed:
                if len(terrain_list_neo) == 0:
                    change_needed = False
                for ter in terrain_list_neo:
                    if ter.do_gen and ter.form != 3 and ter.form != 20 and ter.form != 5:
                        neo_terrain = None
                        #Check
                        form = ter.form
                        form = Terrain.similar_terrains_check(form)
                        if ter.check_gen(terrain_list,0,32):
                            neo_terrain = Terrain(form,(ter.x,ter.rect.y+32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,-32,0):
                            neo_terrain = Terrain(form,(ter.x-32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,32,0):
                            neo_terrain = Terrain(form,(ter.x+32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,0,-32):
                            neo_terrain = Terrain(form,(ter.x,ter.y-32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                    ter.gen = False
                    terrain_list_neo.remove(ter)
            return terrain_list

        elif type=="coast":
            change_needed = True
            terrain_list = pygame.sprite.Group()
            waters = pygame.sprite.Group()
            for a in range(4):
                new_terrain = Terrain(10,(12*32-1,(5+a)*32),0)
                terrain_list.add(new_terrain)
                waters.add(new_terrain)
            terrain_list_neo = terrain_list.copy()
            while change_needed:
                if len(terrain_list_neo) == 0:
                    change_needed = False
                for ter in terrain_list_neo:
                    if ter.do_gen:
                        neo_terrain = None
                        #Check
                        if ter.check_gen(terrain_list,0,32):
                            neo_terrain = Terrain(ter.form,(ter.x,ter.rect.y+32,32,32),ter.generation+0.5)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                            waters.add(neo_terrain)
                        if ter.check_gen(terrain_list,-32,0):
                            neo_terrain = Terrain(ter.form,(ter.x-32,ter.y,32,32),ter.generation+0.5)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                            waters.add(neo_terrain)
                        if ter.check_gen(terrain_list,32,0):
                            neo_terrain = Terrain(ter.form,(ter.x+32,ter.y,32,32),ter.generation+0.5)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                            waters.add(neo_terrain)
                        if ter.check_gen(terrain_list,0,-32):
                            neo_terrain = Terrain(ter.form,(ter.x,ter.y-32,32,32),ter.generation+0.5)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                            waters.add(neo_terrain)
                    ter.gen = False
                    terrain_list_neo.remove(ter)
                    #"""
            bingo = False
            for i in range(25):
                for j in range(25):
                    location = (i*32-1,j*32)
                    number = random.randint(1,100)
                    for terrain_checked in waters:
                        bingo = terrain_checked.rect.colliderect((location[0]+10,location[1]-10,16,16))
                        if bingo:
                            break
                    
                    if bingo == False:
                        if number < 61:
                            new_terrain = None
                        elif number < 68:
                            if random.randint(1,13) != 1:
                                new_terrain = Terrain(4,location,3)
                            else:
                                new_terrain = Terrain(40,location,2.9)
                        elif number < 78:
                            new_terrain = Terrain(1,location,3)
                        elif number < 89:
                            new_terrain = Terrain(2,location,3)
                        elif number <100:
                            if random.randint(1,13) <= 2:
                                new_terrain = Terrain(3,location,3)
                            else:
                                new_terrain = Terrain(5,location,3)
                        else:
                            new_terrain = Terrain(10,location,2.5)
                        if new_terrain is not None:
                            terrain_list.add(new_terrain)
            terrain_list_neo = terrain_list.copy()
            for water in waters:
                terrain_list_neo.remove(water)
            change_needed = True
            while change_needed:
                if len(terrain_list_neo) == 0:
                    change_needed = False
                for ter in terrain_list_neo:
                    if ter.do_gen and ter.form not in [3,5,20]:
                        neo_terrain = None
                        form = ter.form
                        form = Terrain.similar_terrains_check(form)
                        #Check
                        if ter.check_gen(terrain_list,0,32):
                            neo_terrain = Terrain(form,(ter.x,ter.rect.y+32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,-32,0):
                            neo_terrain = Terrain(form,(ter.x-32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,32,0):
                            neo_terrain = Terrain(form,(ter.x+32,ter.y,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                        if ter.check_gen(terrain_list,0,-32):
                            neo_terrain = Terrain(form,(ter.x,ter.y-32,32,32),ter.generation+1)
                            terrain_list.add(neo_terrain)
                            terrain_list_neo.add(neo_terrain)
                    ter.gen = False
                    terrain_list_neo.remove(ter)#"""
            for terrain in terrain_list:
                if terrain.form == 10:
                    if Terrain.seaRocks_check_coast(terrain.x,terrain.y,terrain_list):
                        Terrain.change_terrain_form(terrain,101,terrain_list)
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
                        if random.randint(1,13) <= 2:
                            new_terrain = Terrain(3,location)
                        else:
                            new_terrain = Terrain(5,location)
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
        elif type == "rich_center":
            terrain_list = pygame.sprite.Group()
            for i in range(25):
                for j in range(25):
                    new_terrain = None
                    location = (i*32,j*32+2)
                    number = random.randint(1,100)
                    if i in [3,21] and j != 12:
                        if number > 50:
                            new_terrain = Terrain(4,location)
                    elif i >= 9 and i <= 15:
                        if number < 46:
                            new_terrain = Terrain(1,location)
                        elif number < 90:
                            new_terrain = Terrain(2,location)
                        else:
                            if random.randint(1,13) <= 2:
                                new_terrain = Terrain(3,location)
                            else:
                                new_terrain = Terrain(5,location)
                    elif i in [0,1,23,24] and j == 12:
                        new_terrain = Terrain(2,location)
                    if new_terrain is not None:
                        terrain_list.add(new_terrain)
            return terrain_list
        elif type == "manual":
            returned = Terrain.get_map(map_name)
            villages = returned[1]
            map_terrain = returned[0]
            armies = returned[2]
            terrain_list = pygame.sprite.Group()
            for a in range(25):
                for b in range(25):
                    location = (a*32-1,b*32)
                    if map_terrain[b][a] == 0:
                        new_terrain = None
                    elif map_terrain[b][a] in [2.5,2.6]:
                        new_terrain = Terrain(2,location,1,map_terrain[b][a])
                    elif int(map_terrain[b][a]) > 410:
                        new_terrain = Terrain(41,location,owner=map_terrain[b][a])
                    else:
                        new_terrain = Terrain(map_terrain[b][a],location)
                    if new_terrain is not None:
                        terrain_list.add(new_terrain)
            return [terrain_list, villages, armies]
                    
            
            # FINISH IT
    def check_gen(self,terrains,x_change,y_change):
        if (0 > self.x+x_change or self.x+x_change > 780 or -10 > self.y+y_change or self.y+y_change > 800):
            return False
        for j in terrains:
            if j.rect.colliderect((self.x+x_change,self.y+y_change+3,16,16)):
                return False
        if random.randint(1,100+int(self.generation)*60) <= 100:
            return True
        else:
            return False
    def check_for_water(x,y,terrains):
        for ter in terrains:
            if ter.rect.colliderect((x+32,y,19,19)):
                if ter.move_type == 2:
                    return True
            elif ter.rect.colliderect((x-32,y,19,19)):
                if ter.move_type == 2:
                    return True
            elif ter.rect.colliderect((x,y+32,19,19)):
                if ter.move_type == 2:
                    return True
            elif ter.rect.colliderect((x,y-32,19,19)):
                if ter.move_type == 2:
                    return True
        return False
            

    def get_map(name):
        name = name.lower()
        if name == "yorktown":
            map_terrain_data = yorktown.terrain_map
            map_village_data = yorktown.villages
            map_army_data = yorktown.armies
        elif name == "bastion":
            map_terrain_data = bastion.terrain_map
            map_village_data = bastion.villages
            map_army_data = bastion.armies
        return [map_terrain_data, map_village_data, map_army_data]
    def similar_terrains_check(terrain):
        if terrain in [4,40]:
            if random.randint(1,13) == 1:
                return 40
            else:
                return 4
        else:
            return terrain
    def seaRocks_check_coast(x,y,terrains):
        collider_east = None
        collider_north = None
        collider_south = None
        collider_west = None
        chance = 0
        for terr in terrains:
            collision_south = terr.rect.collidepoint(x,y+16)
            if collision_south:
                if terr.move_type != 2:
                    collider_south = terr
                    if terr.move_type != 1:
                        chance =+ 2
                    continue           
            collision_north = terr.rect.collidepoint(x,y-16)
            if collision_north:
                if terr.move_type != 2:
                    collider_north = terr
                    if terr.move_type != 1:
                        chance =+ 2
                    continue
            collision_east = terr.rect.collidepoint(x+16,y)
            if collision_east:
                if terr.move_type != 2:
                    collider_east = terr
                    if terr.move_type != 1:
                        chance =+ 2
                    continue
            collision_west = terr.rect.collidepoint(x-16,y)
            if collision_west:
                if terr.move_type != 2:
                    collider_west = terr
                    if terr.move_type != 1:
                        chance =+ 2
        if (collider_west is not None or collider_east is not None or collider_north is not None or collider_south is not None) and chance != 8:
            if random.randint(1,12+chance) >= 12:
                return True
        return False 
    def change_terrain_form(terrain,new_type,terrains):
        x = terrain.x
        y = terrain.y
        terrain.kill()
        new_terrain = Terrain(new_type,(x,y))
        terrains.add(new_terrain)
