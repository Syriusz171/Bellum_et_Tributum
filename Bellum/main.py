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
from config import Config
from particle import Particle
import datetime
WIDHT = 839
HEIGHT = 800
game_on = True
screen = pygame.display.set_mode([WIDHT,HEIGHT])
config = Config()
pygame.display.set_caption("Bellum et Tributum Dev -0.9 Build 4")
icon_of_BeT = pygame.image.load("images/city.png")
pygame.display.set_icon(icon_of_BeT)
pygame.init()
FPS = pygame.time.Clock()
background_image = pygame.image.load("images/Background.png")
background_image2 = pygame.image.load("images/Bellum_menu_neo.png")
player1 = Player(1,"Player1")
player2 = Player(2,config.playerNr2Name)
font = pygame.font.SysFont("Times New Roman",20)
font_big = pygame.font.SysFont("Segoe Print Bold",36)
font_small = pygame.font.SysFont("Times New Roman",12)
texts = pygame.sprite.Group()
particles = pygame.sprite.Group()
Text.init_texts(texts)
version = font.render("version: Dev -0.9 Build 4",False,(160,200,200))
#army = Army(2,1)
visible_village_owner = False
visible_army_owner = True
enable_alpinist = True
buttons = pygame.sprite.Group()
map_buttons = pygame.sprite.Group()
start_quick = Button(1,(12*32+16,12*32+18),True)
show_production = Button(2,(819,740),False)
keys_button = Button(3,(819,740),True)
flats_button = Button(12,(14*32+16,10*32+18),False)
track_map_button = Button(11,(14*32+16,14*32+18),False)
rich_center_button = Button(13,(18*32+16,10*32+18),False)
small_input = Button(1,(12*32+16,12*32+18),False)
handicap1 = Button(5,(22*32+16,12*32+18),False)
handicap2 = Button(6,(2*32+16,12*32+18),False)
alpinist_off = Button(400,(17*32+1,12*32+16),False)
generate_map = Button(20,(20*32+1,12*32+16),False)
yorktown_map = Button(15,(18*32+16,14*32+18),False)
map_buttons.add(yorktown_map)
buttons.add(yorktown_map)
if config.developer_mode:
    test_map_button = Button(14,(8*32+16,3*32+18),False)
    buttons.add(test_map_button)
    map_buttons.add(test_map_button)
