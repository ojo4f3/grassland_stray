"""
Section of Grassland Stray: Shifting Savannas
Description: Contains PlatformGame and Level classes that control the game flow and game logic to include collisions.
Last updated: 11 AUG 2023
"""

# ---------------------------------- Imports -------------------------------------------------------------- #
import pygame
from cat import Cat
from game_logic import Level
from non_cat_sprites import Button
from config_and_support import SCREEN_WIDTH, SCREEN_HEIGHT, FONT, TITLE_FONT, MED_FONT


# -------------------------------- Constants -------------------------------------------------------------- #
BLUE = '#274690'
BROWN = '#443B2C'
GREEN = '#678d58'
TAN = '#F1DABF'
TEAL = '#64a6bd'


# --------------------------------   PlatformGame Class ---------------------------------------------------- #
class PlatformGame:
    """
    Class that represents a platform game.
    """
    def __init__(self, display: pygame.display) -> None:
        self._display = display
        self._menu = None
        self._current_level = None
        self._state = 'menu'
        self._cat = pygame.sprite.GroupSingle()
        self._cat_sprite = Cat()
        self._cat.add(self._cat_sprite)

    def run(self) -> None:
        """
        Checks game state and reacts accordingly
        """
        if self._state == 'menu' and self._menu is None:
            self.show_menu()
        elif self._state == 'menu':
            self._menu.run()
            if self._menu.get_state() == 'create_level':
                self._state = 'create_level'
                self._menu.set_state('menu')
            elif self._menu.get_state() == 'tutorial':
                self._state = 'tutorial'
                self.show_tutorial()
        elif self._state == 'tutorial':
            self.show_tutorial()
        elif self._state == 'create_level':
            self.create_level()
        elif self._state == 'level':
            self._current_level.run()
            if self._current_level.get_state() == 'menu':
                self._current_level = None
                self._state = 'menu'

    def show_menu(self) -> None:
        """
        Display game Menu
        """
        self._menu = Menu(self._display, self)
        self._menu.run()

    def show_tutorial(self) -> None:
        """
        Show Tutorial page
        """
        # Background
        image = pygame.image.load("./images/backgrounds/bg_castle.png").convert_alpha()
        image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Title
        title = TITLE_FONT.render("Grassland Stray: Shifting Savannas", True, BROWN)
        subtitle = TITLE_FONT.render("Tutorial", True, BROWN)
        tutorial_text = pygame.image.load("./images/tutorial-text.png").convert_alpha()
        tutorial_text = pygame.transform.scale(tutorial_text, (600, 450))
        # Graphics
        graphic = pygame.image.load("./images/cat/loth-cat1.png").convert_alpha()
        graphic = pygame.transform.scale(graphic, (200, 239))
        right_arrow = pygame.image.load("./images/arrowRight.png").convert_alpha()
        # right_arrow = pygame.transform.scale(right_arrow, (150, 150))
        left_arrow = pygame.image.load("./images/arrowLeft.png").convert_alpha()
        # left_arrow = pygame.transform.scale(left_arrow, (150, 150))
        up_arrow = pygame.image.load("./images/arrowUp.png").convert_alpha()
        # up_arrow = pygame.transform.scale(up_arrow, (150, 150))
        # Mouse
        pygame.mouse.set_visible(1)
        # Button
        return_to_menu = Button((100, 620), 230, BLUE, 'Return to Menu', self._menu.set_state)

        # Draw image and track input
        pygame.mouse.get_visible()
        x_coord, y_coord = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if return_to_menu.rect.collidepoint(x_coord, y_coord):
                        self._state = 'menu'
                        return_to_menu.action('menu')
        self._display.blit(image, (0, 0))
        self._display.blit(title, (380, 100))
        self._display.blit(subtitle, (650, 175))
        self._display.blit(tutorial_text, (150, 250))
        self._display.blit(graphic, (120, 225))
        self._display.blit(right_arrow, (820, 260))
        self._display.blit(left_arrow, (820, 360))
        self._display.blit(up_arrow, (825, 460))
        self._display.blit(return_to_menu.image, return_to_menu.rect.topleft)
        text_rect = return_to_menu.get_text_rect()
        self._display.blit(return_to_menu.get_text(), text_rect)

    def create_level(self) -> None:
        """
        Generates a Level and hands game control over to the Level.
        """
        difficulty = self._menu.get_difficulty()
        self._current_level = Level(self._display, self._cat, difficulty)
        self._state = 'level'
        # track score and lives

    def set_state(self, state: str) -> None:
        """
        Sets the game state
        """
        self._state = state


