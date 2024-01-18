"""
Section of Grassland Stray: Shifting Savannas
Description: Platform game with randomly generated levels.
Last update: 11 AUG 2023
"""

# --------------------------------   Imports -------------------------------------------------------- #
import pygame
from config_and_support import BLOCK_SIZE, FONT

# --------------------------------   Constants ------------------------------------------------------ #
PATH = "./images"


# --------------------------------   Block Class ---------------------------------------------------- #
class Block(pygame.sprite.Sprite):
    """
    Class that represents terrain and object blocks
    """
    def __init__(self, x_coord: int, y_coord: int, path: str) -> None:
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        if 'boxes' in path or 'platform' in path:
            # Terrain and box images are slightly too large
            self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.image.get_rect(bottomleft=(x_coord, y_coord + BLOCK_SIZE))

    def update(self, horizontal_shift: int) -> None:
        """
        Updates the block's position due to window scrolling
        """
        self.rect.x += horizontal_shift

    def change_alpha(self, opacity: int) -> None:
        """
        Adjusts the images opacity
        """
        self.image.set_alpha(opacity)


# --------------------------------   Button Class ---------------------------------------------------- #
class Button:
    def __init__(self, coord: tuple, width: int, color: str, text: str, function=None) -> None:
        """
        Button class used for menu options
        """
        self._coord = coord
        self._color = color
        self.image = pygame.Surface((width, 100))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=self._coord)
        self._font = FONT
        self._text = self._font.render(text, True, (255, 255, 255))
        self.action = function

    def get_text(self) -> pygame.Surface:
        """
        Returns the button's text
        """
        return self._text

    def get_text_rect(self) -> pygame.rect:
        """
        Returns the button's text rect
        """
        return self._text.get_rect(center=self.rect.center)
