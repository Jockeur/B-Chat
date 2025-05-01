import time
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
        self.selected_surface = 'message_surface'
        
        self.room = "Groupe général de discussion"
        self.messages={}
        self.contacts = {}
        self.message=""
        self.contact_search=""
        self.typingOn=False
        self.brightTheme=True
        self.LETTER_timer = 0
        self.colors = {
            "background": pygame.Color(183, 188, 189),
            "text": pygame.Color(0, 0, 0),
            "bubble": pygame.Color(128, 140, 144),
            "bubble_sender": pygame.Color(36, 175, 227),
            "top_bar": pygame.Color(129, 134, 135),
            "top_bar_text": pygame.Color(255, 255, 255),
            "contact_list": pygame.Color(0, 0, 0),
            "contact_list_text": pygame.Color(255, 255, 255),
            "typing_area": pygame.Color(36, 175, 227),
            "typing_area_text": pygame.Color(0, 0, 0),
            "typing_area_border": pygame.Color(0, 0, 0),}
        self.choosen_contact = None

        self.scroll = 0

        self.username = ""
        self.password = ""

        self.client: Client
        
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
                    if self.selected_surface == 'message_surface' and self.choosen_contact != None:
                        self.message = self.message[:-1]
                    elif self.selected_surface == 'contact_surface':
                        self.contact_search = self.contact_search[:-1]
                elif event.key != pygame.K_RETURN and event.key != pygame.K_CARET:
                    # if it's not include the character typed in the message (except for the special characters such as ^ or ENTER)
                    if self.selected_surface == 'message_surface' and self.choosen_contact != None:
                        if event.unicode != "":
                            self.message += event.unicode
                    elif self.selected_surface == 'contact_surface':
                        if event.unicode != "":
                            self.contact_search += event.unicode
                elif event.key == pygame.K_RETURN and self.message != "":
                    # if the user is typing a message and presses ENTER
                    if self.selected_surface == 'message_surface' and self.choosen_contact != None:
                        # Send the message to the server
                        self.client.send_message(self.message.strip(), self.choosen_contact)
                        # Register the message in the local file
                        self.client.update_file(self.client.socket)
                        
                        self.message = ""
                    else:
                        pass
            elif event.type == pygame.MOUSEWHEEL:
                if self.scroll + event.y >= 0 and self.scroll + event.y <= len(self.messages.values()):
                    self.scroll += event.y
                
    def update(self):
        pass
    
    def draw(self):
        # Clear the screen
        self.screen.fill(self.colors['background'])

        # get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Render the subsurfaces
        self.contact_surface = self.screen.subsurface((0, 0, self.screen.get_width()/5, self.screen.get_height()))
        self.message_surface = self.screen.subsurface((self.screen.get_width()/5, 0, self.screen.get_width()/5*4, self.screen.get_height()))

        # RENDER YOUR GAME HERE
        if self.choosen_contact != None:
            ## Render user interaction
            message_fit = self.fit_text(self.message, self.message_surface.get_width() - 20)

            type_area_height = 10
            for line in message_fit:
                type_area_height += self.font.size(line)[1] + 10

            # Render the typing area
            type_area = pygame.Rect(0, self.message_surface.get_height() - type_area_height, self.message_surface.get_width(), type_area_height)
            pygame.draw.rect(self.message_surface, self.colors['bubble_sender'], type_area, border_radius=15)
            
            ## Render the bar to type the message
            if self.selected_surface == 'message_surface' and time.time()%1 > 0.5:
                bar = pygame.Rect(10 + self.font.size(message_fit[-1])[0], self.message_surface.get_height() - 35, 3, 25)
                pygame.draw.rect(self.message_surface, self.colors['typing_area_text'], bar)

            # Rendering the message that the user is curently typing
            for j in range(len(message_fit)):
                text_height = 10
                typing_surface = self.font.render(message_fit[j].strip(), True, "black")
                for line in message_fit[:j]:
                    text_height += self.font.size(line)[1] + 10
                self.message_surface.blit(typing_surface, (10, self.message_surface.get_height() - type_area_height + text_height))
            

            ## Render messages
            for i in range(len(self.messages) - self.scroll):
                message_offset = 10

                message = self.messages[str(i)]["message"]
                message_lines = self.fit_text(message, self.message_surface.get_width()/2 - 20)
                message_width = 0

                # Set the minimal width to fit the entire message
                for line in message_lines:
                    if self.font.size(line)[0] > message_width:
                        message_width = self.font.size(line)[0]

                # Calculate the bubble position based on the other's
                y_bubble = message_offset + type_area_height

                bubble_height = 10
                for j in range(len(list(self.messages.values())[i:len(self.messages.values()) - self.scroll])):
                    message_fit = self.fit_text(self.messages[str(i+j)]["message"], self.message_surface.get_width()/2 - 20)
                    y_bubble = y_bubble + 20 if j > 0 else y_bubble
                    for line in message_fit:
                        if j == 0:
                            bubble_height += message_offset + self.font.size(line)[1]
                        else:
                            y_bubble += message_offset + self.font.size(line)[1]
                bubble_x = 10 if self.messages[str(i)]["sender"] == 0 else self.message_surface.get_width() - message_width - 3*message_offset

                y_bubble += bubble_height

                message_bubble = pygame.Rect(bubble_x, self.message_surface.get_height() - y_bubble, message_width + message_offset*2, bubble_height)

                # Render the bubble
                bubble_color = self.colors['bubble'] if self.messages[str(i)]["sender"] == 0 else self.colors['bubble_sender']
                pygame.draw.rect(self.message_surface, bubble_color, message_bubble, border_radius=15)
                
                # Render each line of the message
                for j in range(len(message_lines)):
                    text_height = 10
                    message_font = self.font.render(message_lines[j].strip(), True, "black")
                    for line in message_lines[:j]:
                        text_height += self.font.size(line)[1] + 10
                    self.message_surface.blit(message_font, (bubble_x + message_offset, self.message_surface.get_height() - y_bubble + text_height))

        ## Render the top bar with the groupe infos (group name, who's currently typing, etc.)
        top_rect = pygame.Rect(0, 0, self.message_surface.get_width(), 50)
        pygame.draw.rect(self.message_surface, (129, 134, 135), top_rect)
        pygame.draw.line(self.message_surface, (0, 0, 0), (0, 50), (self.message_surface.get_width(), 50))
        group_name = self.font.render(self.room, True, "white")
        self.message_surface.blit(group_name, (10, 12))

        # Render the contact list
        pygame.draw.line(self.screen, (0, 0, 0), (self.contact_surface.get_width(), 0), (self.contact_surface.get_width(), self.screen.get_height()))

        # Title
        title = self.font.render("Contacts", True, "black")
        self.contact_surface.blit(title, (10, 10))

        # Search bar
        search_bar = pygame.Rect(10, 60, self.contact_surface.get_width() - 20, 50)
        pygame.draw.rect(self.contact_surface, (255, 255, 255), search_bar, border_radius=15)
        pygame.draw.rect(self.contact_surface, (0, 0, 0), search_bar, 2, border_radius=15)
        search_text = self.font.render(self.contact_search, True, "black")
        self.contact_surface.blit(search_text, (search_bar.x + 10, search_bar.y + 10))
        ## Render the bar to type the username
        if self.selected_surface == 'contact_surface' and time.time()%1 > 0.5:
            bar = pygame.Rect(search_bar.x + 10 + self.font.size(self.contact_search)[0], search_bar.y + 10, 3, 25)
            pygame.draw.rect(self.contact_surface, self.colors['typing_area_text'], bar)

        # Render the contact list
        contact_list = []
        if self.contact_search != "":
            for i in range(len(self.contacts)):
                if self.contact_search.lower() in self.contacts[str(i)]['username'].lower() and self.contacts[str(i)]['username'].lower() != self.username.lower():
                    contact_list.append(self.contacts[str(i)])
        else:
            for i in range(len(self.contacts)):
                if self.contacts[str(i)]['username'].lower() != self.username.lower():
                    contact_list.append(self.contacts[str(i)])
        contact_list = contact_list[:10]  # Limit to 10 contacts for display

        for contact in contact_list:
            contact_rect = pygame.Rect(10, 120 + contact_list.index(contact) * 60, self.contact_surface.get_width() - 20, 50)
            pygame.draw.rect(self.contact_surface, (255, 255, 255), contact_rect, border_radius=15)
            pygame.draw.rect(self.contact_surface, (0, 0, 0), contact_rect, 2, border_radius=15)
            contact_name = self.font.render(contact['username'], True, "black")
            self.contact_surface.blit(contact_name, (contact_rect.x + 10, contact_rect.y + 10))
            # Check if the contact is hovered
            if contact_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(self.contact_surface, (35, 149, 73), contact_rect, border_radius=15)
                contact_name = self.font.render(contact['username'], True, "white")
                self.contact_surface.blit(contact_name, (contact_rect.x + 10, contact_rect.y + 10))
                if pygame.mouse.get_pressed()[0]:
                    self.choosen_contact = contact['contact_id']
                    self.contact_search = ""
                    self.update_messages()
                    self.scroll = 0
                    self.client.update_file(self.client.socket)


        # Render add contact button
        add_contact_rect = pygame.Rect(10, self.contact_surface.get_height() - 60, 50, 50)
        pygame.draw.rect(self.contact_surface, (35, 149, 73) if 10 <= mouse_x <= 60 and
                         self.contact_surface.get_height() - 60 <= mouse_y <= self.contact_surface.get_height() - 10 else (51, 255, 119), add_contact_rect, border_radius=15)
        add_contact = pygame.image.load(f"./img/add_contact.png").convert_alpha()
        self.contact_surface.blit(add_contact, (add_contact_rect.x, add_contact_rect.y))


        # Render the mouse cursor
        
        if self.choosen_contact != None and mouse_x >= self.contact_surface.get_width() and mouse_x <= self.message_surface.get_width() and mouse_y >= self.message_surface.get_height() - type_area_height and mouse_y <= self.message_surface.get_height():
            pygame.draw.rect(self.message_surface, self.colors['typing_area_border'], type_area, 2, border_radius=15)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            if self.selected_surface != 'message_surface' and pygame.mouse.get_pressed()[0]:
                self.selected_surface = 'message_surface'
        elif 10 <= mouse_x <= self.contact_surface.get_width() - 20 and 60 <= mouse_y <= 110:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            if self.selected_surface != 'contact_surface' and pygame.mouse.get_pressed()[0]:
                self.selected_surface = 'contact_surface'
        elif 10 <= mouse_x <= 60 and self.contact_surface.get_height() - 60 <= mouse_y <= self.contact_surface.get_height() - 10:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
        self.clock.tick(60)

    ## Fonctions Pygame quand l'utilisateur n'est pas connecté
    def enter_username(self):
        while True:
            self.screen.fill((183,188,189))
            self.screen.blit(self.font.render("Quel est votre pseudo ?", True, "black"), (10, 10))
            self.screen.blit(self.font.render(self.message, True, "black"), (10, 50))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.message != "":
                        self.username = self.message
                        self.message = ""
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        self.message = self.message[:-1]
                    else:
                        self.message += event.unicode

    def enter_password(self):
        while True:
            self.screen.fill((183,188,189))
            self.screen.blit(self.font.render("Quel est votre mot de passe ?", True, "black"), (10, 10))
            self.screen.blit(self.font.render(self.message, True, "black"), (10, 50))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.message != "":
                        self.password = self.message
                        self.message = ""
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        self.message = self.message[:-1]
                    else:
                        self.message += event.unicode

    def login(self):
        logged = False
        while not logged:
            self.enter_username()
            self.enter_password()
            self.client = Client(self)
            result = self.client.login(self.username, self.password)
            if result:
                logged = True
                break
    
    ## Fonction principale
    def run(self):
        self.login()
        self.client.update_file(self.client.socket)
        with open(f"./contacts.json", 'r') as file:
            self.contacts = json.load(file)
            file.close()
        self.client.main()
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
    
    def update_messages(self):
        self.messages = {}
        if self.choosen_contact != None:
            with open(f"./contacts.json", 'r') as file:
                self.messages = json.load(file)[self.choosen_contact]['messages']
                file.close()
    
    def save_messages(self):
        with open(f'./contacts.json', 'r+') as file:
                    file.seek(0)
                    data = json.load(file)
                    data[self.choosen_contact]['messages'] = self.messages
                    file.seek(0)
                    json.dump(data, file, indent=2)
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