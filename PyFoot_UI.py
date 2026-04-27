import pygame_gui
import pygame
from constants import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

easy_button = pygame.Rect(SCREEN_WIDTH/2 - EASY_BUTTON_WIDTH/2, 2*SCREEN_HEIGHT/5 - EASY_BUTTON_HEIGHT/2, EASY_BUTTON_WIDTH, EASY_BUTTON_HEIGHT)

pygame_gui.elements.UIButton(easy_button, "Easy", manager)
