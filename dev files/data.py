"""
Section of Grassland Stray: Shifting Savannas
Description: Contains PlatformGame and Level classes that control the game flow and game logic to include collisions.
"""
import csv
import random

# ---------------------------------------- Trial Level for Testing -----------------------------------
to_be_added = ['sc_001', 'sc_002', 'sc_003', 'sc_004', 'sc_005', 'sc_006', 'sc_007', 'sc_008', 'sc_009', 'sc_010', 'sc_011', 'sc_012', 'sc_013', 'sc_014', 'sc_015']

scene_list = random.sample(to_be_added, 15)
scene_list.insert(0, 'sc_091')
scene_list.append('sc_100')


# stitched_level is a list of lists: platform, boxes, plants, background sprites
def stitch_level(scene_list: list) -> list:
    sprite_class = ['platform', 'boxes', 'plants', 'background']
    path = "../level_data"
    stitched_level = []

    for sprite_type in sprite_class:
        sprite_list = combine_group(sprite_type, scene_list, path)
        stitched_level.append(sprite_list)
    return stitched_level


def combine_group(sprite_type: str, scenes: list, path: str) -> list:
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


def read_sprite_data(file_name: str):
    with open(f"{file_name}", 'r') as file:
        data = csv.reader(file)
        list_data = list(data)
        return list_data


final_level = stitch_level(scene_list)