buttons.add(generate_map)
buttons.add(start_quick)
buttons.add(alpinist_off)
buttons.add(show_production)
buttons.add(keys_button)
buttons.add(flats_button)
buttons.add(track_map_button)
buttons.add(small_input)
buttons.add(handicap2)
buttons.add(handicap1)
buttons.add(rich_center_button)
do_input = False
special_input = None
input_text = 'Player1'
map = None
gen_button_text = font.render("Begin",False,(35,35,36))
was_defeated = False
kliczek = Kliczek()
armies = pygame.sprite.Group()
#----
villages = pygame.sprite.Group()
villages_ = pygame.sprite.Group()
#----
date_of_today = datetime.datetime.now()
armies_ = pygame.sprite.Group()   #armies_ is sprites that belong to the player that has a turn now
def start(bonus_starting_gold,modes,map,map_name=None):
    #===== AI TEST =====#
    player2.is_AI = config.playerNr2AI
    if map_name in ["yorktown"]:
        if date_of_today.month == 4 and date_of_today.day == 1 or config.force_jokes:
            player_bandit = Player(3,"Germans")
        else:
            player_bandit = Player(3,"Bandits")
        player_bandit.is_AI = True
        players.add(player_bandit)
    if map != "manual":
        terrains = Terrain.generate(map)
    else:
        return_list = Terrain.generate(map,map_name)
        villages_return = return_list[1]
        terrains = return_list[0]
        armies_return = return_list[2]
        for vil in villages_return:
            if vil[3] == 1:
                owner = player1
            elif vil[3] == 2:
                owner = player2
            elif vil[3] == 3:
                owner = player_bandit
            if len(vil) > 4:
                if vil[4]:
                    only_for_AnI = True
                else:
                    only_for_AnI = False
            else:
                only_for_AnI = False
            if owner.is_AI == False and only_for_AnI:
                pass
            else:
                village = Village.locate_village(vil[2],owner,(vil[0]*32,vil[1]*32+32),True)
                villages.add(village)
                owner.get_villaged(village)
        for arm in armies_return:
            if arm[3] == 1:
                owner = player1
            elif arm[3] == 2:
                owner = player2
            elif arm[3] == 3:
                owner = player_bandit
            if len(arm) > 4:
                if arm[4]:
                    only_for_AnI = True
                else:
                    only_for_AnI = False
            else:
                only_for_AnI = False
            if owner.is_AI == False and only_for_AnI:
                pass
            else:
                army = Army.conscript(arm[2],owner,(arm[0]*32,arm[1]*32+32),False)
                armies.add(army)
                owner.get_armied(army)
    for mode in modes:
        if mode =="Dev":
            army = Army.conscript(201,player1,(13*32,7*32),False,texts)
            armies.add(army)
            player1.get_armied(army)
            army = Army.conscript(201,player2,(11*32,7*32),False,texts)
            armies.add(army)
            player2.get_armied(army)
    for p in players:
        p.gold += bonus_starting_gold
    if map != "manual":
        army1 = Army.conscript(0,player2,(2*32,13*32),False,texts)
        #armies1 = pygame.sprite.Group()
        #armies1.add(army1)
        army2 = Army.conscript(0,player1,(22*32,13*32),False,texts)
        print(army1.x/32,army1.y/32,army2.x/32,army2.y/32)
        #armies2 = pygame.sprite.Group()
        #armies2.add(army1)
        player1.get_armied(army2)
        player2.get_armied(army1)
        armies.add(army1)
        armies.add(army2)
        city1 = Village.locate_village(60,player1,(22*32,13*32),True)
        city2 = Village.locate_village(60,player2,(2*32,13*32),True)
        collider3 = pygame.sprite.spritecollideany(city1,terrains)
        if collider3 is not None:
            collider3.kill()
        collider1 = pygame.sprite.spritecollideany(city2,terrains)
        if collider1 is not None:
            collider1.kill()
        #===== AI bonus =====#
        if player2.is_AI:
            village = Village.locate_village(3,player2,(10*32,14*32),True)
            player2.get_villaged(village)
            villages.add(village)
            collision = pygame.sprite.spritecollideany(village,terrains)
            if collision is not None:
                collision.kill()
            village = Village.locate_village(3,player2,(2*32,12*32),True)
            player2.get_villaged(village)
            villages.add(village)
            collision = pygame.sprite.spritecollideany(village,terrains)
            if collision is not None:
                collision.kill()
            village = Village.locate_village(3,player2,(1*32,12*32),True)
            player2.get_villaged(village)
            villages.add(village)
            collision = pygame.sprite.spritecollideany(village,terrains)
            if collision is not None:
                collision.kill()
            village = Village.locate_village(3,player2,(10*32,15*32),True)
            player2.get_villaged(village)
            villages.add(village)
            collision = pygame.sprite.spritecollideany(village,terrains)
            if collision is not None:
                collision.kill()
            army = Army.conscript(1,player2,(10*32,14*32),False,texts,True)
            player2.get_armied(army)
            armies.add(army)
            army = Army.conscript(1,player2,(2*32,12*32),False,texts,is_defending=True)
            player2.get_armied(army)
            armies.add(army)
            
        print(city1)
        villages.add(city1)
        villages.add(city2)
        player1.get_villaged(city1)
        player2.get_villaged(city2)
    player1.name = input_text
    print(player1.name)
    for arm in player1.armies:
        armies_.add(arm)
    for vil in player1.villages:
        villages_.add(vil)
    Text.add_text(texts,(f"{player1.name} turn"))
    return terrains
