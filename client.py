import sys, socket
import errno

from threading import Thread

from slogging import log

HEADER_LENGTH = 10

SENDING_MESSAGE = 1

IP = ""
PORT = 10000
class Client():
    def __init__(self, app):
        self.i_username = app.username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.app = app
        
        self.socket.connect((IP, PORT))
        self.socket.setblocking(False)
        self.send_username()
        self.main()
        
        
    def main(self):
        receive_thread = Thread(target=self.receive_message)
        receive_thread.start()
        
    def receive_message(self):
        '''Une boucle vérifiant que l'utilisateur est toujours connecté et enregistre un message si jamais il en a reçu un'''
        while self.app.running:
            try:
                # On essaye de voir si on reçoit un message
                # Nos messages commencerons toujours par le header du pseudo de notre envoyeur
                username_header = self.socket.recv(HEADER_LENGTH)
                
                # Si on ne reçoit rien, c'est que la connection a été fermée (socket.close() ou socket.shutdown(socket.SHUT_RDWR))
                if not len(username_header):
                    log('Connection fermée par le serveur')
                    # Alors on stop le programme
                    sys.exit()
                    
                # Sinon c'est qu'on a quelque chose !
                # Alors on récupère le username
                username_length = int(username_header.decode('utf-8').strip())
                username = self.socket.recv(username_length).decode('utf-8')
                
                # Puis le message
                message_header = self.socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = self.socket.recv(message_length).decode('utf-8')
                
                self.app.register_message(username, message)
            
            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data, error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                    
                # Else we can just continue since we just didn't receive anything
                continue
            
            except Exception as e:
                # Il s'est passé autre chose, STOP !
                print('Reading error : {}'.format(str(e)))
                sys.exit()

    def send_message(self, message):
        # ki ki l'a envoyé
        username_header = f"{len(self.i_username):<{HEADER_LENGTH}}".encode('utf-8')
        
        message = message.encode('utf-8')
        # On détermine son header (la taille du message en gros)
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        op_header = f"{SENDING_MESSAGE:<{HEADER_LENGTH}}".encode('utf-8')
        # On envoie le tout au serveur
        self.socket.send(op_header + message_header + message)
        
    def send_username(self):
        username = self.i_username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        self.socket.send(username_header + username)