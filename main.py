"""
Title: Grassland Stray: Shifting Savannas
Version: 1.0.1
Description: Platform game with randomly generated levels.
Last update: 11 AUG 2023
Author: Steven Crowther

Graphic resources for blocks and player character created by Kenny www.kenney.nl, used under public domain license
"""


# ---------------------------------- Imports -------------------------------------------------------------- #
import sys
import pygame
from game import PlatformGame
from config_and_support import SCREEN_WIDTH, SCREEN_HEIGHT


# --------------------------------------   Pygame Init ---------------------------------------------------- #
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("  Grassland Stray: Shifting Savannas  ")
fps_controller = pygame.time.Clock()

game = PlatformGame(screen)
play_game = True


# --------------------------------   Game Loop ----------------------------------------------------------- #
while play_game:
    # Check for window close / exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play_game = False

    # Run game, update window, and control FPS
    background_image = pygame.image.load("./images/backgrounds/bg_grasslands.png").convert_alpha()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_image, (0, 0))
    game.run()
    pygame.display.update()
    fps_controller.tick(60)

# Quit game
pygame.quit()
sys.exit()
