import socket
import threading

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def receive_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print("Disconnected from server.")
                break
            print(msg)
        except:
            print("An error occured. Connection closed.")
            break
    client.close()

def start():
    connection = connect()
    print("Connected to the server. Listening for messages...")
    print("Press Ctrl+C to discconect.")

    receive_thread = threading.Thread(target=receive_messages, args=(connection,))
    receive_thread.start()

    receive_thread.join()
    print('Disconnected')

if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print("\nDisconnected manually.")