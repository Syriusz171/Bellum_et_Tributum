### #===== Main changes: =====#
Added:  
- Modding
    - Allows to add new translations to the game or to overwrite existing one.
- Logs:
    - Logs next to nothing. Allows to tell if crash was just user pressing ESC.
- "Fullscreen" mode
    - Press Ctrl + F.

Changed:

Removed:

Fixed:

### #===== Other changes =====#
Added:  
- Error handling when loading terrain:
    - If terrain type (internally called "form") does not exist, then it loads new error texture and documents incident in the logs.
### #===== Dev info =====#
Removed:  
- Some useless print statements in the code,
Fixed:  
- Typographical error in code.
