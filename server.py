import socket
from slogging import log
import json
import os
import threading

from threads import process_connection
from utils import *

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
    
    # Envoyer la connexion dans un thread afin de pouvoir accepter de nouvelles connexions
    log('Entering thread for ' + str(client_address))
    t_conn = threading.Thread(target=process_connection, args=(connection, client_address, f'{os.getcwd}/messages.json'))
    t_conn.start()