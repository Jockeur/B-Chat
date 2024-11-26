import json, socket
import threading

from utils import *
from slogging import *

def process_connection(s: socket.socket, client_address: str, data_file: str):
    try:
        log(f'Connection from {client_address}')
        
        # Dans une boucle infin attendre de recevoir des informations du client
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
                    
                # Si cet ID est 1 (FETCH_ID), le client veut récupérer les messages
                elif data_id == FETCH_ID:
                    # On envoie les messages à l'utilisateur
                    send_messages(s, f'{os.getcwd()}/messages.json')
                
                    
            # Si le client se déconecte, on sort de la boucle
            else:
                log(f'No more data from {client_address}')
                break
        
    finally:
        # Clean up the connection
        s.close()