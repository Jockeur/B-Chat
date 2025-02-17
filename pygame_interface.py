import pygame
from client import Client

class App():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(size=36)
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.messages={}
        self.message=""
        self.typingOn=False
        self.brightTheme=True
        self.LETTER_timer = 0
        
        # # Partie logique
        # self.client = Client(self)
        
        # self.username = self.client.i_username
        
        self.run()
   
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # if the user is typing a message
            elif event.type == pygame.KEYDOWN:
                # if it's a backspace
                if event.key == pygame.K_BACKSPACE:
                    # remove the last character
                    self.message = self.message[:-1]
                else:
                    # if it's not include the character typed in the message
                    self.message += event.unicode
                
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill((255,255,255))
        
        # RENDER YOUR GAME HERE
        text_surface = self.font.render(self.message, True, "black")
        self.screen.blit(text_surface, (0, 0))
        
        pygame.display.flip()
        self.clock.tick(60)
        
    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            
        pygame.quit()
        
        
App()