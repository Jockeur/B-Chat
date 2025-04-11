import bluetooth
import time
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Label, messagebox
from pynput import keyboard

# App Logic (Moved up to avoid NameError)
client_sock = None  # Client socket for outgoing connections
server_sock = None  # Server socket for listening
server_client_sock = None  # Socket for accepted client (server mode)
historique = []
username = ""

def save_historique(msg):
    historique.append(msg)

def update_status(text):
    status_label.config(text=text)
    root.update()

def receive_messages(sock, source):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                decoded = data.decode('utf-8')
                if "is typing..." in decoded:
                    typing_label.config(text=decoded, highlightbackground="#00FF00", highlightcolor="#00FF00")
                else:
                    chat_display.insert(tk.END, f"{source}: {decoded}\n")
                    typing_label.config(text="", highlightbackground="#2E2E2E", highlightcolor="#2E2E2E")
        except Exception as e:
            chat_display.insert(tk.END, f"Erreur réception ({source}): {e}\n")
            break

def start_app():
    global username
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Error", "Username cannot be empty!")
        return
    username_frame.grid_forget()  # Hide username frame after starting
    connect_button.config(state=tk.NORMAL)
    send_button.config(state=tk.NORMAL)
    status_label.config(text="Starting server and ready to connect...")
    threading.Thread(target=run_server, daemon=True).start()

# Server Logic
def run_server():
    chat_display.insert(tk.END, "Scanning for devices...\n")
    nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True, flush_cache=True, lookup_class=True)
    chat_display.insert(tk.END, f"Appareils trouvés: {nearby_devices}\n")

    try:
        local_address_list = bluetooth.read_local_bdaddr()
        local_address = local_address_list[0]
        chat_display.insert(tk.END, f"Adresse locale: {local_address}\n")
    except Exception as e:
        chat_display.insert(tk.END, f"Erreur adresse locale: {e}\n")
        root.destroy()
        return

    global server_sock
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
        server_sock.bind((local_address, 0))
        actual_port = server_sock.getsockname()[1]
        update_status(f"Listening on {local_address} port {actual_port}")
        chat_display.insert(tk.END, f"Lié à {local_address} sur port {actual_port}\n")
    except Exception as e:
        chat_display.insert(tk.END, f"Erreur liaison: {e}\n")
        server_sock.close()
        root.destroy()
        return

    server_sock.listen(1)
    chat_display.insert(tk.END, "En attente de connexion...\n")
    while True:
        try:
            global server_client_sock
            server_client_sock, client_info = server_sock.accept()
            chat_display.insert(tk.END, f"Connecté à {client_info}\n")
            update_status(f"Connected to {client_info[0]} (Server)")
            threading.Thread(target=receive_messages, args=(server_client_sock, "Server"), daemon=True).start()
        except Exception as e:
            chat_display.insert(tk.END, f"Erreur connexion: {e}\n")
            break

# Client Logic
def connect_to_server():
    global client_sock
    server_address = server_entry.get()
    port = int(port_entry.get())
    chat_display.insert(tk.END, f"Connexion à {server_address} sur port {port}...\n")
    client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
        client_sock.connect((server_address, port))
        chat_display.insert(tk.END, "Connecté au serveur!\n")
        update_status(f"Connected to {server_address} (Client)")
        connect_button.config(state=tk.DISABLED)
        threading.Thread(target=receive_messages, args=(client_sock, "Client"), daemon=True).start()
    except Exception as e:
        chat_display.insert(tk.END, f"Erreur connexion: {e}\n")
        client_sock.close()
        update_status("Connection failed")

# GUI Setup
root = tk.Tk()
root.title("Bluetooth Chat")
root.state('zoomed')  # Maximized window, adapts to screen size, taskbar visible
root.configure(bg="#080808")  # Dark mode background

# Make the grid responsive
root.grid_rowconfigure(3, weight=1)  # Chat area expands
root.grid_columnconfigure(0, weight=1)

# Username input (initially active)
username_frame = tk.Frame(root, bg="#080808")
username_frame.grid(row=0, column=0, columnspan=3, padx=20, pady=10)
tk.Label(username_frame, text="Choose Username:", bg="#080808", fg="#FFFFFF", font=("Arial", 12)).grid(row=0, column=0, padx=5, sticky="e")
username_entry = Entry(username_frame, width=30, bg="#080808", fg="#FFFFFF", insertbackground="white", font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=5, pady=10, sticky="w")
start_button = Button(username_frame, text="Start Chat", bg="#080808", fg="#FFFFFF", font=("Arial", 12), command=start_app, state=tk.NORMAL)
start_button.grid(row=0, column=2, padx=5, pady=10)

