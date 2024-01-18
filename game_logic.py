"""
Section of Grassland Stray: Shifting Savannas
Description: Contains PlatformGame and Level classes that control the game flow and game logic to include collisions.
Last updated: 11 AUG 2023
"""

# -------------------------------- Imports ------------------------------------------------------ #
import pygame
from non_cat_sprites import Block
from level_generation import create_level
from config_and_support import BLOCK_SIZE, SCREEN_HEIGHT

# -------------------------------- Constant ----------------------------------------------------- #
PATH = "./images"


# --------------------------------   Level Class ---------------------------------------------------- #
class Level:
    """
    Class that represents a level and handles object collisions and interactions.
    """
    def __init__(self, display: pygame.display, cat: pygame.sprite.GroupSingle, difficulty: str):
        self._display = display
        self._layout = create_level(difficulty)
        self._state = 'level'
        self._x_shift = 0
        self._total_shift = 0
        self._cat = cat

        # Cat set up
        self._cat.sprite.set_location(200, 200)
        # End goal set up
        self._objective = pygame.sprite.GroupSingle()

        # Terrain set up
        self._platform = self._create_sprite_group('platform', 0)
        # Box sprites
        self._boxes = self._create_sprite_group('boxes', 1)
        # Plant sprites
        self._plants = self._create_sprite_group('plants', 2)
        # Background sprites
        self._faded_sprites = self._create_sprite_group('background', 3)

        # Collision sprites
        self._collision_sprites = pygame.sprite.Group()
        self._collision_sprites.add(self._platform)
        self._collision_sprites.add(self._boxes)

    def get_state(self) -> str:
        """
        Returns the current game state
        """
        return self._state

    def _create_sprite_group(self, sprite_class: str, level_index: int) -> pygame.sprite.Group:
        """
        Cycles through the game layout information to generate the terrain, objects, etc.
        """
        sprite_group = pygame.sprite.Group()

        # Cycle through the level layout
        for row, level_row in enumerate(self._layout[level_index]):
            for index, cell in enumerate(level_row):
                x_coord = index * BLOCK_SIZE
                y_coord = row * BLOCK_SIZE

                # organizes block images for the display
                if cell != '-1':
                    if sprite_class == 'platform':
                        path = f"{PATH}/{sprite_class}/{cell}.png"
                        block = Block(x_coord, y_coord, path)
                        sprite_group.add(block)
                    elif sprite_class == 'boxes':
                        path = f"{PATH}/{sprite_class}/{cell}.png"
                        block = Block(x_coord, y_coord, path)
                        sprite_group.add(block)
                    elif sprite_class == 'plants':
                        path = f"{PATH}/{sprite_class}/{cell}.png"
                        block = Block(x_coord, y_coord, path)
                        sprite_group.add(block)
                        if cell == '107':
                            self._objective.add(block)
                    elif sprite_class == 'background':
                        # Uses plants sprite class as the images are the same just reduced opacity
                        path = f"{PATH}/plants/{cell}.png"
                        block = Block(x_coord, y_coord, path)
                        block.change_alpha(160)
                        sprite_group.add(block)
        return sprite_group

    def x_collision_check(self, sprite: pygame.sprite) -> None:
        """
        Checks whether a sprite is colliding with the environment horizontally
        """
        sprites_rect = sprite.rect
        sprites_momentum = sprite.get_momentum()
        for block in self._collision_sprites:
            if block.rect.colliderect(sprites_rect):
                # Collision on the right
                if sprites_momentum.x > 0:
                    sprites_rect.right = block.rect.left
                    sprites_momentum.x = 0
                # Collision on the left
                elif sprites_momentum.x < 0:
                    sprites_rect.left = block.rect.right
                    sprites_momentum.x = 0

        # return to Menu once reaching the objective
        if sprite.rect.colliderect(self._objective.sprite):
            self._state = 'menu'

    def y_collision_check(self, sprite: pygame.sprite) -> None:
        """
        Check whether a sprite is colliding with the environment vertically
        """
        sprite.gravity()
        sprites_rect = sprite.rect
        sprites_momentum = sprite.get_momentum()
        for block in self._collision_sprites:
            if block.rect.colliderect(sprites_rect):
                # Collision with ground
                if sprites_momentum.y > 0:
                    sprites_rect.bottom = block.rect.top
                    sprites_momentum.y = 0
                    sprite._grounded = True
                # Collision with ceiling
                elif sprites_momentum.y < 0:
                    sprites_rect.top = block.rect.bottom
                    sprites_momentum.y = 2

        # return to Menu if Cat falls off the platform
        if sprite.rect.top > SCREEN_HEIGHT:
            self._state = 'menu'

    def _window_scroll(self) -> None:
        """
        Updates the Cat's x position and scrolls the window if needed
        """
        self._x_shift = self._cat.sprite.check_scroll()

    def run(self) -> None:
        """
        Check for collisions and update positions
        """
        # Environment
        # Background elements
        self._faded_sprites.update(self._x_shift)
        self._faded_sprites.draw(self._display)

        # Plants
        self._plants.update(self._x_shift)
        self._plants.draw(self._display)

        # Platform
        self._platform.update(self._x_shift)
        self._platform.draw(self._display)
        self._window_scroll()

        # Boxes
        self._boxes.update(self._x_shift)
        self._boxes.draw(self._display)

        # Check for collisions caused by the world scrolling
        self.x_collision_check(self._cat.sprite)

        # Cat
        self._cat.update()
        self.y_collision_check(self._cat.sprite)
        self._cat.sprite.move_x()
        self.x_collision_check(self._cat.sprite)
        self._cat.draw(self._display)
