import socket

HEADER_LENGTH = 10

## Operations IDs
SENDING_MESSAGE = 1
ACCESS_DENIED = 403
ACCESS_GRANTED = 200

'''Fonctions communes au server et au client'''
def receive_op_id(s: socket.socket):
        try:
            op_header = s.recv(HEADER_LENGTH)

            if not len(op_header):
                return False
                
            return int(op_header.decode('utf-8').strip())
        except ConnectionResetError:
            return False

def get_message(s: socket.socket):
        try:
            username_header = s.recv(HEADER_LENGTH)

            if not len(username_header):
                 return False
            
            username_length = int(username_header.decode('utf-8').strip())
            username = s.recv(username_length)

            message_header = s.recv(HEADER_LENGTH)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())
            message = s.recv(message_length)

            return {'username': {'header': username_header, 'data': username},'message': {'header': message_header, 'data': message}}

        except:
            return False