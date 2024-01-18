"""
Section of Grassland Stray: Shifting Savannas
Description: Contains the Cat class which is the player's character
"""

# ---------------------------------- Imports ---------------------------------------------------- #
import pygame
from os import walk
import config_and_support as cs

SPEED = 7
ANIMATION_SPEED = 0.16
CAT_IMAGES_PATH = "./images/cat"
LEFT_BUFFER = cs.SCREEN_WIDTH * .20
RIGHT_BUFFER = cs.SCREEN_WIDTH * .70


# ---------------------------------- Imports ---------------------------------------------------- #
class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Visual set up
        self._images = []
        self._animation_setup()
        self._current_image = 0
        self.image = self._images[self._current_image]

        # Movement
        self.rect = self.image.get_rect(topleft=(200, 200))
        self._facing = 'RIGHT'
        self._speed = SPEED
        self._momentum = pygame.math.Vector2(0, 0)
        self._x_movement = 0
        self._gravity = 2
        self._jump_power = -30
        self._grounded = False
        self._state = 'falling'

    def _animation_setup(self) -> None:
        """
        Accesses the animation images and saves them in the self._images attribute
        """
        for home_dir, subdir, images in walk(CAT_IMAGES_PATH):
            for image in images:
                cat_python_image = pygame.image.load(f"{CAT_IMAGES_PATH}/{image}").convert_alpha()
                self._images.append(cat_python_image)

    def _animate(self) -> None:
        # Cycle through animation images at animation speed
        self._current_image += ANIMATION_SPEED
        # Repeat cycle images
        if self._current_image >= len(self._images):
            self._current_image %= len(self._images)

        frame = self._images[int(self._current_image)]
        if self._facing == 'RIGHT':
            self.image = frame
        else:
            rev_frame = pygame.transform.flip(frame, True, False)
            self.image = rev_frame

    def set_location(self, x_coord: int, y_coord: int) -> None:
        """
        Method is set the Cat's initial position
        """
        self.rect.center = (x_coord, y_coord)

    def _event_listener(self) -> None:
        """
        Captures user keyboard input to mave the Cat
        """
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self._momentum.x = -1
            self._facing = 'LEFT'
            self._animate()
        elif pressed_keys[pygame.K_RIGHT]:
            self._momentum.x = 1
            self._facing = 'RIGHT'
            self._animate()
        else:
            self._momentum.x = 0
        self._x_movement = self._momentum.x * self._speed

        if pressed_keys[pygame.K_UP] and self._grounded:
            self._jump()

    def _check_state(self) -> None:
        """
        Method used to define the Cat's state: falling, jumping, running, stopped for animation purposes
        """
        if self._momentum.y < 0:
            self._state = 'jumping'
        elif self._momentum.y > 1.5:
            self._state = 'falling'
        else:
            if self._momentum.x != 0:
                self._state = 'running'
            else:
                self._state = 'stopped'

    def _jump(self) -> None:
        """
        Triggers the Cat's upward movement on jump
        """
        self._momentum.y = self._jump_power
        self._state = 'jumping'
        self._grounded = False

    def get_momentum(self) -> pygame.Vector2:
        """Returns the Cat's momentum"""
        return self._momentum

    def move_x(self) -> None:
        """
        Horizontal movement
        """
        self.rect.x += self._x_movement

    def gravity(self) -> None:
        """
        Constant downward movement unless on a solid object
        """
        self._momentum.y += self._gravity
        self.rect.y += self._momentum.y

    def check_scroll(self) -> int:
        """
        Determines if the Cat moves horizontally or if the platform should scroll
        """
        if self.rect.left < LEFT_BUFFER and self._momentum.x < 0:
            self._speed = 0
            return SPEED
        elif self.rect.right > RIGHT_BUFFER and self._momentum.x > 0:
            self._speed = 0
            return -SPEED
        else:
            self._speed = SPEED
            return 0

    def update(self) -> None:
        """
        Continuous update with input and reaction
        """
        self._event_listener()
        self._check_state()
