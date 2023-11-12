import socket
import threading

def handle_client(client_socket):
    while True:
        msg = client_socket.recv(1024)
        if msg:
            print(f"Received: {msg.decode('utf-8')}")
            broadcast(msg, client_socket)

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)

def remove(connection):
    if connection in clients:
        clients.remove(connection)

# Server IP and port
SERVER = "127.0.0.1"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
server.listen()

clients = []

print(f"Server listening on {SERVER}:{PORT}...")

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    print(f"Connection from {addr} has been established.")
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()