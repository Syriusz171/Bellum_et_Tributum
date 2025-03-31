import pygame
from player import Player
from army import Army
from village import Village
from unit import Unit
from text import Text
class Turn(Army):
    def turn(players,armies,villages,texts,terrains,particles,config,game_turn):
        activate_next = False
        armies_ = None
        #for arm in armies:
            #if arm.is_boat:
            #    arm.units_boat.empty()
            #    arm.units_boat = pygame.sprite.spritecollide(arm,armies,False)
        for p in players:
            if p.defeted:
                p.defeted_tell_not = True
        for p in players:
            if p.active:
                activate_next = True
                p.activate()
                if p.number == len(players):
                    Army.heal(armies,villages)
                    Army.reset_march(armies)
                    Player.check_production(villages,players)
                    Player.mk2_collect_global(players)
                    Village.turns_left_change(villages)
                    Army.summon_militia_global(players,armies,texts,config)
                    #Army.pathfind(p,armies,villages,terrains,particles)
                    for pe in players:
                        pe.active = True
                    game_turn += 1
                    for p in players:
                        if p.is_AI == 1:
                            for army in p.armies:
                                for i in range(3):
                                    direction = army.drunk_move_army(terrains,armies,villages)
                                    Army.move_me(army,players,armies,villages,terrains,direction,texts)
                    for pe in players:
                        pe.active = False
                    for p in players:
                        if p.number == 1:
                            if p.defeted == False:
                                player1 = p
                                player1.activate()
                                armies_ = player1.armies.copy()
                                villages_= player1.villages.copy()
                                Text.add_text(texts,f"{p.name} turn")
                                return armies_, villages_,game_turn
                            else:
                                return  [p.armies,p.villages,game_turn]
            elif p.active == False and activate_next:
                if p.defeted == False:
                    p.activate()
                    Text.add_text(texts,f"{p.name} turn")
                    armies_ = p.armies.copy()
                    villages_ = p.villages.copy()
                    activate_next = False
                    turn_return = [armies_,villages_,game_turn]
                    return turn_return
                else:
                    return  [p.armies,p.villages,game_turn]