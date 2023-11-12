import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            print(msg)
        except:
            print("An error occurred!")
            sock.close()
            break

# Server IP and port
SERVER = "127.0.0.1"
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

thread = threading.Thread(target=receive_messages, args=(client,))
thread.start()

while True:
    message = input('')
    if message == 'QUIT':
        break
    client.send(message.encode('utf-8'))
