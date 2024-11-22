import socket
import sys
from logging import *

# Créer une connection TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
log('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    log('Waiting for a connection...')
    connection, client_address = sock.accept()
    print()
    
    try:
        log(f'Connection from {client_address}')
        
        # Recieve the data in a small chunks and retransmit it
        while True:
            data = connection.recv(16).decode()
            log('recieved "%s"' % data)
            if data:
                log('Sending data back to the client')
                connection.sendall(data.encode())
            else:
                log(f'No more data from {client_address}')
                break
        
    finally:
        # Clean up the connection
        connection.close()