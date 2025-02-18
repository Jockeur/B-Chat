import pygame
import json
import sys
import os
from client import Client

class App():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(size=36)
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
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
                elif event.key != pygame.K_RETURN and event.key != pygame.K_CARET:
                    # if it's not include the character typed in the message (except for the special characters such as ^ or ENTER)
                    self.message += event.unicode
                elif event.key == pygame.K_RETURN and self.message != "":
                    # Send the message to the server
                    self.client.send_message(self.message)

                    # Register the message localy
                    self.register_message(self.username, self.message)
                    self.message = ""
                
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill((255,255,255))
        
        # RENDER YOUR GAME HERE
        # Render all the messages

        for i in range(len(self.messages)):
            message_text = self.font.render(self.messages[str(i)]["message"], True, "black")

            # Calculate the bubble position based on the other's
            y_bubble = 50
            for j in range(len(list(self.messages.values())[i:])):
                y_bubble += 60
            bubble_x = 10 if self.messages[str(i)]["sender"] == self.username else self.screen.get_width() - message_text.get_width() - 30
            message_offset = 10

            message_bubble = pygame.Rect(bubble_x, self.screen.get_height() - y_bubble, message_text.get_width() + 20, 50)

            bubble_color = pygame.Color(128, 140, 144) if self.username != self.messages[str(i)]["sender"] else pygame.Color(36, 175, 227)

            pygame.draw.rect(self.screen, bubble_color, message_bubble, border_radius=15)
            self.screen.blit(message_text, (bubble_x + message_offset, self.screen.get_height() - y_bubble + round(25/2)))

        # Render the typing area
        type_area = pygame.Rect(0, self.screen.get_height() - 50, self.screen.get_width(), 50)
        pygame.draw.rect(self.screen, pygame.Color(36, 175, 227), type_area, border_radius=15)

        # Rendering the message that the user is curently typing
        typing_surface = self.font.render(self.message, True, "black")
        self.screen.blit(typing_surface, (10, self.screen.get_height() - 50 + round(25/2)))

        pygame.display.flip()
        self.clock.tick(60)
        
    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            
        pygame.quit()
        sys.exit()
        


    ## Fonctions utilitaires
    def register_message(self, username: str, message: str):
        self.messages[str(len(list(self.messages.values())))] = {"sender": username, "message": message}
        self.save_messages()
        
    def save_messages(self):
        with open(f'{os.getcwd()}/messages.json', 'r+') as file:
                    file.seek(0)
                    json.dump(self.messages, file, indent=2)
                    file.truncate()


App()