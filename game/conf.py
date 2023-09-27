import pygame
from misc import env_default
import os

Vector2 = pygame.math.Vector2

CONTROLLER_DEAD_ZONE = 3000

BACKGROUND = (0x18, 0x18, 0x18)
TRANSPARENT = (0x00, 0x00, 0x00, 0x00)
BLACK = (0x00, 0x00, 0x00)
BLUE = (0x6c, 0x71, 0xc4)

WIDTH  = env_default( 'WIDTH', 1920+400)
HEIGHT = env_default('HEIGHT', 1080+200)

WHITE = 240, 240, 240
GREY = 72,72,72
LIGHT_GREY = 189,174,173
BLACK = 24,24,24
RED = 238,21,21

BORDER_COLOR = (0x8c, 0x3b, 0x3c)
OBJECT_COLOR = (0xaa, 0xaa, 0xaa)

BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3

BUTTON_SELECT = 4
BUTTON_START = 6

DPAD_UP = 11
DPAD_DOWN = 12
DPAD_LEFT = 13
DPAD_RIGHT = 14

LEFT_STICK_X  = 0
LEFT_STICK_Y  = 1
RIGHT_STICK_X = 2
RIGHT_STICK_Y = 3
LEFT_TRIGGER  = 4
RIGHT_TRIGGER = 5

x, y = WIDTH/4, HEIGHT/4
MIDDLE_RECT = (x, y, x*2, y*2)

PLAY = 0
LOST = 1
MENU = 2
LOAD = 3


GUI_FONT = 'fonts/SourceCodePro.ttf'

unlocked = os.environ.get('UNLOCKED')
benchmark = os.environ.get('BENCHMARK')
