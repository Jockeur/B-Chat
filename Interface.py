import pyxel

class App:
    def __init__(self):
        #juste les trucs obligatoires
        pyxel.init(512,300,title="BWI-Chat")
        pyxel.load("ressource.pyxres")
        
        # valeurs:
        self.messages=[]
        self.typingOn=False
        self.selectedMessage=None
        self.brightTheme=True
        self.tilesetSmol_x=0
        self.tilesetSmol_y=32
        self.tilesetBIG_x=64
        self.tilesetBIG_y=64
        self.txtColor=6
        
        pyxel.run(self.update,self.draw)
        
    def typeIn(self):
        if pyxel.btnr(pyxel.KEY_T) and self.typingOn==False:
            self.messages.append("")
            self.typingOn=True
            if self.selectedMessage==None:
                self.selectedMessage=0
            else:
                self.selectedMessage+=1
                
    def ThemeColorChange(self):
        if pyxel.btnr(pyxel.KEY_B) and pyxel.btnr(pyxel.KEY_CTRL):
            self.brightTheme=True
        if pyxel.btnr(pyxel.KEY_D) and pyxel.btnr(pyxel.KEY_CTRL):
            self.brightTheme=False
            
    def update(self):
        
        self.ThemeColorChange()

    def draw(self):
        if self.brightTheme==True:
            pyxel.cls(7)
            self.txtColor=6
            self.tilesetSmol_x=0
            self.tilesetSmol_y=32
            self.tilesetBIG_x=64
            self.tilesetBIG_y=64
        else:
            pyxel.cls(0)
            self.txtColor=1
            self.tilesetSmol_x=0
            self.tilesetSmol_y=0
            self.tilesetBIG_x=64
            self.tilesetBIG_y=0
            
        pyxel.blt(400,250,0,self.tilesetSmol_x,self.tilesetSmol_y,64,32)
        pyxel.text(405,255,'bon, je crois',self.txtColor)
        pyxel.text(405,262,'quon a notre',self.txtColor)
        pyxel.text(405,269,'interface',self.txtColor)
        pyxel.blt(330,150,0,self.tilesetBIG_x,self.tilesetBIG_y,128,64)
        pyxel.text(335,155,'En vrai clean ou pas ?',self.txtColor)
App()