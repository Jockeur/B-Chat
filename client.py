import sys, socket
import threading

from slogging import log
from threads import *
from utils import *

# Créer une connection TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = input('Quelle est l\'addresse du serveur ? > ')

# Se connecter au socket sur le port où le serveur écoute
server_address = ('127.0.0.1', 10000)
log('Connecting to %s port %s' % server_address)
sock.connect(server_address)

pseudo = input('Quel est votre pseudo ? > ')
sock.sendall(pseudo.encode())

# On délegue le travail à deux Threads : Un qui reçoit les messages, l'autre qui les envoie
receive_thread = threading.Thread(target=receive_message, args=(sock,))
send_thread = threading.Thread(target=send_message, args=(sock,))

try:
    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()
except Exception as e:
    print(f'Error -> {e}')
    
sock.close()