import socket
import threading

def receive_messages(client socket):
  while true:
    try:
      message = client_socket.recv(1024).decode('utf-8')
      if message:
        print(messsage)
      else:
        break
