import socket
from slogging import log
import json
import os

messages={}
with open(f'{os.getcwd()}/messages.json', 'r+') as file:
    messages = json.load(file)

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
    connection, client_address = sock.accept()
    print()
    
    try:
        log(f'Connection from {client_address}')
        
        # Recieve the data in a small chunks and retransmit it
        while True:
            data = connection.recv(16).decode()
            log('received "%s"' % data)
            if data:
                log('Sending data back to the client')
                connection.sendall(data.encode())
                message += data
            else:
                log(f'No more data from {client_address}')
                messages['test'] = message
                with open(f'{os.getcwd()}/messages.json', 'r+') as file:
                    file.seek(0)
                    json.dump(messages, file)
                    file.truncate()
                break
        
    finally:
        # Clean up the connection
        connection.close()