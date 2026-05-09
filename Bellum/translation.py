import config
import glob
class Translation():
    def check_language():
        text_translated = ""
        # Checking language
        LangFiles = glob.glob(f"data/*/Languages/{config.language}/{config.language}.py")
        # Loading British English as the base language (any missing translation keys will be loaded from English instead of throwing an error)
        EnglishFiles = glob.glob(f"data/*/Languages/en_uk/en_uk.py")
        for EnglishFile in EnglishFiles:
            with open((EnglishFile),"r") as file:
                text_translated += file.read()
                file.close
        #Reading translation        
        for LangFile in LangFiles:
            if LangFile not in EnglishFiles:
                with open((f"{LangFile}"),"r",encoding="utf-8") as file:
                    text_translated += file.read()
                    text_translated += "\n"
                    file.close(); 
        # Writing translation into currect_language.py
        with open("currect_language.py","w",encoding="utf-8") as lang:
            lang.write("#=================#\n#WARNING! This file is TEMPORARY! It will be erased when running the game!\n#In order to change translations go to data folder!\n\n")
            lang.write(text_translated)
            lang.close
        
        