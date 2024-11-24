import sys, socket
from slogging import log

# Créer une connection TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Se connecter au socket sur le port où le serveur écoute
server_address = (sys.argv[1], 10000)
log('Connecting to %s port %s' % server_address)
sock.connect(server_address)

## On peut envoyer et recevoir des data grâce à sock.sendall() et sock.recv() respectivement
## Comme pour le serveur
try:
    # Demander le message à l'utilisateur
    message = input()
    log('sending "%s"' % message)
    # On envoie le message au serveur
    sock.sendall(message.encode())
    
    # Valeurs permettant de check que le serveur à bien reçu toute les data qu'on lui envoie
    amount_received = 0
    amount_expected = len(message.encode())
    
    # Tant qu'on a pas reçu ce qu'on a envoyé, on attend de recevoir
    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        log('received "%s"' % data.decode())

# Quand tout est fini, fermer la connexion
finally:
    log('closing socket')
    sock.close()