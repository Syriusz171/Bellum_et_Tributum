import pygame
from player import Player
import random
from army import Army
from unit import Unit
from Direction import Direction
from kliczek import Kliczek
from terrain import Terrain
from button import Button
from village import Village
from turn import Turn
from text import Text
WIDHT = 839
HEIGHT = 800
game_on = True
screen = pygame.display.set_mode([WIDHT,HEIGHT])
pygame.display.set_caption("Bellum, Bellum dev -1.0")
pygame.init()
FPS = pygame.time.Clock()
background_image = pygame.image.load("images/Background.png")
background_image2 = pygame.image.load("images/Bellum_menu.png")
player1 = Player(1,"Player1")
player2 = Player(2,"Player2")
font = pygame.font.SysFont("Times New Roman",20)
texts = pygame.sprite.Group()
Text.init_texts(texts)
version = font.render("version: dev -1.0",False,(160,200,200))
#army = Army(2,1)
buttons = pygame.sprite.Group()
start_quick = Button(1,(12*32+16,12*32+18),True)
show_production = Button(2,(819,740),False)
keys_button = Button(3,(819,740),True)
flats_button = Button(12,(14*32+16,10*32+18),False)
track_map_button = Button(11,(14*32+16,14*32+18),False)
small_input = Button(1,(12*32+16,12*32+18),False)
buttons.add(start_quick)
buttons.add(show_production)
buttons.add(keys_button)
buttons.add(flats_button)
buttons.add(track_map_button)
buttons.add(small_input)
do_input = False
special_input = None
input_text = 'Player1'
kliczek = Kliczek()
armies = pygame.sprite.Group()
#----
villages = pygame.sprite.Group()
#----
armies_ = pygame.sprite.Group()   #armies_ is sprites that belong to the player that has a turn now
def start():
    army1 = Army.conscript(100,player2,(12*32+16,10*32+19),False)
    #armies1 = pygame.sprite.Group()
    #armies1.add(army1)
    army2 = Army.conscript(3,player1,(13*32+16,9*32+19),False)
    #armies2 = pygame.sprite.Group()
    #armies2.add(army1)
    player1.get_armied(army2)
    player2.get_armied(army1)
    armies.add(army1)
    armies.add(army2)
    city1 = Village.locate_village(60,player1,(22*32+16,12*32+16),True)
    city2 = Village.locate_village(60,player2,(2*32+16,12*32+16),True)
    print(city1)
    villages.add(city1)
    villages.add(city2)
    player1.get_villaged(city1)
    player2.get_villaged(city2)
    player1.name = input_text
    print(player1.name)
    for arm in player1.armies:
        armies_.add(arm)
    Text.add_text(texts,(f"{player1.name} turn"))
