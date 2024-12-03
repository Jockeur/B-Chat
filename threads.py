import json, socket
import threading

from utils import *
from slogging import *


# Client Threads
def send_message(s: socket.socket):
    while True:
        try:
            message = str(SEND_ID) + input()
            s.sendall(message.encode())
        except Exception as e:
            print(f'Error -> {e}')
            s.close()
            break
        
def receive_message(s: socket.socket):
    while True:
        try:
            message = s.recv(1024).decode()
            print(message)
        except Exception as e:
            print(f'Error -> {e}')
            s.close()
            break


# Server Threads
def process_connection(s: socket.socket, client_address: str, data_file: str):
    try:
        log(f'Connection from {client_address}')
        
        # Dans une boucle infinie attendre de recevoir des informations du client
        while True:
            # Attendre les données du client
            data:str = s.recv(1024).decode()
            log('received "%s"' % data)
            # Si le client a envoyé des données
            if data:
                # L'id du "paquet" utilisé est le premier caractère de notre message reçu venant du client
                data_id = int(data[0])
                
                # Si cet ID est 0 (SEND_ID), le client nous envoie un message
                if data_id == SEND_ID:
                    # On enregistre le messages dans le fichier messages.json
                    register_message(data[1:], f'{os.getcwd()}/messages.json')
                    
                    # Et on le renvoie à tout les autres
                    
                    
                # Si cet ID est 1 (FETCH_ID), le client veut récupérer les messages
                elif data_id == FETCH_ID:
                    # On envoie les messages à l'utilisateur
                    pass
                
                    
            # Si le client se déconecte, on sort de la boucle
            else:
                log(f'No more data from {client_address}')
                break
        
    finally:
        # Clean up the connection
        s.close()