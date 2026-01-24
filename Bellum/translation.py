import config
import glob
class Translation():
    def check_language():
        text_translated = ""
        # Checking language
        files = glob.glob(f"data/*/Languages/{config.language}/{config.language}.py")
        print (files)
        # Loading British English as the base language (any missing translation keys will be loaded from English and will not throw error)
        with open(("data/BeT/Languages/en_uk/en_uk.py"),"r") as file:
            text_translated = file.read()
            file.close
        for LangFile in files:
            print (LangFile)
            if LangFile != "data\\BeT\\Languages\\en_uk\\en_uk.py":
                with open((f"{LangFile}"),"r") as file:
                    text_translated += file.read()
                    text_translated += "\n"
                    file.close(); 
        # Loading translation
        with open("currect_language.py","w") as lang:
            lang.write("#=================#\n#WARNING! This file is TEMPORARY! It will be erased when running the game!\n#In order to change translations go to data folder!\n\n")
            lang.write(text_translated)
            lang.close
        
        