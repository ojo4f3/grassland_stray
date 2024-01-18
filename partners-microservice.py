"""
Section of Grassland Stray: Shifting Savannas
Description: Provides a microservice through a socket that aids with level generation.
Last update: 29 JUL 2023
"""

import socket
import random
import json


ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4, TCP
ss.bind((socket.gethostname(), 54545))  # localhost
ss.listen(5)  # queue of 5 connections


def generate_dungeon(num_of_scenes, scene_range):
    """
    Parameters: number_of_scenes (int) and scene_range (list of two integers representing a range, both inclusive)
    Returns:    list of number_of_scenes integers, all within the provided scene_range
    """
    scene_list = []
    start = scene_range[0]
    stop = scene_range[1] + 1
    for i in range(num_of_scenes):
        scene_list.append(random.randrange(start, stop))
    return scene_list


def is_valid(request_dict):
    """
    Parameters: dictionary of scene information
    Returns: Tuple. First value is True if the data is valid, False if not. Second value is empty string or error string.
    """
    if "num_of_scenes" not in request_dict:
        return False, "num_of_scenes missing"
    if type(request_dict["num_of_scenes"]) is not int:
        return False, "num_of_scenes must be an integer"
    if request_dict["num_of_scenes"] <= 0:
        return False, "num_of_scenes must be greater than 0"

    if "scene_range" not in request_dict:
        return False, "scene_range missing"
    if type(request_dict["scene_range"]) is not list:
        return False, "scene_range is not a list"
    if len(request_dict["scene_range"]) < 2:
        return False, "scene_range does not have start and end values"
    if len(request_dict["scene_range"]) > 2:
        return False, "scene_range has more than two values"
    if type(request_dict["scene_range"][0]) is not int:
        return False, "scene_range list must contain integers"
    if type(request_dict["scene_range"][1]) is not int:
        return False, "scene_range tuple must contain integers"
    if request_dict["scene_range"][0] > request_dict["scene_range"][1]:
        return False, "first integer in scene_range must be less than second integer"
    if request_dict["scene_range"][0] <= 0 or request_dict["scene_range"][1] <= 0:
        return False, "scene_range integers must be greater than 0"
    return True, ""


def server_loop():
    while True:
        client_socket, address = ss.accept()  # stores client socket object and client IP addr
        request = client_socket.recv(2048)
        request = request.decode("utf-8")
        request_dict = json.loads(request)
        test_validity, validity_statement = is_valid(request_dict)
        if test_validity:
            dungeon = generate_dungeon(request_dict["num_of_scenes"], request_dict["scene_range"])
            json_dungeon = {'scene_list': dungeon}
            message = json.dumps(json_dungeon)
            client_socket.send(bytes(message, "utf-8"))  # must send as bytes
        else:
            client_socket.send(bytes(validity_statement, "utf-8"))


if __name__ == '__main__':
    server_loop()
