import socket
import threading

def receive_messages(client_socket):
  while True:
    try:
      message = client_socket.recv(1024).decode('utf-8')
      if message:
        print(message)
      else:
        break
    finally:
      pass

# Pour envoyer les messages, faut mettre sur le Front End maintenant
def send_messages(client_socket):
  while True:
        message = input("Enter your message: ")
        if message:
            client_socket.sendall(message.encode('utf-8'))
        else:
            break
