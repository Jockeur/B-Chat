import socket

HEADER_LENGTH = 10

## Operations IDs
SENDING_MESSAGE = 1
CHECK_FILE = 2
EOF = 3
FILE_CORRECT = 4
FILE_INCORRECT = 5
UPDATE_FILE = 6
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

            contact_id_header = s.recv(HEADER_LENGTH)
            if not len(contact_id_header):
                return False
            contact_id = s.recv(int(contact_id_header.decode('utf-8').strip()))

            message_header = s.recv(HEADER_LENGTH)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())
            message = s.recv(message_length)

            return {'username': {'header': username_header, 'data': username},'message': {'header': message_header, 'data': message}, 'contact_id': {'header': contact_id_header, 'data': contact_id}}

        except:
            return False