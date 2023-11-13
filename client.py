import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 12345

class ChatClient:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.window = tk.Tk()
        self.window.title("Chat Room")

        self.name = simpledialog.askstring("Name", "Enter your name:", parent=self.window)
        self.sock.sendall(self.name.encode('utf-8'))

        self.chat_area = scrolledtext.ScrolledText(self.window)
        self.chat_area.pack(padx=20, pady=5)
        self.chat_area.config(state='disabled')

        self.msg_entry = tk.Entry(self.window, width=50)
        self.msg_entry.pack(padx=20, pady=5)
        self.msg_entry.bind("<Return>", self.write)

        self.send_button = tk.Button(self.window, text="Send", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        self.window.mainloop()

    def write(self, event=None):
        message = self.msg_entry.get()
        if message:
            self.sock.sendall(message.encode('utf-8'))
        self.msg_entry.delete(0, tk.END)

    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message:
                    self.chat_area.config(state='normal')
                    self.chat_area.insert('end', message + '\n')
                    self.chat_area.yview('end')
                    self.chat_area.config(state='disabled')
                else:
                    # Server has closed the connection
                    break
            except OSError:
                # An error occurred, such as the server being unreachable
                break

        # Clean up and close the window if disconnected
        self.chat_area.config(state='normal')
        self.chat_area.insert('end', 'You have been disconnected from the server.\n')
        self.chat_area.config(state='disabled')
        self.sock.close()

    def on_close(self):
        self.sock.close()
        self.window.destroy()

client = ChatClient(HOST, PORT)
