import bluetooth
import time
import threading
from pynput import keyboard

#Ici on recherche tout les Appareils Bluetooth Environnant
nearby_devices=bluetooth.discover_devices(duration=15, lookup_names=True, flush_cache=True, lookup_class=True)
print(f"Appareils Bluetooth trouvés: {nearby_devices}")

#Ici on établi le Socket Bluetooth
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

#Ici on va mettre le port socket en écoute pour pouvoir recevoir les messages
port=bluetooth.PORT_ANY
server_sock.bind(("",port))
server_sock.listen(1)
print(f"En attente de connexion sur le port {port}...")

#Ici on accepte la connection entrante
print("En attente de connexion...")
client_sock, client_info=server_sock.accept()
print(f"Connexion accepté de {client_info}")

#Ici on régle la réception de data
data=client_sock.recv(1024)
print(f"Données Reçues: {data}")

#Maintenant on va garder l'historique des messages
historique=[]
def save_historique(msg):
        historique.append(msg)

#Maintenant on définit notre pseudo
username=input("Écrivez votre Pseudo: ")

#Maintenant on commence l'envoi de message
def sending_messages():
        while True:
                msg=input("Entrez votre message a envoyer:")
                client_sock.send((username + ": " + msg).encode())
                save_historique(msg)

#Ici on règle les indicateurs "Est en train d'écrire"
keyboard_in_use=False
user_writing_active_state=False
last_key_event_time=0
def on_press(key):
        global keyboard_in_use
        keyboard_in_use=True
        last_key_event_time=time.time()
def on_release(key):
        global keyboard_in_use
        keyboard_in_use=False
        last_key_event_time=time.time()
def check_keyboard_activity():
        global user_writing_active_state
        while True:
                current_time=time.time()
                if (current_time - last_key_event_time)<1:
                        user_writing_active_state=True
                else:
                        user_writing_active_state=False
                time.sleep(0.1)
def send_typing_indicator():
        while True:
                if user_writing_active_state:
                        typing_indicator=((username + " is typing...").encode())
                        client_sock.send(typing_indicator)
                time.sleep(0.5)

#On commence l'écouteur de clavier
listener=keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

#On commence la function check_keyboard_activity dans un threads distinct
keyboard_activity_thread = threading.Thread(target=check_keyboard_activity)
keyboard_activity_thread.start()

#On commence la function sending_messages_thread dans un threads distinct
sending_messages_thread = threading.Thread(target=sending_messages)
sending_messages_thread.start()

#On commence la function send_typing_indicator dans un threads distinct
typing_indicator_thread=threading.Thread(target=send_typing_indicator)
typing_indicator_thread.start()

#On garde les écouteurs actives
listener.join()
keyboard_activity_thread.join()
typing_indicator_thread.join()
sending_messages_thread.join()