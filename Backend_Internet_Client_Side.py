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
