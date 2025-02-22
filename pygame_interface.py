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
        self.contact_surface = None
        self.message_surface = None
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.room = "Groupe général de discussion"
        self.messages={}
        self.message=""
        self.typingOn=False
        self.brightTheme=True
        self.LETTER_timer = 0

        self.scroll = 0

        self.username = ""
        
        self.run()

    ## Fonctions Pygame quand l'utilisateur est connecté
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
            elif event.type == pygame.MOUSEWHEEL:
                if self.scroll + event.y >= 0 and self.scroll + event.y <= len(self.messages.values()):
                    self.scroll += event.y
                
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill((183,188,189))

        # RENDER YOUR GAME HERE

        # Render the subsurfaces
        self.contact_surface = self.screen.subsurface((0, 0, self.screen.get_width()/5, self.screen.get_height()))
        self.message_surface = self.screen.subsurface((self.screen.get_width()/5, 0, self.screen.get_width()/5*4, self.screen.get_height()))

        # Render all the messages
        for i in range(len(self.messages)):
            message = self.messages[str(i)]["message"]
            message_lines = self.fit_text(message, round(self.message_surface.get_width()/2))
            message_width = 0

            # Calculate the bubble position based on the other's
            y_bubble = 50
            for j in range(len(list(self.messages.values())[i:len(self.messages.values()) - self.scroll])):
                y_bubble += 60 + 50*(len(self.fit_text(self.messages[str(i+j)]["message"], self.message_surface.get_width()//2)) - 1)
            bubble_x = 10 if self.messages[str(i)]["sender"] == self.username else self.message_surface.get_width() - self.font.size(message).get_width() - 30
            message_offset = 10

            for line in message_lines:
                if self.font.size(line)[0] > message_width:
                    message_width = self.font.size(line)[0]

            message_bubble = pygame.Rect(bubble_x, self.message_surface.get_height() - y_bubble, message_width + message_offset*2, 50*len(message_lines))

            # Render the bubble
            bubble_color = pygame.Color(128, 140, 144) if self.username != self.messages[str(i)]["sender"] else pygame.Color(36, 175, 227)
            pygame.draw.rect(self.message_surface, bubble_color, message_bubble, border_radius=15)
            
            # Render each line of the message
            for j in range(len(message_lines)):
                message_font = self.font.render(message_lines[j].strip(), True, "black")
                self.message_surface.blit(message_font, (bubble_x + message_offset, self.message_surface.get_height() - y_bubble + 13 + j*30))

        ## Render user interaction
        message_fit = self.fit_text(self.message, self.message_surface.get_width() - 20)

        type_area_height = 10
        for line in message_fit:
            type_area_height += self.font.size(line)[1] + 10


        # Render the typing area
        type_area = pygame.Rect(0, self.message_surface.get_height() - type_area_height, self.message_surface.get_width(), type_area_height)
        pygame.draw.rect(self.message_surface, pygame.Color(36, 175, 227), type_area, border_radius=15)

        # Rendering the message that the user is curently typing
        for j in range(len(message_fit)):
            text_height = 10
            typing_surface = self.font.render(message_fit[j].strip(), True, "black")
            for line in message_fit[:j]:
                text_height += self.font.size(line)[1] + 10
            self.message_surface.blit(typing_surface, (10, self.message_surface.get_height() - type_area_height + text_height))

        # Render the top bar with the groupe infos (group name, who's currently typing, etc.)
        top_rect = pygame.Rect(0, 0, self.message_surface.get_width(), 50)
        pygame.draw.rect(self.message_surface, (129, 134, 135), top_rect)
        pygame.draw.line(self.message_surface, (0, 0, 0), (0, 50), (self.message_surface.get_width(), 50))
        group_name = self.font.render(self.room, True, "white")
        self.message_surface.blit(group_name, (10, 12))

        # Render the contact list
        pygame.draw.line(self.screen, (0, 0, 0), (self.contact_surface.get_width(), 0), (self.contact_surface.get_width(), self.screen.get_height()))

        pygame.display.flip()
        self.clock.tick(60)

    ## Fonctions Pygame quand l'utilisateur n'est pas connecté
    def wait_for_username(self):
        self.screen.fill((183,188,189))
        self.screen.blit(self.font.render("Quel est votre pseudo ?", True, "black"), (10, 10))
        self.screen.blit(self.font.render(self.message, True, "black"), (10, 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.message != "":
                    self.username = self.message
                    self.message = ""
                    self.client = Client(self)
                elif event.key == pygame.K_BACKSPACE:
                    self.message = self.message[:-1]
                else:
                    self.message += event.unicode
    
    ## Fonction principale
    def run(self):
        while self.username == "":
            self.wait_for_username()
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

    def fit_text(self, text: str, max_width: int):
        if self.font.size(text)[0] > max_width:
            temp = text
            i = 1
            while self.font.size(temp)[0] > max_width:
                try:
                    if text[-i-1] == " ":
                        temp = text[:-i]
                except IndexError:
                    i = self.fit_text_just(text, max_width)
                    break
                i += 1
            first_part = text[:-i]
            second_part = text[-i:].strip()
            return [first_part] + self.fit_text(second_part, max_width)
        return [text]
    
    def fit_text_just(self, text: str, max_width: int):
        temp = text
        i = 1
        while self.font.size(temp)[0] > max_width:
            temp = text[:-i]
            i += 1
        return i

App()