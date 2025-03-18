import bluetooth
import time
import threading
from pynput import keyboard

# Server address and port from your server output
server_address = "F4:CE:23:FA:42:99"  # Replace with your server's Bluetooth address
port = 4  # Replace with the port your server bound to (e.g., 4)

# Create the client socket
client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Connect to the server
print(f"Tentative de connexion à {server_address} sur le port {port}...")
try:
    client_sock.connect((server_address, port))
    print("Connecté au serveur!")
except Exception as e:
    print(f"Erreur de connexion: {e}")
    client_sock.close()
    exit(1)

# Message history
historique = []
def save_historique(msg):
    historique.append(msg)

# Receive messages in a separate thread
def receive_messages():
    while True:
        try:
            data = client_sock.recv(1024)
            if data:
                print(f"Reçu du serveur: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Erreur lors de la réception: {e}")
            break

# Set up username
username = input("Écrivez votre pseudo: ")

# Send messages
def sending_messages():
    while True:
        msg = input("Entrez un message à envoyer au serveur: ")
        try:
            client_sock.send((username + ": " + msg).encode('utf-8'))
            save_historique(msg)
        except Exception as e:
            print(f"Erreur lors de l'envoi: {e}")
            break

# Typing indicator logic
keyboard_in_use = False
user_writing_active_state = False
last_key_event_time = 0

def on_press(key):
    global keyboard_in_use, last_key_event_time
    keyboard_in_use = True
    last_key_event_time = time.time()

def on_release(key):
    global keyboard_in_use, last_key_event_time
    keyboard_in_use = False
    last_key_event_time = time.time()

def check_keyboard_activity():
    global user_writing_active_state
    while True:
        current_time = time.time()
        if (current_time - last_key_event_time) < 1:
            user_writing_active_state = True
        else:
            user_writing_active_state = False
        time.sleep(0.1)

def send_typing_indicator():
    while True:
        if user_writing_active_state:
            try:
                typing_indicator = (username + " is typing...").encode('utf-8')
                client_sock.send(typing_indicator)
            except Exception as e:
                print(f"Erreur lors de l'envoi de l'indicateur: {e}")
                break
        time.sleep(0.5)

# Start keyboard listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Start threads
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

keyboard_activity_thread = threading.Thread(target=check_keyboard_activity)
keyboard_activity_thread.start()

sending_messages_thread = threading.Thread(target=sending_messages)
sending_messages_thread.start()

typing_indicator_thread = threading.Thread(target=send_typing_indicator)
typing_indicator_thread.start()

# Keep the main thread alive
try:
    listener.join()
    receive_thread.join()
    keyboard_activity_thread.join()
    sending_messages_thread.join()
    typing_indicator_thread.join()
except KeyboardInterrupt:
    print("Déconnexion...")
finally:
    client_sock.close()