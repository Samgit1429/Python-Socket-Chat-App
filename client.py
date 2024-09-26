# client.py
import socket
import threading
import time

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        return client
    except ConnectionRefusedError:
        print("[ERROR] Cannot connect to the server. Make sure the server is running.")
        return None


def send_messages(client):
    while True:
        msg = input()
        if msg.lower() == 'q':
            client.send(DISCONNECT_MESSAGE.encode(FORMAT))
            break
        else:
            client.send(msg.encode(FORMAT))


def receive_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print("Disconnected from server.")
                break
            print(msg)
        except ConnectionResetError:
            print("[ERROR] Connection lost.")
            break
        except OSError:
            print("[ERROR] Conection closed.")
            break
    client.close()


def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()
    print("Connected to the server. Type your messages below.")
    print("Type 'q' to disconnect.")

    receive_thread = threading.Thread(target=receive_messages, args=(connection,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(connection,))
    send_thread.start()

    send_thread.join()
    receive_thread.join()

    print('Disconnected')


if __name__ == "__main__":
    start()
