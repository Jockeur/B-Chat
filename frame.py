import pyxel
from client import Client
from math import floor, ceil

class App:
    def __init__(self):
        #juste les trucs obligatoires
        pyxel.init(256,160,title="BWI-Chat",quit_key=pyxel.KEY_NONE)
        pyxel.load("assets.pyxres")
        
        # valeurs:
        self.messages=[]
        self.message=""
        self.typingOn=False
        self.brightTheme=True
        self.LETTER_timer = 0
        
        # Partie logique
        self.client = Client(self)
        
        print("Tu lances pyxel ?")
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
            
    def ThemeColorChange(self):
        if pyxel.btnp(pyxel.KEY_B) and pyxel.btn(pyxel.KEY_CTRL):
            self.brightTheme=True
        if pyxel.btnp(pyxel.KEY_D) and pyxel.btn(pyxel.KEY_CTRL):
            self.brightTheme=False
            
    def register_message(self, message: str):
        self.messages.append(message)
            
    def update(self):
        self.TypeIn()
        #self.ThemeColorChange()

    def draw(self):
        
        pyxel.cls(7)
        
        for i in range(len(self.messages)):
            # On peut mettre 43 caractères sur une ligne de la bulle
            max_ligne_bulle = self.ligne_message(i)
            
            # Calcul de la distance par rapport au bas de l'écran et des autres bulles
            y_bulles = 0
            for j in range(len(self.messages[i:])):
                y_bulles += 19 * (self.ligne_message(i+j)+1)
            
            if max_ligne_bulle == 0:
                # Ajouter la gauche de la bulle
                pyxel.blt(0, pyxel.height - 19 - y_bulles + 3, 0, 0, 32, 16, 16, colkey=0)
                
                # Ajouter autant de bulle pleine qu'il faut pour couvrir tous les caractères
                for j in range(floor((len(self.messages[i])-3)//3.5)):
                    pyxel.blt(16 + 16*j, pyxel.height - 19 - y_bulles + 3, 0, 16, 32, 16, 16, colkey=0)
                
                lettres_restantes = floor(len(self.messages[i])-3.5*floor(len(self.messages[i])/3.5))
                
                # Calcul farfelu pour ajouter la fin de la bulle au bon endroit et que ça ne fasse pas un gros pâté déguelasse
                pyxel.blt(ceil((len(self.messages[i])-3)//3.5)*16 + ceil(16*(floor((lettres_restantes/3.5)*100))/100), pyxel.height - 19 - y_bulles + 3, 0, 32, 32, 16, 16, colkey=0)
                
                pyxel.text(5, pyxel.height - 19 - y_bulles + 8, self.messages[i], 0)
            
            
            # Le message prend 2 lignes
            if max_ligne_bulle == 1:
                # Ajouter la gauche de la double bulle
                pyxel.blt(0, pyxel.height - 19 - y_bulles + 3, 0, 0, 0, 16, 32, colkey=0)
                
                # Ajouter autant de double bulle pleine qu'il faut pour chaque caractères
                for j in range(9):
                    pyxel.blt(16 + 16*j, pyxel.height - 19 - y_bulles + 3, 0, 16, 0, 16, 32, colkey=0)
                
                pyxel.blt(32 + 16*j, pyxel.height - 19 - y_bulles + 3, 0, 32, 0, 16, 32, colkey=0)
                
                for j in range(max_ligne_bulle+1):
                    pyxel.text(5, pyxel.height - 19 - y_bulles + j*16 + 8, self.messages[i][j*41:(j+1)*41], 0)
                      
        
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
            
            # Fill the middle lines
            for j in range(message_len_max-1):
                for i in range(floor(pyxel.width/16)):
                    pyxel.blt(i*16, pyxel.height-16*(j+2), 0, 16, 0, 16, 16, colkey=0)
                    
            # bottom-left corner
            pyxel.blt(0, pyxel.height - 16, 0, 0, 16, 16, 16, colkey=0)
            
            # bottom-right corner
            pyxel.blt(pyxel.width - 16, pyxel.height - 16, 0, 32, 16, 16, 16, colkey=0)
            
            # Fill the lower box
            for i in range(floor(fit)):
                pyxel.blt(16*(i+1), pyxel.height - 16, 0, 16, 16, 16, 16, colkey=0)
            
            # Write the message in the box
            for i in range(message_len_max+1):
                pyxel.text(5, pyxel.height - 16*(message_len_max-i+1) + 6, self.message[i*61:(i+1)*61], 7)
                
    def ligne_message(self, index: int):
        return len(self.messages[index])//41
        
                
App()