# --------------------------------- Menu Class ------------------------------------------------------------ #
class Menu:
    """
    Class that represents the game menu
    """
    def __init__(self, display, game: PlatformGame):
        self._display = display
        self._game = game
        self._state = 'menu'
        self._difficulty = 'normal'
        self._selected_difficulty = None
        # Background
        self.image = pygame.image.load("./images/backgrounds/bg_castle.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Title
        self._title = TITLE_FONT.render("Grassland Stray: Shifting Savannas", True, BROWN)
        self._instruction = MED_FONT.render("Select Your Level", True, BROWN)
        # Cat graphic
        self._graphic = pygame.image.load("./images/cat/loth-cat1.png").convert_alpha()
        self._graphic = pygame.transform.scale(self._graphic, (240, 286))
        # Mouse
        pygame.mouse.set_visible(1)
        # Buttons
        self._easy_button = Button((600, 350), 125, TEAL, 'Easy', self.select_easy)
        self._normal_button = Button((750, 350), 150, GREEN, 'Normal', self.select_normal)
        self._hard_button = Button((925, 350), 125, BLUE, 'Hard', self.select_hard)
        self._start_button = Button((725, 500), 200, BROWN, 'START!', self.change)
        self._tutorial = Button((200, 600), 200, BROWN, 'Tutorial Page', self.view_tutorial)
        self._buttons = [self._easy_button, self._normal_button, self._hard_button, self._start_button, self._tutorial]

    def get_input(self) -> None:
        """
        Get user's input via the mouse
        """
        pygame.mouse.get_visible()
        x_coord, y_coord = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for button in self._buttons:
                        if button.rect.collidepoint(x_coord, y_coord):
                            if button == self._start_button:
                                self._game.set_state('create_level')
                            button.action()

    def run(self) -> None:
        """
        Checks for input and updates display
        """
        self.get_input()
        self.update_images()
        pygame.display.update()

    def update_images(self) -> None:
        """
        Draws and updates the display
        """
        self._display.blit(self.image, (0, 0))
        self._display.blit(self._title, (200, 125))
        self._display.blit(self._instruction, (680, 275))
        self._display.blit(self._graphic, (200, 250))

        # Buttons with text
        for button in self._buttons:
            self._display.blit(button.image, button.rect.topleft)
            text_rect = button.get_text_rect()
            self._display.blit(button.get_text(), text_rect)
        if self._selected_difficulty:
            self._selected_difficulty.image.fill(TAN)

    def select_easy(self) -> None:
        """
        Sets the difficulty to easy
        """
        self._difficulty = 'easy'
        if self._selected_difficulty:
            if self._selected_difficulty == self._normal_button:
                self._selected_difficulty.image.fill(GREEN)
            elif self._selected_difficulty == self._hard_button:
                self._selected_difficulty.image.fill(BLUE)
        self._selected_difficulty = self._easy_button

    def select_normal(self) -> None:
        """
        Sets the difficulty to normal
        """
        self._difficulty = 'normal'
        if self._selected_difficulty:
            if self._selected_difficulty == self._easy_button:
                self._selected_difficulty.image.fill(TEAL)
            elif self._selected_difficulty == self._hard_button:
                self._selected_difficulty.image.fill(BLUE)
        self._selected_difficulty = self._normal_button

    def select_hard(self) -> None:
        """
        Sets the difficulty to hard
        """
        self._difficulty = 'hard'
        if self._selected_difficulty:
            if self._selected_difficulty == self._easy_button:
                self._selected_difficulty.image.fill(TEAL)
            elif self._selected_difficulty == self._normal_button:
                self._selected_difficulty.image.fill(GREEN)
        self._selected_difficulty = self._hard_button

    def change(self) -> None:
        """
        Changes the game state to being a level
        """
        self._state = 'create_level'

    def view_tutorial(self) -> None:
        """
        Activates the tutorial view
        """
        self._state = 'tutorial'

    def get_state(self) -> str:
        """
        Returns the menu's state
        """
        return self._state

    def set_state(self, input_state: str) -> None:
        """
        Sets menu's state
        """
        self._state = input_state

    def get_difficulty(self) -> str:
        """
        Sets the game's difficulty level by returning the menu's difficulty info from the user
        """
        return self._difficulty
