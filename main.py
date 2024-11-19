import pyxel

class App:
    def __init__(self):
        pyxel.init(256, 160, title="BWI-Chat")
        self.messages = [] # Stocke tous les messages
        self.input_text = "" # Stocke le message en cours d'écriture par l'utilisateur
        pyxel.run(self.update, self.draw)
        
    def input(self):
        # Pour chaque touche de A à Z
        for k in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
            # Ajouter le text si la touche est préssée
            if pyxel.btnp(k):
                # Retourne le caractère associé à la touche
                self.input_text += chr(k).lower()
                
        # Vérifier la touche retour
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.input_text) > 0:
            # Retirer le caractère précédent
            self.input_text = self.input_text[:-1]
                                    
        # Vérifier si espace est pressé
        if pyxel.btnp(pyxel.KEY_SPACE):
            # Ajouter un espace
            self.input_text += " "
        
    def update(self):
            self.input()
        
    def draw(self):
        pyxel.cls(0)
        pyxel.text(5, 152, self.input_text, 7)
            
App()