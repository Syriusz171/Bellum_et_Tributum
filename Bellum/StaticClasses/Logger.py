import datetime
'''class Logger():'''
def InitLog(Version: str):
    '''Clears old Latest.log. Writes current time and version of the game.'''
    with open("Logs/Latest.log","w") as Log:
        CurrentTime = datetime.datetime.now()
        Log.write(f"[{CurrentTime.hour}:{CurrentTime.minute}:{CurrentTime.second}] Bellum et Tributum {Version} started.\n")
        Log.close()
def WriteToLog(Message: str):
    '''Logs a message into Logs/Latest.log. Adds currect time and a new line at the end.'''
    with open("Logs/Latest.log","a") as Log:
        CurrentTime = datetime.datetime.now()
        Log.write(f"[{CurrentTime.hour}:{CurrentTime.minute}:{CurrentTime.second}] {Message}\n")
        Log.close()