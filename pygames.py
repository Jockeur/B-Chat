import pygame
from client import Client

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

class App():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font('Comic Sans MS', 36)
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.messages={}
        self.message=""
        self.typingOn=False
        self.brightTheme=True
        self.LETTER_timer = 0
        
        # Partie logique
        self.client = Client(self)
        
        self.username = self.client.i_username
        
        self.run()
    
    # On check chaque entrée, on la process, si c'est un caractère spécial on l'ajoute
    def TypeIn(self):
        # if pygame.btnr(pygame.KEY_T) and self.typingOn==False:
        #     self.typingOn=True
        # if pygame.btnp(pygame.KEY_ESCAPE) and self.typingOn==True:
        #     self.typingOn=False
            
        # if self.typingOn==True:
        # for k in range(pygame.KEY_0, pygame.KEY_9+1):
        #     if pygame.btnp(k) and pygame.btn(pygame.KEY_SHIFT):
        #         self.message+=chr(k)
        # if pygame.btnp(pygame.KEY_COMMA) and not pygame.btn(pygame.KEY_SHIFT):
        #     self.message+=","
        # if pygame.btnp(pygame.KEY_COMMA) and pygame.btn(pygame.KEY_SHIFT):
        #     self.message+="?"
        # if pygame.btnp(pygame.KEY_1) and not pygame.btn(pygame.KEY_SHIFT):
        #     self.message+="&"
        # if pygame.btnp(pygame.KEY_3) and not pygame.btn(pygame.KEY_SHIFT):
        #     self.message+="\""
        # if pygame.btnp(pygame.KEY_4) and not pygame.btn(pygame.KEY_SHIFT):
        #     self.message+="'"
        # if pygame.btnp(pygame.KEY_5) and not pygame.btn(pygame.KEY_SHIFT):
        #     self.message+="("
        # if pygame.btnp(pygame.KEY_6) and not pygame.btn(pygame.KEY_SHIFT):
        #     self.message+="-"
        # if pygame.btnp(pygame.KEY_RIGHTPAREN) and not pygame.btn(pygame.KEY_SHIFT):
        #     self.message+=")"
        # if pygame.btnp(pygame.KEY_EQUALS) and not pygame.btn(pygame.KEY_SHIFT):
        #     self.message+="="
        # if pygame.btnp(pygame.KEY_EQUALS) and pygame.btn(pygame.KEY_SHIFT):
        #     self.message+="+"
        # if pygame.btnp(pygame.KEY_SEMICOLON) and pygame.btn(pygame.KEY_SHIFT):
        #     self.message+="."
        # if pygame.btnp(pygame.KEY_COLON) and pygame.btn(pygame.KEY_SHIFT):
        #     self.message+="/"
        # if pygame.btnp(pygame.KEY_COLON) and not pygame.btn(pygame.KEY_SHIFT):
        #     self.message+=":"
        # if pygame.btnp(pygame.KEY_8) and not pygame.btn(pygame.KEY_SHIFT):
        #     self.message+="\\"
        # if pygame.btnp(pygame.KEY_EXCLAIM):
        #     self.message+="!"
        # if pygame.btnp(pygame.KEY_ASTERISK):
        #     self.message+="*"
        # if pygame.btnp(pygame.KEY_BACKSPACE) or (pygame.btn(pygame.KEY_BACKSPACE) and self.backspace_timer>=400) and len(self.message) > 0:
        #     self.message=self.message[:-1]
        # for k in range(pygame.KEY_A, pygame.KEY_Z+1):
        #     if pygame.btn(pygame.KEY_BACKSPACE) and not pygame.btn(k):
        #         self.backspace_timer+=1
        # if pygame.btnr(pygame.KEY_BACKSPACE):
        #     self.backspace_timer=0
        # for k in range(pygame.KEY_A, pygame.KEY_Z+1):
        #     if (pygame.btnp(k) or (pygame.btn(k) and self.LETTER_timer>=20)) and pygame.btn(pygame.KEY_SHIFT):
        #         self.message+=chr(k).upper()
        #         self.backspace_timer=0
        #     elif pygame.btnp(k) or (pygame.btn(k) and self.LETTER_timer>=20):
        #         self.message+=chr(k)
        #         self.backspace_timer=0
        #     elif pygame.btnr(k):
        #         self.LETTER_timer=0
        #     if pygame.btn(k):
        #         self.LETTER_timer+=1
        # if pygame.btnp(pygame.KEY_SPACE):
        #     self.message+=" "
        
        self.message += pygame.TEXTINPUT
        
        ## Si la touche est entrée
        if pygame.btnp(pygame.KEY_RETURN) and len(self.message)!=0:
            
            # Envoyer le message au serveur
            self.client.send_message(self.message)
            
            # Stocker et envoyer le message
            self.messages[str(len(self.messages))] = {"sender": self.username, "message": self.message}
            self.save_messages()
            self.message=""
   
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill("white")
        
        # RENDER YOUR GAME HERE
        self.font.render(self.message, True, "black")
        
        pygame.display.flip()
        self.clock.tick(60)
        
    def manage_typing(self):
        pressed = pygame.key.get_pressed()
        self.message += pressed.unicode
        
    def run(self):
        while self.running:
            self.events()
            self.manage_typing()
            self.update()
            self.draw()
            
        pygame.quit()
        
        
        
        