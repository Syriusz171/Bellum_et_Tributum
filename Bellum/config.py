class Config():
    def __init__(self) -> None:
        # UNUSED
        self.civs = [1,1,1,1]
        # Player 2 name
        self.playerNr2Name = "Player2"
        # Debug mode! Set it True to see more
        self.debug_mode = True
        # Developer mode! Allows to see new map with new, unfinished features!
        self.developer_mode = True
        # Starting gold
        self.starting_gold = 65
        # Difficulty, requires player2 to be AI! Max value is 7. Controls how often AI spawns troops. Default value is 2.
        self.difficulty = 7
        # Controls if the AI has a chance of spawning a spearman unit instead of militia one. Does not apply to invasion mode.
        self.allow_AI_spearman = True
        # Controls if AI can make other units.
        self.allow_AI_units = True
        # Force April Fools mode! Forces game to load jokes!
        self.force_jokes = False
###===================================###
    # NEW CONFIG FILES
    # CONFIGS WILL BE SLOWLY MOVING TO THERE FROM THE TOP ONES!
###===================================###


    #=GENERAL SETTINGS=#
#Useless
civs = [1,1,1,1]
# Player 2 name
playerNr2Name = "Player2"
# Debug mode! Set it True to see more
debug_mode = True
# Developer mode! Allows to see new map with new, unfinished features!
developer_mode = True
# Starting gold
starting_gold = 65
# Difficulty, requires player2 to be AI! Max value is 7. Controls how often AI spawns troops. Default value is 2.
difficulty = 7
# Controls if the AI has a chance of spawning a spearman unit instead of militia one. Does not apply to invasion mode.
allow_AI_spearman = True
# Controls if AI can make other units.
allow_AI_units = True
# Force April Fools mode! Forces game to load jokes!
force_jokes = False
#===============================#
# Language configs

# Sets the language,
# Valid options: en_uk, pl_pl
# Default option is en_uk, example: language = "en_uk"
language = "en_uk"
