import sys, socket
from slogging import log

from utils import *

# Créer une connection TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se connecter au socket sur le port où le serveur écoute
server_address = (sys.argv[1], 10000)
log('Connecting to %s port %s' % server_address)
sock.connect(server_address)

## On peut envoyer et recevoir des data grâce à sock.sendall() et sock.recv() respectivement
## Comme pour le serveur
try:
    messages_file = f'{os.getcwd()}/message_client.json'
    # On demande les messages au serveur
    fetch_messages(sock, messages_file)
    print_messages(messages_file)
    # Demander le message à l'utilisateur
    message = str(SEND_ID) + input('> ')
    log('sending "%s"' % message)
    # On envoie le message au serveur
    sock.sendall(message.encode())
    fetch_messages(sock, messages_file)


# Quand tout est fini, fermer la connexion
finally:
    log('closing socket')
    sock.close()