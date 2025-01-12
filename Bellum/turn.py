import pygame
from player import Player
from army import Army
from village import Village
from unit import Unit
from text import Text
class Turn(Army):
    def __init__() -> None:
        super().__init__()
    def turn(players,armies,villages,texts):
        activate_next = False
        armies_ = None
        for p in players:
            if p.active:
                activate_next = True
                p.activate()
                if p.number == len(players):
                    Army.heal(armies,villages)
                    Army.reset_march(armies)
                    Player.check_production(villages,players)
                    Player.collect_global(players)
                    for p in players:
                        if p.number == 1:
                            player1 = p
                            player1.activate()
                            armies_ = player1.armies.copy()
                            villages_= player1.villages.copy()
                            Text.add_text(texts,f"{p.name} turn")
                            return armies_, villages_
            elif p.active == False and activate_next:
                p.activate()
                Text.add_text(texts,f"{p.name} turn")
                armies_ = p.armies.copy()
                villages_ = p.villages.copy()
                activate_next = False
                turn_return = [armies_,villages_]
                return turn_return