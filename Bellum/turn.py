import pygame
from player import Player
from army import Army
from village import Village
import config
from unit import Unit
from text import Text
from StaticClasses.UnitF import UnitF
from particle import Particle
from StaticClasses import Logger
from Enums.Direction import Direction
class Turn(Army):
    def turn(players,armies,villages,texts,terrains,particles,game_turn):
        part = Particle((200,600),"sword",20,-1,rotate=5)
        particles.add(part)
        activate_next = False
        armies_ = None
        Text.deactivate_text(texts,"PlayerDef")

        # TO DO: Rewrite turn ending system!
        #for Player in players:
            

        
        #for p in players:
            #if p.defeated:
                #p.defeated_tell_not = True
        for p in players:
            if p.active:
                activate_next = True
                p.activate()
                if p.number == len(players):
                    if config.logger_log_turns:
                        Logger.WriteToLog(f"Ending turn {game_turn}.")

                    UnitF.heal(armies,villages)
                    Army.reset_march(armies)
                    Player.check_production(villages,players)
                    Player.mk2_collect_global(players)
                    Village.turns_left_change(villages)
                    Army.summon_militia_global(players,armies,texts)
                    Army.spawn_at_enemy_points(players,armies,terrains,texts)
                    
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
                            if p.defeated == False:
                                player1 = p
                                player1.activate()
                                armies_ = player1.armies#.copy()
                                villages_= player1.villages#.copy()
                                Text.add_text(texts,f"{p.name} turn")
                                
                                #Logging
                                if config.logger_log_turns:
                                    Logger.WriteToLog(f"Started turn {game_turn}.")

                                return armies_, villages_,game_turn
                            else:
                                if config.logger_log_turns:
                                    Logger.WriteToLog(f"Started turn {game_turn}.")
                                return  [p.armies,p.villages,game_turn]
            elif p.active == False and activate_next:
                if p.defeated == False:
                    p.activate()
                    Text.add_text(texts,f"{p.name} turn")
                    armies_ = p.armies#.copy()
                    villages_ = p.villages#.copy()
                    activate_next = False
                    turn_return = [armies_,villages_,game_turn]
                    return turn_return
                else:
                    return  [p.armies,p.villages,game_turn]
    def ChangeActivePlayer(players,armies,villages,texts,terrains,particles,game_turn):

        #===Some dull visuals===#
        part = Particle((200,600),"sword",20,-1,rotate=5)
        particles.add(part)
        Text.deactivate_text(texts,"PlayerDef")


        for player in players:
            if player.played_turn:
                continue
            if player.defeated == True:
                continue
            player.activate()
            Text.add_text(texts,f"{player.name} turn")
            player.played_turn = True
            return [player.armies,player.villages,game_turn]
        
        #All players played their turns or lost:
        return Turn.EndTurn(players,armies,villages,texts,terrains,particles,game_turn)




    def EndTurn(players,armies,villages,texts,terrains,particles,game_turn):
        if config.logger_log_turns:
            Logger.WriteToLog(f"Ending turn {game_turn}.")

        #The turn ending
        UnitF.heal(armies,villages) #Heals all units.
        Army.reset_march(armies)    #Resets movement points
        Player.check_production(villages,players)   #Checks how much are players producing
        Player.mk2_collect_global(players)          #Gives the resources to players
        Village.turns_left_change(villages)         #Decreaments villages' cooldown on conscripting armies.
        Army.summon_militia_global(players,armies,texts)    #Spawns level one AI's units (this AI has no economy, villages just print armies for free).
        Army.spawn_at_enemy_points(players,armies,terrains,texts)   #"Bastion" map's units form the edge of the map.
        game_turn += 1
        for player in players:
            player.played_turn = False

            if player.is_AI == 1:
                player.active = True
                for army in player.armies:
                    for i in range(4):
                        direction = army.drunk_move_army(terrains,armies,villages)
                        Army.move_me(army,players,armies,villages,terrains,direction,texts)
                player.active = False
        for player in players:
            if player.defeated == False:
                Text.add_text(texts,f"{player.name} turn")
                
                #Logging that function is exited!
                if config.logger_log_turns:
                    Logger.WriteToLog(f"Started turn {game_turn}.")
                player.played_turn = True
                return [player.armies,player.villages,game_turn]
        Text.add_text(texts,"ERROR: Tried to turn when there is no non-defeated player.")
        Logger.WriteToLog(f"ERROR: Turn initialized but no players are alive! Player count: {len(players)}.")
        