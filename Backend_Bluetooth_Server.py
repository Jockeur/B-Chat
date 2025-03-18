import bluetooth
import time
import threading
from pynput import keyboard

# Discover nearby Bluetooth devices
print("Veuillez attendre un instant le temps que nous scannions des appareils Bluetooth environnants...")
nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True, flush_cache=True, lookup_class=True)
print(f"Appareils Bluetooth trouvés: {nearby_devices}")

# Get the local Bluetooth adapter address
try:
    local_address_list = bluetooth.read_local_bdaddr()  # Returns a list
    local_address = local_address_list[0]  # Extract the first (and only) address as a string
    print(f"Adresse Bluetooth locale: {local_address}")
except Exception as e:
    print(f"Erreur lors de la récupération de l'adresse locale: {e}")
    exit(1)

# Create the Bluetooth server socket
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# Bind to the local address with dynamic port (port 0)
try:
    server_sock.bind((local_address, 0))  # Use the string address, port 0 for dynamic assignment
    actual_port = server_sock.getsockname()[1]  # Get the assigned port
    print(f"Socket lié à l'adresse {local_address} sur le port {actual_port}")
except Exception as e:
    print(f"Erreur lors de la liaison du socket: {e}")
    server_sock.close()
    exit(1)

# Start listening for connections
server_sock.listen(1)
print(f"En attente de connexion sur le port {actual_port}...")

# Accept incoming connection
print("En attente de connexion...")
try:
    client_sock, client_info = server_sock.accept()
    print(f"Connexion acceptée de {client_info}")
except Exception as e:
    print(f"Erreur lors de l'acceptation de la connexion: {e}")
    server_sock.close()
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
                print(f"Données reçues: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Erreur lors de la réception: {e}")
            break

# Set up username
username = input("Écrivez votre pseudo: ")

# Send messages
def sending_messages():
    while True:
        msg = input("Entrez votre message à envoyer: ")
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
    print("Arrêt du programme...")
finally:
    client_sock.close()
    server_sock.close()