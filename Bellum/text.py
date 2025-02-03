import pygame
class Text(pygame.sprite.Sprite):
    def __init__(self,text,type="chat",active=True,time_left = 160,p_x=300,p_y=550):
        super().__init__()
        self.text = str(text)
        if type == "chat":
            self.text_font = pygame.font.SysFont("Times New Roman",24)
        elif type == "keys":
            self.text_font = pygame.font.SysFont("Times New Roman",18)
        else:
            self.text_font = pygame.font.SysFont("Times New Roman",15)
        self.text1 = self.text_font.render(self.text,False,(160,200,200))
        self.time_left = time_left
        self.type = type
        self.y = p_y
        self.x = p_x
        self.active = active
    def add_text(texts,input_text,type="chat",active=True,time_left = 160,p_x=300,p_y=550):
        if type == "chat":
            new_text = Text(input_text)
        else:
            new_text = Text(input_text,type,active,time_left,p_x,p_y)
        print(new_text.text)
        texts.add(new_text)   
    def init_texts(texts):
        Text.add_text(texts,"W,S,A,D ---> Move army","keys",False,None,550,400)
        Text.add_text(texts,"Mouse click ---> Select/Deselect army","keys",False,None,550,440)
        Text.add_text(texts,"Minus ---> Deselect player's armies","keys",False,None,540,480)
        Text.add_text(texts,"Enter ---> Turn","keys",False,None,550,520)
        Text.add_text(texts,"O ---> Village ownership visibility","keys",False,None,550,560)
        Text.add_text(texts,"P ---> Army ownership visibility","keys",False,None,550,600)
        Text.add_text(texts,"Village types:","vill_type",False,None,550,400)
        Text.add_text(texts,"1 -> Lumber:","vill_type",False,None,550,430)
        Text.add_text(texts,"2 -> Food:","vill_type",False,None,550,460)
        Text.add_text(texts,"3 -> Spear:","vill_type",False,None,550,490)
        Text.add_text(texts,"4 -> Bows:","vill_type",False,None,550,520)
        Text.add_text(texts,"5 -> Mining:","vill_type",False,None,550,560)
        Text.add_text(texts,"Press \'c\' to cancel;","vill_type",False,None,550,590)
        Text.add_text(texts,"Press \'Space\' to found village;","vill_type",False,None,550,620)
        Text.add_text(texts,"Army types:","conscipt",False,None,550,400)
        Text.add_text(texts,"1 -> Spearman","conscipt",False,None,550,430)
        Text.add_text(texts,"2 -> Archer:","conscipt",False,None,550,460)
        Text.add_text(texts,"3 -> Horseman:","conscipt",False,None,550,490)
        Text.add_text(texts,"4 -> Catapult:","conscipt",False,None,550,520)
        Text.add_text(texts,"5 -> Settler:","conscipt",False,None,550,560)
        Text.add_text(texts,"6 -> Alpinist:","conscipt",False,None,550,590)
        Text.add_text(texts,"Press \'c\' to cancel;","conscipt",False,None,550,620)
        Text.add_text(texts,"Press \'Space\' to conscipt army;","conscipt",False,None,550,650)

    def activate_text(texts,type_act):
        for t in texts:
            if t.type == type_act:
                if t.active:
                    t.active = False
                else:
                    t.active = True
    def deactivate_text(texts,type_act):
        for t in texts:
            t.active = False
    def print_text(texts,screen):
        neo_y = 550
        for t in texts:
            if t.type == "chat":
                t.y = neo_y
                neo_y -= 20
                screen.blit(t.text1,(30,t.y))
                t.time_left -= 1
                if t.time_left <= 0:
                    t.kill()
            else:
                if t.active:
                    screen.blit(t.text1,(t.x,t.y))