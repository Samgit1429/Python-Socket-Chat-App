import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import datetime

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # Can be adjusted to point to the actual server IP
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


class ChatClient:
    def __init__(self, root):
        self.client = None

        # GUI setup
        self.root = root
        self.root.title("Chat Client")

        # Text area for chat history
        self.chat_window = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD, height=20, width=60)
        self.chat_window.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Entry box for typing messages
        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)
        self.message_entry.bind('<Return>', self.send_message)  # Bind "Enter" key to send message
        self.message_entry.config(state='disabled')  # Initially disabled until connected

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10)
        self.send_button.config(state='disabled')  # Disabled until connected

        # Connect and Disconnect buttons
        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_server)
        self.connect_button.grid(row=2, column=0, padx=10, pady=10)

        self.disconnect_button = tk.Button(root, text="Disconnect", command=self.disconnect_from_server, state='disabled')
        self.disconnect_button.grid(row=2, column=1, padx=10, pady=10)

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(ADDR)
            self.update_chat_window("Connected to the server.\n")

            # Enable sending messages and disable connection button
            self.message_entry.config(state='normal')
            self.send_button.config(state='normal')
            self.connect_button.config(state='disabled')
            self.disconnect_button.config(state='normal')

            # Start receiving messages
            self.start_receiving_messages()
        except:
            self.update_chat_window("Failed to connect to the server.\n")

    def send_message(self, event=None):
        msg = self.message_entry.get()
        if msg:
            self.client.send(msg.encode(FORMAT))
            self.message_entry.delete(0, tk.END)
        if msg == 'q':
            self.disconnect_from_server()

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
                self.update_chat_window(msg + "\n")
            except OSError:
                break

    def update_chat_window(self, message):
        """Utility to update the chat window and auto-scroll to the latest message"""
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, message)
        self.chat_window.yview(tk.END)
        self.chat_window.config(state='disabled')

    def disconnect_from_server(self):
        if self.client:
            self.client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            self.client.close()
            self.client = None
            self.update_chat_window("Disconnected from the server.\n")

            # Disable message entry and buttons
            self.message_entry.config(state='disabled')
            self.send_button.config(state='disabled')
            self.connect_button.config(state='normal')
            self.disconnect_button.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
