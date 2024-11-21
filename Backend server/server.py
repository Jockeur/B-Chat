import socket
import sys

# Créer une connection TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print ('starting up on %s port %s' % server_address, file=sys.stderr)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('Waiting for a connection...', file=sys.stderr)
    connection, client_address = sock.accept()
    
    try:
        print('Connection from ', client_address, file=sys.stderr)
        
        # Recieve the data in a small chunks and retransmit it
        while True:
            data = connection.recv(16).decode()
            print('recieved "%s"' % data)
            if data:
                print('Sending data back to the client', file=sys.stderr)
                connection.sendall(data.encode())
            else:
                print('No more data from ', client_address, file=sys.stderr)
                break
        
    finally:
        # Clean up the connection
        connection.close()