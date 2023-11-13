import socket
import threading
import sys

is_server_running = True
clients = []
client_threads = []

def handle_client(client_socket):
    name = client_socket.recv(1024).decode('utf-8')
    welcome_message = f"{name} has joined the chat!"
    broadcast(welcome_message.encode('utf-8'))

    while True:
        try:
            msg = client_socket.recv(1024)
            if msg:
                broadcast(msg, name)
            else:
                # No message means the client has disconnected
                break
        except:
            # An exception occurred, meaning something went wrong (e.g., sudden disconnection)
            break

    # When the client disconnects
    client_socket.close()
    remove(client_socket)
    goodbye_message = f"{name} has left the chat."
    broadcast(goodbye_message.encode('utf-8'))

def receive_server_commands():
    global is_server_running
    while True:
        cmd = input("Enter 'quit' to shut down the server: ")
        if cmd == 'quit':
            print("Shutting down the server...")
            is_server_running = False
            server.close()
            break

def broadcast(message, name=""):
    for client in clients:
        try:
            if name:
                client.send(f"{name}: {message.decode('utf-8')}".encode('utf-8'))
            else:
                client.send(message)
        except:
            client.close()
            remove(client)

def remove(connection):
    if connection in clients:
        clients.remove(connection)

SERVER = "127.0.0.1"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
server.listen()

clients = []

print(f"Server listening on {SERVER}:{PORT}...")

# Start a new thread for server commands
command_thread = threading.Thread(target=receive_server_commands)
command_thread.start()

while is_server_running:
    try:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print(f"Connection from {addr} has been established.")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
    except OSError:
        break
    
# Server shutdown sequence
for client_socket in clients:
    try:
        client_socket.sendall("Server is shutting down.".encode('utf-8'))
    except:
        pass
    client_socket.close()

for thread in client_threads:
    thread.join()

print("Server has been shut down.")
