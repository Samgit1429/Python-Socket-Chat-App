import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import time
import datetime

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

class ChatClient:
    def __init__(self, root):
        self.client = None

        #GUI setup
        self.root = root
        self.root.title("Chat Client")

        self.chat_window = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD)
        self.chat_window.pack(padx=20, pady=20)

        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack(pady=10)
        self.message_entry.bind('<Return>', self.send_message)

        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=5)

        self.discconect_button = tk.Button(root, text="Disconnect", command=self.disconnect_from_server)
        self.discconect_button.pack(pady=5)

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(ADDR)
            self.chat_window.config(state='normal')
            self.chat_window.insert(tk.END, "Connected to the server.\n")
            self.chat_window.config(state='disabled')
            self.start_receiving_messages()
        except:
            self.chat_window.config(state='normal')
            self.chat_window.insert(tk.END, "Failed to connect to the server.\n")
            self.chat_window.config(state='disabled')

    def send_message(self, event=None):
        msg = self.message_entry.get()
        if msg:
            self.client.send(msg.encode(FORMAT))
            self.message_entry.delete(0, tk.END)
        if msg == 'q':
            self.discconect_from_server()

    def start_receiving_messages(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                msg = self.client.recv(1024).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    break
                self.chat_window.config(state='normal')
                self.chat_window.insert(tk.END, msg + "\n")
                self.chat_window.config(state='disabled')
            except OSError:
                break

    def disconnect_from_server(self):
        if self.client:
            self.client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            self.client.close()
            self.client = None
            self.chat_window.config(state='normal')
            self.chat_window.insert(tk.END, "Disconnected from the server.\n")
            self.chat_window.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()