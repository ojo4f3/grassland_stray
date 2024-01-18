"""
Section of Grassland Stray: Shifting Savannas
Description: Contains PlatformGame and Level classes that control the game flow and game logic to include collisions.
Last updated: 11 AUG 2023
"""

# ---------------------------- Imports ---------------------------------------------------------- #
import json
import socket
from datetime import datetime

# ------------------------ Constants ------------------------------------------------------------ #
# Default message input size
HEADER = 64
FORMAT = 'utf-8'

# Set up server Host
PORT = 54545
HOST_MACHINE = socket.gethostbyname(socket.gethostname())
HOST = (HOST_MACHINE, PORT)


# ---------------------------------- Send_Receive Function -------------------------------------- #
def send_receive(message: dict) -> list:
    """
    Sends a string message (JSON) via a socket to the server
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(HOST)

    json_request = json.dumps(message)
    encoded_message = json_request.encode(FORMAT)

    # Send  message
    client.send(encoded_message)
    start_micro = int(datetime.now().strftime('%f').split('.')[0])

    # Listen for reply
    received_json = client.recv(2048).decode(FORMAT)
    json_data = json.loads(received_json)
    client.close()
    end_micro = int(datetime.now().strftime('%f').split('.')[0])
    elapsed_time = end_micro - start_micro
    print(f"Request successful: response in {elapsed_time / 1000}ms")
    return json_data['scene_list']


# --------------------------------------- Test Code --------------------------------------------- #
if __name__ == '__main__':
    scenes = (1, 15)
    test_level = {
        "num_of_scenes": 12,
        "scene_range": [8, 23]
    }

    result = send_receive(test_level)
    print(result)
