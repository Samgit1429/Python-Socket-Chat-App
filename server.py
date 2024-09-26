# server.py
import threading
import socket

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")

    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[DISCONNECT] {addr} disconnected")
                break

            print(f"[{addr}] {msg}")
            broadcast(f"[{addr}] {msg}")
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()


def broadcast(message):
    with clients_lock:
        for client in list(clients):
            try:
                client.sendall(message.encode(FORMAT))
            except:
                # Handle broken connections
                clients.remove(client)
                client.close()


def accept_connections():
    server.listen()
    print('[SERVER STARTED] Listening...')
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")


def server_input():
    while True:
        msg = input()
        if msg.lower() == 'shutdown':
            print("Shutting down server...")
            with clients_lock:
                for client in clients:
                    try:
                        client.sendall(DISCONNECT_MESSAGE.encode(FORMAT))
                        client.close()
                    except:
                        pass
                clients.clear()
            server.close()
            break
        else:
            broadcast(f"[SERVER] {msg}")


def start():
    print('[SERVER STARTED]!')
    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.start()

    input_thread = threading.Thread(target=server_input)
    input_thread.start()

    accept_thread.join()
    input_thread.join()


if __name__ == "__main__":
    start()
