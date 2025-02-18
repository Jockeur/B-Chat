import select
import socket
from slogging import log

HEADER_LENGTH = 10
class Server():
    def __init__(self):
        # L'addresse et le port de connexion du serveur
        self.HOST = '0.0.0.0'
        self.PORT = 10000
        
        self.socket: socket.socket
        
        # La liste de tous les socket_list connectés à notre serveur
        self.socket_list = []
        self.clients = {}
        self.start()
    
    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log('starting up on %s port %s' % (self.HOST, self.PORT))
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen(1)
        
        self.socket_list.append(self.socket)
        
        while True:
        
            # On récupère nos sockets prêts (qui on des donnés à envoyer) et ceux en erreur
            read_sockets, _, error_sockets = select.select(self.socket_list, [], self.socket_list)
            
            # On regarde tous nos sockets prêts
            for notified_socket in read_sockets:
                # Si le socket est notre serveur, c'est qu'un client essaye de se connecter
                if notified_socket == self.socket:
                    client_socket, client_address = self.socket.accept()
                    username = self.receive_message(client_socket)
                    # Si le client s'est déconnecté
                    if username == False:
                        # On passe à la suite (ignorer la suite de la boucle)
                        continue
                    
                    # On ajoute notre socket à notre list de socket
                    self.socket_list.append(client_socket)
                    
                    # On ajoute notre client à notre clien_list
                    self.clients[client_socket] = username
                    log(f"Connection acceptée venant de {client_address[0]}:{client_address[1]}, nom {username['data'].decode('utf-8')}")
                # Si le socket n'est pas le serveur, alors qq'un essaye de nous envoyer un message
                else:
                    message = self.receive_message(notified_socket)
                    # On vérifie d'abord que le client ne s'est pas déconnecté
                    if message == False:
                        print(f"Connection fermée de {self.clients[notified_socket]['data'].decode('utf-8')}")
                        self.socket_list.remove(notified_socket)
                        del self.clients[notified_socket]
                        
                        continue
                    
                    username = self.clients[notified_socket]
                    print(f"Message reçu de {username['data'].decode('utf-8')}: {message['data'].decode('utf-8').strip()}")
                    
                    # Le renvoyer à tout le monde parce qu'on est gentil et qu'on aime partager les choses 🥰 (j'vais cabler frr)
                    for client in self.clients:
                        # Par contre on le renvoit pas à l'envoyeur ça c'est pas gentil 🥲
                        if client != notified_socket:
                            client.sendall(username['header'] + username['data'] + message['header'] + message['data'])
                            
            # On peut maintenant s'occuper des sockets en erreur (les connards qui se sont déconectés)
            for notified_socket in error_sockets:
                self.socket_list.remove(notified_socket)
                del self.clients[notified_socket]
                
    def broadcast_message(self, message: str, sender: socket.socket):
        for c in self.clients:
            print(c)
        
    def receive_message(self, s: socket.socket):
        try:
            message_header = s.recv(HEADER_LENGTH)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())

            return {'header': message_header, 'data': s.recv(message_length)}

        except:
            return False
        
Server()