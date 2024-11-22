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
    message = input()
    log('sending "%s"' % message)
    sock.sendall(message.encode())
    
    # En attente de réponse
    amount_received = 0
    amount_expected = len(message.encode())
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        log('received "%s"' % data.decode())
        
finally:
    log('closing socket')
    sock.close()