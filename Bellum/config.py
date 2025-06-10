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
        self.starting_gold = 55
        # Pseudo AI! Allows to automate player's 2 turns! Change it to 1 to enable!
        self.playerNr2AI = 1
        # Difficulty, requires player2 to be AI! Max value is 7. Controls how often AI spawns troops. Default value is 2.
        self.difficulty = 7
        # Controls if the AI has a chance of spawning a spearman unit instead of militia one. Does not apply to invasion mode.
        self.allow_AI_spearman = True
        # Controls if AI can make other units.
        self.allow_AI_units = True
        # Force April Fools mode! Forces game to load jokes!
        self.force_jokes = False
