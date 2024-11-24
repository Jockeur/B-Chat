import socket
from slogging import log
import json
import os

messages = {}
# Créer une connection TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
log('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    message=""
    # Wait for a connection
    log('Waiting for a connection...')
    # Quand la connexion est accepté récupérer le socket dans connection et l'addresse dans client_address
    connection, client_address = sock.accept()
    
    try:
        log(f'Connection from {client_address}')
        
        # Dans une boucle infin attendre de recevoir des informations du client
        while True:
            # Attendre les données du client
            data = connection.recv(1024).decode()
            log('received "%s"' % data)
            # Si le client a envoyé des données
            if data:
                # On renvoit la data au client
                log('Sending data back to the client')
                connection.sendall(data.encode())
                
                # On enregistre le messages dans le fichier messages.json
                message += data
                with open(f'{os.getcwd()}/messages.json', 'r+') as file:
                    messages:dict = json.load(file)
                    message_id = int(list(messages['messages'].keys())[-1]) + 1
                    messages['messages'][str(message_id)] = {'message': message, 'sender_id': 1}
                    print(messages)
                    file.seek(0)
                    json.dump(messages, file, indent=4)
                    file.truncate()
            # Si le client se déconecte, on sort de la boucle
            else:
                log(f'No more data from {client_address}')
                break
        
    finally:
        # Clean up the connection
        connection.close()