# ------------------ Terrain
terrains = Terrain.generate("Start_menu")
#-------------------
show_selected = False
#--------------------
REAL_show_production = False
menu = 1
selected_type = 0
spawn_type = 0
#
players = pygame.sprite.Group()
players.add(player1)
players.add(player2)
player1.activate()
#(12*32+16,12*32+18)
quick_text = font.render("Start",False,(35,35,36))
REFRESH = pygame.USEREVENT + 1
CHECK_VICTORY = pygame.USEREVENT + 2
pygame.time.set_timer(CHECK_VICTORY,2500)
pygame.time.set_timer(REFRESH,400)
game_turn = 1
while game_on:
    """
                print("Kliczek będzie wspaniały!")
        """
    mouse = pygame.mouse.get_pos()
    kliczek.move_kliczek(mouse)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_on = False
                #========================TURN========================#
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if menu == 0:
                    particles.empty()
                    turn_return = Turn.turn(players,armies,villages,texts,terrains,particles,config,game_turn)
                    armies_ = turn_return[0]
                    villages_ = turn_return[1]
                    game_turn = turn_return[2]
                    selected_type = 0
                    not_boated = armies.copy()
                    for arm in armies:
                        armies1 = armies.copy()
                        armies1.remove(arm)
                        if arm.is_boat and arm.formation not in [201,202,203]:
                            arm.is_boat = False
                        elif arm.formation in [201,202,203]:
                            arm.units_boat.empty()
                            arm.is_boat = True
                            collision_during_turn = pygame.sprite.spritecollideany(arm,armies1)
                            if collision_during_turn is not None:
                                not_boated.remove(collision_during_turn)
                                arm.units_boat.add(not_boated)
                    for army in not_boated:
                        army.on_boat = False
                    Village.unselect_villages(villages,texts)
                    Text.deactivate_text(texts,"vill_type")
                    selected_type = 0
                    spawn_type = 0
                    show_selected = False
                do_input = False
                special_input = 'return'
                #====Moving====#
            elif event.key == pygame.K_a:
                #Army.move_self(Direction.LEFT,armies_,terrains,armies,texts,villages)
                Army.move_all(players,armies,villages,terrains,Direction.LEFT,texts)
            elif event.key == pygame.K_d:
                Army.move_all(players,armies,villages,terrains,Direction.RIGHT,texts)
            elif event.key == pygame.K_w:
                Army.move_all(players,armies,villages,terrains,Direction.UP,texts) #Multi army movement 11 XII Anno Domeni 2024
            elif event.key == pygame.K_s:
                Army.move_all(players,armies,villages,terrains,Direction.BOTTOM,texts)
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                Army.unselect(armies_,texts)
                Village.unselect_villages(villages,texts)
                #====End====#
            elif event.key == pygame.K_LEFT:
                selected_type -= 1
                if selected_type < 1:
                    selected_type = 8
            elif event.key == pygame.K_RIGHT:
                selected_type += 1
                if selected_type > 8:
                    selected_type = 1
            elif event.key == pygame.K_BACKSPACE:
                if do_input:

                    special_input = 'backspace'
            elif event.key == pygame.K_RSHIFT:
                for text in texts:
                    if text.type == "chat":
                        text.kill()
                Text.add_text(texts,"Chat cleared!")
            elif event.key == pygame.K_SPACE:
                print(selected_type)
                new_village = None
                #========Town founding=======#
                for arm in armies_:
                    if arm.formation == 100 and arm.selected:
                        can_found_village = True
                        army_collide = pygame.sprite.spritecollideany(arm,villages)#Village foundation system 2I2025
                        army_terrain_collide = pygame.sprite.spritecollideany(arm,terrains)
                        spawn_type = selected_type
                        if army_collide is None:
                            if selected_type != 0 and selected_type != 6:
                                #===== Port town =====#
                                if selected_type == 8:
                                    if Terrain.check_for_water(arm.rect.centerx,arm.rect.centery,terrains) == False:
                                        can_found_village = False
                                        Text.add_text(texts,"Must be build on coast! ")
                                if army_terrain_collide is not None:
                                    if selected_type == 1 and army_terrain_collide.form != 1 or (selected_type == 2 and army_terrain_collide.form != 2) or (selected_type == 5 and army_terrain_collide.form not in [3,5]) or (selected_type == 8 and army_terrain_collide.form in [2,5]) or army_terrain_collide.form in [10,11]:
                                        Text.add_text(texts,"Invalid terrain type! ")
                                        can_found_village = False
                                    elif selected_type == 5:
                                        if army_terrain_collide.form == 5:
                                            spawn_type = 6
                                        else:
                                            spawn_type = 5
                                elif selected_type in [1,2,5]:
                                    can_found_village = False
                                if selected_type == 8:
                                    spawn_type = 20
                                if can_found_village:
                                    new_village = Village.locate_village(spawn_type,arm.owner,arm.rect.bottomleft,False,texts)
                                    if new_village is not None:
                                        villages.add(new_village)
                                        villages_.add(new_village)
                                        Player.get_villaged(arm.owner,new_village)
                                        arm.kill()
                                        Text.deactivate_text(texts,"vill_type")
                        else:
                            Text.add_text(texts,"Cannot stack villages!")
                for vil in villages_:
                    new_army = None
                    if vil.selected:
                        village_collision = pygame.sprite.spritecollideany(vil,armies)
                        if village_collision is None:
                            if selected_type == 6 and enable_alpinist == False:
                                Text.add_text(texts,"Cannot create army! Alpinists are turned off!")
                                continue
                            if selected_type != 0:
                                if vil.vill_type != 60 and vil.can_conscript_turns > 0:
                                    Text.add_text(texts,f"This village cannot create army in the next {vil.can_conscript_turns} turns!")
                                elif vil.health <= 0:
                                    Text.add_text(texts,"This village is ruined! Cannot create army!")
                                else:
                                    if selected_type == 5:
                                        type1 = 100
                                    elif selected_type == 6:
                                        type1 = 400
                                    elif selected_type == 7:
                                        type1 = 201
                                    elif selected_type == 8: #The first builded boats at 1 III AD 2025 19:39
                                        type1 = 202
                                    else:
                                        type1 = selected_type
                                    spawn_type = type1
                                    if type1 >= 200 and type1 <= 250:
                                        if vil.vill_type != 20:
                                            Text.add_text(texts,"Must be build in port town!")
                                            continue
                                    new_army = Army.conscript(type1,vil.owner,vil.rect.bottomleft,True,texts)
                                    if new_army is not None:
                                        armies.add(new_army)
                                        armies_.add(new_army)
                                        show_selected = False
                                        Text.deactivate_text(texts,"conscript")
                                        Village.unselect_villages(villages,texts)
                                        Player.get_armied(vil.owner,new_army)
                                        vil.can_conscript_turns = 4
            #=====================================================#
            elif event.key == pygame.K_c:
                selected_type = 0
                for vil in villages:
                    vil.selected = False
                for arm in armies_:
                    if arm.formation == 100:
                        arm.unselect_me(texts)
                Text.deactivate_text(texts,"vill_type")
            elif event.key == pygame.K_1:
                selected_type = 1
            elif event.key == pygame.K_2:
                selected_type = 2
            elif event.key == pygame.K_3:
                selected_type = 3
            elif event.key == pygame.K_4:
                selected_type = 4
            elif event.key == pygame.K_5:
                selected_type = 5
            elif event.key == pygame.K_6:
                selected_type = 6
            elif event.key == pygame.K_7:
                selected_type = 7
            elif event.key == pygame.K_8:
                selected_type = 8
            elif event.key == pygame.K_o:
                if visible_village_owner:
                    visible_village_owner = False
                else:
                    visible_village_owner = True
            elif event.key == pygame.K_p:
                if visible_army_owner:
                    visible_army_owner = False
                else:
                    visible_army_owner = True
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
            if selected_type == 5:
                type1 = 100
            elif selected_type == 6:
                type1 = 400
            elif selected_type == 7:
                type1 = 201
            elif selected_type == 8:
                type1 = 202
            else:
                type1 = selected_type
            spawn_type = type1
            for arm in armies_:
                if arm.owner.is_AI > 0:
                    particles.empty()
                    turn_return = Turn.turn(players,armies,villages,texts,terrains,particles,config,game_turn)
                    armies_ = turn_return[0]
                    villages_ = turn_return[1]
                    game_turn = turn_return[2]
                    selected_type = 0
                    spawn_type = 0
                    show_selected = False
                    Village.unselect_villages(villages,texts)
                    Text.deactivate_text(texts,"vill_type")
                    break
                break
            """for arm in armies:
                armies1 = armies.copy()
                armies1.remove(arm)
                if arm.is_boat and arm.formation not in [201,202,203]:
                    arm.is_boat = False
                elif arm.formation in [201,202,203]:
                    arm.units_boat.empty()
                    arm.is_boat = True
                    collision_during_turn = pygame.sprite.spritecollideany(arm,armies1)
                    if collision_during_turn is not None:
                        not_boated.remove(collision_during_turn)
                        arm.units_boat.add(not_boated)"""
        elif event.type == CHECK_VICTORY:
            if was_defeated == False:
                for p in players:
                    if len(p.armies) == 0 and len(p.villages) == 0 and menu == 0 and p.defeted_tell_not == False:
                        was_defeated = p
                        p.defeted = True
        elif event.type == pygame.MOUSEBUTTONUP:
            #===== Kliczek collides here =====#
            kliczek_button = pygame.sprite.spritecollideany(kliczek,buttons)
            clicked_village = pygame.sprite.spritecollideany(kliczek,villages)
            #kliczek_collide = pygame.sprite.spritecollideany(kliczek,armies)
            kliczek_collide = pygame.sprite.spritecollide(kliczek,armies,False)

            if clicked_village is not None and len(kliczek_collide) == 0:
                clicked_village.select_village(villages,texts)
                if clicked_village.selected == False:
                    show_selected = False
                else:
                    show_selected = True
                Text.activate_text(texts,"conscipt")
                    
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
                    generate_map.activate_button(True)
                    alpinist_off.activate_button(True)
                    flats_button.activate_button(True)
                    track_map_button.activate_button(True)
                    rich_center_button.activate_button(True)
                    Button.activate_group(map_buttons,True)
                    small_input.activate_button(True)
                    handicap2.activate_button(True)
                    handicap1.activate_button(True)
                if kliczek_button.type == 6 or kliczek_button.type == 5 and menu == 1:
                    if kliczek_button.update_button():
                        if kliczek_button.type == 6:
                            player2.gold_handicap = 5
                        else:
                            player1.gold_handicap = 5
                    else:
                        if kliczek_button.type == 6:
                            player2.gold_handicap = 0
                        else:
                            player1.gold_handicap = 0
                elif kliczek_button.type == 400 and menu == 1:
                    enable_alpinist = alpinist_off.update_button()
                if kliczek_button.type in [11,12,13,14,15] and kliczek_button.active:
                    modes = [1]
                    map_name = None
                    if kliczek_button.type == 12: #Map selection 3 I AD 2025 19:40
                        map = "flats"
                    elif kliczek_button.type == 13:
                        map = "rich_center"
                    elif kliczek_button.type == 15:
                        map = "manual"
                        map_name = "yorktown"
                    elif kliczek_button.type == 14:
                        map = "coast"
                        modes.append("Dev")
                    else:
                        map = "track"
                    Text.add_text(texts,f"Selected \'{map}\' map!")
                if kliczek_button.type == 20 and menu == 1:
                    if map is not None or input_text.lower() == "map":
                    #start_quick.activate_button(False)
                        terrains.empty()
                        menu = 0
                        Button.activate_group(map_buttons,False)
                        generate_map.activate_button(False)
                        small_input.activate_button(False)
                        keys_button.activate_button(False)
                        show_production.activate_button(True)
                        flats_button.activate_button(False)
                        rich_center_button.activate_button(False)
                        track_map_button.activate_button(False)
                        handicap2.activate_button(False)
                        handicap1.activate_button(False)
                        alpinist_off.activate_button(False)
                        if input_text.lower() == "map":
                            map = "deserted"
                            modes = [1]
                        elif input_text.lower() == "dallas": # Respect paid 8 II AD 2025
                            Text.add_text(texts,"Rest in peace president Kennedy!")
                        terrains = start(config.starting_gold,modes,map,map_name)
                        Text.deactivate_text(texts,"keys")
                    else:
                        Text.add_text(texts,"Select a map!") 
            if len(kliczek_collide) != 0:
                for kliczek_collide2 in kliczek_collide:
                    kliczek_collide2.selection(texts)
                    if kliczek_collide2.is_boat:
                        kliczek_collide2.units_boat.empty()
                        kliczek_collide.remove(kliczek_collide2)
                        for kli in kliczek_collide:
                            kliczek_collide2.units_boat.add(kli)
                            kli.on_boat = True
                            kli.unselect_me(texts)
                            #kli.selection(texts)
                            """if kli.selected:
                                kli.selected = False
                            else:
                                kli.selected = True"""
                            #kli.unselect_me(texts)
                        break
                    if config.debug_mode and kliczek_collide2.selected:
                        Text.add_text(texts,f"Morale is {kliczek_collide2.morale}")
                        Text.add_text(texts,f"Health is {kliczek_collide2.health}")
                    print(kliczek_collide2.selected)
                    if kliczek_collide2.formation == 100:
                        Text.activate_text(texts,"vill_type")
    #========BLITING========#
    if menu != 1:
        screen.blit(background_image, (0,0))
    else:
        screen.blit(background_image2, (0,0))
    for ter in terrains:
        screen.blit(ter.look,ter.rect)
    for vil in villages:
        if visible_village_owner:
            vil.update_color()
            screen.blit(vil.new_banner,vil.rect)
        else:
            screen.blit(vil.banner,vil.rect)
    for arm in armies:
        if visible_army_owner:
            arm.update_color()#Fixed 11.01.2025
            screen.blit(arm.new_banner,arm.rect)
        else:
            screen.blit(arm.banner,arm.rect)
    for b in buttons:
        if b.active:
            screen.blit(b.picture,b.rect)
    if start_quick.active:
        screen.blit(quick_text,(12*32,12*32+2))
    if generate_map.active:
        screen.blit(gen_button_text,(generate_map.rect.left+8,generate_map.rect.centery-10))
    if small_input.active:
            input_text_render = font.render(input_text,True,(25,25,25),(181,123,76))
            screen.blit(input_text_render,(small_input.rect.left+8,small_input.rect.centery-10))
    if REAL_show_production:
        gold_text = font.render(f"Gold:{round(player1.gold,2)}+{round(player1.p_gold,2)};{round(player2.gold,2)}+{player2.p_gold}",False,(160,200,200))
        lumber_text = font.render(f"Lumber:{round(player1.lumber)}+{round(player1.p_lumber,2)};{player2.lumber}+{player2.p_lumber}",False,(160,200,200))
        food_text = font.render(f"Food:{round(player1.food,2)}+{round(player1.p_food,2)};{round(player2.food,2)}+{player2.p_food}",False,(160,200,200))
        spear_text = font.render(f"Sprears:{player1.spear}+{player1.p_spear};{player2.spear}+{player2.p_spear}",False,(160,200,200))
        bow_text = font.render(f"Bows:{player1.bow}+{player1.p_bow};{player2.bow}+{player2.p_bow}",False,(160,200,200))
        screen.blit(gold_text,(631,40))
        screen.blit(lumber_text,(631,60))
        screen.blit(food_text,(631,80))
        screen.blit(spear_text,(631,100))
        screen.blit(bow_text,(631,120))
    #Particle.decay(particles)
    for arm in armies_:
        if arm.owner.is_AI > 0:
            please_wait = font_big.render(f"Please wait!",False,(142,130,130))
            screen.blit(please_wait,(70,600))
    Particle.render_particles(particles,screen)
    Text.print_text(texts,screen)

    if show_selected and spawn_type != 0:
        Unitname = Army.Id_to_name(spawn_type)
        show_selected_text = font_small.render(f"Selected unit {selected_type}: The {Unitname}",False,(31,31,200))
        screen.blit(show_selected_text,(490,200))

    if was_defeated != False:
        if was_defeated.defeted_tell_not != True:
            if date_of_today.month == 4 and date_of_today.day == 1 or config.force_jokes:
                defeated_text = font_big.render(f"{was_defeated.name}\'s country has experienced a rapid unsheduled disassembly!",False,(178,35,35))
            else:
                defeated_text = font_big.render(f"{was_defeated.name} has been defeated!",False,(150,31,30))
            screen.blit(defeated_text,(320,180))
    if menu == 0:
        turn_text = font_small.render(f"Turn {game_turn}",False,(33,33,220))
        screen.blit(turn_text,(800,655))
    kliczek.draw_kliczek(screen)
    if menu == 1:
        screen.blit(version,(570,750))

    pygame.display.flip()
    FPS.tick(40)