# ------------------ Terrain
terrains = Terrain.generate("Start_menu")
#-------------------
REAL_show_production = False
menu = 1
selected_village_type = 0
#
players = pygame.sprite.Group()
players.add(player1)
players.add(player2)
player1.activate()
#(12*32+16,12*32+18)
quick_text = font.render("Start",False,(35,35,36))
REFRESH = pygame.USEREVENT + 1
pygame.time.set_timer(REFRESH,5000)
while game_on:
    """
    while menu == 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_on = False
            elif event.type == pygame.QUIT:
                game_on = False
            elif event.type == pygame.MOUSEBUTTONUP:
                print("Kliczek będzie wspaniały!")
                kliczek_collide = pygame.sprite.spritecollideany(kliczek,buttons)
                if kliczek_collide is not None:
                    if kliczek_collide.type == 1:
                        menu = 0
                        terrains.empty()
                        terrains = Terrain.generate("flats")
                        start_quick.activate_button(False)
                        show_production.activate_button(True)
        screen.blit(background_image2,(0,0))
        for b in buttons:
            if b.active:
                screen.blit(b.picture,b.rect)
        for ter in terrains:
            screen.blit(ter.look,ter.rect)
        pygame.display.flip()
        if game_on == False:
            break
        """
    mouse = pygame.mouse.get_pos()
    kliczek.move_kliczek(mouse)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_on = False
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if menu == 0:
                    armies_ = Turn.turn(players,armies,villages,texts)
                do_input = False
                special_input = 'return'
            elif event.key == pygame.K_a:
                Army.move_self(Direction.LEFT,armies_,terrains,armies,texts)
            elif event.key == pygame.K_d:
                Army.move_self(Direction.RIGHT,armies_,terrains,armies,texts)
            elif event.key == pygame.K_w:
                Army.move_self(Direction.UP,armies_,terrains,armies,texts) #Multi army movement 11 XII Anno Domeni 2024
            elif event.key == pygame.K_s:
                Army.move_self(Direction.BOTTOM,armies_,terrains,armies,texts)
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                Army.unselect(armies_,texts)
            elif event.key == pygame.K_BACKSPACE:
                if do_input:
                    special_input = 'backspace'
            elif event.key == pygame.K_SPACE:
                print(selected_village_type)
                for arm in armies_:
                    if arm.formation == 100 and arm.selected:
                        can_found_village = True
                        army_collide = pygame.sprite.spritecollideany(arm,villages)#Village foundation system 2I2025
                        army_terrain_collide = pygame.sprite.spritecollideany(arm,terrains)
                        if army_collide is None:
                            if selected_village_type != 0:
                                if army_terrain_collide is not None:
                                    if (selected_village_type == 1 and army_terrain_collide.form != 1) or (selected_village_type == 2 and army_terrain_collide.form != 2) or (selected_village_type == 5 and army_terrain_collide.form != 3):
                                        Text.add_text(texts,"Invalid terrain type! ")
                                        can_found_village = False
                                if can_found_village:
                                    new_village = Village.locate_village(selected_village_type,arm.owner,arm.rect.center)
                                    villages.add(new_village)
                                    arm.kill()
                                    Text.deactivate_text(texts,"vill_type")
                        else:
                            Text.add_text(texts,"Cannot stack villages!")
            #=====================================================#
            elif event.key == pygame.K_c:
                selected_village_type = 0
                Text.deactivate_text(texts,"vill_type")
            elif event.key == pygame.K_1:
                selected_village_type = 1
            elif event.key == pygame.K_2:
                selected_village_type = 2
            elif event.key == pygame.K_3:
                selected_village_type = 3
            elif event.key == pygame.K_4:
                selected_village_type = 4
            elif event.key == pygame.K_5:
                selected_village_type = 5
            if do_input:
                if special_input is None:
                    input_text += event.unicode
                elif special_input == 'backspace':
                    input_text = input_text[:-1]
                    print(type(input_text))
                elif special_input == 'return':
                    do_input = False
                special_input = None
        elif event.type == pygame.QUIT:
            game_on = False
        elif event.type == REFRESH:
            Player.check_production(villages,players)
        elif event.type == pygame.MOUSEBUTTONUP:
            kliczek_button = pygame.sprite.spritecollideany(kliczek,buttons)
            if kliczek_button is not None:
                if kliczek_button.type == 2 and menu == 0:
                    if REAL_show_production:
                        REAL_show_production = False
                    else:
                        REAL_show_production = True
                if kliczek_button.type == 2 and menu == 1:
                    Text.activate_text(texts,"keys")

                if kliczek_button.type == 1 and menu == 1:
                    if start_quick.active == False:
                        if small_input.active:
                            if do_input:
                                do_input = False
                            else:
                                do_input = True
                    start_quick.activate_button(False)
                    flats_button.activate_button(True)
                    track_map_button.activate_button(True)
                    small_input.activate_button(True)


                if kliczek_button.type == 11 or kliczek_button.type == 12 and menu == 1:
                    menu = 0
                    terrains.empty()
                    if kliczek_button.type == 12: #Map selection 3 I AD 2025 19:40
                        terrains = Terrain.generate("flats")
                    else:
                        terrains = Terrain.generate("track")
                    #start_quick.activate_button(False)
                    small_input.activate_button(False)
                    keys_button.activate_button(False)
                    show_production.activate_button(True)
                    flats_button.activate_button(False)
                    track_map_button.activate_button(False)
                    start()
                    Text.deactivate_text(texts,"keys")
            kliczek_collide = pygame.sprite.spritecollideany(kliczek,armies)
            if kliczek_collide is not None:
                kliczek_collide.selection()
                print(kliczek_collide.selected)
                if kliczek_collide.formation == 100:
                    Text.activate_text(texts,"vill_type")
                Text.add_text(texts,"Army selected")
    if menu != 1:
        screen.blit(background_image, (0,0))
    else:
        screen.blit(background_image2, (0,0))
    for ter in terrains:
        screen.blit(ter.look,ter.rect)
    for arm in armies:
        arm.update_color()
        screen.blit(arm.new_banner,arm.rect)
    for vil in villages:
        screen.blit(vil.banner,vil.rect)
    for b in buttons:
        if b.active:
            screen.blit(b.picture,b.rect)
    if start_quick.active:
        screen.blit(quick_text,(12*32,12*32+2))
    if small_input.active:
            input_text_render = font.render(input_text,True,(25,25,25),(181,123,76))
            screen.blit(input_text_render,(small_input.rect.left+8,small_input.rect.centery-10))
    if REAL_show_production:
        gold_text = font.render(f"Gold:{player1.gold}+{player1.p_gold};{player2.gold}+{player2.p_gold}",False,(160,200,200))
        lumber_text = font.render(f"Lumber:{player1.lumber}+{player1.p_lumber};{player2.lumber}+{player2.p_lumber}",False,(160,200,200))
        food_text = font.render(f"Food:{player1.food}+{player1.food};{player2.food}+{player2.p_food}",False,(160,200,200))
        spear_text = font.render(f"Sprears:{player1.spear}+{player1.p_spear};{player2.spear}+{player2.p_spear}",False,(160,200,200))
        bow_text = font.render(f"Bows:{player1.bow}+{player1.p_bow};{player2.bow}+{player2.p_bow}",False,(160,200,200))
        screen.blit(gold_text,(648,40))
        screen.blit(lumber_text,(648,60))
        screen.blit(food_text,(648,80))
        screen.blit(spear_text,(648,100))
        screen.blit(bow_text,(648,120))
    Text.print_text(texts,screen)
    kliczek.draw_kliczek(screen)
    if menu == 1:
        screen.blit(version,(661,750))

    pygame.display.flip()
    FPS.tick(40)