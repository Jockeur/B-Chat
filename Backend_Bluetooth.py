import bluetooth

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

#Maintenant on commence l'envoi de message
msg=input("Entrez votre message a envoyer:")
client_sock.send(msg)
save_historique(msg)