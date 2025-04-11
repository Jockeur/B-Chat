import json
import os
import select
import socket
import utils
import hashlib

from slogging import log
from utils import SENDING_MESSAGE, ACCESS_DENIED, ACCESS_GRANTED, HEADER_LENGTH, receive_op_id, get_message
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
                    (logging, username) = self.check_login(client_socket)

                    if logging:
                        # On ajoute le nouveau client à notre liste de clients
                        self.socket_list.append(client_socket)
                        self.clients[client_socket] = {'address': client_address, 'username': username['data']}
                        log(f"Nouvelle connexion de {client_address}")
                    else:
                        log(f"Connection refusée de {client_address}")
                        client_socket.close()

                # Si le socket n'est pas le serveur, alors qq'un essaye de nous envoyer un message
                else:
                    operation_id = receive_op_id(notified_socket)
                    
                    match operation_id:
                        case False:
                            log(f"Connection fermée de {self.clients[notified_socket]['username'].decode('utf-8')}")
                            self.delete_client(notified_socket)
                        case utils.SENDING_MESSAGE:
                            self.process_message(notified_socket)
                        case utils.CHECK_FILE:
                            print("Check file")
                            self.check_file(notified_socket)
                            
            # On peut maintenant s'occuper des sockets en erreur (les sockets qui se sont déconectés)
            for notified_socket in error_sockets:
                self.delete_client(notified_socket)

        
    def process_message(self, s: socket.socket):
        message_infos = get_message(s)
        # On vérifie d'abord que le client ne se soit pas déconnecté
        if message_infos == False:
            log(f"Connection fermée de {self.clients[s]['data'].decode('utf-8')}")
            self.delete_client(s)

            return
                    
        username = message_infos['username']
        message = message_infos['message']
        log(f"Message reçu de {username['data'].decode('utf-8')}: {message['data'].decode('utf-8').strip()}")
        
        with open(f'{os.getcwd()}/messages.json', 'r+') as file:
            file.seek(0)
            data = json.load(file)
            m_id = str(len(list(data.values())))
            data[m_id] = {}
            data[m_id]["sender"] = username['data'].decode('utf-8')
            data[m_id]["message"] = message['data'].decode('utf-8').strip()
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
                    
        # Le renvoyer à tout le monde
        for client in self.clients:
            # Par contre on le renvoit pas à l'envoyeur
            if client != s:
                op_header = f"{SENDING_MESSAGE:<{HEADER_LENGTH}}".encode('utf-8')
                client.sendall(op_header + username['header'] + username['data'] + message['header'] + message['data'])

    
    def check_login(self, s: socket.socket):
        username_header = s.recv(HEADER_LENGTH)
        # Si le client s'est déconnecté
        if not len(username_header):
            return False
        username = {'header': username_header, 'data': s.recv(int(username_header.decode('utf-8').strip()))}

        password_header = s.recv(HEADER_LENGTH)
        # Si le client s'est déconnecté
        if not len(password_header):
            # On passe à la suite (ignorer la suite de la boucle)
            return False
        password = {'header': password_header, 'data': s.recv(int(password_header.decode('utf-8').strip())).decode('utf-8').strip()}

        # On vérifie dans notre DB si le client est bien inscrit
        # Nos utilisateurs son stockés dans un fichier json (voir utils.py)
        print(username['data'].decode('utf-8').strip() + " " + password['data'])
        with open(f'{os.getcwd()}/users.json', 'r') as file:
            users = json.load(file)
            for id in users:
                if users[id]['username'] == username['data'].decode('utf-8').strip() and users[id]['password'] == password['data']:
                    op_header = f"{ACCESS_GRANTED:<{HEADER_LENGTH}}".encode('utf-8')
                    s.sendall(op_header)
                    return (True, username)
        # Si on arrive ici, c'est que le client n'est pas inscrit
        op_header = f"{ACCESS_DENIED:<{HEADER_LENGTH}}".encode('utf-8')
        s.sendall(op_header)
        return (False, username)
    
    
    # On peut vérifier si les deux fichier correspondent grâce à un hash de ces derniers
    def check_file(self, s: socket.socket):
        s.setblocking(True)
        hash_header = s.recv(HEADER_LENGTH)
        if not hash_header:
            self.delete_client(s)
        
        # Hash du fichier envoyé par le client
        file_hash = s.recv(int(hash_header.decode("utf-8").strip()))
        log(f"Hash reçu de {self.clients[s]['username'].decode('utf-8')}: {file_hash.decode('utf-8').strip()}")
        # Hash du server
        og_file_hash = hashlib.md5(open(f'{os.getcwd()}/messages.json', 'r').read().encode('utf-8')).hexdigest()
        if og_file_hash == file_hash.decode('utf-8'):
            op_header = f"{utils.FILE_CORRECT:<{HEADER_LENGTH}}".encode('utf-8')
            s.sendall(op_header)
        else:
            op_header = f"{utils.FILE_INCORRECT:<{HEADER_LENGTH}}".encode('utf-8')
            s.sendall(op_header)
            # On envoie le fichier
            with open(f'{os.getcwd()}/messages.json', 'r') as f:
                message = f.read()
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                print(message_header)
                s.sendall(message_header)
                s.sendall(message.encode('utf-8'))
                f.close()
        s.setblocking(False)
        
    
    def delete_client(self, s: socket.socket):
        self.socket_list.remove(s)
        del self.clients[s]
            
        
Server()