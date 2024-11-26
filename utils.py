from slogging import log
import json
import os
import socket

SEND_ID = 0
FETCH_ID = 1

# Fonctions pour le client
def fetch_messages(s: socket.socket, messages_file):
    s.sendall("1".encode())
    datas = s.recv(1024).decode()
    data = json.loads(datas)
    with open(messages_file, 'w+') as file:
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        
def send_message(message: str, s: socket.socket):
    s.sendall(message.encode())
    
def print_messages(file):
    messages = {}
    with open(file, 'r') as f:
        messages = json.load(f)
    for i in messages['messages']:
        log(messages['messages'][i]['message'])
    
    
# Fonctions pour le serveur
def register_message(message, file):
    with open(file, 'r+') as f:
        messages:dict = json.load(f)
        message_id = int(list(messages['messages'].keys())[-1]) + 1
        messages['messages'][str(message_id)] = {'message': message, 'sender_id': 1}
        f.seek(0)
        json.dump(messages, f, indent=4)
        f.truncate()
        
def send_messages(s: socket.socket, file):
    messages = ""
    with open(file, 'r') as f:
        messages = json.dumps(json.load(f))
        s.sendall(messages.encode())
        