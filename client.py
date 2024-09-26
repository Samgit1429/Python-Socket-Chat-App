import socket
import threading
import time

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send_messages(client, msg):
    while True:
        msg = input()
        if msg.lower == 'q':
            client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            break
        else:
            client.send(msg.encode(FORMAT))

def receive_massages(client):
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print("Disconneceted from server.")
                break
            print(msg)
        except:
            print("An error occured. Connection closed.")
            break
    client.close()

def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()
    print("Connected to the server. Type your messages below.")
    print("Type 'q' to disconnect.")

    receive_thread = threading.Thread(target=receive_massages, args=(connection,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(connection,))
    send_thread.start()

    send_thread.join()
    receive_thread.join()

    print('Disconnected')

if __name__ == "__main__":
    start()