# Connection inputs (always visible)
connect_frame = tk.Frame(root, bg="#080808")
connect_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10)
server_label = Label(connect_frame, text="Server Address:", bg="#080808", fg="#FFFFFF", font=("Arial", 12))
server_label.grid(row=0, column=0, padx=20, pady=10, sticky="e")
server_entry = Entry(connect_frame, width=30, bg="#080808", fg="#FFFFFF", insertbackground="white", font=("Arial", 12))
server_entry.insert(0, "F4:CE:23:FA:42:99")
server_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
port_label = Label(connect_frame, text="Port:", bg="#080808", fg="#FFFFFF", font=("Arial", 12))
port_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")
port_entry = Entry(connect_frame, width=10, bg="#080808", fg="#FFFFFF", insertbackground="white", font=("Arial", 12))
port_entry.insert(0, "4")
port_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
connect_button = Button(connect_frame, text="Connect", bg="#080808", fg="#FFFFFF", font=("Arial", 12), state=tk.DISABLED, command=connect_to_server)
connect_button.grid(row=1, column=2, padx=10, pady=10)

# Chat display
chat_display = scrolledtext.ScrolledText(root, width=80, height=25, wrap=tk.WORD, bg="#080808", fg="#FFFFFF", insertbackground="white")
chat_display.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

# Status label
status_label = Label(root, text="Enter username to begin", font=("Arial", 12), bg="#080808", fg="#FFFFFF")
status_label.grid(row=4, column=0, columnspan=3, padx=20, pady=5, sticky="ew")

# Typing indicator
typing_label = Label(root, text="", font=("Arial", 12, "italic"), bg="#080808", fg="#BBBBBB")
typing_label.grid(row=5, column=0, columnspan=3, padx=20, pady=5, sticky="ew")

# Message input
message_entry = Entry(root, width=60, bg="#080808", fg="#FFFFFF", insertbackground="white", font=("Arial", 12))
message_entry.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

# Send button
def send_message(event=None):  # Supports Enter key
    msg = message_entry.get().strip()
    if msg and (client_sock or server_client_sock):
        try:
            # Send to all connected sockets
            if client_sock:
                client_sock.send((username + ": " + msg).encode('utf-8'))
            if server_client_sock:
                server_client_sock.send((username + ": " + msg).encode('utf-8'))
            save_historique(msg)
            chat_display.insert(tk.END, f"You: {msg}\n")
            message_entry.delete(0, tk.END)
        except Exception as e:
            chat_display.insert(tk.END, f"Erreur envoi: {e}\n")

send_button = Button(root, text="Send", command=send_message, bg="#4A4A4A", fg="#FFFFFF", font=("Arial", 12), state=tk.DISABLED)
send_button.grid(row=6, column=1, padx=10, pady=10, sticky="e")

# Bind Enter key to send
root.bind('<Return>', send_message)

# Typing indicator logic
keyboard_in_use = False
user_writing_active_state = False
last_key_event_time = 0

def on_press(key):
    global keyboard_in_use, last_key_event_time
    keyboard_in_use = True
    last_key_event_time = time.time()

def on_release(key):
    global keyboard_in_use
    keyboard_in_use = False

def check_keyboard_activity():
    global user_writing_active_state, last_key_event_time
    while True:
        if keyboard_in_use:
            last_key_event_time = time.time()
        if time.time() - last_key_event_time > 1:
            user_writing_active_state = False
            typing_label.config(text="", highlightbackground="#2E2E2E", highlightcolor="#2E2E2E")
        elif time.time() - last_key_event_time < 1 and keyboard_in_use:
            user_writing_active_state = True
            typing_label.config(text=f"{username} is typing...", highlightbackground="#00FF00", highlightcolor="#00FF00")
        time.sleep(0.05)

def send_typing_indicator():
    while True:
        if user_writing_active_state and (client_sock or server_client_sock):
            try:
                typing_indicator = (username + " is typing...").encode('utf-8')
                if client_sock:
                    client_sock.send(typing_indicator)
                if server_client_sock:
                    server_client_sock.send(typing_indicator)
            except Exception as e:
                chat_display.insert(tk.END, f"Erreur indicateur: {e}\n")
                break
        time.sleep(0.5)

# Start keyboard listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

threading.Thread(target=check_keyboard_activity, daemon=True).start()
threading.Thread(target=send_typing_indicator, daemon=True).start()

# Run GUI
root.mainloop()