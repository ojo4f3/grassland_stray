import time
import json
import socket
import threading

# ------------------- Message format set up ----------------------------
# Default message input size
HEADER = 64
FORMAT = 'utf-8'

# --------------------  Set up server Host ------------------------------
# Listening on port 7567
PORT = 7567
# Host device's local IP address
HOST_MACHINE = socket.gethostbyname(socket.gethostname())
HOST = (HOST_MACHINE, PORT)
DISCONNECT_MESSAGE = "DISCONNECT"

# -------------------- Create Socket ------------------------------------
# Socket family: IPV4
# Type: default
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to an address
server.bind(HOST)


#  ------------------- Function ---------------------------
def comm_thread(connection: socket, address: str):
    """
    Handles individual connections
    """
    print(f"New connection: {address} connected.")
    time.sleep(1)
    connected = True
    while connected:
        # Will wait until a message is received from the client
        # First message will have a size of 64 bytes and message_length is the length of the next message
        message_length = connection.recv(HEADER).decode(FORMAT)
        if message_length:
            received_json = connection.recv(int(message_length)).decode(FORMAT)
            json_data = json.loads(received_json)
            text = json_data['fail']
            # Close connection when client disconnects
            if text == DISCONNECT_MESSAGE:
                connected = False
            print(text)
            connection.send("Message received".encode(FORMAT))
    connection.close()


def start_connection() -> None:
    """
    Create and handle new connections
    """
    server.listen()
    while True:
        connection, client_address = server.accept()
        # Define and start thread
        thread = threading.Thread(target=comm_thread, args=(connection, client_address))
        thread.start()
        # Report number of connections (subtract 1 to account for original start_connection call)
        print(f"Active connections: {threading.active_count() - 1}\n")


if __name__ == "__main__":
    print("Server is starting. Listening on port 7567...")
    start_connection()
