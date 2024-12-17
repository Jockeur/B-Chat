import pyxel
from client import Client
from math import floor

class App:
    def __init__(self):
        #juste les trucs obligatoires
        pyxel.init(256,160,title="BWI-Chat",quit_key=pyxel.KEY_NONE)
        pyxel.load("assets.pyxres")
        
        # valeurs:
        self.messages=[]
        self.message=""
        self.m_offset={}
        self.typingOn=False
        self.brightTheme=True
        self.up_right=(0,0)
        self.LETTER_timer = 0
        #self.line=""
        
        # Partie logique
        self.client = Client()
        
        pyxel.run(self.update,self.draw)
    
    # On check chaque entrée, on la process, si c'est un caractère spécial on l'ajoute
    def TypeIn(self):
        # if pyxel.btnr(pyxel.KEY_T) and self.typingOn==False:
        #     self.typingOn=True
        # if pyxel.btnp(pyxel.KEY_ESCAPE) and self.typingOn==True:
        #     self.typingOn=False
            
        # if self.typingOn==True:
        for k in range(pyxel.KEY_0, pyxel.KEY_9+1):
            if pyxel.btnp(k) and pyxel.btn(pyxel.KEY_SHIFT):
                self.message+=chr(k)
        if pyxel.btnp(pyxel.KEY_COMMA) and not pyxel.btn(pyxel.KEY_SHIFT):
            self.message+=","
        if pyxel.btnp(pyxel.KEY_COMMA) and pyxel.btn(pyxel.KEY_SHIFT):
            self.message+="?"
        if pyxel.btnp(pyxel.KEY_1) and not pyxel.btn(pyxel.KEY_SHIFT):
            self.message+="&"
        if pyxel.btnp(pyxel.KEY_3) and not pyxel.btn(pyxel.KEY_SHIFT):
            self.message+="\""
        if pyxel.btnp(pyxel.KEY_4) and not pyxel.btn(pyxel.KEY_SHIFT):
            self.message+="'"
        if pyxel.btnp(pyxel.KEY_5) and not pyxel.btn(pyxel.KEY_SHIFT):
            self.message+="("
        if pyxel.btnp(pyxel.KEY_6) and not pyxel.btn(pyxel.KEY_SHIFT):
            self.message+="-"
        if pyxel.btnp(pyxel.KEY_RIGHTPAREN) and not pyxel.btn(pyxel.KEY_SHIFT):
            self.message+=")"
        if pyxel.btnp(pyxel.KEY_EQUALS) and not pyxel.btn(pyxel.KEY_SHIFT):
            self.message+="="
        if pyxel.btnp(pyxel.KEY_EQUALS) and pyxel.btn(pyxel.KEY_SHIFT):
            self.message+="+"
        if pyxel.btnp(pyxel.KEY_SEMICOLON) and pyxel.btn(pyxel.KEY_SHIFT):
            self.message+="."
        if pyxel.btnp(pyxel.KEY_COLON) and pyxel.btn(pyxel.KEY_SHIFT):
            self.message+="/"
        if pyxel.btnp(pyxel.KEY_COLON) and not pyxel.btn(pyxel.KEY_SHIFT):
            self.message+=":"
        if pyxel.btnp(pyxel.KEY_8) and not pyxel.btn(pyxel.KEY_SHIFT):
            self.message+="\\"
        if pyxel.btnp(pyxel.KEY_EXCLAIM):
            self.message+="!"
        if pyxel.btnp(pyxel.KEY_ASTERISK):
            self.message+="*"
        if pyxel.btnp(pyxel.KEY_BACKSPACE) or (pyxel.btn(pyxel.KEY_BACKSPACE) and self.backspace_timer>=400) and len(self.message) > 0:
            self.message=self.message[:-1]
        for k in range(pyxel.KEY_A, pyxel.KEY_Z+1):
            if pyxel.btn(pyxel.KEY_BACKSPACE) and not pyxel.btn(k):
                self.backspace_timer+=1
        if pyxel.btnr(pyxel.KEY_BACKSPACE):
            self.backspace_timer=0
        for k in range(pyxel.KEY_A, pyxel.KEY_Z+1):
            if (pyxel.btnp(k) or (pyxel.btn(k) and self.LETTER_timer>=20)) and pyxel.btn(pyxel.KEY_SHIFT):
                self.message+=chr(k).upper()
                self.backspace_timer=0
            elif pyxel.btnp(k) or (pyxel.btn(k) and self.LETTER_timer>=20):
                self.message+=chr(k)
                self.backspace_timer=0
            elif pyxel.btnr(k):
                self.LETTER_timer=0
            if pyxel.btn(k):
                self.LETTER_timer+=1
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.message+=" "
        
        ## Si la touche est entrée
        if pyxel.btnp(pyxel.KEY_RETURN) and len(self.message)!=0:
            
            # Envoyer le message au serveur
            self.client.send_message(self.message)
            
            # Stocker et envoyer le message
            self.messages.append(self.message)
            self.message=""
            if len(self.message)<=14:
                self.m_offset[len(list(self.m_offset.keys()))+1]=33
            if len(self.message)>14:
                self.m_offset[len(list(self.m_offset.keys()))+1]=65
                
    def ThemeColorChange(self):
        if pyxel.btnp(pyxel.KEY_B) and pyxel.btn(pyxel.KEY_CTRL):
            self.brightTheme=True
        if pyxel.btnp(pyxel.KEY_D) and pyxel.btn(pyxel.KEY_CTRL):
            self.brightTheme=False
            
    def update(self):
        self.TypeIn()
        #self.ThemeColorChange()

    def draw(self):
        # Désolé mais pour l'instant j'en ai un peu rien à faire du mode sombre
        
        # if self.brightTheme==True:
        #     pyxel.cls(7)
        #     self.txtColor=6
        #     self.tilesetSmol_x=0
        #     self.tilesetSmol_y=32
        #     self.tilesetBIG_x=64
        #     self.tilesetBIG_y=64
        #     self.TypingBar=176
        # else:
        #     pyxel.cls(0)
        #     self.txtColor=1
        #     self.tilesetSmol_x=0
        #     self.tilesetSmol_y=0
        #     self.tilesetBIG_x=64
        #     self.tilesetBIG_y=0
        #     self.TypingBar=160
        pyxel.cls(7)
        
        # Le nombre de cases pleines que l'on pourra mettre entre les borne d'une boite pour écrire
        fit = (pyxel.width - 16*2)/16
        
        # Le nombre de ligne dont on a besoin pour afficher notre message en entier (-1)
        message_len_max = len(self.message)//61
        
        if message_len_max == 0:
            pyxel.blt(0, pyxel.height - 16, 0, 0, 32, 16, 16, colkey=0)
            for i in range(floor(fit)):
                pyxel.blt(16*(i+1), pyxel.height - 16, 0, 16, 32, 16, 16, colkey=0)
            pyxel.blt(pyxel.width-16, pyxel.height-16, 0, 32, 32, 16, 16, colkey=0)
            pyxel.text(5,pyxel.height-10,self.message, 7)
            
        elif message_len_max == 1:
            pyxel.blt(0, pyxel.height-32, 0, 0, 0, 16, 32, colkey=0)
            for i in range(floor(fit)):
                pyxel.blt(16*(i+1), pyxel.height - 32, 0, 16, 0, 16, 32, colkey=0)
            pyxel.blt(pyxel.width-16, pyxel.height - 32, 0, 32, 0, 16, 32, colkey=0)
            for i in range(message_len_max+1):
                pyxel.text(5, pyxel.height - 16*(message_len_max-i+1) + 6, self.message[i*61:(i+1)*61], 7)
                
        elif message_len_max >= 2:
            # up-lef corner
            pyxel.blt(0, pyxel.height-(16*(message_len_max+1)), 0, 0, 0, 16, 16, colkey=0)
            # up-right corner
            pyxel.blt(pyxel.width - 16, pyxel.height-(16*(message_len_max+1)), 0, 32, 0, 16, 16, colkey=0)
            # Fill the upper box
            for i in range(floor(fit)):
                pyxel.blt(16*(i+1), pyxel.height-16*(message_len_max+1), 0, 16, 0, 16, 16, colkey=0)
            
            # Fille the middle lines
            for j in range(message_len_max-1):
                for i in range(floor(pyxel.width/16)):
                    pyxel.blt(i*16, pyxel.height-16*(j+2), 0, 16, 0, 16, 16, colkey=0)
                    
            # bottom-lef corner
            pyxel.blt(0, pyxel.height - 16, 0, 0, 16, 16, 16, colkey=0)
            # bottom-right corner
            pyxel.blt(pyxel.width - 16, pyxel.height - 16, 0, 32, 16, 16, 16, colkey=0)
            # Fill the lower box
            for i in range(floor(fit)):
                pyxel.blt(16*(i+1), pyxel.height - 16, 0, 16, 16, 16, 16, colkey=0)
            
            # Write the message in the box
            for i in range(message_len_max+1):
                pyxel.text(5, pyxel.height - 16*(message_len_max-i+1) + 6, self.message[i*61:(i+1)*61], 7)
            
            
        # for m in range(len(self.messages)):
        #     if len(self.messages[m])<=14:
        #         pyxel.blt(192,111,0,self.tilesetSmol_x,self.tilesetSmol_y,64,32)
        #         #14 caractères max par ligne
        #         #for i in range(1,6):
        #             #for l in range(i,i*14):
        #                 #self.line+=self.messages[m][l]
        #                 #pyxel.text(195,114-(self.m_offset-m*33)+(i*6),self.line,self.txtColor)
        #         pyxel.text(195,114, self.messages[m],self.txtColor)
        #     else:
        #         pyxel.blt(128,111,0,self.tilesetBIG_x,self.tilesetBIG_y,128,64)
        #         #14 caractères max par ligne
        #         pyxel.text(132,115,self.messages[m],self.txtColor)
                
App()
