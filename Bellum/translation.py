import config
class Translation():
    def check_language():
        text_translated = None
        if config.language == "en_uk":
            with open(("Language/en_uk/en_uk.py"),"r") as file:
                text_translated = file.read()
            with open("currect_language.py","w") as lang:
                lang.write(text_translated)
        elif config.language == "pl_pl":
            with open(("Language/pl_pl/pl_pl.py"),"r") as file:
                text_translated = file.read()
            with open("currect_language.py","w") as lang:
                lang.write(text_translated)