### #===== Main changes: =====#
Added:  
- Modding
    - Allows to add new translations to the game or to overwrite existing one.
- Logs:
    - Logs next to nothing. Allows to tell if crash was just user pressing ESC.
- "Fullscreen" mode
    - Press Ctrl + F.

Changed:
- AI changes:
    - Bot's chance to conscript militia militia lowered, it now spawns better units more frequently.
    - Bot's armies have more chance to move
    - Bot gets an extra town on "Yorktown" map.
Removed:

Fixed:
- Game should no longer crash if player is eliminated.
### #===== Other changes =====#
Added:  
- Error handling when loading terrain:
    - If terrain type (internally called "form") does not exist, then it loads new error texture and documents incident in the logs.
### #===== Dev info =====#
Removed:  
- Some useless print statements in the code,
Fixed:  
- Typographical error in code.
