import os
import sys, socket, hashlib
import errno

from threading import Thread

from slogging import log
from utils import *

IP = "127.0.0.1"
PORT = 10000
class Client():
    def __init__(self, app):
        self.i_username = app.username
        self.i_password = app.password
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.app = app
        
        self.socket.connect((IP, PORT))
        self.socket.setblocking(False)
        
        
    def main(self):
        self.check_file(self.socket)
        receive_thread = Thread(target=self.receive_message)
        receive_thread.start()
        

    def receive_message(self):
        '''Une boucle vérifiant que l'utilisateur est toujours connecté et enregistre un message si jamais il en a reçu un'''
        while self.app.running:
            try:
                # On essaye de voir si on reçoit un message
                # Nos messages commencerons toujours par l'operation ID pour savoir quelle opération effectuer
                operation_id = receive_op_id(self.socket)
                print('Op id : ' + str(operation_id))
                    
                # Sinon c'est qu'on a quelque chose !
                # Alors on effectue l'opération adéquate
                if operation_id == SENDING_MESSAGE:
                    self.process_message(self.socket)
                # Si on ne reçoit rien, c'est que la connection a été fermée (socket.close() ou socket.shutdown(socket.SHUT_RDWR))
                elif operation_id == False:
                    log('Connection fermée par le serveur')
                    # Alors on stop le programme
                    self.socket.close()
                    self.app.running = False
                    sys.exit()
            
            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data, error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    self.app.running = False
                    self.socket.close()
                    sys.exit()
                    
                # Else we can just continue since we just didn't receive anything
                continue
            
            except Exception as e:
                # Il s'est passé autre chose, STOP !
                print('Reading error : {}'.format(str(e)))
                self.app.running = False
                self.socket.close()
                sys.exit()


    def process_message(self, s: socket.socket):
        message = get_message(s)        
        self.app.register_message(message['username']['data'].decode('utf-8').strip(), message['message']['data'].decode('utf-8').strip())


    def send_message(self, message):
        # ki ki l'a envoyé
        username_header = f"{len(self.i_username):<{HEADER_LENGTH}}".encode('utf-8')
        username = self.i_username.encode('utf-8')
        
        message = message.encode('utf-8')
        # On détermine son header (la taille du message en gros)
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        op_header = f"{SENDING_MESSAGE:<{HEADER_LENGTH}}".encode('utf-8')
        # On envoie le tout au serveur
        self.socket.send(op_header + username_header + username + message_header + message)
        

    def send_username(self):
        username = self.i_username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        self.socket.send(username_header + username)


    def login(self, username: str, password: str):
        username = username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        password = password.encode('utf-8')
        password_header = f"{len(password):<{HEADER_LENGTH}}".encode('utf-8')

        self.socket.send(username_header + username + password_header + password)
        
        while True:
            try:
                return receive_op_id(self.socket) == ACCESS_GRANTED
            except BlockingIOError:
                continue

    
    def check_file(self, s: socket.socket):
        print("Check file")
        s.setblocking(True)
        file = open(f'{os.getcwd()}/messages.json', 'r')
        file_hash = hashlib.md5(file.read().encode('utf-8')).hexdigest()

        op_id = f"{CHECK_FILE:<{HEADER_LENGTH}}".encode('utf-8')
        header = f"{len(file_hash):<{HEADER_LENGTH}}".encode('utf-8')
        s.send(op_id + header + file_hash.encode('utf-8'))
        
        response = int(s.recv(HEADER_LENGTH).decode('utf-8').strip())
        print(response == FILE_CORRECT)
        if response == FILE_CORRECT:
            return True
        elif response == FILE_INCORRECT:
            print("updating file")
            f = open(f"{os.getcwd()}/messages.json", "w")
            file_length = s.recv(HEADER_LENGTH)
            f.write(s.recv(int(file_length.decode('utf-8').strip())).decode('utf-8'))
            f.close()
        s.setblocking(False)


    def update_file(self, s: socket.socket):
        op_id = f"{UPDATE_FILE:<{HEADER_LENGTH}}".encode('utf-8')
        s.send(op_id)

        l = s.recv(HEADER_LENGTH)
        length = int(l.decode('utf-8').strip())
        data = s.recv(length)
        with open(f'{os.getcwd}/message_client.json', 'w') as f:
            f.write(data.decode('utf-8'))