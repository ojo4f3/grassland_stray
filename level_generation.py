"""
Section of Grassland Stray: Shifting Savannas
Description: Used to request level generation and high score records from supporting microservice
 (high score has not been implemented yet)
Last updated: 11 AUG 2023
"""

# ------------------------------------------ Imports -------------------------------------------------
import csv
import random
from client import send_receive

# ------------------------------------------ Constants -----------------------------------------------
SCENE_TOTAL = 25
NUM_OF_SCENES = 15
PATH = "./level_data"
SPRITE_CLASSES = ['platform', 'boxes', 'plants', 'background']


# ------------------------------------------ Functions -----------------------------------------------
def stitch_level(scene_list: list) -> list:
    """
    Combines all level information (location and image) into a list of lists
    """
    # stitched_level is a list of lists: platform, boxes, plants, background sprites
    stitched_level = []

    for sprite_type in SPRITE_CLASSES:
        sprite_list = combine_group(sprite_type, scene_list, PATH)
        stitched_level.append(sprite_list)
    return stitched_level


def combine_group(sprite_type: str, scenes: list, path: str) -> list:
    """
    Combines the information of one sprite class and returns the resultant list
    """
    file_data = []
    for element in scenes:
        file_data.append(read_sprite_data(f"{path}/{element}/_{sprite_type}.csv"))

    sprite_list = []
    for index in range(12):
        row_list = []
        for scene in range(len(file_data)):
            row_list += file_data[scene][index]
        sprite_list.append(row_list)
    return sprite_list


def read_sprite_data(file_name: str) -> list:
    """
    Retrieves the scene's data for a specific sprite type
    """
    with open(f"{file_name}", 'r') as file:
        data = csv.reader(file)
        list_data = list(data)
        return list_data


# ----------------------------------------- Call Service ---------------------------------------------
def generate_level(difficulty: str) -> list:
    """
    Receives a difficulty level and calls the microservice for a list of scenes
    """
    # Form the level generation request
    if difficulty == 'easy':
        scene_range = [1, SCENE_TOTAL // 2]
    elif difficulty == 'normal':
        scene_range = [1 * SCENE_TOTAL // 4, 3 * SCENE_TOTAL // 4]
    else:
        scene_range = [SCENE_TOTAL // 2, SCENE_TOTAL]
    level_request = {
        'num_of_scenes': NUM_OF_SCENES,
        'scene_range': scene_range
    }

    # Call microservice
    response = send_receive(level_request)
    return response


# ---------------------------------------- Create New Level ------------------------------------------
def create_level(difficulty: str) -> list:
    """
    Main level generation function which all other functions support. Requests the microservice create a list of scenes
     and then returns a list of lists with all information for game_logic.py to build the level
    """
    # Request list generation
    gen_list = generate_level(difficulty)

    short_name = 'sc_00'
    medium_name = 'sc_0'
    first_scene = medium_name + str(random.randint(91, 91))  # will update when there are more opening scenes
    scene_list = [first_scene]

    for frame in gen_list:
        if frame < 10:
            scene_list.append(short_name + str(frame))
        else:
            scene_list.append(medium_name + str(frame))

    last_scene = 'sc_' + str(random.randint(100, 100))  # will update when there are more closing scenes
    scene_list.append(last_scene)
    return stitch_level(scene_list)


# ------------------------------------------- High Score Response ------------------------------------
# response format = [
#     {
#         'scene_list': [2, 5, 12, 4, 22, 3, 7, 15, 12, 6, 11, 4, 6, 28, 20]
#     },
#     {
#         'score_1': 239,
#         'score_2': 214,
#         'score_3': 198,
#         'score_4': 176,
#         'score_5': 172,
#         'score_6': 160,
#         'score_7': 142,
#         'score_8': 122,
#         'score_9': 105,
#         'score_10': 54
#     }
# ]
