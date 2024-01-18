import json
import socket

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


# -------------------- Create Socket ------------------------------------
def send_receive(message: dict) -> None:
    """
    Sends the string message via the socket to the server
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(HOST)
    listening = True

    json_request = json.dumps(message)
    encoded_message = json_request.encode(FORMAT)
    message_length = len(encoded_message)
    byte_length = str(message_length).encode(FORMAT)
    byte_length += b' ' * (HEADER - len(byte_length))

    # Send size and then message
    client.send(byte_length)
    client.send(encoded_message)

    while listening:
        # Listen for reply
        reply_length = int(client.recv(HEADER).decode(FORMAT))
        if reply_length:
            print(client.recv(reply_length).decode(FORMAT))

        reply_length = int(client.recv(HEADER).decode(FORMAT))
        if reply_length:
            received_json = client.recv(reply_length).decode(FORMAT)
            json_data = json.loads(received_json)
            print(json_data)
            client.close()
            listening = False


send_receive({'gender': 'girl', 'letter': 'c'})
send_receive({'gender': 'boy', 'letter': 'j'})

